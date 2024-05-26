import os
import sys
import tkinter as tk

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from customtkinter import *
from loginPageView import LoginPage
from dashboardPageView import DashboardPage
from configPageView import ConfigPage
from analyticsPageView import AnalyticsPage
from adminPageView import AdminPage
from models.connect import Connection as connection

# view.py is the starting point of the GUI. This is where each Pages are defined. (Parent Class)

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Toll-less Toll by CSGO")
        self.attributes('-fullscreen', True)
        self.tk.call('source', 'views/assets/theme/forest-dark.tcl')
        
        icon = tk.PhotoImage(file = 'views/assets/app-icon.png')
        
        self.iconphoto(True, icon)
        
        self.loginFrame = LoginPage(self)
        self.dashboardFrame = DashboardPage(self)
        self.analyticsFrame = AnalyticsPage(self)
        self.configFrame = ConfigPage(self)
        self.adminFrame = AdminPage(self)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.loginFrame.grid(row=0, column=0, sticky="nsew")
        self.dashboardFrame.grid(row=0, column=0, sticky="nsew")
        self.analyticsFrame.grid(row=0, column=0, sticky="nsew")
        self.configFrame.grid(row=0, column=0, sticky="nsew")
        self.adminFrame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(self.loginFrame)
        
    # Function to show Frame (Can be used by the child Classes)
    def show_frame(self, cont, changeCameraDisplay=None, cap=None, placeholder_label=None):
        if changeCameraDisplay:
            cont.setCameraDisplay(changeCameraDisplay, cap, placeholder_label)
        cont.tkraise()

if __name__ == "__main__":
    connection.connect('database/test.db')
    app = MainWindow()
    app.mainloop()
