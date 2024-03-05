from ultralytics import YOLO

model = YOLO('trained_models/trained_yolov8n.pt')

def detect_vehicle(frame):
    return model.predict(source=frame)