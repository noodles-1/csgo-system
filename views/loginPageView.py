import os
import sys
import tkinter as tk
from customtkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

class LoginPage(tk.Frame):
    def closeApplication(self):
        self.master.destroy()

    def minimizeApplicaiton(self):
        self.master.iconify()

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg = "blue")
        
        coverImage = Image.open("views/assets/blue-iris-updated.png")
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
                                hover_color = "#48BFE3",
                                command = self.closeApplication)
        closeButton.pack(side = "right", padx = 10, pady = 10)

        minimizeButton = CTkButton(toolbarFrame, 
                                image = minimizePhoto,
                                text = "",
                                width = 20,
                                height = 20,
                                fg_color = "#000000",
                                bg_color = "#000000",
                                hover = True,
                                hover_color = "#48BFE3",
                                command = self.minimizeApplicaiton)
        minimizeButton.pack(side = "right", padx = 0, pady = 10)

        mainFrame = tk.Frame(self, bg = "black")
        mainFrame.pack(expand = True, fill = "both", side = "top")

        mainFrameLeft = tk.Frame(mainFrame, bg = "#000000")
        mainFrameRight = tk.Frame(mainFrame, bg = "#000000")

        mainFrameLeft.pack(expand = True, fill = "both", side = "left")
        mainFrameRight.pack(fill = "both", side = "left")

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

        employeeidEntry = CTkEntry(loginFormFrame, font = ('Montserrat', 14), placeholder_text = "Employee ID", width = 305, height = 50, border_width = 2, border_color = "#48BFE3", fg_color = "#000000", corner_radius = 15)
        employeeidEntry.pack(pady = 10, padx = 10, expand = True, fill = "x")

        passwordEntry = CTkEntry(loginFormFrame, show = "*", font = ('Montserrat', 14), placeholder_text = "Password", width = 305, height = 50, border_width = 2, border_color = "#48BFE3", fg_color = "#000000", corner_radius = 15)
        passwordEntry.pack(pady = 10, padx = 10, expand = True, fill = "x")

        loginButton = CTkButton(loginFormFrame, 
                                text = "Login",
                                height = 32,
                                width = 148,
                                text_color = '#48BFE3',
                                command = lambda: parent.show_frame(parent.dashboardFrame), 
                                border_color = '#48BFE3', 
                                fg_color = '#000000', 
                                border_width = 2,
                                corner_radius = 15,
                                font = ('Montserrat', 15))
        loginButton.pack(pady = 10)
        
        loginButton.bind("<Enter>", lambda event: loginButton.configure(text_color="#000000", fg_color = "#48BFE3")) 
        loginButton.bind("<Leave>", lambda event: loginButton.configure(text_color="#48BFE3", fg_color = "#000000"))  

        forgotButton = CTkButton(loginFormFrame, text = 'Forgot Password?', border_color = '#000000', fg_color = '#000000', height = 5, width = 20, font = ('Montserrat', 10))
        forgotButton.pack()