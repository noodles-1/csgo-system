import os
import sys
import tkinter as tk
from customtkinter import *
from tkinter import ttk
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

        forgotButton = CTkButton(loginFormFrame, text = 'Forgot Password?', border_color = '#000000', fg_color = '#000000', height = 5, width = 20)
        forgotButton.pack()
        

class DashboardPage(tk.Frame):
    def closeApplication(self):
        self.master.destroy()

    def minimizeApplicaiton(self):
        self.master.iconify()

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg = "#090E18")
        self.tk.call('source', 'views/assets/theme/forest-dark.tcl')

        style = ttk.Style()
        
        style.theme_use('forest-dark')
        #style.theme_use('default')

        closeImage = Image.open("views/icons/icon_close_darkmode.png")
        closeImage = closeImage.resize((20, 20))
        closePhoto = ImageTk.PhotoImage(closeImage)

        minimizeImage = Image.open("views/icons/icon_minimize_darkmode.png")
        minimizeImage = minimizeImage.resize((20, 20))
        minimizePhoto = ImageTk.PhotoImage(minimizeImage)

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

        mainFrame = tk.Frame(self, bg = "#090E18")
        mainFrame.pack(expand = True, fill = "both", side = "top")

        bottomFrame = tk.Frame(self, bg = "#090E18")
        bottomFrame.pack(fill = "both", side = "top", padx = 20)

        analyticsButton = CTkButton(bottomFrame,
                                    text = 'Analytics',
                                    command = lambda: parent.show_frame(parent.analyticsFrame),
                                    font = ('Montserrat', 15),
                                    border_width = 1,
                                    corner_radius = 15,
                                    border_color = '#5E60CE',
                                    text_color = '#5E60CE',
                                    fg_color = '#090E18',
                                    height = 30,
                                    width = 140)
        
        adminButton = CTkButton(bottomFrame,
                                text = 'Admin',
                                command = lambda: parent.show_frame(parent.adminFrame), 
                                font = ('Montserrat', 15),
                                border_width = 1,
                                corner_radius = 15,
                                border_color = '#5E60CE',
                                text_color = '#5E60CE',
                                fg_color = '#090E18',
                                height = 30,
                                width = 140)
        
        analyticsButton.pack(side = 'right', padx = 10, pady = 10)
        adminButton.pack(side = 'right', padx = 10, pady = 10)


        leftMainFrame = tk.Frame(mainFrame, bg = "#090E18")
        rightMainFrame = tk.Frame(mainFrame, bg = "#090E18")
        leftMainFrame.pack(side = 'left', fill = 'both', expand = True, pady = 5)
        rightMainFrame.pack(side = 'left', fill = 'both', expand = True, pady = 5)

        databaseFrame = tk.Frame(rightMainFrame, bg = '#1B2431')
        databaseFrame.pack(expand = True, fill = 'both', padx = 15, pady = 10)

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

        # ADD or REMOVE headers as needed
        databaseTable = ttk.Treeview(databaseFrame, columns = ('licensePlate', 'vehicleType', 'cameraID', 'time', 'date', 'price'), show = "headings", style = 'Custom.Treeview')

        for _ in range(100):
            databaseTable.insert('', 'end', values=('', '', '', '', '', ''))

        databaseTable.tag_configure('even', background='#2A2D2E', foreground='#FFFFFF')
        databaseTable.tag_configure('odd', background='#343638', foreground='#FFFFFF')
        
        databaseTable.heading('licensePlate', text="License Plate", anchor='center')
        databaseTable.heading('vehicleType', text="Vehicle Type", anchor='center')
        databaseTable.heading('cameraID', text="Camera ID", anchor='center')
        databaseTable.heading('time', text="Time", anchor='center')
        databaseTable.heading('date', text="Date", anchor='center')
        databaseTable.heading('price', text="Price", anchor='center')

        databaseTable.column('licensePlate', width=150, anchor='center')
        databaseTable.column('vehicleType', width=150, anchor='center')
        databaseTable.column('cameraID', width=120, anchor='center')
        databaseTable.column('time', width=100, anchor='center')
        databaseTable.column('date', width=100, anchor='center')
        databaseTable.column('price', width=80, anchor='center')

        databaseTable.pack(expand=True, fill='both', padx=0, pady=0)

        xscrollbar = ttk.Scrollbar(databaseFrame, orient='horizontal', command=databaseTable.xview)
        databaseTable.configure(xscrollcommand=xscrollbar.set)
        xscrollbar.pack(side='bottom', fill='both', padx=0, pady=0)

        topLeftMainFrame = tk.Frame(leftMainFrame, bg = "#090E18")
        middleLeftMainFrame = tk.Frame(leftMainFrame, bg = "#090E18")
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
        upTimeLabel = CTkLabel(upTimeBottomLabelLeftMainFrame, text = 'Up Time: ', text_color = 'white', font = ('Montserrat', 12))
        cameraIDLabel = CTkLabel(cameraIDBottomLeftFrame, text = 'Camera ID: ', text_color = 'white', font = ('Montserrat', 12))

        vehicleDetectedLabel.pack(side = 'left', padx = 5)
        upTimeLabel.pack(side = 'left')
        cameraIDLabel.pack(side = 'left')
        
        cameraFrame = CTkFrame(topLeftMainFrame, border_width = 2, bg_color = '#1B2431', fg_color = '#1B2431')
        cameraFrame.pack(fill = 'both', expand = True, padx = 15, pady = 10)

        placeholder_delete_this_label = CTkLabel(cameraFrame, text = 'PLACEHOLDER ONLY. ADD CAMERA HERE', font = ('Montserrat', 45), text_color = 'white')
        placeholder_delete_this_label.pack(fill = 'both', expand = True)

        settingsButton = CTkButton(middleLeftMainFrame,
                                    text = 'Settings',
                                    height = 32,
                                    width = 148,
                                    text_color = '#48BFE3',
                                    command = lambda: parent.show_frame(parent.configFrame), 
                                    border_color = '#48BFE3', 
                                    fg_color = '#090E18', 
                                    border_width = 1,
                                    hover_color = '#48BFE3',
                                    corner_radius = 15,
                                    font = ('Montserrat', 15))
        
        settingsButton.pack(side = 'left', padx = 5, pady = 20)

        '''
        @Mendoza
        topLeftMainFrame is the Frame where the camera should be setup and visualized.
        '''

        '''
        @Roa
        rightMainFrame is the Frame where the Live Database should be setup and visualized.
        If you require specific buttons for the live database, message me immediately.
        '''


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
