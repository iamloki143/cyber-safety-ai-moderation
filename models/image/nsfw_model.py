from transformers import pipeline
from PIL import Image

# Load NSFW classification model
nsfw_classifier = pipeline(
    "image-classification",
    model="Falconsai/nsfw_image_detection"
)

def predict_nsfw(image_path):
    image = Image.open(image_path).convert("RGB")

    results = nsfw_classifier(image)

    # results example:
    # [{'label': 'nsfw', 'score': 0.91}, {'label': 'sfw', 'score': 0.08}]

    for result in results:
        if result["label"].lower() == "nsfw":
            return result["score"], True

    return 0.0, False