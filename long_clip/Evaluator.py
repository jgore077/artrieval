from .model import longclip, tokenize
from .formatting import getImagePaths,preprocessImages
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
        embeddings_file,
        metrics:list[str],
        device,
    ) -> None:
        self.device=device
        self.long_clip_model_name=long_clip_model_name
        self.model,self.preprocess=longclip.load(long_clip_model_name,device=self.device)
        self.metadata_file:str=metadata_file
        self.embeddings_file:str=embeddings_file
        self.metrics=metrics
        self._load_metadata()
        self._load_embeddings()
        self._build_keymap()
        
        
        
    def _load_embeddings(self):
        
        
        if not self.embeddings_file.endswith('.pt'):
            raise Exception("the embeddings file must be a .pt file")
        
        embedding_dir=os.path.dirname(self.embeddings_file)
        if not os.path.exists(embedding_dir):
            os.makedirs(embedding_dir,exist_ok=True)
            
        if not os.path.exists(self.embeddings_file):
            self.embeddings=self._make_image_embeddings()
            return
        
        self.embeddings=torch.load(self.embeddings_file,map_location=self.device)
        
        
    def _make_image_embeddings(self):
        files=getImagePaths(self.metadata)
        images=preprocessImages(files,self.preprocess,self.device)
        embeddings=self.model.encode_image(images)
        torch.save(embeddings,self.embeddings_file)
        self.embeddings=embeddings
    
    
    def _load_metadata(self):
        with open(self.metadata_file,"r",encoding="utf-8") as f:
            self.metadata=json.load(f)
            
    def _build_keymap(self):
        self.keymap={}
        for i,key in enumerate(self.metadata):
                self.keymap[key]=i
                

    def search(self,querys:dict|str,k=100):
        """
        Takes a path to a querys file or a dictionary of querys then finds the top k results for each query
        """
        if type(querys)==str:
            querys=load_querys(querys)
        encoded_querys=longclip.tokenize(list(querys.values()),truncate=True).to(self.device)
        text_features = self.model.encode_text(encoded_querys)
        scores=sim_matrix(self.embedd,text_features)