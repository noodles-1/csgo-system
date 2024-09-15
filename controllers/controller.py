import os
import sys
import cv2
import psutil
import math
import csv
import pandas as pd
import random
import smtplib
import torch
import base64
#import pytesseract as tess

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from datetime import datetime as datetime_module
from dotenv import load_dotenv
from anthropic import Anthropic
from ultralytics import YOLO
#from cnocr import CnOcr

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from controllers.dbController import DBController

load_dotenv(dotenv_path='.env')
CLAUDE_KEY = os.getenv('CLAUDE_KEY')

class AIController:
    vehicleClasses = set([2, 3, 5, 7])
    vehicle_detection_model = YOLO(os.path.join(parent, 'yolov8n.pt'))
    lp_detection_model = YOLO(os.path.join(parent, 'trained_models/lp_detection/trained_yolov8n_3.pt'))
    #cnocr = CnOcr(det_model_name='en_PP-OCRv3_det', rec_model_name='en_PP-OCRv3')
    device = '0' if torch.cuda.is_available() else 'cpu'

    @staticmethod
    def detect_vehicle(frame):
        return AIController.vehicle_detection_model.track(source=frame, verbose=False, persist=True, classes=list(AIController.vehicleClasses), device=AIController.device)

    @staticmethod
    def detect_license_plate(frame):
        return AIController.lp_detection_model.predict(source=frame, verbose=False, device=AIController.device)
    
    '''
    @staticmethod
    def get_license_number_cnocr(frame):
        return AIController.cnocr.ocr(img_fp=frame)
    '''
    
    '''
    @staticmethod
    def get_license_number_tesseract(frame):
        return tess.image_to_string(frame, lang='eng', config='--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
    '''

    @staticmethod
    def get_license_number_claude(frame):
        anthropic = Anthropic(api_key=CLAUDE_KEY)
        _, buffer = cv2.imencode('.jpg', frame)
        encoded_image = base64.b64encode(buffer).decode('utf-8')
        
        response = anthropic.messages.create(
            model='claude-3-5-sonnet-20240620',
            max_tokens=1000,
            messages=[
                {
                    'role': 'user',
                    'content': [
                        {
                            'type': 'image',
                            'source': {
                                'type': 'base64',
                                'media_type': 'image/jpeg',
                                'data': encoded_image
                            }
                        },
                        {
                            'type': 'text',
                            'text': 'This image contains a license plate. Extract the license plate number to string. Do not include any other text.'
                        }
                    ]
                }
            ]
        )

        return response.content[0].text.strip().replace(' ', '')

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

cameraEnabled = False
dipModule = 0
loggedIn = False
currUser = None

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

class ReportGenerationController:
    @staticmethod
    def busiestTimeReport(file_path):
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
    
    @staticmethod
    def revenueReport(file_path):
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
    
    @staticmethod
    def vehiclesDetectedReport(file_path):
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
    def downloadAndProcessCSV():
        """
        Description:
        - This function saves a CSV file with a modified name to the user's "Downloads" folder after downloading it from a specified path and processing it if necessary.

        Returns:
        - success (bool): Indicates whether the operation was successful.
        - output_path (str or None): If successful, returns the path to the downloaded and processed CSV file; otherwise, returns None.
        """
        try:
            results = DBController.getFilteredLicensePlates()
            data = []
            for result in results.data:
                row = result[0]
                data.append({
                    'id': row.id,
                    'userId': row.userId,
                    'settingId': row.settingId,
                    'location': row.location,
                    'licenseNumber': row.licenseNumber,
                    'vehicleType': row.vehicleType,
                    'price': row.price,
                    'date': row.date,
                    'time': row.time,
                    'imageUrl': row.image
                })

            dataFrame = pd.DataFrame(data)

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
        
    @staticmethod
    def get_cpu_usage():
        cpu_percent = psutil.cpu_percent(interval=1)
        return [], [cpu_percent]

    @staticmethod
    def get_memory_usage():
        memory_percent = psutil.virtual_memory().percent
        return [], [memory_percent]

class AccountController:
    @staticmethod
    def generate_OTP():
        return str(random.randint(100000, 999999))
    
    @staticmethod
    def verify_OTP(otp, user_input_otp):
        return otp == user_input_otp
    
    @staticmethod
    def send_OTP(receiver_email, otp):
        #sender_email = os.getenv('CSGO_OTP_USER')
        #password = os.getenv("CSGO_OTP_PASS")
        credentials = DBController.getUser(email='csgotolllesstoll@gmail.com') # Change accordingly
        if not credentials:
            raise ValueError("Failed to retrieve email credentials from the database")
        
        sender_email = credentials.email
        password = credentials.password
        
        # if not sender_email or not password:
        #     raise ValueError("Email credentials are not set in Environment Variables")
        
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "CSGO Verification Code"
        
        body = f"""\
        <html>
            <body>
                <p>We have received a request to access the account {receiver_email}.</p>
                <p>This code is only valid for 5 minutes</p>
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