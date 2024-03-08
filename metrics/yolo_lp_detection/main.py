import cv2
import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
root = os.path.dirname(parent)
sys.path.append(root)

from controllers import controller

img = cv2.imread('test_images/1.jpg')
vehicle_results = controller.detect_vehicle(frame=img)
x1, y1, x2, y2 = vehicle_results[0].boxes[4].xyxy[0]
cropped_vehicle = img[int(y1.item()):int(y2.item()), int(x1.item()):int(x2.item())]

controller.detect_license_plate(frame=cropped_vehicle)