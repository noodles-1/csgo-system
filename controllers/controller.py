import pytesseract
import cv2
import math

from ultralytics import YOLO

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
vehicle_detection_model = YOLO('trained_models/vehicle_detection/trained_yolov8n.pt')
lp_detection_model = YOLO('trained_models/lp_detection/trained_yolov8n_2.pt')

classNames = [
    "person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
    "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
    "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
    "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
    "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
    "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
    "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
    "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
    "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
    "teddy bear", "hair drier", "toothbrush"
]

def bounding_box(frame, box):
    x1, y1, x2, y2 = box.xyxy[0]
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

    cv2.rectangle(frame, (x1, y1), (x2, y2), (200, 50, 50), 2)

    confidence = math.ceil((box.conf[0] * 100)) / 100

    cls = int(box.cls[0])

    org = [x1, y1]
    font = cv2.FONT_HERSHEY_PLAIN
    fontScale = 2
    color = (255, 255, 255)
    thickness = 2

    cv2.putText(frame, classNames[cls] + ' ' + str(confidence), org, font, fontScale, color, thickness)

def detect_vehicle(frame):
    return vehicle_detection_model.predict(source=frame)

def detect_license_plate(frame):
    return lp_detection_model.predict(source=frame, save=True)

def validate_license_number(frame):
    return pytesseract.image_to_string(image=frame, lang='eng', config='--psm 10 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')