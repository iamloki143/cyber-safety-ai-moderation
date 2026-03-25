import cv2
import os

from models.image.inference import analyze_image

# NEW IMPORTS
from models.image.caption import generate_caption
from models.utils.reason_generator import generate_detailed_reason


def analyze_video(video_path):

    cap = cv2.VideoCapture(video_path)

    frame_count = 0
    unsafe_frames = 0
    total_checked = 0
    total_confidence = 0

    category = "safe"
    final_reason = "The video appears safe."

    while cap.isOpened():

        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1

        # analyze every 30th frame
        if frame_count % 30 == 0:

            total_checked += 1

            frame_path = f"temp_frame_{frame_count}.jpg"
            cv2.imwrite(frame_path, frame)

            result = analyze_image(frame_path)

            if result["status"] == "unsafe":

                unsafe_frames += 1
                category = result["category"]

                total_confidence += result["confidence"]

                # generate caption BEFORE deleting file
                caption = generate_caption(frame_path)

                final_reason = generate_detailed_reason(
                    caption,
                    content_type="video",
                    category=category
                )

            # delete temp frame
            if os.path.exists(frame_path):
                os.remove(frame_path)

    cap.release()

    # -------------------------
    # CONFIDENCE CALCULATION
    # -------------------------

    if total_checked == 0:
        total_checked = 1

    frame_ratio = unsafe_frames / total_checked

    avg_model_conf = (total_confidence / unsafe_frames) if unsafe_frames > 0 else 0

    # combine both (more realistic)
    confidence = (frame_ratio + avg_model_conf) / 2

    # -------------------------
    # FINAL DECISION
    # -------------------------

    if unsafe_frames > 0:

        return {
            "status": "unsafe",
            "category": category,
            "confidence": round(confidence, 2),
            "description": final_reason
        }

    return {
        "status": "safe",
        "category": "safe",
        "confidence": round(1 - confidence, 2),
        "description": "The video appears safe and does not contain harmful content."
    }