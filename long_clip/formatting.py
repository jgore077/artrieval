from long_clip.model import longclip
import json
import torch
from PIL import Image
from typing import Tuple


FP="file_path"


def getImagePaths(metadata:dict)->list:
    """
    Return all file paths from a metadata file
    """
    return [obj[FP] for obj in metadata.values()]

def preprocessImages(file_paths:list[str],preproccess,device):
    images = []
    for file_path in file_paths:
         images.append(preproccess(Image.open(file_path)).unsqueeze(0).to(device))
    return images

# convert our data into input-ready format
def dataToInput(file_path:str, image_preprocess, device)->Tuple[torch.Tensor, torch.Tensor, dict]:
    with open(file_path, "r", encoding="utf-8") as f:
        samples = json.load(f)

    texts = []
    images = []
    idx_key_map = {}
    for idx, (key, sample) in enumerate(samples.items()):
        texts.append(sample["description"])
        images.append(image_preprocess(Image.open(sample["file_path"])).unsqueeze(0).to(device))
        idx_key_map[idx] = key

    texts = longclip.tokenize(texts).to(device)
    images = torch.cat(images, dim=0)
    return texts, images, idx_key_map

# given the model predictions, return a results dict
def probsToSamples(probs, idx_key_map)->dict:
    results = {}
    for idx, image_results in enumerate(probs):
        max_index, max_value = max(enumerate(image_results), key=lambda x: x[1])
        results[idx_key_map[idx]] = idx_key_map[max_index]

    return results

# print results dict
def printResults(results):
    for key in results:
        print(f"Description of sample {key} returned image of sample {results[key]}")