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

def updateVehiclePrice(vehicleType, newPrice):
    global vehiclePrices
    
    # vehicleType Jeepney, jeepney, jEepney, etc. != to each other
    vehicleType = vehicleType.upper() # any input ni user will be all uppercase
    
    if vehicleType not in vehiclePrices:
        print("Error: Vehicle type not found.")
        return
    
    if not isinstance(newPrice, float):
        print("Error: Price should be a whole number") # 0 - Infinity
        return
    
    if newPrice < 0:
        print("Error: Price should be non-negative.")
        return
    
    vehiclePrices[vehicleType] = newPrice # Simple assignment to the dictionary
    print(f"Price for {vehicleType} updated to {newPrice}.")