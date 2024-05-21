import os
import sys
import cv2
import psutil
import math
import datetime
from datetime import datetime as datetime_module
import csv
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
import hashlib

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from ultralytics import YOLO
from cnocr import CnOcr

class AIController:
    vehicleClasses = set([i for i in range(9)])
    vehicle_detection_model = YOLO('trained_models/vehicle_detection/trained_yolov8n_2.pt')
    lp_detection_model = YOLO('trained_models/lp_detection/trained_yolov8n_3.pt')
    cnocr = CnOcr(det_model_name='en_PP-OCRv3_det', rec_model_name='en_PP-OCRv3')

    @staticmethod
    def detect_vehicle(frame):
        return AIController.vehicle_detection_model.track(source=frame, verbose=False, persist=True, device=0, workers=0, classes=list(AIController.vehicleClasses))

    @staticmethod
    def detect_license_plate(frame):
        return AIController.lp_detection_model.predict(source=frame, verbose=False, device=0, workers=0)
    
    @staticmethod
    def get_license_number_cnocr(frame):
        return AIController.cnocr.ocr(img_fp=frame)
    
    @staticmethod
    def setVehicleClasses(id: int, isEnabled: bool):
        '''
        Adds or removes a vehicle ID from the vehicleClasses set. ID will be added
        if the isEnabled parameter is True, and removed otherwise.
        '''
        if isEnabled:
            AIController.vehicleClasses.add(id)
        else:
            if id in AIController.vehicleClasses:
                AIController.vehicleClasses.remove(id)

def bounding_box(frame, box, color, classNames):
    x1, y1, x2, y2 = box.xyxy[0]
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

    confidence = math.ceil((box.conf[0] * 100)) / 100

    cls = int(box.cls[0])

    org = [x1, y1]
    font = cv2.FONT_HERSHEY_PLAIN
    fontScale = 2
    thickness = 2

    cv2.putText(frame, classNames[cls] + ' ' + str(confidence), org, font, fontScale, (255, 255, 255), thickness)

def generateRevenueReport():
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

def generateBusiestTimeReport():
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
    '''
        With the restrictions functions, I can make some of it shorter, but I still dont know how to retrieve the user's restriction
        or how they are stored/saved in the system.
        
        Once that is known, the functions may change in the future, but the logic would still remain the same.
        
        If a user ID that's currently in session has a 1 restriction for n widgets, n widgets' state = normal.
        If a user ID that's currently in session has a 0 restriction for n widgets, n widget's state = disabled.
        
        Functions are called in the __init__ method of the pages(config, dashboard, and analytics)
    '''
    def dashboard_page_restriction(adminButton, userType):
        if userType == "admin":
            adminButton.config(state = 'normal')
        else:
            adminButton.config(state = 'disabled')
    
    def analytics_page_restriction(downloadButton, userType):
        if userType == "admin":
            downloadButton.config(state = 'normal')
        else:
            downloadButton.config(state = 'disabled')
    
    def config_page_restriction(carTrueRadioButton, carFalseRadioButton, truckTrueRadioButton,
                                truckFalseRadioButton, jeepneyTrueRadioButton, jeepneyFalseRadioButton,
                                busTrueRadioButton, busFalseRadioButton, motorTrueRadioButton,
                                motorFalseRadioButton, tricycleTrueRadioButton, tricycleFalseRadioButton,
                                vanTrueRadioButton, vanFalseRadioButton, taxiTrueRadioButton,
                                taxiFalseRadioButton, mJeepneyTrueRadioButton, mJeepneyFalseRadioButton,
                                carEntry, truckEntry, jeepneyEntry,
                                busEntry, motorcycleEntry, tricycleEntry,
                                vanEntry, taxiEntry, mjeepneyEntry,
                                fromComboBox, toComboBox, everyComboBox,
                                addButton, userType):
        
        if userType == "admin":
            carTrueRadioButton.config(state='normal')
            carFalseRadioButton.config(state='normal')
            truckTrueRadioButton.config(state='normal')
            truckFalseRadioButton.config(state='normal')
            jeepneyTrueRadioButton.config(state='normal')
            jeepneyFalseRadioButton.config(state='normal')
            busTrueRadioButton.config(state='normal')
            busFalseRadioButton.config(state='normal')
            motorTrueRadioButton.config(state='normal')
            motorFalseRadioButton.config(state='normal')
            tricycleTrueRadioButton.config(state='normal')
            tricycleFalseRadioButton.config(state='normal')
            vanTrueRadioButton.config(state='normal')
            vanFalseRadioButton.config(state='normal')
            taxiTrueRadioButton.config(state='normal')
            taxiFalseRadioButton.config(state='normal')
            mJeepneyTrueRadioButton.config(state='normal')
            mJeepneyFalseRadioButton.config(state='normal')
            carEntry.config(state='normal')
            truckEntry.config(state='normal')
            jeepneyEntry.config(state='normal')
            busEntry.config(state='normal')
            motorcycleEntry.config(state='normal')
            tricycleEntry.config(state='normal')
            vanEntry.config(state='normal')
            taxiEntry.config(state='normal')
            mjeepneyEntry.config(state='normal')
            fromComboBox.config(state='normal')
            toComboBox.config(state='normal')
            everyComboBox.config(state='normal')
            addButton.config(state='normal')
        else:
            carTrueRadioButton.config(state='disabled')
            carFalseRadioButton.config(state='disabled')
            truckTrueRadioButton.config(state='disabled')
            truckFalseRadioButton.config(state='disabled')
            jeepneyTrueRadioButton.config(state='disabled')
            jeepneyFalseRadioButton.config(state='disabled')
            busTrueRadioButton.config(state='disabled')
            busFalseRadioButton.config(state='disabled')
            motorTrueRadioButton.config(state='disabled')
            motorFalseRadioButton.config(state='disabled')
            tricycleTrueRadioButton.config(state='disabled')
            tricycleFalseRadioButton.config(state='disabled')
            vanTrueRadioButton.config(state='disabled')
            vanFalseRadioButton.config(state='disabled')
            taxiTrueRadioButton.config(state='disabled')
            taxiFalseRadioButton.config(state='disabled')
            mJeepneyTrueRadioButton.config(state='disabled')
            mJeepneyFalseRadioButton.config(state='disabled')
            carEntry.config(state='disabled')
            truckEntry.config(state='disabled')
            jeepneyEntry.config(state='disabled')
            busEntry.config(state='disabled')
            motorcycleEntry.config(state='disabled')
            tricycleEntry.config(state='disabled')
            vanEntry.config(state='disabled')
            taxiEntry.config(state='disabled')
            mjeepneyEntry.config(state='disabled')
            fromComboBox.config(state='disabled')
            toComboBox.config(state='disabled')
            everyComboBox.config(state='disabled')
            addButton.config(state='disabled')
    
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
    
    def update_user_credentials():
        pass
            
class EnvironmentController:
    def encrypt_variable():
        pass
    
    def decrypt_variable():
        pass
    
    def verify_variable():
        pass