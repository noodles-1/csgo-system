import cv2
import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
root = os.path.dirname(parent)
sys.path.append(root)

from controllers import controller

results = controller.detect_license_plate(frame=cv2.imread('test_images/13.jpg'))
print(results)