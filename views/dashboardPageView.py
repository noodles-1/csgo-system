import os
import sys
import cv2
import tkinter as tk
import re
import socket
import numpy as np

from datetime import datetime
from customtkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import controllers.controller as cont
import views.switchView as switch

from controllers.controller import AIController
from controllers.dbController import DBController
from controllers.s3controller import S3Controller
from controllers.socketController import SocketController
from controllers.pollController import PollController

classnames = [
    "person", "bicycle", "car", "motorcycle", "aeroplane", "bus", "train", "truck", "boat",
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

class DashboardPage(tk.Frame):
    # Close Application
    def closeApplication(self):
        self.master.destroy()

    # Minimize or Iconify the Application
    def minimizeApplicaiton(self):
        self.master.iconify()
    
    def update_uptime(self):
        if self.counting_enabled:
            self.uptime_seconds += 1 
        
        hours = self.uptime_seconds // 3600
        minutes = (self.uptime_seconds % 3600) // 60
        seconds = self.uptime_seconds % 60
        
        time_string = f"{hours:02}:{minutes:02}:{seconds:02}"
        
        self.upTimeCount.configure(text=time_string)
        
        self.after(1000, self.update_uptime)
    
    class StartCamera:
        def __init__(self, currUser):
            self.currUser = currUser
            self.vehicleCount = 0

        def start(self, cap, placeholder_label, cameraId, databaseTable, vehiclesDetectedCount):
            if AIController.vehicle_detection_model.predictor:
                AIController.vehicle_detection_model.predictor.trackers[0].reset()

            detected_ids = set()

            def isValidLicensePlate(licensePlate: str) -> bool:
                regex1 = r'^[A-Z]{3}\d{3,4}$'
                regex2 = r'^\d{3,4}[A-Z]{3}$'
                return re.fullmatch(regex1, licensePlate) is not None or re.fullmatch(regex2, licensePlate) is not None
                
            def showFrame():
                success, frame = cap.read()
                currSetting = PollController.currSetting
                AIController.setVehicleClasses(2, currSetting.detectCar if currSetting else True)
                AIController.setVehicleClasses(3, currSetting.detectMotorcycle if currSetting else True)
                AIController.setVehicleClasses(5, currSetting.detectBus if currSetting else True)
                AIController.setVehicleClasses(7, currSetting.detectTruck if currSetting else True)

                if cont.loggedIn and success:
                    results = AIController.detect_vehicle(frame)
                    annotated_frame = results[0].plot()

                    for result in results:
                        for boxes in result.boxes:
                            if not boxes.id:
                                continue

                            id = int(boxes.id.item())
                            vehicle_id = int(boxes.cls.item())

                            self.vehicleCount = max(self.vehicleCount, id)
                            vehiclesDetectedCount.configure(text=f'{self.vehicleCount}')
                            
                            if id in detected_ids:
                                continue

                            detected_ids.add(id)
                            x1, y1, x2, y2 = boxes.xyxy[0]
                            cropped_vehicle = frame[int(y1.item()):int(y2.item()), int(x1.item()):int(x2.item())]
                            extracted_lp = None
                            
                            if currSetting:
                                lp_result = AIController.detect_license_plate(frame=cropped_vehicle)

                                if not lp_result[0].boxes:
                                    detected_ids.remove(id)
                                    continue

                                x1, y1, x2, y2 = lp_result[0].boxes[0].xyxy[0]
                                cropped_lp = cropped_vehicle[int(y1.item()):int(y2.item()), int(x1.item()):int(x2.item())]

                                # client_socket_foggy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                client_socket_lowlight = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                # client_socket_foggy.connect(('localhost', 8001))
                                client_socket_lowlight.connect(('localhost', 8000))

                                SocketController.sendImage(client_socket_lowlight, cropped_lp)
                                processed_lp = SocketController.receiveImage(client_socket_lowlight)

                                client_socket_lowlight.close()

                                if processed_lp is None:
                                    detected_ids.remove(id)
                                    continue

                                # Convert to grayscale
                                gray = cv2.cvtColor(processed_lp, cv2.COLOR_BGR2GRAY)

                                # Apply Gaussian Blur to reduce noise
                                blur = cv2.GaussianBlur(gray, (5, 5), 0)

                                # Apply thresholding
                                _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                                # Apply dilation to connect text regions
                                kernel = np.ones((2, 2), np.uint8)
                                dilated = cv2.dilate(thresh, kernel, iterations=1)

                                # Optionally apply erosion to reduce noise
                                eroded = cv2.erode(dilated, kernel, iterations=1)
                
                                extracted_lp_results = AIController.get_license_number_cnocr(frame=eroded)
                                temp = [extracted_lp_results[i]['text'] for i in range(len(extracted_lp_results))]
                                extracted_lp = ''.join(temp).replace(' ', '')
                                
                                if not isValidLicensePlate(extracted_lp):
                                    detected_ids.remove(id)
                                    continue
                                
                            try:
                                date = datetime.now().date()
                                time = datetime.now().time()
                                camera = DBController.getCamera(id=cameraId)
                                if classnames[vehicle_id] == 'car':
                                    price = currSetting.carPrice if currSetting else 0
                                elif classnames[vehicle_id] == 'motorcycle':
                                    price = currSetting.motorcyclePrice if currSetting else 0
                                elif classnames[vehicle_id] == 'bus':
                                    price = currSetting.busPrice if currSetting else 0
                                elif classnames[vehicle_id] == 'truck':
                                    price = currSetting.truckPrice if currSetting else 0
                                imageUrl = None
                                if currSetting:
                                    imageUrl = S3Controller().uploadImage(cropped_vehicle, f'[{date} - {time}] {classnames[vehicle_id]} - id: {id}')
                                response = DBController.addLicensePlate(self.currUser.id, currSetting.id if currSetting else 0, camera.location, extracted_lp or 'none', classnames[vehicle_id], price, imageUrl or 'none')

                                if response.ok:
                                    databaseTable.insert('', 0, values=(extracted_lp or 'none', classnames[vehicle_id], cameraId, time, date, price))
                            except Exception as e:
                                with open('logs.txt', 'a') as file:
                                    now = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                                    file.write(f'[{now}] Error at function views/dashboardPageView.py/dbController.py StartCamera/start()/showFrame() - {repr(e)}\n')
                                    print(repr(e))
                                    return

                    resized_frame = cv2.resize(annotated_frame, (640, 360))
                    frame_rgb = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(frame_rgb)
                    img_tk = ImageTk.PhotoImage(image=img)

                    if cont.cameraEnabled:
                        placeholder_label.configure(image=img_tk, text='')
                    placeholder_label.after(30 if cont.cameraEnabled else 800, showFrame)
                else:
                    cap.release()
                
            showFrame()
    
    # Function to change the camera displayed
    def changeCameraDisplay_callback(self, cameraName):
        print("Callback called with camera name:", cameraName)
        if self.cap:
            self.cap.release()

        result = DBController.getCamera(name=cameraName)
        ip_addr = result.id
        cameraUrl = f'rtsp://{ip_addr}:554'

        self.cap = cv2.VideoCapture('https://noodelzcsgoaibucket.s3.ap-southeast-1.amazonaws.com/videos/IMG_9613_1.mp4')
        DashboardPage.StartCamera(self.currUser).start(self.cap, self.placeholder_label, ip_addr, self.databaseTable, self.vehiclesDetectedCount)
        
        self.uptime_seconds = 0
        self.counting_enabled = True

    def setCurrUser(self, user):
        self.currUser = user
        self.adminButton.configure(state='disabled' if not user.isAdmin else 'normal')

    def __init__(self, parent):
        self.cap = None
        self.currUser = None

        self.uptime_seconds = 0
        self.counting_enabled = False
        self.vehicle_count = 0
        
        tk.Frame.__init__(self, parent, bg = "#090E18")
        
        # Style definition. Can be utilized with the Change Theme from Light to Dark
        style = ttk.Style()
        style.theme_use('forest-dark')
        
        # Close Icon (Currently Set to darkmode, if possible change to lightmode when the the changes)
        closePhoto = CTkImage(light_image = Image.open("views/icons/icon_close_darkmode.png"),
                              dark_image = Image.open("views/icons/icon_close_darkmode.png"),
                              size = (20, 20))

        # Minimize Icon (Currently Set to darkmode, if possible change to lightmode when the the changes)
        minimizePhoto = CTkImage(light_image = Image.open("views/icons/icon_minimize_darkmode.png"),
                              dark_image = Image.open("views/icons/icon_minimize_darkmode.png"),
                              size = (20, 20))

        # Top-most Frame that holds the Close and Minimize buttons.
        toolbarFrame = tk.Frame(self, bg = "#090E18", height = 30)
        toolbarFrame.pack(fill = "both", side = "top")

        closeButton = CTkButton(toolbarFrame, 
                                image = closePhoto,
                                text = "",
                                width = 20,
                                height = 20,
                                fg_color = "#090E18",
                                bg_color = "#000000",
                                hover = True,
                                hover_color = "#48BFE3",
                                command = self.closeApplication)
        closeButton.pack(side = "right", padx = 10, pady = 10)

        minimizeButton = CTkButton(toolbarFrame, 
                                image = minimizePhoto,
                                text = "",
                                width = 20,
                                height = 20,
                                fg_color = "#090E18",
                                bg_color = "#000000",
                                hover = True,
                                hover_color = "#48BFE3",
                                command = self.minimizeApplicaiton)
        minimizeButton.pack(side = "right", padx = 0, pady = 10)
        # End of Toolbar Frame
        
        # Start of Main Frame (Where the contents of the main page is)
        mainContentFrame = CTkScrollableFrame(self, bg_color = "#090E18", fg_color = "#090E18")
        mainContentFrame.pack(expand = True, fill = tk.BOTH, side = tk.TOP)
        
        mainFrame = CTkFrame(mainContentFrame, bg_color = "#090E18")
        mainFrame.pack(expand = True, fill = tk.BOTH, side = tk.TOP)
        
        bottomFrame = tk.Frame(self, bg = "#090E18")
        bottomFrame.pack(fill = "both", side = "top", padx = 20)

        # Goes to the Analytics Page
        analyticsButton = CTkButton(bottomFrame,
                                    text = 'Analytics',
                                    command = lambda: switch.showAnalyticsPage(parent),
                                    font = ('Montserrat', 15),
                                    border_width = 2,
                                    corner_radius = 15,
                                    border_color = '#5E60CE',
                                    text_color = '#5E60CE',
                                    fg_color = '#090E18',
                                    height = 30,
                                    width = 140)
        
        # Goes to the Admin Page (Should be disabled unless the user logged in is an Admin)
        self.adminButton = CTkButton(bottomFrame,
                                text = 'Admin',
                                command = lambda: switch.showAdminPage(parent, self.changeCameraDisplay, self.cap, self.placeholder_label), 
                                font = ('Montserrat', 15),
                                border_width = 2,
                                corner_radius = 15,
                                border_color = '#5E60CE',
                                text_color = '#5E60CE',
                                fg_color = '#090E18',
                                height = 30,
                                width = 140)
        
        analyticsButton.pack(side = 'right', padx = 10, pady = 10)
        self.adminButton.pack(side = 'right', padx = 10, pady = 10)
        
        analyticsButton.bind("<Enter>", lambda event: analyticsButton.configure(text_color="#090E18", fg_color = "#5E60CE")) 
        analyticsButton.bind("<Leave>", lambda event: analyticsButton.configure(text_color="#5E60CE", fg_color = "#090E18")) 
        
        self.adminButton.bind("<Enter>", lambda event: self.adminButton.configure(text_color="#090E18", fg_color = "#5E60CE")) 
        self.adminButton.bind("<Leave>", lambda event: self.adminButton.configure(text_color="#5E60CE", fg_color = "#090E18")) 

        # Separates the Main Frame into two Sides (Left and Right)
        leftMainFrame = tk.Frame(mainFrame, bg = "#090E18")
        rightMainFrame = tk.Frame(mainFrame, bg = "#090E18")
        leftMainFrame.pack(side = 'left', fill = 'both', expand = True, pady = 5)
        rightMainFrame.pack(side = 'left', fill = 'both', expand = True, pady = 5)

        databaseFrame = tk.Frame(rightMainFrame, bg = '#1B2431')
        databaseFrame.pack(expand = True, fill = 'both', padx = 15, pady = 10)
        
        databaseTableFrame = tk.Frame(databaseFrame, bg = '#1B2431')
        databaseTableFrame.pack(expand = True, fill = 'both', padx = 0, pady = 0)

        style.configure("Treeview",
                        background = '#1B2431',
                        foreground = '#FFFFFF',
                        rowheight = 25,
                        fieldbackgrounds = '#1B2431',
                        bordercolor = '#343638',
                        borderwidth = 0)
        
        style.map('Treeview', background = [('selected', '#48BFE3')], foreground = [('selected', '#000000')])
        
        style.configure("Treeview.Heading",
                        background="#1B2431",
                        color = "#1B2431",
                        foreground="white",
                        font = ('Montserrat', 10),
                        relief="flat")
        
        style.map("Treeview.Heading",
                  background=[('active', '#48BFE3')])

        # ADD or REMOVE headers as needed @Database Integration
        self.databaseTable = ttk.Treeview(databaseTableFrame, columns = ('licensePlate', 'vehicleType', 'cameraID', 'time', 'date', 'price'), show = "headings", style = 'Custom.Treeview')

        # Inserts Blank Entries to the Treeview so that it doesnt look bad when the Treeview is Empty.
        #for _ in range(100):
            #databaseTable.insert('', 'end', values=('', '', '', '', '', ''))

        self.databaseTable.tag_configure('even', background='#2A2D2E', foreground='#FFFFFF')
        self.databaseTable.tag_configure('odd', background='#343638', foreground='#FFFFFF')
        
        self.databaseTable.heading('licensePlate', text="License Plate", anchor='center')
        self.databaseTable.heading('vehicleType', text="Vehicle Type", anchor='center')
        self.databaseTable.heading('cameraID', text="Camera ID", anchor='center')
        self.databaseTable.heading('time', text="Time", anchor='center')
        self.databaseTable.heading('date', text="Date", anchor='center')
        self.databaseTable.heading('price', text="Price", anchor='center')

        self.databaseTable.column('licensePlate', width=150, anchor='center')
        self.databaseTable.column('vehicleType', width=150, anchor='center')
        self.databaseTable.column('cameraID', width=120, anchor='center')
        self.databaseTable.column('time', width=100, anchor='center')
        self.databaseTable.column('date', width=100, anchor='center')
        self.databaseTable.column('price', width=80, anchor='center')

        self.databaseTable.pack(side = 'left', expand=True, fill='both', padx=0, pady=0)

        yscrollbar = ttk.Scrollbar(databaseTableFrame, orient='vertical', command=self.databaseTable.yview)
        self.databaseTable.configure(yscrollcommand=yscrollbar.set)
        yscrollbar.pack(side='right', fill='both', padx=5, pady=0)
        
        xscrollbar = ttk.Scrollbar(databaseFrame, orient='horizontal', command=self.databaseTable.xview)
        self.databaseTable.configure(xscrollcommand=xscrollbar.set)
        xscrollbar.pack(side='bottom', fill='both', padx=0, pady=5)
        
        topLeftMainFrame = tk.Frame(leftMainFrame, bg = "#090E18")
        middleLeftMainFrame = tk.Frame(leftMainFrame, bg = "#090E18")
        bottomLeftMainFrame = tk.Frame(leftMainFrame, bg = "#090E18")

        bottomLeftMainFrame.pack(side = 'bottom', fill = 'both', padx = 10)
        middleLeftMainFrame.pack(side = 'bottom', fill = 'both', padx = 10)
        topLeftMainFrame.pack(side = 'bottom', fill = 'both', expand = True)

        vehicleDetectedBottomLeftMainFrame = tk.Frame(bottomLeftMainFrame, bg = '#090E18')
        upTimeBottomLabelLeftMainFrame = tk.Frame(bottomLeftMainFrame, bg = '#090E18')
        cameraIDBottomLeftFrame = tk.Frame(bottomLeftMainFrame, bg = '#090E18')

        vehicleDetectedBottomLeftMainFrame.pack(side = 'left', expand = True, fill = 'x')
        upTimeBottomLabelLeftMainFrame.pack(side = 'left', expand = True, fill = 'x')
        cameraIDBottomLeftFrame.pack(side = 'left', expand = True, fill = 'x')

        vehicleDetectedLabel = CTkLabel(vehicleDetectedBottomLeftMainFrame, text = 'Vehicles Detected: ', text_color = 'white', font = ('Montserrat', 12))
        self.vehiclesDetectedCount = CTkLabel(vehicleDetectedBottomLeftMainFrame, text = '', text_color = 'white', font = ('Montserrat', 12)) # This updates
        
        upTimeLabel = CTkLabel(upTimeBottomLabelLeftMainFrame, text = 'Camera Up Time: ', text_color = 'white', font = ('Montserrat', 12))
        self.upTimeCount = CTkLabel(upTimeBottomLabelLeftMainFrame, text = '', text_color = 'white', font = ('Montserrat', 12)) # This updates
        
        vehicleDetectedLabel.pack(side = 'left', padx = 3)
        self.vehiclesDetectedCount.pack(side = 'left', padx = (0, 5))
        
        upTimeLabel.pack(side = 'left', padx = 3)
        self.upTimeCount.pack(side = 'left', padx = (0, 5))
        
        cameraFrame = CTkFrame(topLeftMainFrame, fg_color = '#1B2431')
        cameraFrame.pack(fill = 'both', expand = True, padx = 15, pady = 10)

        # This is where you should input the camera Frame. Delete the code below this if integrating the camera display.
        self.placeholder_label = CTkLabel(cameraFrame, text='(Change cameras below)', font = ('Montserrat', 45), text_color = 'white')
        self.placeholder_label.pack(fill = 'both', expand = True)
        # ----
        
        dropdownFrame = CTkFrame(cameraFrame, fg_color = "#1B2431")
        dropdownFrame.pack(fill = 'x', side = "bottom", padx = 10, pady = 10)

        cameras = DBController.getCameras()
        
        self.changeCameraDisplay = CTkComboBox(dropdownFrame, values=[camera[0].name for camera in cameras.data], command=self.changeCameraDisplay_callback, width=100, state='readonly')
        self.changeCameraDisplay.set('(NONE)')
        self.changeCameraDisplay.pack(side = "right")
        
        changeCameraLabel = CTkLabel(dropdownFrame, text = "Change Camera", font = ('Montserrat', 13), text_color = "#FFFFFF")
        changeCameraLabel.pack(side = "right", padx = 10)
        
        # Goes to the Config Page
        settingsButton = CTkButton(middleLeftMainFrame,
                                    text = 'Settings',
                                    height = 32,
                                    width = 148,
                                    text_color = '#48BFE3',
                                    command = lambda: switch.showSettingsPage(parent), 
                                    border_color = '#48BFE3', 
                                    fg_color = '#090E18', 
                                    border_width = 2,
                                    hover_color = '#48BFE3',
                                    corner_radius = 15,
                                    font = ('Montserrat', 15))
        
        settingsButton.pack(side = 'left', padx = 5, pady = 20)
        
        settingsButton.bind("<Enter>", lambda event: settingsButton.configure(text_color="#090E18", fg_color = "#48BFE3")) 
        settingsButton.bind("<Leave>", lambda event: settingsButton.configure(text_color="#48BFE3", fg_color = "#090E18")) 

        self.update_uptime()