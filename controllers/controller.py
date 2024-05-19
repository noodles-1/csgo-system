import os
import sys
import cv2
import psutil
import math
import datetime
from datetime import datetime as datetime_module
import csv
import pytesseract
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import tkinter as tk
from scipy.interpolate import make_interp_spline
from scipy.interpolate import interp1d
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

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
        return self.vehicle_detection_model.predict(source=frame)

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

class ReportGenerationController:
    def busiestTimeReport(self, file_path):
        """
        Description:
        - This function generates a report of the busiest time based on the data provided in the specified CSV file for the current date.

        Arguments:
        - file_path (str): The path to the CSV file containing the data.

        Returns:
        - xData (list): A list of time intervals representing the x-axis data.
        - yData (list): A list of corresponding counts representing the y-axis data.
        """
        today = datetime_module.today().strftime('%Y-%m-%d')
        time_counts = {}

        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                time_str = row[3]
                date_str = row[4]

                if date_str == today:
                    time = time_str.split(':')[0]

                    if time in time_counts:
                        time_counts[time] += 1
                    else:
                        time_counts[time] = 1

        xData = list(time_counts.keys())
        yData = list(time_counts.values())

        return xData, yData
    
    def revenueReport(self, file_path):
        """
        Description:
        - This function generates a report of the revenue based on the data provided in the specified CSV file for the latest 15 dates.

        Arguments:
        - file_path (str): The path to the CSV file containing the data.

        Returns:
        - latest_dates (list): A list of the latest 15 dates.
        - latest_revenues (list): A list of corresponding revenues for the latest 15 dates.
        """
        date_revenue = {}

        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                date = row[4]
                price = int(row[5])

                if date not in date_revenue:
                    date_revenue[date] = price
                else:
                    date_revenue[date] += price

        sorted_date_revenue = dict(sorted(date_revenue.items(), key=lambda x: datetime_module.strptime(x[0], "%Y-%m-%d"), reverse=True))

        latest_dates = list(sorted_date_revenue.keys())[:15]
        latest_revenues = [sorted_date_revenue[date] for date in latest_dates]

        return latest_dates, latest_revenues
    
    def vehiclesDetectedReport(self, file_path):
        """
        Description:
        - This function generates a report of the vehicles detected based on the data provided in the specified CSV file for the latest 15 dates.

        Arguments:
        - file_path (str): The path to the CSV file containing the data.

        Returns:
        - latest_dates (list): A list of the latest 15 dates.
        - latest_counts (list): A list of corresponding counts of vehicles detected for the latest 15 dates.
        """
        date_counts = {}

        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                date = row[4]
                date_counts[date] = date_counts.get(date, 0) + 1

        sorted_date_counts = dict(sorted(date_counts.items(), key=lambda x: datetime_module.strptime(x[0], "%Y-%m-%d"), reverse=True))

        latest_dates = list(sorted_date_counts.keys())[:15]
        latest_counts = [sorted_date_counts[date] for date in latest_dates]

        return latest_dates, latest_counts

    @staticmethod
    def downloadAndProcessCSV(filePath):
        """
        Description:
        - This function saves a CSV file with a modified name to the user's "Downloads" folder after downloading it from a specified path and processing it if necessary.

        Arguments:
        - filePath (str): The path to the CSV file to be downloaded and processed.

        Returns:
        - success (bool): Indicates whether the operation was successful.
        - output_path (str or None): If successful, returns the path to the downloaded and processed CSV file; otherwise, returns None.
        """
        try:
            if not os.path.exists(filePath):
                raise FileNotFoundError(f"CSV File '{filePath}' not found.")
            
            dataFrame = pd.read_csv(filePath)

            # Perform processing if needed here

            # Get the path to the "Downloads" folder
            downloadPath = os.path.join(os.path.expanduser("~"), "Downloads")

            outputPath = os.path.join(downloadPath, 'downloaded_data.csv')
            dataFrame.to_csv(outputPath, index = False)

            return True, outputPath
        
        except FileNotFoundError as e:
            print(f"Error: {e}")
            raise 

        except Exception as e:
            print(f"Error: {e}")
            return False, None
        
    def get_cpu_usage():
        cpu_percent = psutil.cpu_percent(interval=1)
        return [], [cpu_percent]

    def get_memory_usage():
        memory_percent = psutil.virtual_memory().percent
        return [], [memory_percent]

class AccountController:
    def dashboard_page_restriction(adminButton, userType):
        if userType == "admin":
            adminButton.config(state = 'normal')
        else:
            adminButton.config(state = 'disabled')
    
    def analytics_page_restriction():
        pass
    
    def config_page_restriction():
        pass
    
    def generate_OTP():
        return str(random.randint(100000, 999999))
    
    def verify_OTP(otp, user_input_otp):
        return otp == user_input_otp
    
    def send_OTP(receiver_email, otp):
        sender_email = os.getenv('CSGO_OTP_USER')
        password = os.getenv("CSGO_OTP_PASS")
        
        if not sender_email or not password:
            raise ValueError("Email credentials are not set in Environment Variables")
        
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "CSGO Verification Code"
        
        body = f"""\
        <html>
            <body>
                <p>We have received a request to access the account {receiver_email}.</p>
                <p>Your Security code is:</p>
                <br>
                <p style = "text-align:center; font-size:20px; font-weight:bold;">{otp}</p>
                <br>
                <p>If you did not request this code, it is possible that someone is trying to access your acccount registered with {receiver_email}.</p>
                <p>Contact your administrator and secure your account as soon as possible.</p>
                <p style = "font-weight:bold">Do not forward or give this code to anyone</p>
                <br>
                <p>Sincerely yours,</p>
                <p>The CSGO Accounts Team</p>
            </body>
        </html>
        """
        message.attach(MIMEText(body, "html"))
        
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
            print("OTP sent successfully")
        except Exception as e:
            print(f"Failed to send OTP: {e}")