import math
import os
import sys
import cv2
import tkinter as tk

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from tkinter import font
from CTkTable import *
from customtkinter import *
from PIL import Image, ImageTk
from controllers import controller

tableDefaultValues = [["License Plate", "Vehicle Type", "Camera ID", "Time", "Date", "Price"]]
quitButtonImage = Image.open("views/icons/icon_close_darkmode.png")

"""Montserrat is already installed on my computer.
But I downloaded a ttf file so that it can use Montserrat font without having the font to be installed on the computer.
Though I havent specified the code to use the ttf file yet instead. so if you dont have the montserrat. you can just install the font with the ttf file
I will update the code to be able to use the font without installation needed 2morrow
"""

"""
You also might encounter an error with webcam. If you dont have a webcam plugged or webcam enabled.
enable it. I used webcam so I can test if its possible to send frames to the front-end with the framework.
you can easily replace the source from webcam to the output of the object detection frames.

note that the width and height of the frames are automatically set depending on the aspect ratio of the monitor.
so use the variables self.newWidth, self.newHeight when setting the image size.
"""

class mainWindow(CTk):
    def __init__(self):
        super().__init__()
        self.title("Automated Congestion Pricing by CSGO")
        self.attributes("-fullscreen", True)
        set_appearance_mode("dark")
        self._current_theme = "dark"
        self.ai = controller.AIModel()

        #calculation to retain the webcam feed size in any window size
        windowWidth = self.winfo_screenwidth()
        windowHeight = self.winfo_screenheight()

        imageWidth = 1160
        imageHeight = 800

        windowAspectRatio = windowWidth / windowHeight
        imageAspectRatio = imageWidth / imageHeight

        if windowAspectRatio >= imageAspectRatio:
            self.newWidth = min(windowWidth, imageWidth)
            self.newHeight = int(self.newWidth / imageAspectRatio)
        else:
            self.newHeight = min(windowHeight, imageHeight)
            self.newWidth = int (self.newHeight * imageAspectRatio)

        #frame declaration
        toolBarFrame = CTkFrame(master = self, fg_color= "#252422")
        mainWindowFrame = CTkFrame(master = self, fg_color= "#252422")
        leftMainWindowFrame = CTkFrame(master = mainWindowFrame, fg_color= "#252422")
        rightMainWindowFrame = CTkScrollableFrame(master = mainWindowFrame, fg_color= "#252422")
        leftTopMainWindowFrame = CTkFrame(master = leftMainWindowFrame, fg_color= "#252422")
        leftMiddleMainWindowFrame = CTkFrame(master = leftMainWindowFrame, fg_color= "#252422")
        leftleftMiddleMainWindowFrame = CTkFrame(master=leftMiddleMainWindowFrame, fg_color= "#252422")
        rightleftMiddleMainWindowFrame = CTkFrame(master=leftMiddleMainWindowFrame, fg_color= "#252422")
        leftBottomMainWindowFrame = CTkFrame(master = leftMainWindowFrame, fg_color= "#252422")

        #widget declaration
        exitButton = CTkButton(master = toolBarFrame,
                               image = CTkImage(quitButtonImage),
                               text = "",
                               command = self.quit,
                               fg_color="transparent",
                               width=25,
                               height=25)

        cameraIdLabel = CTkLabel(master = leftleftMiddleMainWindowFrame,
                                 text = "Camera ID:",
                                 padx = 5,
                                 font = ("Montserrat", 14))

        upTimeLabel = CTkLabel(master = leftleftMiddleMainWindowFrame,
                               text = "Up Time:",
                               padx = 5,
                               font = ("Montserrat", 14))

        # the value of this can be changed during runtime with .configure
        cameraIdValueLabel = CTkLabel(master = rightleftMiddleMainWindowFrame,
                                      text = "123123",
                                      padx = 10,
                                      font = ("Montserrat", 14))

        #the value of this can be changed during runtime with .configure
        upTimeValueLabel = CTkLabel(master = rightleftMiddleMainWindowFrame,
                                    text = "123123",
                                    padx = 10,
                                    font = ("Montserrat", 14))

        logsButton = CTkButton(master = leftBottomMainWindowFrame,
                               text = "Logs",
                               width = 170,
                               height = 50,
                               corner_radius= 25,
                               fg_color = "#FFFFFF",
                               text_color = "black",
                               font = ("Montserrat", 14),
                               hover_color = "#e0e1dd")

        configButton = CTkButton(master = leftBottomMainWindowFrame,
                                 text = "Configuration",
                                 width=170,
                                 height=50,
                                 corner_radius=25,
                                 fg_color = "#FFFFFF",
                                 text_color = "black",
                                 font = ("Montserrat", 14),
                                 hover_color = "#e0e1dd")

        dashboardButton = CTkButton(master = leftBottomMainWindowFrame,
                                    text = "Dashboard",
                                    width = 170,
                                    height = 50,
                                    corner_radius = 25,
                                    fg_color = "#FFFFFF",
                                    text_color = "black",
                                    font = ("Montserrat", 14),
                                    hover_color = "#e0e1dd")

        #I found that CTkTable is a bit hard to work with especially with designing. Subejct to change.
        licensePlateTable = CTkTable(
            master = rightMainWindowFrame,
            row = 50,
            column = 6,
            values = tableDefaultValues,
            font = ("Montserrat", 11))

        self.webcamFeed = tk.Label(master = leftTopMainWindowFrame,
                                   fg = "#252422",
                                   bg = "#252422")

        #layout toolbar
        exitButton.pack(side="right", anchor = "ne", padx = 10, pady = (1, 3))
        toolBarFrame.pack(side = "top", fill = "x")

        #layout main window
        mainWindowFrame.pack(side = "top", expand  = True, fill = "both")

        #layout left main window
        self.webcamFeed.pack(expand = True, fill = "both")
        cameraIdLabel.pack(anchor = "e", side = "top", padx = (30, 5))
        upTimeLabel.pack(anchor = "e", side = "top", padx = (30, 5))
        cameraIdValueLabel.pack(anchor="w", side="top")
        upTimeValueLabel.pack(anchor="w", side="top")
        logsButton.pack(side = "right", padx = (15, 50), anchor = "s", pady = (70, 70))
        configButton.pack(side = "right", padx = 15, anchor = "s", pady = (70, 70))
        dashboardButton.pack(side = "right", padx = 15, anchor = "s", pady = (70, 70))
        leftMainWindowFrame.pack(side = "left", expand = True, fill = "both")
        leftTopMainWindowFrame.pack(side="top", fill = "both", expand = True)
        leftMiddleMainWindowFrame.pack(side="top", fill = "both")
        leftBottomMainWindowFrame.pack(side="top", fill = "both")
        rightleftMiddleMainWindowFrame.pack(side = "right", expand = True, fill = "both")
        leftleftMiddleMainWindowFrame.pack(side = "right", fill = "both")

        #layout right main window
        licensePlateTable.pack(side = "top", fill = "both")
        rightMainWindowFrame.pack(side = "left", fill = "both", expand = True)
        self.start_video()

    def start_webcam(self):
        cap = cv2.VideoCapture(0)

        def show_frame():
            ret, frame = cap.read()

            if ret:
                results = self.ai.detect_vehicle(frame)
                for result in results:
                    for box in result.boxes:
                        controller.bounding_box(frame, box)
                        
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                img = img.resize((self.newWidth, self.newHeight))
                img_tk = ImageTk.PhotoImage(image=img)

                self.webcamFeed.img = img_tk
                self.webcamFeed.config(image=img_tk)

                self.webcamFeed.after(20, show_frame)
            else:
                cap.release()

        show_frame()

    def start_video(self):
        video_path = "https://noodelzcsgoaibucket.s3.ap-southeast-1.amazonaws.com/videos/highway_videoplayback.mp4"
        cap = cv2.VideoCapture(video_path)
        def show_frame():
            ret, frame = cap.read()

            if ret:
                results = self.ai.detect_vehicle(frame)
                for result in results:
                    for box in result.boxes:
                        controller.bounding_box(frame, box)

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                img = img.resize((self.newWidth, self.newHeight))
                img_tk = ImageTk.PhotoImage(image=img)

                self.webcamFeed.img = img_tk
                self.webcamFeed.config(image=img_tk)

                self.webcamFeed.after(20, show_frame)
            else:
                cap.release()

        show_frame()

if __name__ == "__main__":
    app = mainWindow()
    app.mainloop()