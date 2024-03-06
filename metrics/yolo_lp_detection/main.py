import cv2

from ultralytics import YOLO

model = YOLO('trained_models/lp_detection/trained_yolov8n_2.pt')
model.predict(source=cv2.imread('test_images/13.jpg'), save=True)