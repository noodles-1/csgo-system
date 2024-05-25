import os
import sys
import tkinter as tk
import matplotlib

matplotlib.use("TkAgg")

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import views.switchView as switch

from customtkinter import *
from tkinter import ttk
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

'''
Still missing the download to CSV button.
'''
class AnalyticsPage(tk.Frame):
    # Close Application
    def closeApplication(self):
        self.master.destroy()

    # Minimize or Iconify the Application
    def minimizeApplicaiton(self):
        self.master.iconify()
        
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg = "#090E18")
        
        # Style definition. Can be utilized with the Change Theme from Light to Dark
        style = ttk.Style()
        style.theme_use('forest-dark')
        
        # Close Icon (Currently Set to darkmode, if possible change to lightmode when the the changes)
        closePhoto = CTkImage(light_image = Image.open("views/icons/icon_close_lightmode.png"),
                              dark_image = Image.open("views/icons/icon_close_darkmode.png"),
                              size = (20, 20))

        # Minimize Icon (Currently Set to darkmode, if possible change to lightmode when the the changes)
        minimizePhoto = CTkImage(light_image = Image.open("views/icons/icon_minimize_lightmode.png"),
                              dark_image = Image.open("views/icons/icon_minimize_darkmode.png"),
                              size = (20, 20))
        
        # Top-most Frame that holds the Close and Minimize buttons.
        toolbarFrame = tk.Frame(self, bg = "#090E18")
        # Content Frame (Where the contents of the fpage is. "Main Frame")
        contentFrame = CTkScrollableFrame(self, bg_color = "#090E18", fg_color = "#090E18")
        
        toolbarFrame.pack(fill = "x", side = "top")
        contentFrame.pack(fill = "both", side = "top", expand = True)
        
        navigationFrame = tk.Frame(self, bg = "#090E18")
        navigationFrame.pack(fill = "x", side = "top", padx = 20, pady = 2, expand = False)
        
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
        
        # Separates the contentFrame into two rows. First Row Content Frame & Second Row Content Frame
        firstRowContentFrame = CTkFrame(contentFrame, bg_color = "#090E18", fg_color = "#090E18")
        firstRowContentFrame.pack(expand = True, fill = "both", side = "top")
        secondRowContentFrame = CTkFrame(contentFrame, bg_color = "#090E18", fg_color = "#090E18")
        secondRowContentFrame.pack(expand = True, fill = "both", side = "top")
        
        # The graphs' Frame. 1 Frame at the First Row, 3 Frames at the Second Row
        numberOfDetectedVehicleFrame = CTkFrame(firstRowContentFrame, bg_color = "#090E18", fg_color = "#1B2431", corner_radius = 30)
        revenueGeneratedFrame = CTkFrame(secondRowContentFrame, bg_color = "#090E18", fg_color = "#1B2431", corner_radius = 30)
        systemPerformanceFrame = CTkFrame(secondRowContentFrame, bg_color = "#090E18", fg_color = "#1B2431", corner_radius = 30)
        busiestTimeFrame = CTkFrame(secondRowContentFrame, bg_color = "#090E18", fg_color = "#1B2431", corner_radius = 30)
        
        numberOfDetectedVehicleFrame.pack(expand = True, fill = "both", padx = 5, pady = 5, side = "top")
        revenueGeneratedFrame.pack(fill = "both", padx = 5, pady = 5, side = "left", expand = True)
        systemPerformanceFrame.pack(fill = "both", padx = 5, pady = 5, side = "left")
        busiestTimeFrame.pack(fill = "both", padx = 5, pady = 5, side = "left", expand = True)
        
        # Number of Detected Vehicles Graph
        numberOfDetectedVehicleInnerFrame = CTkFrame(numberOfDetectedVehicleFrame, bg_color = "#1B2431", fg_color = "#1B2431")
        numberOfDetectedVehicleInnerFrame.pack(padx = 50, pady = 30, side ="top", expand = True, fill = "both")
        
        #Insert Graph Here
        detectedVehiclesFigure = Figure()
        ax = detectedVehiclesFigure.add_subplot()
        ax.set_title("Number of Detected Vehicles")
        
        detectedVehiclesCanvas = FigureCanvasTkAgg(detectedVehiclesFigure, numberOfDetectedVehicleInnerFrame)
        detectedVehiclesCanvas.draw()
        detectedVehiclesCanvas.get_tk_widget().pack(side = "top", expand = True, fill = "both")
        # End ofNumber of Detected Vehicles Graph
        
        # Number of Revenue Generated Graph
        revenueGeneratedInnerFrame = CTkFrame(revenueGeneratedFrame, bg_color = "#1B2431", fg_color = "#1B2431")
        revenueGeneratedInnerFrame.pack(padx = 50, pady = 30, side ="top", expand = True, fill = "both")
        
        #Insert Graph Here
        revenueGeneratedFigure = Figure(figsize = (3,3))
        ax = revenueGeneratedFigure.add_subplot()
        ax.set_title("Revenue Generated")
        
        revenueGeneratedCanvas = FigureCanvasTkAgg(revenueGeneratedFigure, revenueGeneratedInnerFrame)
        revenueGeneratedCanvas.draw()
        revenueGeneratedCanvas.get_tk_widget().pack(side = "top", expand= True, fill = "both")
        # End of Number of Revenue Generated Graph
        
        # System Performance details
        titleLabelFrame = CTkFrame(systemPerformanceFrame, bg_color = "#1B2431", fg_color = "#1B2431")
        cpuUsageLabelFrame = CTkFrame(systemPerformanceFrame, bg_color = "#1B2431", fg_color = "#1B2431")
        memoryUsageLabelFrame = CTkFrame(systemPerformanceFrame, bg_color = "#1B2431", fg_color = "#1B2431")
        
        titleLabel = CTkLabel(titleLabelFrame, text = "System Perforamnce", font = ('Montserrat', 12), anchor = "w")
        
        cpuUsageLabel = CTkLabel(cpuUsageLabelFrame, text = "CPU Usage", font = ('Montserrat', 12), anchor = "w")
        cpuUsagePercentLabel = CTkLabel(cpuUsageLabelFrame, text = "40%", font = ('Montserrat', 12), anchor = "e")
        
        memoryUsageLabel = CTkLabel(memoryUsageLabelFrame, text = "Memory Usage", font = ('Montserrat', 12), anchor = "w")
        memoryUsagePercentLabel = CTkLabel(memoryUsageLabelFrame, text = "50%", font = ('Montserrat', 12), anchor = "e")
        
        titleLabelFrame.pack(side = "top", pady = (20, 30), padx = (20, 150), fill = "x")
        cpuUsageLabelFrame.pack(side = "top", padx = (20, 20), fill = "x")
        memoryUsageLabelFrame.pack(side = "top", padx = (20, 20), fill = "x")
        
        titleLabel.pack(side = "left", expand = True, fill = "x")
        
        cpuUsageLabel.pack(side = "left", expand = True, fill = "x")
        cpuUsagePercentLabel.pack(side = "left", expand = True, fill = "x")
        
        memoryUsageLabel.pack(side = "left", expand = True, fill = "x")
        memoryUsagePercentLabel.pack(side = "left", expand = True, fill = "x")
        # End of System Performance details
        
        # Busiest Time Graph
        busiestTimeInnerFrame = CTkFrame(busiestTimeFrame, bg_color = "#1B2431", fg_color = "#1B2431")
        busiestTimeInnerFrame.pack(padx = 50, pady = 30, side ="top", expand = True, fill = "both")
        
        #Insert Graph Here
        busiestTimeFigure = Figure(figsize = (3, 3))
        ax = busiestTimeFigure.add_subplot()
        ax.set_title("Revenue Generated")
        
        busiestTimeCanvas = FigureCanvasTkAgg(busiestTimeFigure, busiestTimeInnerFrame)
        busiestTimeCanvas.draw()
        busiestTimeCanvas.get_tk_widget().pack(side = "top", expand = True, fill = "both")
        # End of Busiest Time Graph
        
        # Dashboard Button - Navigates to Dashboard
        dashboardButton = CTkButton(navigationFrame,
                                text = 'Dashboard',
                                command = lambda: switch.showDashboardPage(parent), 
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
        dashboardButton.pack(side = 'right', padx = 5, pady = 1)