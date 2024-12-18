from spacy.cli import download
import spacy
import json
import csv

def download_spacy():
    # Downloads spacy model if not already downloaded
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        print("Downloading 'en_core_web_sm' model...")
        download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")
    return nlp

def assemble_visual_description(vdict)->str:
    return ' '.join(list(vdict.values()))

def assemble_contextual_description(cdict)->str:
    return ' '.join(list(cdict.values()))

def query_assembly(query_type,obj)->str:
  match query_type:
    case "contextual":
        return assemble_contextual_description(obj["contextual"])
    case "visual":
        return assemble_visual_description(obj["visual"])
    case "as-is":
        return obj["description"]
      
def assemble_visual_queries(file_path)->dict:
    with open(file_path,"r",encoding="utf-8") as f:
        data=json.load(f)
    queries={}
    for key in data:
        queries[key]=assemble_visual_description(data[key]["visual"])
        
    return queries

def write_qrel(qrels_path,qrels):
       """
       Writes a 2d array of qrels into the file at qrels_path.
       The format must be as follows:
       [
           [query_id,0,document_id,relevance]
           ...
       ]
       """
       with open(qrels_path,'w',encoding="utf-8",newline="") as qrel_file:
        writer=csv.writer(qrel_file, delimiter='\t',quoting=csv.QUOTE_MINIMAL)
        for row in qrels:
            writer.writerow(row)

def metadata_to_qrel(qrels_path, metadata):
    """
    Take metadata and get a qrel file (.tsv) *assuming only true sample is self
    """
    qrel_2d = []
    for sample_id, sample in metadata.items():
        qrel_2d.append([sample_id, 0, sample_id, 1])
    write_qrel(qrels_path,qrel_2d)

def metadata_to_queries(metadata, path, query_type:str="as-is"):
    """
    Take metadata and convert to format that is required by Evaluator class
    """
    queries = {}
    for sample_id, sample in metadata.items():
        queries[sample_id] = query_assembly(query_type, sample)
    with open(path,'w',encoding='utf-8') as f:
        f.write(json.dumps(queries,indent=4,ensure_ascii=False))

def write_querys(querys_path,querys):
    """
    Writes a querys file (.json) to the file at querys_path
    """
    with open(querys_path,'w',encoding='utf-8') as query_file:
        query_file.write(json.dumps(querys,indent=4,ensure_ascii=False))
