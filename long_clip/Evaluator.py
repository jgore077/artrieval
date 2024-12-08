from .model import longclip, tokenize
from .formatting import getImagePaths,preprocessImages
from ranx import Qrels,Run, evaluate as ranx_eval
from tqdm import tqdm
import torch
import json
import os


def load_querys(querys_path):
    with open(querys_path,encoding="utf-8") as querys_file:
        return json.load(querys_file)
    
def sim_matrix(a, b, eps=1e-8):
    """
    added eps for numerical stability
    """
    a_n, b_n = a.norm(dim=1)[:, None], b.norm(dim=1)[:, None]
    a_norm = a / torch.max(a_n, eps * torch.ones_like(a_n))
    b_norm = b / torch.max(b_n, eps * torch.ones_like(b_n))
    sim_mt = torch.mm(a_norm, b_norm.transpose(0, 1))
    return sim_mt
    
class Evaluator():
    def __init__(self,
        long_clip_model_name,
        metadata_file,
        qrel_file,
        embeddings_file,
        metrics:list[str],
        device,
    ) -> None:
        self.device=device
        self.long_clip_model_name=long_clip_model_name
        self.model,self.preprocess=longclip.load(long_clip_model_name,device=self.device)
        self.metadata_file:str=metadata_file
        self.qrel_file=qrel_file
        self.embeddings_file:str=embeddings_file
        self.metrics=metrics
        self._load_metadata()
        self._load_embeddings()
        self._build_keymap()
        self._load_qrel()
        
        
    def _load_embeddings(self):
        if not self.embeddings_file.endswith('.pt'):
            raise Exception("the embeddings file must be a .pt file")
        
        embedding_dir=os.path.dirname(self.embeddings_file)
        if not os.path.exists(embedding_dir):
            os.makedirs(embedding_dir,exist_ok=True)
            
        if not os.path.exists(self.embeddings_file):
            print("Creating embeddings")
            self.embeddings=self._make_image_embeddings()
            return
        
        print(f"Loading embeddings from {self.embeddings_file}")
        # Load image embeddings to cpu
        self.embeddings=torch.load(self.embeddings_file,weights_only=True).cpu()
        
    def _load_qrel(self):
        self.qrel=Qrels.from_file(self.qrel_file,kind="trec")
       
    def _make_image_embeddings(self, batch_size=32):
        files = getImagePaths(self.metadata)
        all_embeddings = []
        
        # Process in batches
        for i in tqdm(range(0, len(files), batch_size),desc="Computing image embeddings in batches"):
            batch_files = files[i:i + batch_size]
            batch_images = preprocessImages(batch_files, self.preprocess, self.device)
            
            with torch.no_grad():
                # Immediately move embeddings to CPU after computation
                batch_embeddings = self.model.encode_image(batch_images).cpu()
                all_embeddings.append(batch_embeddings)
                
                # Clear the GPU tensors
                del batch_images
                torch.cuda.empty_cache()
        
        # Concatenate on CPU
        embeddings = torch.cat(all_embeddings, dim=0)
        
        # Save from CPU memory
        torch.save(embeddings, self.embeddings_file)
        self.embeddings = embeddings
    
    
    def _load_metadata(self):
        with open(self.metadata_file,"r",encoding="utf-8") as f:
            self.metadata=json.load(f)
            
    def _build_keymap(self):
        self.keymap={}
        for i,key in enumerate(self.metadata):
                self.keymap[i]=key
                

    def search(self,querys:dict|str,truncate=True,batch_size=32):
        """
        Takes a path to a querys file or a dictionary of querys then finds the top k results for each query
        """
        if type(querys)==str:
            querys=load_querys(querys)
            
        encoded_querys=tokenize(list(querys.values()),truncate=truncate).to(self.device)    
        all_text_features = []
    
        # Process encoded queries in batches
        for i in range(0, encoded_querys.size(0), batch_size):
            batch_encoded = encoded_querys[i:i + batch_size]
            
            with torch.no_grad():
                batch_features = self.model.encode_text(batch_encoded)
                # Move features to CPU immediately
                all_text_features.append(batch_features.cpu())
                
                # Clean up GPU memory
                del batch_features
                torch.cuda.empty_cache()
        
        # Clean up encoded queries
        del encoded_querys
        torch.cuda.empty_cache()
        
        # Combine text features on CPU
        text_features = torch.cat(all_text_features, dim=0)
        scores=sim_matrix(text_features,self.embeddings)
        return scores
    
    def scores_to_run(self,scores,queries,k):
        # Dim 0 is the rows and dim 1 is the columns  
        query_ids=list(queries.keys())
        top_k_values, top_k_indices = torch.topk(scores, k=min(k, scores.shape[1]), dim=1)
        
        # Convert tensors to numpy for easier processing
        values = top_k_values.numpy()
        indices = top_k_indices.numpy()
        
        # Create results list
        results = {}
        
        # Process each row
        query_idx=0
        for row_values, row_indices in zip(values, indices):
            # Create dict of {querykey:{metakey, score}}      
            results[query_ids[query_idx]]={self.keymap[idx]: score for idx, score in zip(row_indices, row_values)}
            query_idx+=1
            
        return Run.from_dict(results)
    
    def evaluate(self,scores,queries,k=100):
        run = self.scores_to_run(scores,queries,k)
        return ranx_eval(self.qrel,run,self.metrics)