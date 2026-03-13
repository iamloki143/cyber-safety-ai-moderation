from models.text.inference import predict_text
from models.image.inference import analyze_image


def moderate_text(text):

    result = predict_text(text)

    if result["category"] == "Bullying":
        return {
            "status": "blocked",
            "reason": "Abusive language detected",
            "confidence": result["confidence"]
        }

    return {
        "status": "allowed"
    }


def moderate_image(image_path):

    result = analyze_image(image_path)

    if result["status"] == "unsafe":
        return {
            "status": "blocked",
            "reason": result["category"],
            "confidence": result["confidence"]
        }

    return {
        "status": "allowed"
    }