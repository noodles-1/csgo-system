import os
import sys
import tkinter as tk
from customtkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

class AnalyticsPage(tk.Frame):
    def closeApplication(self):
        self.master.destroy()

    def minimizeApplicaiton(self):
        self.master.iconify()
        
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg = "pink")
        # button = tk.Button(self, text = "Dashboard" , command = lambda: parent.show_frame(parent.dashboardFrame))
        # button.pack()
        
        # Style definition. Can be utilized with the Change Theme from Light to Dark
        style = ttk.Style()
        style.theme_use('forest-dark')
        
        closeImage = Image.open("views/icons/icon_close_darkmode.png")
        closeImage = closeImage.resize((20, 20))
        closePhoto = ImageTk.PhotoImage(closeImage)

        minimizeImage = Image.open("views/icons/icon_minimize_darkmode.png")
        minimizeImage = minimizeImage.resize((20, 20))
        minimizePhoto = ImageTk.PhotoImage(minimizeImage)
        
        toolbarFrame = CTkFrame(self, bg_color = "#090E18", fg_color = "#090E18")
        contentFrame = CTkFrame(self, fg_color = "#090E18", bg_color = "#090E18")
        navigationFrame = CTkFrame(self, bg_color = "#090E18", fg_color = "#090E18")
        
        toolbarFrame.pack(fill = "x", side = "top")
        contentFrame.pack(expand = True, fill = "both", side = "top")
        navigationFrame.pack(fill = "x", side = "top")
        
        # Close Button
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

        # Minimize Button
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
        
        # Dashboard Button - Navigates to Dashboard
        dashboardButton = CTkButton(navigationFrame,
                                text = 'Dashboard',
                                command = lambda: parent.show_frame(parent.dashboardFrame), 
                                font = ('Montserrat', 15),
                                border_width = 2,
                                corner_radius = 15,
                                border_color = '#5E60CE',
                                text_color = '#5E60CE',
                                fg_color = '#090E18',
                                height = 30,
                                width = 140)
        dashboardButton.bind("<Enter>", lambda event: dashboardButton.configure(text_color="#090E18", fg_color = "#5E60CE")) 
        dashboardButton.bind("<Leave>", lambda event: dashboardButton.configure(text_color="#5E60CE", fg_color = "#090E18")) 
        dashboardButton.pack(side = 'right', padx = 10, pady = 10)
        
        firstRowContentFrame = CTkFrame(contentFrame, bg_color = "#090E18", fg_color = "#090E18")
        firstRowContentFrame.pack(expand = True, fill = "both", side = "top")
        secondRowContentFrame = CTkFrame(contentFrame, bg_color = "#090E18", fg_color = "#090E18")
        secondRowContentFrame.pack(expand = True, fill = "both", side = "top")
        
        numberOfDetectedVehicleFrame = CTkFrame(firstRowContentFrame, bg_color = "#090E18", fg_color = "#1B2431", corner_radius = 30)
        revenueGeneratedFrame = CTkFrame(secondRowContentFrame, bg_color = "#090E18", fg_color = "#1B2431", corner_radius = 30)
        systemPerformanceFrame = CTkFrame(secondRowContentFrame, bg_color = "#090E18", fg_color = "#1B2431", corner_radius = 30)
        busiestTimeFrame = CTkFrame(secondRowContentFrame, bg_color = "#090E18", fg_color = "#1B2431", corner_radius = 30)
        
        numberOfDetectedVehicleFrame.pack(expand = True, fill = "both", padx = 20, pady = 20, side = "top")
        revenueGeneratedFrame.pack(fill = "both", padx = 20, pady = 20, side = "left")
        systemPerformanceFrame.pack(fill = "both", padx = 20, pady = 20, side = "left")
        busiestTimeFrame.pack(fill = "both", padx = 20, pady = 20, side = "left")