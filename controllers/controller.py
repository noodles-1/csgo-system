import pytesseract

from ultralytics import YOLO

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
vehicle_detection_model = YOLO('trained_models/vehicle_detection/trained_yolov8n.pt')
lp_detection_model = YOLO('trained_models/lp_detection/trained_yolov8n_2.pt')

def detect_vehicle(frame):
    return vehicle_detection_model.predict(source=frame)

def detect_license_plate(frame):
    return lp_detection_model.predict(source=frame)

def validate_license_number(frame):
    return pytesseract.image_to_string(image=frame, lang='eng', config='--psm 10 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')