import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
root = os.path.dirname(parent)
sys.path.append(root)

from ultralytics import YOLO

model = YOLO('trained_models/vehicle_detection/trained_yolov8n_3.pt')
model.val(data='../datasets/ph-vehicles/data.yaml', device=0, workers=0)