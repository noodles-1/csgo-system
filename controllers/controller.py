import pytesseract

from ultralytics import YOLO

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
model = YOLO('../trained_models/trained_yolov8m.pt')

def detect_vehicle(frame):
    return model.predict(source=frame)

def validate_license_number(frame):
    return pytesseract.image_to_string(image=frame, lang='eng', config='--psm 10 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')