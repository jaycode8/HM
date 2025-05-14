import cv2
import random
from ultralytics import YOLO
import numpy as np
from PIL import Image

def prediction(img):
    model = YOLO("model/best.pt")
    image = np.array(img)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    results = model(image)
    result = results[0]

    return result.names