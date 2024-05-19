import os
import sys
import tkinter as tk

from customtkinter import *
from PIL import Image

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from customtkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from controllers.dbController import DBController as db

class LoginPage(tk.Frame):
    # Close Application
    def closeApplication(self):
        self.master.destroy()

    # Minimize or Iconify the Application
    def minimizeApplicaiton(self):
        self.master.iconify()

    # Function that is called when the credentials are incorrect.
    def incorrectCredentials(self, incorrectLabel: CTkLabel):
        incorrectLabel.configure(text_color = "#d62828")
        self.after(2000, lambda: incorrectLabel.configure(text_color="#000000"))
    
    # Function that is called to go to the Forgot Password Page (Unfinished)
    def forgotPasswordFunction(self):
        pass
    
    # Function that is called when clicking Login
    def verifyCredentials(self, usernameEntry: CTkEntry, passwordEntry: CTkEntry, incorrectLabel: CTkLabel):
        username, password = usernameEntry.get(), passwordEntry.get()
        print("verify credentials called", username, password)
        
        response = db.loginUser(password=password, username=username)
        if response.ok:
            self.master.show_frame(self.master.dashboardFrame)
        else:
            incorrectLabel.configure(text=(response.messages['username'] or response.messages['password']))
            self.incorrectCredentials(incorrectLabel)

        passwordEntry.delete(0, "end")
        usernameEntry.delete(0, "end")
    
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg = "blue")
        
        # Cover Image (The Eye)
        coverPhoto = CTkImage(light_image = Image.open("views/assets/blue-iris-updated.png"),
                              dark_image = Image.open("views/assets/blue-iris-updated.png"),
                              size = (838, 479))

        # Close Icon (Currently Set to darkmode, if possible change to lightmode when the the changes)
        closePhoto = CTkImage(light_image = Image.open("views/icons/icon_close_lightmode.png"),
                              dark_image = Image.open("views/icons/icon_close_darkmode.png"),
                              size = (20, 20))

        # Minimize Icon (Currently Set to darkmode, if possible change to lightmode when the the changes)
        minimizePhoto = CTkImage(light_image = Image.open("views/icons/icon_minimize_lightmode.png"),
                              dark_image = Image.open("views/icons/icon_minimize_darkmode.png"),
                              size = (20, 20))

        # Top-most Frame that holds the Close and Minimize buttons.
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
        # End of Toolbar Frame
        
        # Start of Main Frame (Where the contents of the main page is)
        mainFrame = tk.Frame(self, bg = "black")
        mainFrame.pack(expand = True, fill = "both", side = "top")

        mainFrameLeft = tk.Frame(mainFrame, bg = "#000000")
        mainFrameRight = tk.Frame(mainFrame, bg = "#000000")

        mainFrameLeft.pack(expand = True, fill = "both", side = "left")
        mainFrameRight.pack(fill = "both", side = "left")

        labelImageCover = CTkLabel(mainFrameLeft, image = coverPhoto, text = "")
        labelImageCover.pack(side = "top", fill = "both", expand = True)
        
        # This is the Frame where the login form is rooted to.
        loginFormFrame = tk.Frame(mainFrameRight, bg = "#000000")
        loginFormFrame.pack(fill = "none", expand = True, side = "top", padx = 110)

        titleFrame = tk.Frame (loginFormFrame, bg = "#000000")
        titleFrame.pack(expand = True, fill = 'x')

        automatedLabel = tk.Label(titleFrame, text = "Automated", font = ('Montserrat', 40, "bold"), fg = "#48BFE3", bg = "#000000")
        automatedLabel.pack(padx = 10, fill = "x", pady = 0, ipady = 0)

        congestionLabel = tk.Label(titleFrame, text = "Congestion Pricing", font = ('Montserrat', 24, "bold"), fg = "#80FFDB", bg = "#000000")
        congestionLabel.pack(padx = 10, fill = "x", pady = 0, ipady = 0)

        usernameEntry = CTkEntry(loginFormFrame, font = ('Montserrat', 14), placeholder_text = "Username", width = 305, height = 50, border_width = 2, border_color = "#48BFE3", fg_color = "#000000", corner_radius = 15)
        usernameEntry.pack(pady = 10, padx = 10, expand = True, fill = "x")

        passwordEntry = CTkEntry(loginFormFrame, show = "*", font = ('Montserrat', 14), placeholder_text = "Password", width = 305, height = 50, border_width = 2, border_color = "#48BFE3", fg_color = "#000000", corner_radius = 15)
        passwordEntry.pack(pady = (10, 0), padx = 10, expand = True, fill = "x")
        
        incorrectLabel = CTkLabel(loginFormFrame, font = ('Monteserrat', 12, 'italic'), text = "Incorrect Username or Password", anchor = "w", text_color = "#000000")
        incorrectLabel.pack(pady = (0, 10), padx = 20, expand = True, fill = "x")

        loginButton = CTkButton(loginFormFrame, 
                                text = "Login",
                                height = 32,
                                width = 148,
                                text_color = '#48BFE3',
                                command = lambda: self.verifyCredentials(usernameEntry, passwordEntry, incorrectLabel),
                                border_color = '#48BFE3',
                                fg_color = '#000000', 
                                border_width = 2,
                                corner_radius = 15,
                                font = ('Montserrat', 15))
        loginButton.pack(pady = 10)
        
        loginButton.bind("<Enter>", lambda event: loginButton.configure(text_color="#000000", fg_color = "#48BFE3")) 
        loginButton.bind("<Leave>", lambda event: loginButton.configure(text_color="#48BFE3", fg_color = "#000000"))  

        forgotButton = CTkButton(loginFormFrame, text = 'Forgot Password?', border_color = '#000000', fg_color = '#000000', height = 5, width = 20, font = ('Montserrat', 10), command = lambda: self.forgotPasswordFunction)
        forgotButton.pack()
        # End of the Main Frame