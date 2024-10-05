import os
import sys
import cv2
import tkinter as tk
import re
import socket
import asyncio
import threading
import tk_async_execute as tk_async

from datetime import datetime
from customtkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

current = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current)
sys.path.append(parent_dir)

import controllers.controller as cont
import views.switchView as switch

from controllers.controller import AIController
from controllers.dbController import DBController
from controllers.s3controller import S3Controller
from controllers.socketController import SocketController
from controllers.pollController import PollController
from controllers.googleController import GoogleController

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

class CongestionStateBar(tk.Canvas):
    def __init__(self, master, width=300, height=5):
        super().__init__(master, width=width, height=height, bg='#1B2431', highlightthickness=0)
        self.configure(highlightbackground='#1B2431')

        self.max_width = width
        self.bar = self.create_rectangle(0, 0, 0, height, fill='green', outline='green')

    def updateBar(self, value):
        # Ensure value is within the range 0.0 to 1.0
        value = max(0.0, min(1.0, value))

        # Calculate color based on value
        if value <= 0.5:
            red = int(255 * (value * 2))
            green = 255
        else:
            red = 255
            green = int(255 * (1 - value) * 2)

        # Convert to hexadecimal color code
        color = f'#{red:02x}{green:02x}00'

        # Update bar width
        bar_width = int(self.max_width * value)
        self.itemconfig(self.bar, fill=color)
        self.coords(self.bar, 0, 0, bar_width, self.winfo_height())

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
        vehicleCount = 0
        detected_ids = set()
        extracted_lps = set()

        def __init__(self, currUser):
            self.currUser = currUser

        @staticmethod
        def isValidLicensePlate(licensePlate: str) -> bool:
            regex1 = r'^[A-Z]{3}\d{3,4}$'
            regex2 = r'^\d{3,4}[A-Z]{3}$'
            return re.fullmatch(regex1, licensePlate) is not None or re.fullmatch(regex2, licensePlate) is not None
        
        async def extract(self, frame, id, cameraId, vehicle_id, currSetting, dynamicSetting, isHeavyTraffic, cropped_vehicle, databaseTable, vehiclesDetectedCount):
            with threading.Lock():
                if id in DashboardPage.StartCamera.extracted_lps:
                    return

                extracted_lp = AIController.get_license_number_claude(frame)

                if not DashboardPage.StartCamera.isValidLicensePlate(extracted_lp):
                    DashboardPage.StartCamera.detected_ids.remove(id)
                    return
                
                DashboardPage.StartCamera.extracted_lps.add(id)

                try:
                    date = datetime.now().date()
                    time = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                    camera = DBController.getCamera(id=cameraId)
                    if classnames[vehicle_id] == 'car':
                        price = 100 if dynamicSetting else 0
                        if currSetting:
                            price = currSetting.carPrice
                    elif classnames[vehicle_id] == 'motorcycle':
                        price = 100 if dynamicSetting else 0
                        if currSetting:
                            price = currSetting.motorcyclePrice
                    elif classnames[vehicle_id] == 'bus':
                        price = 100 if dynamicSetting else 0
                        if currSetting:
                            price = currSetting.busPrice
                    elif classnames[vehicle_id] == 'truck':
                        price = 100 if dynamicSetting else 0
                        if currSetting:
                            price = currSetting.truckPrice
                    imageUrl = None
                    if currSetting or (dynamicSetting and isHeavyTraffic):
                        imageUrl = S3Controller().uploadImage(cropped_vehicle, f'[{date} - {time}] {classnames[vehicle_id]} - id: {id}')
                    response = DBController.addLicensePlate(self.currUser.id, currSetting.id if currSetting else 0, camera.location, extracted_lp or 'none', classnames[vehicle_id], price, imageUrl or 'none')

                    if response.ok:
                        tk_async.tk_execute(databaseTable.insert, '', 0, values=(id, extracted_lp or 'none', classnames[vehicle_id], cameraId, datetime.now().strftime('%H:%M:%S'), date, price))
                        DashboardPage.StartCamera.vehicleCount += 1
                        tk_async.tk_execute(vehiclesDetectedCount.configure, text=f'{DashboardPage.StartCamera.vehicleCount}')
                except Exception as e:
                    with open('logs.txt', 'a') as file:
                        now = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                        file.write(f'[{now}] Error at function views/dashboardPageView.py/dbController.py StartCamera/start()/showFrame() - {repr(e)}\n')
                        print(repr(e))
                        return
                    
                return extracted_lp
        
        def start(self, cap, placeholder_label, cameraId, databaseTable, vehiclesDetectedCount):
            if AIController.vehicle_detection_model.predictor:
                AIController.vehicle_detection_model.predictor.trackers[0].reset()

            draw_boxes = True
            x_offset = 400
            y_offset = 60
            vehicle_offset = 0.65
            motorbike_offset = 0.875
            alpha = 0.4

            def showFrame():
                success, frame = cap.read()
                currSetting = PollController.currSetting
                dynamicSetting = PollController.dynamicSetting
                isHeavyTraffic = PollController.isHeavyTraffic
                AIController.setVehicleClasses(2, currSetting.detectCar if currSetting else True)
                AIController.setVehicleClasses(3, currSetting.detectMotorcycle if currSetting else True)
                AIController.setVehicleClasses(5, currSetting.detectBus if currSetting else True)
                AIController.setVehicleClasses(7, currSetting.detectTruck if currSetting else True)

                if cont.loggedIn and success:
                    frame_height, frame_width = frame.shape[0], frame.shape[1]
                    results = AIController.detect_vehicle(frame)
                    annotated_frame = results[0].plot()

                    # draw boxes to show detection boundary
                    if draw_boxes:
                        overlay = annotated_frame.copy()

                        top_left_1 = (0, 0)
                        bottom_right_1 = (frame_width, int(frame_height * vehicle_offset))

                        top_left_2 = (0, int(frame_height * vehicle_offset))
                        bottom_right_2 = (x_offset, frame_height)

                        top_left_3 = (frame_width - x_offset, int(frame_height * vehicle_offset))
                        bottom_right_3 = (frame_width, frame_height)

                        top_left_4 = (x_offset, int(frame_height * vehicle_offset))
                        bottom_right_4 = (frame_width - x_offset, int(frame_height * motorbike_offset))
                        
                        top_left_5 = (x_offset, frame_height - y_offset)
                        bottom_right_5 = (frame_width - x_offset, frame_height)

                        cv2.rectangle(overlay, top_left_1, bottom_right_1, (220, 0, 60), -1)
                        cv2.rectangle(overlay, top_left_2, bottom_right_2, (220, 0, 60), -1)
                        cv2.rectangle(overlay, top_left_3, bottom_right_3, (220, 0, 60), -1)
                        cv2.rectangle(overlay, top_left_5, bottom_right_5, (220, 0, 60), -1)
                        cv2.addWeighted(overlay, alpha, annotated_frame, 1 - alpha, 0, annotated_frame)

                    for result in results:
                        for boxes in result.boxes:
                            with threading.Lock():
                                if not boxes.id:
                                    continue

                                id = int(boxes.id.item())
                                vehicle_id = int(boxes.cls.item())

                                if id in DashboardPage.StartCamera.detected_ids:
                                    continue

                                DashboardPage.StartCamera.detected_ids.add(id)
                                
                                x1, y1, x2, y2 = boxes.xyxy[0]
                                vehicle_x1, vehicle_y1, vehicle_x2, vehicle_y2 = int(x1.item()), int(y1.item()), int(x2.item()), int(y2.item())

                                mul = motorbike_offset if vehicle_id == 3 else vehicle_offset
                                frame_height_min = frame_height * mul

                                # check if vehicle is beyond the detection boundary
                                if vehicle_y2 < frame_height_min:
                                    continue

                                cropped_vehicle = frame[vehicle_y1:vehicle_y2, vehicle_x1:vehicle_x2]

                                if currSetting or (dynamicSetting and isHeavyTraffic):
                                    lp_result = AIController.detect_license_plate(frame=cropped_vehicle)

                                    if not lp_result[0].boxes:
                                        DashboardPage.StartCamera.detected_ids.remove(id)
                                        continue

                                    x1, y1, x2, y2 = lp_result[0].boxes[0].xyxy[0]
                                    lp_x1, lp_y1, lp_x2, lp_y2 = int(x1.item()) + vehicle_x1, int(y1.item()) + vehicle_y1, int(x2.item()) + vehicle_x1, int(y2.item()) + vehicle_y1
                                    
                                    # check if the actual localized lp is within the lower half of the video
                                    # if not, redo prediction
                                    if lp_y1 < frame_height_min:
                                        continue
                                    if frame_height - y_offset < lp_y2 or lp_x1 < x_offset or frame_width - x_offset < lp_x2:
                                        DashboardPage.StartCamera.detected_ids.remove(id)
                                        continue

                                    cropped_lp = frame[lp_y1:lp_y2, lp_x1:lp_x2]

                                    if cont.dipModule == 2:
                                        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                        client_socket.connect(('127.0.0.1', 8001))
                                    elif cont.dipModule == 1:
                                        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                        client_socket.connect(('127.0.0.1', 8000))
                                    if cont.dipModule != 0:
                                        SocketController.sendImage(client_socket, cropped_lp)
                                        processed_lp = SocketController.receiveImage(client_socket)
                                        client_socket.close()

                                        if processed_lp is None:
                                            DashboardPage.StartCamera.detected_ids.remove(id)
                                            continue
                                        
                                    tk_async.async_execute(self.extract(
                                        (processed_lp if cont.dipModule != 0 else cropped_lp),
                                        id,
                                        cameraId,
                                        vehicle_id,
                                        currSetting,
                                        dynamicSetting,
                                        isHeavyTraffic,
                                        cropped_vehicle,
                                        databaseTable,
                                        vehiclesDetectedCount,
                                    ), wait=False, visible=False)

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
        origin_coords = result.originCoords
        dest_coords = result.destCoords
        cameraUrl = f'rtsp://{ip_addr}:554'

        if cameraName == 'test_cam1':
            cameraUrl = 'https://noodelzcsgoaibucket.s3.ap-southeast-1.amazonaws.com/videos/videos/new/test_cam4.mp4'
        elif cameraName == 'test_cam2':
            cameraUrl = 'https://noodelzcsgoaibucket.s3.ap-southeast-1.amazonaws.com/videos/videos/cut+videos/location+2/test_cam8.mp4'
        elif cameraName == 'test_cam3':
            cameraUrl = 'https://noodelzcsgoaibucket.s3.ap-southeast-1.amazonaws.com/videos/videos/cut+videos/location+1/test_cam10.mp4'

        if self.timer is not None:
            self.master.after_cancel(self.timer)
            self.timer = None
            self.master.after(5000, self.trafficPoll, result.location, origin_coords, dest_coords)
        else:
            self.trafficPoll(result.location, origin_coords, dest_coords)

        self.cap = cv2.VideoCapture(cameraUrl)
        DashboardPage.StartCamera(self.currUser).start(self.cap, self.placeholder_label, ip_addr, self.databaseTable, self.vehiclesDetectedCount)
        
        self.uptime_seconds = 0
        self.counting_enabled = True

    def setCurrUser(self, user):
        self.currUser = user
        self.adminButton.configure(state='disabled' if not user.isAdmin else 'normal')

    def trafficPoll(self, location, origin_coords, dest_coords):
        data = GoogleController.getDistanceMatrix(origin_coords, dest_coords)
        duration = data['rows'][0]['elements'][0]['duration']['value']
        duration_in_traffic = data['rows'][0]['elements'][0]['duration_in_traffic']['value']
        traffic_ratio = 1 - min(1, duration / duration_in_traffic)
        PollController.isHeavyTraffic = traffic_ratio >= 0.5
        response = DBController.addCongestion(location, traffic_ratio)
        if not response.ok:
            with open(os.path.join(parent_dir, 'logs.txt'), 'a') as file:
                now = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                file.write(f'[{now}] Error at function invocation views/dashboardPageView.py trafficPoll() - {repr(response.messages["error"])}\n')
        self.congestionBar.updateBar(traffic_ratio)
        self.update()
        self.timer = self.after(30000, self.trafficPoll, location, origin_coords, dest_coords)
    
    def dipModuleRadio_callback(self):
        cont.dipModule = self.dipModuleVar.get()

    def __init__(self, parent):
        self.timer = None
        self.cap = None
        self.currUser = None

        self.uptime_seconds = 0
        self.counting_enabled = False
        self.vehicle_count = 0

        self.maxCongestionBarWidth = 300

        tk.Frame.__init__(self, parent, bg = "#090E18")
        
        # Style definition. Can be utilized with the Change Theme from Light to Dark
        style = ttk.Style()
        style.theme_use('forest-dark')
        
        # Close Icon (Currently Set to darkmode, if possible change to lightmode when the the changes)
        closePhoto = CTkImage(light_image = Image.open(os.path.join(parent_dir, "views/icons/icon_close_darkmode.png")),
                              dark_image = Image.open(os.path.join(parent_dir, "views/icons/icon_close_darkmode.png")),
                              size = (20, 20))

        # Minimize Icon (Currently Set to darkmode, if possible change to lightmode when the the changes)
        minimizePhoto = CTkImage(light_image = Image.open(os.path.join(parent_dir, "views/icons/icon_minimize_darkmode.png")),
                              dark_image = Image.open(os.path.join(parent_dir, "views/icons/icon_minimize_darkmode.png")),
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
                                    text = 'Reports',
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
        self.databaseTable = ttk.Treeview(databaseTableFrame, columns = ('id', 'licensePlate', 'vehicleType', 'cameraID', 'time', 'date', 'price'), show = "headings", style = 'Custom.Treeview')

        # Inserts Blank Entries to the Treeview so that it doesnt look bad when the Treeview is Empty.
        #for _ in range(100):
            #databaseTable.insert('', 'end', values=('', '', '', '', '', ''))

        self.databaseTable.tag_configure('even', background='#2A2D2E', foreground='#FFFFFF')
        self.databaseTable.tag_configure('odd', background='#343638', foreground='#FFFFFF')
        
        self.databaseTable.heading('id', text="ID", anchor='center')
        self.databaseTable.heading('licensePlate', text="License Plate", anchor='center')
        self.databaseTable.heading('vehicleType', text="Vehicle Type", anchor='center')
        self.databaseTable.heading('cameraID', text="Camera ID", anchor='center')
        self.databaseTable.heading('time', text="Time", anchor='center')
        self.databaseTable.heading('date', text="Date", anchor='center')
        self.databaseTable.heading('price', text="Charge", anchor='center')

        self.databaseTable.column('id', width=60, anchor='center')
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
        middleLeftMainFrameInner = tk.Frame(middleLeftMainFrame, bg = '#090E18')
        middleLeftMainFrameInnerUpper = tk.Frame(middleLeftMainFrameInner, bg = '#090E18')
        middleLeftMainFrameInnerLower = tk.Frame(middleLeftMainFrameInner, bg = '#090E18')
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
        # Used for Testing without connection to DB
        # self.changeCameraDisplay = CTkComboBox(dropdownFrame, values=['(NONE)'], command=self.changeCameraDisplay_callback, width=100, state='readonly')
        self.changeCameraDisplay.set('(NONE)')
        self.changeCameraDisplay.pack(side = "right")
        
        changeCameraLabel = CTkLabel(dropdownFrame, text = "Change Camera", font = ('Montserrat', 13), text_color = "#FFFFFF")
        changeCameraLabel.pack(side = "right", padx = 10)
        
        congestionBarFrame = tk.Frame(middleLeftMainFrame, bg = '#090E18')
        congestionBarFrame.pack(fill = 'both', side = 'top', padx = 20)

        # Creating canvas to hold the progress bar
        self.congestionBarCanvas = tk.Canvas(congestionBarFrame, width=self.maxCongestionBarWidth, height=5, bg="#090E18", highlightthickness=0)
        self.congestionBarCanvas.pack(side = 'top')

        # Creating and packing the progress bar
        self.congestionBar = CongestionStateBar(self.congestionBarCanvas, width=self.maxCongestionBarWidth, height=10)
        self.congestionBar.pack()

        congestionBarLabel = CTkLabel(congestionBarFrame, text = "Congestion State", font = ('Montserrat', 13), text_color = "#FFFFFF")
        congestionBarLabel.pack(side = "top", fill = 'both', expand = True)

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
        
        self.dipModuleVar = IntVar(value = 0)

        dipModuleLabel = CTkLabel(middleLeftMainFrameInnerUpper, text = 'Select filter', font = ('Montserrat', 12))
        noneRadioButton = CTkRadioButton(master=middleLeftMainFrameInnerLower, text="Remove filter",
                                            value=0, variable = self.dipModuleVar, command = self.dipModuleRadio_callback)
        lowLightRadioButton = CTkRadioButton(master=middleLeftMainFrameInnerLower, text="Lowlight filter",
                                            value=1, variable = self.dipModuleVar, command = self.dipModuleRadio_callback)
        foggyRadioButton = CTkRadioButton(master=middleLeftMainFrameInnerLower, text="Foggy filter",
                                            value=2, variable = self.dipModuleVar, command = self.dipModuleRadio_callback)

        
        settingsButton.pack(side = 'left', padx = 5, pady = 20)
        middleLeftMainFrameInner.pack(side = tk.RIGHT, padx = 5, pady = 5)
        middleLeftMainFrameInnerUpper.pack(side = tk.TOP)
        middleLeftMainFrameInnerLower.pack(side = tk.TOP)
        dipModuleLabel.pack(expand = True, fill = 'x', padx = 5, pady = 0)
        noneRadioButton.pack(padx=20, pady=5, side=tk.LEFT)
        lowLightRadioButton.pack(padx=20, pady=5, side=tk.LEFT)
        foggyRadioButton.pack(padx=20, pady=5, side=tk.LEFT)
        
        settingsButton.bind("<Enter>", lambda event: settingsButton.configure(text_color="#090E18", fg_color = "#48BFE3")) 
        settingsButton.bind("<Leave>", lambda event: settingsButton.configure(text_color="#48BFE3", fg_color = "#090E18")) 

        self.update_uptime()