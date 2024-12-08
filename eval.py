from long_clip.Evaluator import Evaluator
from metaprocessor import assemble_visual_queries
import argparse
import torch
import json

parser = argparse.ArgumentParser(
    description='Evaluator for processing and analyzing files'
)

parser.add_argument(
    '--long-clip-model', '-m', required=True, type=str,help='Path to the long CLIP model'
)

parser.add_argument(
    '--metadata', '-d', required=True, type=str, help='Path to the metadata file'
)

parser.add_argument(
    '--qrel', required=True, type=str, help='Path to the qrel file'
)

parser.add_argument(
    '--querys', required=True, type=str, help='Path to the querys file'
)

parser.add_argument(
    '--embeddings', '-e', required=True, type=str, help='Path to the embeddings file'
)

args = parser.parse_args()


device = "cuda" if torch.cuda.is_available() else "cpu"
evaluator=Evaluator(
    args.long_clip_model,
    args.metadata,
    args.qrel,
    args.embeddings,
    ["precision@1","mrr"],
    device
)

with open(args.querys,encoding="utf-8") as visual_file:
    queries=json.load(visual_file)
    
scores=evaluator.search(queries)
print(evaluator.evaluate(scores,queries))