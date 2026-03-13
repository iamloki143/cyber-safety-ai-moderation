import os
import sys

sys.path.append(os.path.dirname(__file__))

from violence_model import predict_violence

image_path = os.path.join(os.path.dirname(__file__), "test9.jpg")

score, is_violent = predict_violence(image_path)

print("Violence Score:", score)

if is_violent:
    print("Violence: YES")
else:
    print("Violence: NO")