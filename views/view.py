import os
import sys
import tkinter as tk
from customtkinter import *
from PIL import Image, ImageTk

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Frame Switching Example")
        self.attributes('-fullscreen', True)

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

    def show_frame(self, cont):
        cont.tkraise()

class LoginPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg = "blue")

        #coverImage = ImageTk.PhotoImage(Image.open("views\assets\blue-iris.png"))
        coverImage = Image.open("views/assets/blue-iris.png")
        coverImage = coverImage.resize((838, 479))
        coverPhoto = ImageTk.PhotoImage(coverImage)

        closeImage = Image.open("views/icons/icon_close_darkmode.png")
        closeImage = closeImage.resize((20, 20))
        closePhoto = ImageTk.PhotoImage(closeImage)

        minimizeImage = Image.open("views/icons/icon_minimize_darkmode.png")
        minimizeImage = minimizeImage.resize((20, 20))
        minimizePhoto = ImageTk.PhotoImage(minimizeImage)

        toolbarFrame = tk.Frame(self, bg = "#000000", height = 30)
        toolbarFrame.pack(fill = "both", side = "top")

        closeButton = CTkButton(toolbarFrame, 
                                image = closePhoto,
                                text = "",
                                width = 20,
                                height = 20,
                                fg_color = "#000000",
                                bg_color = "#000000",
                                hover = True,
                                hover_color = "#48BFE3")
        closeButton.pack(side = "right", padx = 10, pady = 10)

        minimizeButton = CTkButton(toolbarFrame, 
                                image = minimizePhoto,
                                text = "",
                                width = 20,
                                height = 20,
                                fg_color = "#000000",
                                bg_color = "#000000",
                                hover = True,
                                hover_color = "#48BFE3")
        minimizeButton.pack(side = "right", padx = 0, pady = 10)

        mainFrame = tk.Frame(self, bg = "green")
        mainFrame.pack(expand = True, fill = "both", side = "top")

        mainFrameLeft = tk.Frame(mainFrame, bg = "#000000")
        mainFrameRight = tk.Frame(mainFrame, bg = "#000000")

        mainFrameLeft.pack(expand = True, fill = "both", side = "left")
        mainFrameRight.pack(fill = "both", side = "left")

        #labelImageCover = tk.Label(mainFrameLeft, image = coverPhoto, text = "")
        labelImageCover = CTkLabel(mainFrameLeft, image = coverPhoto, text = "")
        labelImageCover.pack(side = "top", fill = "both", expand = "yes")

        loginFormFrame = tk.Frame(mainFrameRight, bg = "#000000")
        loginFormFrame.pack(fill = "none", expand = True, side = "top", padx = 110)

        titleFrame = tk.Frame (loginFormFrame, bg = "#000000")
        titleFrame.pack(expand = True, fill = 'x')

        automatedLabel = tk.Label(titleFrame, text = "Automated", font = ('Montserrat', 40, "bold"), fg = "#48BFE3", bg = "#000000")
        automatedLabel.pack(padx = 10, fill = "x", pady = 0, ipady = 0)

        congestionLabel = tk.Label(titleFrame, text = "Congestion Pricing", font = ('Montserrat', 24, "bold"), fg = "#80FFDB", bg = "#000000")
        congestionLabel.pack(padx = 10, fill = "x", pady = 0, ipady = 0)

        employeeidEntry = CTkEntry(loginFormFrame, font = ('Montserrat', 14), placeholder_text = "Employee ID", width = 305, height = 50)
        employeeidEntry.pack(pady = 10, padx = 10, expand = True, fill = "x")

        passwordEntry = CTkEntry(loginFormFrame, show = "*", font = ('Montserrat', 14), placeholder_text = "Password", width = 305, height = 50)
        passwordEntry.pack(pady = 10, padx = 10, expand = True, fill = "x")

        loginButton = CTkButton(loginFormFrame, 
                                text = "Login",
                                height = 32,
                                width = 148,
                                text_color = '#48BFE3',
                                command = lambda: parent.show_frame(parent.dashboardFrame), 
                                border_color = '#48BFE3', 
                                fg_color = '#000000', 
                                border_width = 1,
                                hover_color = '#48BFE3',
                                corner_radius = 15,
                                font = ('Montserrat', 15))
        loginButton.pack(pady = 10)

        #button = tk.Button(loginFormFrame, text = "Login", command=lambda: parent.show_frame(parent.dashboardFrame))
        #button.pack()

class DashboardPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg = "green")
        label = tk.Label(self, text = "This is The Dashboard Page", font = ('Helvetica', 14))
        label.pack(pady = 10, padx = 10)
        button1 = tk.Button(self, text = "Analytics", command = lambda: parent.show_frame(parent.analyticsFrame))
        button1.pack()
        button2 = tk.Button(self, text = "Configuration", command = lambda: parent.show_frame(parent.configFrame))
        button2.pack()
        button3 = tk.Button(self, text = "Admin", command = lambda: parent.show_frame(parent.adminFrame))
        button3.pack()

class AnalyticsPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg = "pink")
        label = tk.Label(self, text = "This is the Analaytics Page", font = ('Helvetica', 14))
        label.pack(pady = 10, padx = 10)
        button = tk.Button(self, text = "Dashboard" , command = lambda: parent.show_frame(parent.dashboardFrame))
        button.pack()

class ConfigPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg = "red")
        label = tk.Label(self, text = "This is the Config Page", font = ('Helvetica', 14))
        label.pack(pady = 10, padx = 10)
        button1 = tk.Button(self, text = "Dashboard", command = lambda: parent.show_frame(parent.dashboardFrame))
        button1.pack()
        button2 = tk.Button(self, text = "Logout", command = lambda: parent.show_frame(parent.loginFrame))
        button2.pack()
                                                                                 
class AdminPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg = "brown")
        label = tk.Label(self, text = "This is the Admin Page", font = ('Helvetica', 14))
        label.pack(pady = 10, padx = 10)
        button = tk.Button(self, text = "Dashboard", command = lambda: parent.show_frame(parent.dashboardFrame))
        button.pack()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
