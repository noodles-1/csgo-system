import os
import sys
import asyncio
import tkinter as tk
import tk_async_execute as tk_async

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from customtkinter import *
from views.loginPageView import LoginPage
from views.dashboardPageView import DashboardPage
from views.analyticsPageView import AnalyticsPage
from views.adminPageView import AdminPage
from views.configPageView import ConfigPage
from views.forgotPageView import ForgetPasswordPage
from models.connect import Connection as connection
from controllers.pollController import PollController

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
        self.forgotFrame = ForgetPasswordPage(self)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.loginFrame.grid(row=0, column=0, sticky="nsew")
        self.dashboardFrame.grid(row=0, column=0, sticky="nsew")
        self.analyticsFrame.grid(row=0, column=0, sticky="nsew")
        self.configFrame.grid(row=0, column=0, sticky="nsew")
        self.adminFrame.grid(row=0, column=0, sticky="nsew")
        self.forgotFrame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(self.loginFrame)

        self.currUser = None
        
    # Function to show Frame (Can be used by the child Classes)
    def show_frame(self, cont, changeCameraDisplay=None, cap=None, placeholder_label=None):
        if changeCameraDisplay:
            cont.setCameraDisplay(changeCameraDisplay, cap, placeholder_label)
        cont.tkraise()
    
    def setUser(self, user):
        self.currUser = user
        self.dashboardFrame.setCurrUser(user)
        self.configFrame.applyRestrictions(user)
        self.analyticsFrame.applyRestrictions(user)

def startAsyncLoop(loop):
    loop.call_soon(loop.stop)
    loop.run_forever()
    app.after(30000, startAsyncLoop, loop)

async def runAsync():
    asyncio.create_task(poll())

async def poll():
    while True:
        PollController.updateFutureSettings()
        PollController.updateActiveSetting()
        await asyncio.sleep(30)

if __name__ == "__main__":
    connection.connect('database/test.db')

    loop = asyncio.get_event_loop()
    loop.create_task(runAsync())

    app = MainWindow()
    app.after(30000, startAsyncLoop, loop)

    tk_async.start()
    app.mainloop()
    tk_async.stop()