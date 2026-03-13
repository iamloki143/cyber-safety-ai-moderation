import os
import sys

sys.path.append(os.path.dirname(__file__))

from inference import analyze_image

image_path = os.path.join(os.path.dirname(__file__), "test9.jpg")

result = analyze_image(image_path)

print("Final Result:")
print(result)