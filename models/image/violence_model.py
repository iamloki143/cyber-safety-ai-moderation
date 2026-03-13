from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def predict_violence(image_path):
    image = Image.open(image_path).convert("RGB")

    labels = ["violence", "fighting", "weapon", "safe image"]

    inputs = processor(text=labels, images=image, return_tensors="pt", padding=True)

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits_per_image
    probs = logits.softmax(dim=1)

    violence_score = probs[0][0].item()
    fighting_score = probs[0][1].item()
    weapon_score = probs[0][2].item()
    safe_score = probs[0][3].item()

    max_score = max(violence_score, fighting_score, weapon_score)

    if max_score > safe_score:
        return max_score, True
    else:
        return safe_score, False