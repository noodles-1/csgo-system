import os
import sys
import cv2

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
root = os.path.dirname(parent)
sys.path.append(root)

from ultralytics import YOLO
# from controllers import controller

# ai = controller.AIController()
# ai.detect_vehicle(frame=cv2.imread('test_images/8.jpg'))

model = YOLO('yolov8n.pt')
model.train(data='../datasets/ph-vehicles/data.yaml', pretrained=True, epochs=25, device=0, workers=0)