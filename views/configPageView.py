import os
import sys
import tkinter as tk
from customtkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

class ConfigPage(tk.Frame):
    def closeApplication(self):
        self.master.destroy()

    def minimizeApplicaiton(self):
        self.master.iconify()
        
    def fromComboBox_callback(self, choice):
        print("From Combobox callback: ", choice)

    def toComboBox_callback(self, choice):
        print("From Combobox callback: ", choice)
    
    def themeRadioButton_callback(self):
        print("Radio Button Theme callback: ", self.themeVar.get())
        
    def applyButton_callback(self):
        print("Apply Button Pressed")
    
    def scheduleApplyButton_callback(self):
        print("Schedule Apply Button Pressed")
        
    def add_row(self):
        addImage = Image.open("views/icons/icons_add.png")
        addImage = addImage.resize((25, 25))
        addPhoto = ImageTk.PhotoImage(addImage)
        
        newRowFrame = tk.Frame(self.scheduleLineFrame, bg="#1B2431")
        newRowFrame.pack(fill="x", side="top", padx=5, pady=5, expand = True)

        fromLabel = CTkLabel(newRowFrame, text="From", font=('Montserrat', 15), text_color="#FFFFFF", anchor="w")
        fromLabel.pack(side="left", padx=5)

        fromComboBox = CTkComboBox(newRowFrame, values=["1 AM", "2 AM", "3 AM", "4 AM",
                                                             "5 AM", "6 AM", "7 AM", "8 AM",
                                                             "9 AM", "10 AM", "11 AM", "12 PM",
                                                             "1 PM", "2 PM", "3 PM", "4 PM",
                                                             "5 PM", "6 PM", "7 PM", "8 PM",
                                                             "9 PM", "10 PM", "11 PM", "12 AM"],
                                      command=self.fromComboBox_callback,
                                      width = 80)
        fromComboBox.set("1 AM")
        fromComboBox.pack(side="left", padx=5)

        toLabel = CTkLabel(newRowFrame, text="To", font=('Montserrat', 15), text_color="#FFFFFF", anchor="w")
        toLabel.pack(side="left", padx=5)

        toComboBox = CTkComboBox(newRowFrame, values=["1 AM", "2 AM", "3 AM", "4 AM",
                                                           "5 AM", "6 AM", "7 AM", "8 AM",
                                                           "9 AM", "10 AM", "11 AM", "12 PM",
                                                           "1 PM", "2 PM", "3 PM", "4 PM",
                                                           "5 PM", "6 PM", "7 PM", "8 PM",
                                                           "9 PM", "10 PM", "11 PM", "12 AM"],
                                    command=self.toComboBox_callback,
                                    width = 80)
        toComboBox.set("1 AM")
        toComboBox.pack(side="left", padx=5)

        everyLabel = CTkLabel(newRowFrame, text="Every", font=('Montserrat', 15), text_color="#FFFFFF", anchor="w")
        everyLabel.pack(side="left", padx=5)

        everyComboBox = CTkComboBox(newRowFrame,
                                       values=["Mondays", "Tuesdays", "Wednesdays", "Thursdays", "Fridays",
                                               "Saturdays", "Sundays"],
                                       command=self.toComboBox_callback,
                                       width = 100)
        everyComboBox.set("Mondays")
        everyComboBox.pack(side="left", padx=5)

        addButton = CTkButton(newRowFrame,
                                text = "",
                                command=lambda: self.add_row(),
                                image=addPhoto,
                                width=10,
                                height=10,
                                fg_color="#1B2431",
                                bg_color="#1B2431",
                                corner_radius=150)
        addButton.pack(side="left", padx=5)

    def passwordChangeSaveButton_callback(self):
        print("Save Button Pressed")
    
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg = "#090E18")
        
        # Style definition. Can be utilized with the Change Theme from Light to Dark
        style = ttk.Style()
        style.theme_use('forest-dark')
        
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
        
        mainFrameLeft = tk.Frame(mainFrame, bg = "#090E18")
        mainFrameRight = tk.Frame(mainFrame, bg = "#090E18")
        
        mainFrameLeft.pack(expand = True, fill = "both", side = "left")
        mainFrameRight.pack(expand = True, fill = "both", side = "left")

        # Left side of the panel
        addScheduleFrame = CTkScrollableFrame(mainFrameLeft, bg_color = "#1B2431",
                                              label_text = "Active Hours", label_font = ('Montserrat', 15),
                                              label_text_color = "#FFFFFF",
                                              label_anchor = "w",
                                              label_fg_color = "#1B2431",
                                              fg_color = "#1b2431",
                                              width = 500)
        addScheduleFrame.pack(expand = True, fill = "both", side = "top", padx = 10)

        lineSeparator = tk.Frame(addScheduleFrame, height = 2, bg = "#FFFFFF")
        lineSeparator.pack(fill = "x", side = "top", pady = 5)

        self.scheduleLineFrame = tk.Frame(addScheduleFrame, bg = "#1B2431")
        self.scheduleLineFrame.pack(fill = "x", side = "top", padx = 5)
    
        self.add_row()
        
        reservedFrame = tk.Frame(mainFrameLeft, bg = "#090E18") # This is just a styling frame, unused, and can be used in the future.
        reservedFrame.pack(expand = True, fill = "both", side = "top")
        # End of Left Side of the Panel

        # Right Side of the Panel
        # Detectable Vehicles Frame
        detectableVehiclesFrame = tk.Frame(mainFrameRight, bg = "#1B2431")
        detectableVehiclesFrame.pack(expand = True, fill = "both", side = "top", padx = 10)
        
        detectableVehiclesLabel = CTkLabel(detectableVehiclesFrame, text = "Detectable Vehicles Type", text_color = "#FFFFFF", font = ('Montserrat', 15), anchor = "w")
        detectableVehiclesLabel.pack(fill = "x", padx = 5)
        
        lineSeparator = tk.Frame(detectableVehiclesFrame, height = 2, bg = "#FFFFFF")
        lineSeparator.pack(fill = "x", side = "top", pady = 5)
        
        VehiclesFrame = tk.Frame(detectableVehiclesFrame, bg = "#1B2431")
        VehiclesFrame.pack(fill = "both", padx = 10, side = "top", expand = True)
        
        VehiclesFrameFirstRow = tk.Frame(VehiclesFrame, bg = "#1B2431")
        VehiclesFrameSecondRow = tk.Frame(VehiclesFrame, bg = "#1B2431")
        VehiclesFrameFirstRow.pack(side = "top", fill = "both", expand = True)
        VehiclesFrameSecondRow.pack(side = "top", fill = "both", expand = True)
        
        carFrame = tk.Frame(VehiclesFrameFirstRow, bg = "#1B2431")
        truckFrame = tk.Frame(VehiclesFrameFirstRow, bg = "#1B2431")
        jeepneyFrame = tk.Frame(VehiclesFrameFirstRow, bg = "#1B2431")
        busFrame = tk.Frame(VehiclesFrameSecondRow, bg = "#1B2431")
        motorcycleFrame = tk.Frame(VehiclesFrameSecondRow, bg = "#1B2431")
        
        carFrame.pack(side = "left", padx = 10, expand = True, fill = "x")
        truckFrame.pack(side = "left", padx = 20, expand = True, fill = "x")
        jeepneyFrame.pack(side = "left", padx = 10, expand = True, fill = "x")
        busFrame.pack(side = "left", padx = 10, expand = True)
        motorcycleFrame.pack(side = "left", padx = 20, expand = True)
        
        
        self.carVar = IntVar(value = 1)
        carTrueRadioButton = CTkRadioButton(carFrame, variable = self.carVar, value = 1, text = "Enable", font = ('Monteserrat', 13), text_color = "#FFFFFF")
        carFalseRadioButton = CTkRadioButton(carFrame, variable = self.carVar, value = 0, text = "Disable", font = ('Monteserrat', 13), text_color = "#FFFFFF")
        carRadioLabel = CTkLabel(carFrame, text = "Car", font = ('Monteserrat', 13, "bold"), text_color = "#FFFFFF")
        carRadioLabel.pack(side = "top", padx = 20, pady = 5, expand = True, fill = "x")
        carTrueRadioButton.pack(side = "left", padx = 10, pady = 5, expand = True, fill = "x")
        carFalseRadioButton.pack(side = "right", padx = 10, pady = 5, expand = True, fill = "x")
        
        self.truckVar = IntVar(value = 1)
        truckTrueRadioButton = CTkRadioButton(truckFrame, variable = self.truckVar, value = 1, text = "Enable", font = ('Monteserrat', 13), text_color = "#FFFFFF")
        truckFalseRadioButton = CTkRadioButton(truckFrame, variable = self.truckVar, value = 0, text = "Disable", font = ('Monteserrat', 13), text_color = "#FFFFFF")
        truckRadioLabel = CTkLabel(truckFrame, text = "Truck", font = ('Monteserrat', 13, "bold"), text_color = "#FFFFFF")
        truckRadioLabel.pack(side = "top", padx = 10, pady = 5)
        truckTrueRadioButton.pack(side = "left", padx = 10, pady = 5)
        truckFalseRadioButton.pack(side = "right", padx = 10, pady = 5)
        
        
        self.jeepneyVar = IntVar(value = 1)
        jeepneyTrueRadioButton = CTkRadioButton(jeepneyFrame, variable = self.jeepneyVar, value = 1, text = "Enable", font = ('Monteserrat', 13), text_color = "#FFFFFF")
        jeepneyFalseRadioButton = CTkRadioButton(jeepneyFrame, variable = self.jeepneyVar, value = 0, text = "Disable", font = ('Monteserrat', 13), text_color = "#FFFFFF")
        jeepneyRadioLabel = CTkLabel(jeepneyFrame, text = "Jeepney", font = ('Monteserrat', 13, "bold"), text_color = "#FFFFFF")
        jeepneyRadioLabel.pack(side = "top", padx = 10, pady = 5)
        jeepneyTrueRadioButton.pack(side = "left", padx = 10, pady = 5)
        jeepneyFalseRadioButton.pack(side = "right", padx = 10, pady = 5)
        
        self.busVar = IntVar(value = 1)
        busTrueRadioButton = CTkRadioButton(busFrame, variable = self.busVar, value = 1, text = "Enable", font = ('Monteserrat', 13), text_color = "#FFFFFF")
        busFalseRadioButton = CTkRadioButton(busFrame, variable = self.busVar, value = 0, text = "Disable", font = ('Monteserrat', 13), text_color = "#FFFFFF")
        busRadioLabel = CTkLabel(busFrame, text = "Bus", font = ('Monteserrat', 13, "bold"), text_color = "#FFFFFF")
        busRadioLabel.pack(side = "top", padx = 10, pady = 5)
        busTrueRadioButton.pack(side = "left", padx = 10, pady = 5)
        busFalseRadioButton.pack(side = "right", padx = 10, pady = 5)
        
        self.motorVar = IntVar(value = 1)
        motorTrueRadioButton = CTkRadioButton(motorcycleFrame, variable = self.motorVar, value = 1, text = "Enable", font = ('Monteserrat', 13), text_color = "#FFFFFF")
        motorFalseRadioButton = CTkRadioButton(motorcycleFrame, variable = self.motorVar, value = 0, text = "Disable", font = ('Monteserrat', 13), text_color = "#FFFFFF")
        motorRadioLabel = CTkLabel(motorcycleFrame, text = "Motorcycle", font = ('Monteserrat', 13, "bold"), text_color = "#FFFFFF")
        motorRadioLabel.pack(side = "top", padx = 10, pady = 5)
        motorTrueRadioButton.pack(side = "left", padx = 10, pady = 5)
        motorFalseRadioButton.pack(side = "right", padx = 10, pady = 5)
        # End of Detectable Vehicles Frame
        
        # Conggestion Price Frame
        congestionPricingFrame = tk.Frame(mainFrameRight, bg = "#1B2431")
        congestionPricingFrame.pack(expand = True, fill = "both", side = "top", padx = 10, pady = (20, 0))
        
        congestionPricingLabel = CTkLabel(congestionPricingFrame, text = "Congestion Price", text_color = "#FFFFFF", font = ('Montserrat', 15), anchor = "w")
        congestionPricingLabel.pack(fill = "x", padx = 5, side = "top")
        
        lineSeparator = tk.Frame(congestionPricingFrame, height = 2, bg = "#FFFFFF")
        lineSeparator.pack(fill = "x", side = "top", pady = 5)
        
        allVehiclesFrame = tk.Frame(congestionPricingFrame, bg = "#1B2431")
        allVehiclesFrame.pack(fill = 'both', padx = 5, side = "top", expand = True)
        
        allvehiclesFirstRowFrame = tk.Frame(allVehiclesFrame, bg = "#1B2431")
        allvehiclesSecondRowFrame = tk.Frame(allVehiclesFrame, bg = "#1B2431")
        allvehiclesFirstRowFrame.pack(side = "top", expand = True, fill = "both")
        allvehiclesSecondRowFrame.pack(side = "top", expand = True, fill = "both")
        
        carFrame = tk.Frame(allvehiclesFirstRowFrame, bg = "#1B2431")
        truckFrame = tk.Frame(allvehiclesFirstRowFrame, bg = "#1B2431")
        jeepneyFrame = tk.Frame(allvehiclesFirstRowFrame, bg = "#1B2431")
        busFrame = tk.Frame(allvehiclesSecondRowFrame, bg = "#1B2431")
        motorcycleFrame = tk.Frame(allvehiclesSecondRowFrame, bg = "#1B2431")
        
        carFrame.pack(side = "left", padx = 20)
        truckFrame.pack(side = "left", padx = 20)
        jeepneyFrame.pack(side = "left", padx = 20)
        busFrame.pack(side = "left", padx = 20)
        motorcycleFrame.pack(side = "left", padx = 20)
        
        carEntry = CTkEntry(carFrame, corner_radius = 20,
                            border_color = "#FFFFFF",
                            fg_color = "#FFFFFF",
                            text_color = "#000000")
        truckEntry = CTkEntry(truckFrame,
                            corner_radius = 20,
                            border_color = "#FFFFFF",
                            fg_color = "#FFFFFF",
                            text_color = "#000000")
        jeepneyEntry = CTkEntry(jeepneyFrame,
                            corner_radius = 20,
                            border_color = "#FFFFFF",
                            fg_color = "#FFFFFF",
                            text_color = "#000000")
        busEntry = CTkEntry(busFrame,
                            corner_radius = 20,
                            border_color = "#FFFFFF",
                            fg_color = "#FFFFFF",
                            text_color = "#000000")
        motorcycleEntry = CTkEntry(motorcycleFrame,
                                    corner_radius = 20,
                                    border_color = "#FFFFFF",
                                    fg_color = "#FFFFFF",
                                    text_color = "#000000")
        
        carEntry.pack(side = "left", padx = 10)
        truckEntry.pack(side = "left", padx = 10)
        jeepneyEntry.pack(side = "left", padx = 10)
        busEntry.pack(side = "left", padx = 10)
        motorcycleEntry.pack(side = "left", padx = 10)
        
        carlabel = CTkLabel(carFrame,
                            text = "Car",
                            text_color = "#FFFFFF",
                            font = ('Montserrat', 15))
        truckLabel = CTkLabel(truckFrame,
                              text = "Truck",
                              text_color = "#FFFFFF",
                              font = ('Montserrat', 15))
        jeepneyLabel = CTkLabel(jeepneyFrame,
                                text = "Jeepney",
                                text_color = "#FFFFFF",
                                font = ('Montserrat', 15))
        busLabel = CTkLabel(busFrame,
                            text = "Bus",
                            text_color = "#FFFFFF",
                            font = ('Montserrat', 15))
        motorcycleLabel = CTkLabel(motorcycleFrame,
                                    text = "Motorcycle",
                                    text_color = "#FFFFFF",
                                    font = ('Montserrat', 15))
        
        carlabel.pack(side = "left")
        truckLabel.pack(side = "left")
        jeepneyLabel.pack(side = "left")
        busLabel.pack(side = "left")
        motorcycleLabel.pack(side = "left")
        # End of Congestion Price Frame
        
        # Change Theme Frame
        changeThemeFrame = tk.Frame(mainFrameRight, bg = "#1B2431")
        changeThemeFrame.pack(fill = "both", side = "top", padx = 10, pady = (20, 20))
        
        changeThemeLabel = CTkLabel(changeThemeFrame, text = "Change Theme", text_color = "#FFFFFF", font = ('Montserrat', 15), anchor = "w")
        changeThemeLabel.pack(fill = "x", padx = 5)
        
        lineSeparator = tk.Frame(changeThemeFrame, height = 2, bg = "#FFFFFF")
        lineSeparator.pack(fill = "x", side = "top", pady = 5)
        
        changeThemeForm = tk.Frame(changeThemeFrame, bg = "#1B2431")
        changeThemeForm.pack(fill = "both", side = "top", pady = 5, expand = True, padx = 20)
        
        self.themeVar = IntVar(value = 2)
        lightRadioButton = CTkRadioButton(changeThemeForm,
                                            text = "Light",
                                            text_color = "#FFFFFF",
                                            value = 1,
                                            variable = self.themeVar,
                                            command = self.themeRadioButton_callback,
                                            font = ('Montserrat', 13),
                                            border_color = "#FFFFFF",
                                            hover_color = "#FFFFFF",
                                            fg_color = "#80FFDB",
                                            border_width_checked = 10,
                                            border_width_unchecked = 2,
                                            width = 4,
                                            height = 4)
        darkRadioButton = CTkRadioButton(changeThemeForm,
                                            text = "Dark",
                                            text_color = "#FFFFFF",
                                            value = 2,
                                            variable = self.themeVar,
                                            command = self.themeRadioButton_callback,
                                            font = ('Montserrat', 13),
                                            border_color = "#FFFFFF",
                                            hover_color = "#FFFFFF",
                                            fg_color = "#80FFDB",
                                            border_width_checked = 10,
                                            border_width_unchecked = 2,
                                            width = 4,
                                            height = 4)
        defaultRadioButton = CTkRadioButton(changeThemeForm,
                                            text = "System Default",
                                            text_color = "#FFFFFF",
                                            value = 3,
                                            variable = self.themeVar,
                                            command = self.themeRadioButton_callback,
                                            font = ('Montserrat', 13),
                                            border_color = "#FFFFFF",
                                            hover_color = "#FFFFFF",
                                            fg_color = "#80FFDB",
                                            border_width_checked = 10,
                                            border_width_unchecked = 2,
                                            width = 4,
                                            height = 4)
        
        lightRadioButton.pack(side = "left", pady = 10)
        darkRadioButton.pack(side = "left", padx = 50, pady = 10)
        defaultRadioButton.pack(side = "left", pady = 10)
        # End of Change Theme Frame
        
        # Change Password Frame
        changePasswordFrame = tk.Frame(mainFrameRight, bg = "#1B2431")
        changePasswordFrame.pack(fill = "both", side = "top", padx = 10)
        
        changePasswordLabel = CTkLabel(changePasswordFrame, text = "Change Password", text_color = "#FFFFFF", font = ('Montserrat', 15), anchor = "w")
        changePasswordLabel.pack(fill = "x", padx = 5)
        
        lineSeparator = tk.Frame(changePasswordFrame, height = 2, bg = "#FFFFFF")
        lineSeparator.pack(fill = "x", side = "top", pady = 5)
        
        changePasswordEntryFrame = tk.Frame(changePasswordFrame, bg = "#1B2431")
        changePasswordEntryFrame.pack(expand = False, fill = "x", padx = 10)
        
        currentPasswordEntry = CTkEntry(changePasswordEntryFrame,
                                            placeholder_text = "Old Password",
                                            text_color = "#252422",
                                            show = "*",
                                            font = ('Montserrat', 15),
                                            width = 200,
                                            fg_color = "#FFFFFF",
                                            corner_radius = 15,
                                            border_color = "#FFFFFF")
        
        newPasswordEntry = CTkEntry(changePasswordEntryFrame,
                                            placeholder_text = "New Password",
                                            text_color = "#252422",
                                            show = "*",
                                            font = ('Montserrat', 15),
                                            width = 200,
                                            fg_color = "#FFFFFF",
                                            corner_radius = 15,
                                            border_color = "#FFFFFF")
        
        confirmPasswordEntry = CTkEntry(changePasswordEntryFrame,
                                            placeholder_text = "Confirm Password",
                                            text_color = "#252422",
                                            show = "*",
                                            font = ('Montserrat', 15),
                                            width = 200,
                                            fg_color = "#FFFFFF",
                                            corner_radius = 15,
                                            border_color = "#FFFFFF")
        
        confirmButton = CTkButton(changePasswordEntryFrame,
                                            text = "Save",
                                            text_color = "#000000",
                                            font = ('Montserrat', 15),
                                            fg_color = "#48BFE3",
                                            corner_radius = 15,
                                            command = self.passwordChangeSaveButton_callback,
                                            border_color = "#48BFE3",
                                            border_width = 2)

        confirmButton.bind("<Enter>", lambda event: confirmButton.configure(text_color="#48BFE3", fg_color = "#1B2431", border_color = "#48BFE3")) 
        confirmButton.bind("<Leave>", lambda event: confirmButton.configure(text_color="#1B2431", fg_color = "#48BFE3", border_color = "#48BFE3"))  
        
        currentPasswordEntry.pack(padx = (10, 40), pady = 10, side = "left")
        newPasswordEntry.pack(padx = 10, pady = 10, side = "left")
        confirmPasswordEntry.pack(padx = 10, pady = 10, side = "left")
        confirmButton.pack(padx = 10, pady = 10, side = "right")
        # End of Change Password Frame
        # End of Right Side of the Panel
        
        # Bottom Frame for navigation buttons
        bottomFrame = tk.Frame(self, bg = "#090E18")
        bottomFrame.pack(fill = "both", side = "top", padx = 20, pady = 20)
        
        # Apply Button, function placeholder is print. For the assignee, update the "command"
        applyButton = CTkButton(bottomFrame,
                                    text = 'Apply Now', 
                                    command = self.applyButton_callback,
                                    font = ('Montserrat', 15, "bold"),
                                    border_width = 2,
                                    corner_radius = 15,
                                    border_color = '#5E60CE',
                                    text_color = '#090E18',
                                    fg_color = '#5E60CE',
                                    height = 30,
                                    width = 130)
        
        applyButton.bind("<Enter>", lambda event: applyButton.configure(text_color="#5E60CE", fg_color = "#090E18")) 
        applyButton.bind("<Leave>", lambda event: applyButton.configure(text_color="#090E18", fg_color = "#5E60CE")) 
        
        # Scheduled Apply Buttom, function placeholder is print. For the assignee, update the "command"
        scheduledApplyButton = CTkButton(bottomFrame,
                                text = 'Scheduled Apply',
                                command = self.scheduleApplyButton_callback, 
                                font = ('Montserrat', 12),
                                border_width = 2,
                                corner_radius = 15,
                                border_color = '#5E60CE',
                                text_color = '#5E60CE',
                                fg_color = '#090E18',
                                height = 30,
                                width = 140)
        
        scheduledApplyButton.bind("<Enter>", lambda event: scheduledApplyButton.configure(text_color="#090E18", fg_color = "#5E60CE")) 
        scheduledApplyButton.bind("<Leave>", lambda event: scheduledApplyButton.configure(text_color="#5E60CE", fg_color = "#090E18")) 

        # Navigate back to Dashboard
        dashboardButton = CTkButton(bottomFrame,
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

        # Logout of the account. For the Assignee, make sure to dispose necessary information before logging out.
        logoutButton = CTkButton(bottomFrame,
                                text = 'Logout',
                                command = lambda: parent.show_frame(parent.loginFrame), 
                                font = ('Montserrat', 15, "bold"),
                                border_width = 2,
                                corner_radius = 15,
                                border_color = '#C1121F',
                                text_color = '#090E18',
                                fg_color = '#C1121F',
                                height = 30,
                                width = 100)

        logoutButton.bind("<Enter>", lambda event: logoutButton.configure(text_color="#C1121F", fg_color = "#090E18")) 
        logoutButton.bind("<Leave>", lambda event: logoutButton.configure(text_color="#090E18", fg_color = "#C1121F")) 
        
        applyButton.pack(side = 'right', padx = 10, pady = 10)
        scheduledApplyButton.pack(side = 'right', padx = 10, pady = 10)
        dashboardButton.pack(side = 'right', padx = 10, pady = 10)
        logoutButton.pack(side = 'right', padx = 10, pady = 10)
        # End of Bottom Frame for navigation Buttons