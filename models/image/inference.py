import os
from models.image.nsfw_model import predict_nsfw
from models.image.violence_model import predict_violence
def analyze_image(image_path):
    nsfw_score, is_nsfw = predict_nsfw(image_path)
    violence_score, is_violent = predict_violence(image_path)

    # Decision logic
    if is_nsfw and nsfw_score > 0.6:
        return {
            "status": "unsafe",
            "category": "sexual_content",
            "confidence": nsfw_score
        }

    if is_violent:
        return {
            "status": "unsafe",
            "category": "violence",
            "confidence": violence_score
        }

    return {
        "status": "safe",
        "category": "none",
        "confidence": max(1 - nsfw_score, violence_score)
    }