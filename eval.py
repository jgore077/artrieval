from long_clip.Evaluator import Evaluator
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

evaluator=Evaluator(
    "./long_clip/checkpoints/longclip-B.pt",
    "bins.json",
    "image_embeddings/metadata.pt",
    ["precision@1","mrr"],
    device
)

evaluator.search("data/as_is_v_visual/visual.json")