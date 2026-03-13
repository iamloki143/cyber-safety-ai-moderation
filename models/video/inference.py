import cv2
import os

from models.image.inference import analyze_image


def analyze_video(video_path):

    cap = cv2.VideoCapture(video_path)

    frame_count = 0
    unsafe_frames = 0
    category = "safe"

    while cap.isOpened():

        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1

        # analyze every 30th frame
        if frame_count % 30 == 0:

            frame_path = "temp_frame.jpg"

            cv2.imwrite(frame_path, frame)

            result = analyze_image(frame_path)

            if result["status"] == "unsafe":

                unsafe_frames += 1
                category = result["category"]

    cap.release()

    if unsafe_frames > 3:

        return {
            "status": "unsafe",
            "category": category,
            "confidence": 0.85
        }

    return {
        "status": "safe",
        "category": "safe",
        "confidence": 0.90
    }