import os
import sys
import cv2
import tkinter as tk

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from customtkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from controllers import controller

class DashboardPage(tk.Frame):
    # Close Application
    def closeApplication(self):
        self.master.destroy()

    # Minimize or Iconify the Application
    def minimizeApplicaiton(self):
        self.master.iconify()
    
    # Function to change the camera displayed
    def changeCameraDisplay_callback(self, choice):
        # Insert Logic Here
        print("Change Camera Display callback: ", choice)

    def __init__(self, parent):
        self.ai = controller.AIController()

        tk.Frame.__init__(self, parent, bg = "#090E18")
        
        # Style definition. Can be utilized with the Change Theme from Light to Dark
        style = ttk.Style()
        style.theme_use('forest-dark')

        # Close Icon (Currently Set to darkmode, if possible change to lightmode when the the changes)
        closeImage = Image.open("views/icons/icon_close_darkmode.png")
        closeImage = closeImage.resize((20, 20))
        closePhoto = ImageTk.PhotoImage(closeImage)

        # Minimize Icon (Currently Set to darkmode, if possible change to lightmode when the the changes)
        minimizeImage = Image.open("views/icons/icon_minimize_darkmode.png")
        minimizeImage = minimizeImage.resize((20, 20))
        minimizePhoto = ImageTk.PhotoImage(minimizeImage)

        # Top-most Frame that holds the Close and Minimize buttons.
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
        # End of Toolbar Frame
        
        # Start of Main Frame (Where the contents of the main page is)
        mainFrame = tk.Frame(self, bg = "#090E18")
        mainFrame.pack(expand = True, fill = "both", side = "top")

        bottomFrame = tk.Frame(self, bg = "#090E18")
        bottomFrame.pack(fill = "both", side = "top", padx = 20)

        # Goes to the Analytics Page
        analyticsButton = CTkButton(bottomFrame,
                                    text = 'Analytics',
                                    command = lambda: parent.show_frame(parent.analyticsFrame),
                                    font = ('Montserrat', 15),
                                    border_width = 2,
                                    corner_radius = 15,
                                    border_color = '#5E60CE',
                                    text_color = '#5E60CE',
                                    fg_color = '#090E18',
                                    height = 30,
                                    width = 140)
        
        # Goes to the Admin Page (Should be disabled unless the user logged in is an Admin)
        adminButton = CTkButton(bottomFrame,
                                text = 'Admin',
                                command = lambda: parent.show_frame(parent.adminFrame), 
                                font = ('Montserrat', 15),
                                border_width = 2,
                                corner_radius = 15,
                                border_color = '#5E60CE',
                                text_color = '#5E60CE',
                                fg_color = '#090E18',
                                height = 30,
                                width = 140)
        
        analyticsButton.pack(side = 'right', padx = 10, pady = 10)
        adminButton.pack(side = 'right', padx = 10, pady = 10)
        
        analyticsButton.bind("<Enter>", lambda event: analyticsButton.configure(text_color="#090E18", fg_color = "#5E60CE")) 
        analyticsButton.bind("<Leave>", lambda event: analyticsButton.configure(text_color="#5E60CE", fg_color = "#090E18")) 
        
        adminButton.bind("<Enter>", lambda event: adminButton.configure(text_color="#090E18", fg_color = "#5E60CE")) 
        adminButton.bind("<Leave>", lambda event: adminButton.configure(text_color="#5E60CE", fg_color = "#090E18")) 

        # Separates the Main Frame into two Sides (Left and Right)
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

        # ADD or REMOVE headers as needed @Database Integration
        databaseTable = ttk.Treeview(databaseFrame, columns = ('licensePlate', 'vehicleType', 'cameraID', 'time', 'date', 'price'), show = "headings", style = 'Custom.Treeview')
        

        # Inserts Blank Entries to the Treeview so that it doesnt look bad when the Treeview is Empty.
        #for _ in range(100):
            #databaseTable.insert('', 'end', values=('', '', '', '', '', ''))

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
        
        cameraFrame = CTkFrame(topLeftMainFrame, fg_color = '#1B2431')
        cameraFrame.pack(fill = 'both', expand = True, padx = 15, pady = 10)

        # This is where you should input the camera Frame. Delete the code below this if integrating the camera display.
        placeholder_delete_this_label = CTkLabel(cameraFrame, text = 'PLACEHOLDER TEXT HERE', font = ('Montserrat', 45), text_color = 'white')
        placeholder_delete_this_label.pack(fill = 'both', expand = True)
        # ----
        
        dropdownFrame = CTkFrame(cameraFrame, fg_color = "#1B2431")
        dropdownFrame.pack(fill = 'x', side = "bottom", padx = 10, pady = 10)
        
        changeCameraDisplay = CTkComboBox(dropdownFrame, values = ["Camera 1", "Camera 2", "Camera 3", "Camera 4", "Camera 5"], command = self.changeCameraDisplay_callback, width = 100)
        changeCameraDisplay.set("Camera 1")
        changeCameraDisplay.pack(side = "right")
        
        changeCameraLabel = CTkLabel(dropdownFrame, text = "Change Camera", font = ('Montserrat', 13), text_color = "#FFFFFF")
        changeCameraLabel.pack(side = "right", padx = 10)
        
        # Goes to the Config Page
        settingsButton = CTkButton(middleLeftMainFrame,
                                    text = 'Settings',
                                    height = 32,
                                    width = 148,
                                    text_color = '#48BFE3',
                                    command = lambda: parent.show_frame(parent.configFrame), 
                                    border_color = '#48BFE3', 
                                    fg_color = '#090E18', 
                                    border_width = 2,
                                    hover_color = '#48BFE3',
                                    corner_radius = 15,
                                    font = ('Montserrat', 15))
        
        settingsButton.pack(side = 'left', padx = 5, pady = 20)
        
        settingsButton.bind("<Enter>", lambda event: settingsButton.configure(text_color="#090E18", fg_color = "#48BFE3")) 
        settingsButton.bind("<Leave>", lambda event: settingsButton.configure(text_color="#48BFE3", fg_color = "#090E18")) 

        '''
        @Mendoza
        topLeftMainFrame is the Frame where the camera should be setup and visualized.
        How you'll do this is using frames and continuously displaying each frame.
        Refer to oldView.py for reference.
        If you have CCTV camera in your house use it, if not, use a webcam.1
        '''

        '''
        @Roa
        rightMainFrame is the Frame where the Live Database should be setup and visualized.
        If you require specific buttons for the live database, message me immediately.
        '''