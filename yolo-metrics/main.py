from ultralytics import YOLO
import cv2

model = YOLO("models/trained_yolov8n.pt")
model.predict(source=cv2.imread("<image>"), save=True)