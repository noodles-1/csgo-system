import os
import sys
import cv2
import math
import datetime
import csv
import pytesseract
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from ultralytics import YOLO
from cnocr import CnOcr

class AIController:
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        self.vehicle_detection_model = YOLO('trained_models/vehicle_detection/trained_yolov8n_2.pt')
        self.lp_detection_model = YOLO('trained_models/lp_detection/trained_yolov8n_3.pt')
        self.cnocr = CnOcr(det_model_name='en_PP-OCRv3_det', rec_model_name='en_PP-OCRv3')

    def detect_vehicle(self, frame):
        return self.vehicle_detection_model.predict(source=frame, save=True)

    def detect_license_plate(self, frame):
        return self.lp_detection_model.predict(source=frame)

    def get_license_number_tesseract(self, frame):
        return pytesseract.image_to_string(image=frame, lang='eng', config='--psm 10 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    
    def get_license_number_cnocr(self, frame):
        return self.cnocr.ocr(img_fp=frame)

classNames = ["car", "motorbike"]

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

def generate_revenue_report():
    curr_date = datetime.date.today().strftime('%Y-%m-%d')
    df = pd.read_csv('dummy_data/data.csv')
    curr_date_revenue = df.loc[df['Date'] == curr_date]['Price'].sum()

    curr_month = datetime.date.today().strftime('%Y-%m')
    curr_month_revenue = df.loc[df['Date'].str[:7] == curr_month]['Price'].sum()
    
    curr_year = datetime.date.today().strftime('%Y')
    curr_year_revenue = df.loc[df['Date'].str[:4] == curr_year]['Price'].sum()
    
    with open('reports/revenue.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([f'Revenue today ({curr_date})', f'Revenue this month ({curr_month})', f'Revenue this year ({curr_year})'])
        writer.writerow([curr_date_revenue, curr_month_revenue, curr_year_revenue])

def generate_busiest_time_report():
    df = pd.read_csv('dummy_data/data.csv')
    times = [int(time.split(':')[0]) for time in df['Time'].tolist()]
    _, ax = plt.subplots()
    _, bins, _ = ax.hist(times, bins=23, edgecolor='gray')
    ax.set_xticks(bins)
    plt.xlabel('times in 24-hour format')
    plt.ylabel('no. of detected vehicles')
    plt.savefig('reports/busiest_times.jpg')