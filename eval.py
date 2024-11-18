from long_clip.Evaluator import Evaluator
from metaprocessor import assemble_visual_queries
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

evaluator=Evaluator(
    "./long_clip/checkpoints/longclip-B.pt",
    "data/splits/test_original.json",
    "image_embeddings/test.pt",
    ["precision@1","mrr"],
    device
)

evaluator.search(assemble_visual_queries("data/splits/test_original.json"))