import os

from models.image.nsfw_model import predict_nsfw
from models.image.violence_model import predict_violence

# NEW IMPORTS
from models.image.caption import generate_caption
from models.utils.reason_generator import generate_detailed_reason


def analyze_image(image_path):

    # Run models
    nsfw_score, is_nsfw = predict_nsfw(image_path)
    violence_score, is_violent = predict_violence(image_path)

    # -------------------------
    # NSFW DETECTION
    # -------------------------
    if is_nsfw and nsfw_score > 0.6:

        caption = generate_caption(image_path)

        reason = generate_detailed_reason(
            caption,
            content_type="image",
            category="sexual_content"
        )

        return {
            "status": "unsafe",
            "category": "sexual_content",
            "confidence": round(float(nsfw_score), 2),
            "description": reason
        }

    # -------------------------
    # VIOLENCE DETECTION
    # -------------------------
    if is_violent and violence_score > 0.45:

        caption = generate_caption(image_path)

        reason = generate_detailed_reason(
            caption,
            content_type="image",
            category="violence"
        )

        return {
            "status": "unsafe",
            "category": "violence",
            "confidence": round(float(violence_score), 2),
            "description": reason
        }

    # -------------------------
    # SAFE IMAGE (dynamic confidence)
    # -------------------------

    # confidence based on how safe it is
    safety_score = max(1 - nsfw_score, 1 - violence_score)

    return {
        "status": "safe",
        "category": "none",
        "confidence": round(float(safety_score), 2),
        "description": "The image appears safe and does not contain harmful content."
    }