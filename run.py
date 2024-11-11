from long_clip.model import longclip
import torch
import format

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = longclip.load("./long_clip/checkpoints/longclip-B.pt", device=device)

input_path = "./test.json"
text, images, idx_key_map = format.dataToInput(input_path, preprocess, device)

with torch.no_grad():
    image_features = model.encode_image(images)
    text_features = model.encode_text(text)
    
    logits_per_image = image_features @ text_features.T
    probs = logits_per_image.softmax(dim=-1).cpu().numpy()

results = format.probsToSamples(probs, idx_key_map)
format.printResults(results)