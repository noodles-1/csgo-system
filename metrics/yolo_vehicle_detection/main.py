from ultralytics import YOLO
import cv2

model = YOLO('yolov9c.pt')
model.train(data='../datasets/ph-vehicles/data.yaml', pretrained=True, epochs=5, device=0, workers=0, save=True)