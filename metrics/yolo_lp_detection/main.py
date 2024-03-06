from ultralytics import YOLO
import cv2

model = YOLO('trained_models/lp_detection/trained_yolov8n.pt')
model.predict(source=cv2.imread('test_images/3.jpg'), save=True)