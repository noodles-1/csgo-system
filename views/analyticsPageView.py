import os
import sys
import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import asyncio
import tk_async_execute as tk_async
import random
import pandas as pd

matplotlib.use("TkAgg")

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import views.switchView as switch

from datetime import datetime, timedelta
from customtkinter import *
from tkinter import ttk
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from controllers.controller import ReportGenerationController as rgctrl
from controllers.dbController import DBController
from controllers.pollController import PollController

class AnalyticsPage(tk.Frame):
    # Close Application
    def closeApplication(self):
        self.master.destroy()

    # Minimize or Iconify the Application
    def minimizeApplicaiton(self):
        self.master.iconify()
    
    def downloadCSV(self):
        rgctrl.downloadAndProcessCSV()

    def processDataDetected(self, df, hours):
        df['datetime'] = pd.to_datetime(df['date'].astype(str) + ' ' + df['time'].astype(str))

        df.set_index('datetime', inplace=True)
        df = df.resample('h').size()

        start_time = (datetime.now() - timedelta(hours=hours)).replace(minute=0, second=0, microsecond=0)
        end_time = datetime.now().replace(minute=0, second=0, microsecond=0)
        hourly_range = pd.date_range(start=start_time, end=end_time, freq='h')

        df_resampled = df.reindex(hourly_range, fill_value=0)
        return df_resampled
    
    def processDataRevenue(self, df, hours):
        df['datetime'] = pd.to_datetime(df['date'].astype(str) + ' ' + df['time'].astype(str))

        df.set_index('datetime', inplace=True)
        df_resampled = df.resample('min')['price'].sum()

        start_time = (datetime.now() - timedelta(hours=hours)).replace(second=0, microsecond=0)
        end_time = datetime.now().replace(second=0, microsecond=0)
        minute_range = pd.date_range(start=start_time, end=end_time, freq='min')

        df_resampled = df_resampled.reindex(minute_range, fill_value=0)
        return df_resampled

    def processDataBusiest(self, df, hours):
        df['datetime'] = pd.to_datetime(df['date'].astype(str) + ' ' + df['time'].astype(str))

        df.set_index('datetime', inplace=True)
        df = df.resample('min').size()

        start_time = (datetime.now() - timedelta(hours=hours)).replace(second=0, microsecond=0)
        end_time = datetime.now().replace(second=0, microsecond=0)
        minute_range = pd.date_range(start=start_time, end=end_time, freq='min')

        df_resampled = df.reindex(minute_range, fill_value=0)
        return df_resampled

    def detectedVehiclesPoll(self, location):
        if PollController.analyticsShown:
            self.axDetected.clear()

            self.axDetected.plot([], [], marker='o')
            self.axDetected.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            self.axDetected.xaxis.set_major_locator(mdates.HourLocator())
            self.axDetected.set_xlabel('Time')
            self.axDetected.set_ylabel('Number of Detected Vehicles')
            self.axDetected.set_title('Number of Detected Vehicles Within 24 Hours From Now')
            self.axDetected.tick_params(axis='x', rotation=45)
            self.figDetected.tight_layout()

            results = DBController.getLicenseData(location=location)
            data = []
            for result in results.data:
                row = result[0]
                data.append({
                    'vehicle': row.vehicleType,
                    'date': row.date,
                    'time': row.time
                })

            df = pd.DataFrame(data)
            counts = self.processDataDetected(df, 24)
            
            self.axDetected.plot(counts.index, counts.values, color='blue')
            self.axDetected.relim()
            self.axDetected.autoscale_view()
            self.figDetected.canvas.draw()
            self.figDetected.canvas.flush_events()
        self.detectedVehiclesTimer = self.master.after(30000, self.detectedVehiclesPoll, location)

    def revenuePoll(self, location):
        if PollController.analyticsShown:
            self.axRevenue.clear()

            self.axRevenue.plot([], [], marker='o')
            self.axRevenue.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            self.axRevenue.xaxis.set_major_locator(mdates.MinuteLocator(interval=10))
            self.axRevenue.set_xlabel('Time')
            self.axRevenue.set_ylabel('Revenue Generated (Php)')
            self.axRevenue.set_title('Revenue Generated Over Time')
            self.axRevenue.tick_params(axis='x', rotation=45)
            self.figRevenue.tight_layout()

            results = DBController.getLicenseData(location=location)
            data = []
            for result in results.data:
                row = result[0]
                data.append({
                    'price': row.price,
                    'date': row.date,
                    'time': row.time
                })

            df = pd.DataFrame(data)
            counts = self.processDataRevenue(df, 2)
            
            self.axRevenue.plot(counts.index, counts.values, color='blue')
            self.axRevenue.relim()
            self.axRevenue.autoscale_view()
            self.figRevenue.canvas.draw()
            self.figRevenue.canvas.flush_events()
        self.revenueTimer = self.master.after(30000, self.revenuePoll, location)

    def busiestPoll(self, location):
        if PollController.analyticsShown:
            self.axBusiest.clear()

            self.axBusiest.plot([], [], marker='o')
            self.axBusiest.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            self.axBusiest.xaxis.set_major_locator(mdates.MinuteLocator(interval=10))
            self.axBusiest.set_xlabel('Time')
            self.axBusiest.set_ylabel('Volume of Vehicles')
            self.axBusiest.set_title('Busiest Time')
            self.axBusiest.tick_params(axis='x', rotation=45)
            self.figBusiest.tight_layout()

            results = DBController.getLicenseData(location=location)
            data = []
            for result in results.data:
                row = result[0]
                data.append({
                    'vehicle': row.vehicleType,
                    'date': row.date,
                    'time': row.time
                })

            df = pd.DataFrame(data)
            counts = self.processDataDetected(df, 2)
            
            self.axBusiest.plot(counts.index, counts.values, color='blue')
            self.axBusiest.relim()
            self.axBusiest.autoscale_view()
            self.figBusiest.canvas.draw()
            self.figBusiest.canvas.flush_events()
        self.busiestTimer = self.master.after(30000, self.busiestPoll, location)
    
    def detectedVehiclesLocation_callback(self, location: str):
        if self.detectedVehiclesTimer is not None:
            self.master.after_cancel(self.detectedVehiclesTimer)
            self.detectedVehiclesTimer = None
            self.master.after(2000, self.detectedVehiclesPoll, location)
        else:
            self.detectedVehiclesPoll(location)
    
    def revenueGeneratedLocation_callback(self, location):
        if self.revenueTimer is not None:
            self.master.after_cancel(self.revenueTimer)
            self.revenueTimer = None
            self.master.after(2000, self.revenuePoll, location)
        else:
            self.revenuePoll(location)
    
    def busiestTimeLocation_callback(self, location):
        if self.busiestTimer is not None:
            self.master.after_cancel(self.busiestTimer)
            self.busiestTimer = None
            self.master.after(2000, self.busiestTimer, location)
        else:
            self.busiestPoll(location)

    def applyRestrictions(self, user):
        self.downloadCSVButton.configure(state='disabled' if not user.canDownload else 'normal')
        self.updatePercentages()
    
    def __init__(self, parent):
        self.detectedVehiclesTimer = None
        self.revenueTimer = None
        self.busiestTimer = None

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
        numberOfDetectedVehicleInnerFrame.pack(padx = 50, pady = 10, side ="top", expand = True, fill = "both")
        
        response = DBController.getLocations()
        locations = [result[0] for result in response.data]

        #Insert Graph Here
        self.figDetected = plt.Figure()
        self.axDetected = self.figDetected.add_subplot()
        self.axDetected.set_xlabel('Time')
        self.axDetected.set_ylabel('Number of Detected Vehicles')
        self.axDetected.set_title('Number of Detected Vehicles Within 24 Hours From Now')

        self.axDetected.relim()
        self.axDetected.autoscale_view()
        self.figDetected.canvas.draw()
        self.figDetected.canvas.flush_events()
        
        self.detectedVehiclesCanvas = FigureCanvasTkAgg(self.figDetected, numberOfDetectedVehicleInnerFrame)
        self.detectedVehiclesCanvas.draw()
        self.detectedVehiclesCanvas.get_tk_widget().pack(side = "top", expand = True, fill = "both")
        
        detectedVehiclesLocation = CTkComboBox(numberOfDetectedVehicleFrame,
                                               values = locations,
                                               state='readonly',
                                               command = self.detectedVehiclesLocation_callback,
                                               width = 200,
                                               fg_color = '#e5e5e5',
                                               dropdown_fg_color = '#e5e5e5',
                                               text_color = '#000000',
                                               dropdown_text_color = '#000000',
                                               border_color = '#FFFFFF',
                                               button_color = '#FFFFFF')
        detectedVehiclesLocation.pack(side = 'top', pady = (0, 10))
        # End ofNumber of Detected Vehicles Graph
        
        # Number of Revenue Generated Graph
        revenueGeneratedInnerFrame = CTkFrame(revenueGeneratedFrame, bg_color = "#1B2431", fg_color = "#1B2431")
        revenueGeneratedInnerFrame.pack(padx = 50, pady = 10, side ="top", expand = True, fill = "both")
        
        #Insert Graph Here
        self.figRevenue = plt.Figure(figsize=(3, 3))
        self.axRevenue = self.figRevenue.add_subplot()
        self.axRevenue.set_xlabel('Time')
        self.axRevenue.set_ylabel('Revenue Generated (Php)')
        self.axRevenue.set_title('Revenue Generated Over Time')

        self.axRevenue.relim()
        self.axRevenue.autoscale_view()
        self.figRevenue.canvas.draw()
        self.figRevenue.canvas.flush_events()
        
        revenueGeneratedCanvas = FigureCanvasTkAgg(self.figRevenue, revenueGeneratedInnerFrame)
        revenueGeneratedCanvas.draw()
        revenueGeneratedCanvas.get_tk_widget().pack(side = "top", expand= True, fill = "both")
        
        revenueGeneratedLocation = CTkComboBox(revenueGeneratedFrame,
                                               values = locations,
                                               state='readonly',
                                               command = self.revenueGeneratedLocation_callback,
                                               width = 200,
                                               fg_color = '#e5e5e5',
                                               dropdown_fg_color = '#e5e5e5',
                                               text_color = '#000000',
                                               dropdown_text_color = '#000000',
                                               border_color = '#FFFFFF',
                                               button_color = '#FFFFFF')
        revenueGeneratedLocation.pack(side = 'top', pady = (0, 10))
        # End of Number of Revenue Generated Graph
        
        # System Performance details
        titleLabelFrame = CTkFrame(systemPerformanceFrame, bg_color = "#1B2431", fg_color = "#1B2431")
        cpuUsageLabelFrame = CTkFrame(systemPerformanceFrame, bg_color = "#1B2431", fg_color = "#1B2431")
        memoryUsageLabelFrame = CTkFrame(systemPerformanceFrame, bg_color = "#1B2431", fg_color = "#1B2431")
        
        titleLabel = CTkLabel(titleLabelFrame, text = "System Perforamnce", font = ('Montserrat', 12), anchor = "w")
        
        cpuUsageLabel = CTkLabel(cpuUsageLabelFrame, text = "CPU Usage", font = ('Montserrat', 12), anchor = "w")
        self.cpuUsagePercentLabel = CTkLabel(cpuUsageLabelFrame, text = "0%", font = ('Montserrat', 12), anchor = "e")
        
        memoryUsageLabel = CTkLabel(memoryUsageLabelFrame, text = "Memory Usage", font = ('Montserrat', 12), anchor = "w")
        self.memoryUsagePercentLabel = CTkLabel(memoryUsageLabelFrame, text = "0%", font = ('Montserrat', 12), anchor = "e")
        
        titleLabelFrame.pack(side = "top", pady = (20, 30), padx = (20, 150), fill = "x")
        cpuUsageLabelFrame.pack(side = "top", padx = (20, 20), fill = "x")
        memoryUsageLabelFrame.pack(side = "top", padx = (20, 20), fill = "x")
        
        titleLabel.pack(side = "left", expand = True, fill = "x")
        
        cpuUsageLabel.pack(side = "left", expand = True, fill = "x")
        self.cpuUsagePercentLabel.pack(side = "left", expand = True, fill = "x")
        
        memoryUsageLabel.pack(side = "left", expand = True, fill = "x")
        self.memoryUsagePercentLabel.pack(side = "left", expand = True, fill = "x")
        # End of System Performance details
        
        # Busiest Time Graph
        busiestTimeInnerFrame = CTkFrame(busiestTimeFrame, bg_color = "#1B2431", fg_color = "#1B2431")
        busiestTimeInnerFrame.pack(padx = 50, pady = 10, side ="top", expand = True, fill = "both")
        
        #Insert Graph Here
        self.figBusiest = plt.Figure(figsize=(3, 3))
        self.axBusiest = self.figBusiest.add_subplot()
        self.axBusiest.set_xlabel('Time')
        self.axBusiest.set_ylabel('Volume of Vehicles')
        self.axBusiest.set_title('Busiest Time')

        self.axBusiest.relim()
        self.axBusiest.autoscale_view()
        self.figBusiest.canvas.draw()
        self.figBusiest.canvas.flush_events()
        
        busiestTimeCanvas = FigureCanvasTkAgg(self.figBusiest, busiestTimeInnerFrame)
        busiestTimeCanvas.draw()
        busiestTimeCanvas.get_tk_widget().pack(side = "top", expand = True, fill = "both")
        
        busiestTimeLocation = CTkComboBox(busiestTimeFrame,
                                               values = locations,
                                               state='readonly',
                                               command = self.busiestTimeLocation_callback,
                                               width = 200,
                                               fg_color = '#e5e5e5',
                                               dropdown_fg_color = '#e5e5e5',
                                               text_color = '#000000',
                                               dropdown_text_color = '#000000',
                                               border_color = '#FFFFFF',
                                               button_color = '#FFFFFF')
        busiestTimeLocation.pack(side = 'top', pady = (0, 10))
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
        dashboardButton.bind("<Enter>", lambda event: dashboardButton.configure(text_color="#5E60CE", fg_color = "#090E18")) 
        dashboardButton.bind("<Leave>", lambda event: dashboardButton.configure(text_color="#090E18", fg_color = "#5E60CE")) 
        dashboardButton.pack(side = 'right', padx = 5, pady = 1)
        
        # Scheduled Apply Buttom, function placeholder is print. For the assignee, update the "command"
        self.downloadCSVButton = CTkButton(navigationFrame,
                                text = 'Download CSV',
                                command = self.downloadCSV, 
                                font = ('Montserrat', 12),
                                border_width = 2,
                                corner_radius = 15,
                                border_color = '#5E60CE',
                                text_color = '#5E60CE',
                                fg_color = '#090E18',
                                height = 30,
                                width = 140)
        
        self.downloadCSVButton.bind("<Enter>", lambda event: self.downloadCSVButton.configure(text_color="#090E18", fg_color = "#5E60CE"))
        self.downloadCSVButton.bind("<Leave>", lambda event: self.downloadCSVButton.configure(text_color="#5E60CE", fg_color = "#090E18"))
        self.downloadCSVButton.pack(side = 'right', padx = 5, pady = 1)

    def updatePercentages(self):
        if PollController.analyticsShown:
            self.memoryUsagePercentLabel.configure(text=f'{rgctrl.get_memory_usage()[1][0]}%')
            self.cpuUsagePercentLabel.configure(text=f'{rgctrl.get_cpu_usage()[1][0]}%')
        self.after(10000, self.updatePercentages)