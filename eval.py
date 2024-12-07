from long_clip.Evaluator import Evaluator
from metaprocessor import assemble_visual_queries
import torch
import json

device = "cuda" if torch.cuda.is_available() else "cpu"
evaluator=Evaluator(
    "./long_clip/checkpoints/longclip-L.pt",
    "bins.json",
    "data/as_is_v_visual/visual.tsv",
    "image_embeddings/test.pt",
    ["precision@1","mrr"],
    device
)

with open("data/as_is_v_visual/visual.json",encoding="utf-8") as visual_file:
    queries=json.load(visual_file)
    
scores=evaluator.search(queries)
evaluator.evaluate(scores,queries)