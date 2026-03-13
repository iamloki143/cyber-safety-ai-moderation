import os
import sys

sys.path.append(os.path.dirname(__file__))

from nsfw_model import predict_nsfw

image_path = os.path.join(os.path.dirname(__file__), "test2.jpg")

score, is_nsfw = predict_nsfw(image_path)

print("NSFW Confidence:", score)

if is_nsfw and score > 0.6:
    print("Sexual Content: YES")
else:
    print("Sexual Content: NO")