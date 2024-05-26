import os
import sys
import tkinter as tk
from customtkinter import *
from tkinter import ttk
from PIL import Image
from tkcalendar import Calendar

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

class ConfigPage(tk.Frame):
    # Close Application
    def closeApplication(self):
        self.master.destroy()
    
    # Minimize or Iconify the Application
    def minimizeApplicaiton(self):
        self.master.iconify()
    
    # Function that handles the logic for the FROM input.
    def fromComboBox_callback(self, choice):
        print("From Combobox callback: ", choice)

    # Function that handles the logic for the TO input.
    def toComboBox_callback(self, choice):
        print("From Combobox callback: ", choice)
    
    # Function that handles the changing of theme
    def themeRadioButton_callback(self):
        print("Radio Button Theme callback: ", self.themeVar.get())
        
    # Function that applies the settings currently set to.
    def applyButton_callback(self):
        print("Apply Button Pressed")
    
    # Function that applies the settings currently set to with delay
    def scheduleApplyButton_callback(self):
        print("Schedule Apply Button Pressed")
        
    def selectDateTime(self):
        top = tk.Toplevel(bg="#090E18")
        top.title("Select Date/Time")

        # Calendar for date selection
        calendarFrame = tk.Frame(top, bg="#1B2431")
        calendarFrame.pack(padx=10, pady=(10, 2), ipadx=5, ipady=5, expand=True, fill="both")
        cal = Calendar(calendarFrame, selectmode='day', date_pattern='dd/mm/y', foreground="#FFFFFF", background="#1B2431", bordercolor="#1B2431")
        cal.pack(padx=5, pady=5)

        # Frame for time selection
        frame_time = tk.Frame(top, bg="#1B2431")
        frame_time.pack(padx=10, pady=(2, 10), expand=True, fill="x")

        # Spinbox for hours selection
        label_hours = tk.Label(frame_time, text="Hours:", foreground="#FFFFFF", background="#090E18")
        label_hours.grid(row=0, column=0, padx=5, pady=5, sticky = "w")
        spinbox_hours = ttk.Spinbox(frame_time, from_=0, to=23, foreground="#FFFFFF", background="#FFFFFF")
        spinbox_hours.grid(row=0, column=1, padx=5, pady=5, sticky = "ew")

        def getSelectedDateTime():
            global selected_date, selected_hour_from, selected_hour_to, selected_time
            
            self.selected_date = cal.get_date()
            selected_hour = spinbox_hours.get()
            self.selected_time = f"{selected_hour}:00"

            top.destroy()
            #self.selectedDateTimeLabel.configure(text = f"Selected: {self.selected_date} at {self.selected_hour_from} - {self.selected_hour_to}")
            self.dateSelectedEntry.delete(0, END)
            self.dateSelectedEntry.insert(0, f"{self.selected_date}")
            self.timeSelectedEntry.delete(0, END)
            self.timeSelectedEntry.insert(0, f"{self.selected_time}")
            #self.dateSelectedEntry.configure(text = f"{self.selected_date}")
            #self.timeSelectedEntry.configure(text = f"{self.selected_time}")
            

        # Button for confirming selection
        button_confirm = tk.Button(top, text="Confirm", command=getSelectedDateTime, foreground="#FFFFFF", background="#090E18")
        button_confirm.pack(pady=10)
        
    # Function that add rows to the Schedule of the Algorithm
    def add_row(self):
        addImage = Image.open("views/icons/icons_add.png")
        addImage = addImage.resize((25, 25))
        addPhoto = CTkImage(addImage)
        
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

    # Saves the Password Changes
    def passwordChangeSaveButton_callback(self):
        print("Save Button Pressed")
        # Note that you should first verify if the current password matches the saved password of the user.
        # This function is excempted from the Scheduled Apply and Apply Buttons.
        # This Change Password should be realtime updated, and not affected by the said buttons.
    
    def addButton_callback(self):
        pass
    
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

        # Main Frame (Where the contents of the main page is)
        # mainFrame = tk.Frame(self, bg = "#090E18")
        
        mainFrame = CTkFrame(self, bg_color = "#090E18")
        mainFrame.pack(expand = True, fill = "both", side = "top")
        
        # Again, separates the page into two Frame (Left and Right)
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
        VehiclesFrameThirdRow = tk.Frame(VehiclesFrame, bg = "#1B2431")
        VehiclesFrameFirstRow.pack(side = "top", fill = "both", expand = True)
        VehiclesFrameSecondRow.pack(side = "top", fill = "both", expand = True)
        VehiclesFrameThirdRow.pack(side = "top", fill = "both", expand = True)
        
        carFrame = tk.Frame(VehiclesFrameFirstRow, bg = "#1B2431", highlightthickness = 2, highlightbackground = "#FFFFFF")
        truckFrame = tk.Frame(VehiclesFrameFirstRow, bg = "#1B2431", highlightthickness = 2, highlightbackground = "#FFFFFF")
        jeepneyFrame = tk.Frame(VehiclesFrameFirstRow, bg = "#1B2431", highlightthickness = 2, highlightbackground = "#FFFFFF")
        
        busFrame = tk.Frame(VehiclesFrameSecondRow, bg = "#1B2431", highlightthickness = 2, highlightbackground = "#FFFFFF")
        motorcycleFrame = tk.Frame(VehiclesFrameSecondRow, bg = "#1B2431", highlightthickness = 2, highlightbackground = "#FFFFFF")
        tricycleFrame = tk.Frame(VehiclesFrameSecondRow, bg = "#1B2431", highlightthickness = 2, highlightbackground = "#FFFFFF")
        
        vanFrame = tk.Frame(VehiclesFrameThirdRow, bg = "#1B2431", highlightthickness = 2, highlightbackground = "#FFFFFF")
        taxiFrame = tk.Frame(VehiclesFrameThirdRow, bg = "#1B2431", highlightthickness = 2, highlightbackground = "#FFFFFF")
        mJeepneyFrame = tk.Frame(VehiclesFrameThirdRow, bg = "#1B2431", highlightthickness = 2, highlightbackground = "#FFFFFF")
        
        carFrame.pack(side = "left", padx = 5, expand = False, fill = "x")
        truckFrame.pack(side = "left", padx = 10, expand = False, fill = "x")
        jeepneyFrame.pack(side = "left", padx = 5, expand = False, fill = "x")
        
        busFrame.pack(side = "left", padx = 5, expand = False, fill = "x")
        motorcycleFrame.pack(side = "left", padx = 10, expand = False, fill = "x")
        tricycleFrame.pack(side = "left", padx = 5, expand = False, fill = "x")
        
        vanFrame.pack(side = "left", padx = 5, expand = False, fill = "x")
        taxiFrame.pack(side = "left", padx = 10, expand = False, fill = "x")
        mJeepneyFrame.pack(side = "left", padx = 5, expand = False, fill = "x")
        
        # -- First Row --
        self.carVar = IntVar(value = 1)
        carTrueRadioButton = CTkRadioButton(carFrame, variable = self.carVar, value = 1, text = "Enable", font = ('Monteserrat', 13), text_color = "#FFFFFF")
        carFalseRadioButton = CTkRadioButton(carFrame, variable = self.carVar, value = 0, text = "Disable", font = ('Monteserrat', 13), text_color = "#FFFFFF")
        carRadioLabel = CTkLabel(carFrame, text = "Car", font = ('Monteserrat', 13, "bold"), text_color = "#FFFFFF")
        carRadioLabel.pack(side = "top", padx = 10, pady = 5, fill = "x")
        carTrueRadioButton.pack(side = "left", padx = (30,5), pady = 5, fill = "x")
        carFalseRadioButton.pack(side = "right", padx = (5,0), pady = 5, fill = "x")
        
        self.truckVar = IntVar(value = 1)
        truckTrueRadioButton = CTkRadioButton(truckFrame, variable = self.truckVar, value = 1, text = "Enable", font = ('Monteserrat', 13), text_color = "#FFFFFF")
        truckFalseRadioButton = CTkRadioButton(truckFrame, variable = self.truckVar, value = 0, text = "Disable", font = ('Monteserrat', 13), text_color = "#FFFFFF")
        truckRadioLabel = CTkLabel(truckFrame, text = "Truck", font = ('Monteserrat', 13, "bold"), text_color = "#FFFFFF")
        truckRadioLabel.pack(side = "top", padx = 10, pady = 5, fill = "x")
        truckTrueRadioButton.pack(side = "left", padx = (30,5), pady = 5, fill = "x")
        truckFalseRadioButton.pack(side = "right", padx = (5,0), pady = 5, fill = "x")
        
        self.jeepneyVar = IntVar(value = 1)
        jeepneyTrueRadioButton = CTkRadioButton(jeepneyFrame, variable = self.jeepneyVar, value = 1, text = "Enable", font = ('Monteserrat', 13), text_color = "#FFFFFF")
        jeepneyFalseRadioButton = CTkRadioButton(jeepneyFrame, variable = self.jeepneyVar, value = 0, text = "Disable", font = ('Monteserrat', 13), text_color = "#FFFFFF")
        jeepneyRadioLabel = CTkLabel(jeepneyFrame, text = "Jeepney", font = ('Monteserrat', 13, "bold"), text_color = "#FFFFFF")
        jeepneyRadioLabel.pack(side = "top", padx = 10, pady = 5, fill = "x")
        jeepneyTrueRadioButton.pack(side = "left", padx = (30,5), pady = 5, fill = "x")
        jeepneyFalseRadioButton.pack(side = "right", padx = (5,0), pady = 5, fill = "x")
        
        # -- Second Row --
        self.busVar = IntVar(value = 1)
        busTrueRadioButton = CTkRadioButton(busFrame, variable = self.busVar, value = 1, text = "Enable", font = ('Monteserrat', 13), text_color = "#FFFFFF")
        busFalseRadioButton = CTkRadioButton(busFrame, variable = self.busVar, value = 0, text = "Disable", font = ('Monteserrat', 13), text_color = "#FFFFFF")
        busRadioLabel = CTkLabel(busFrame, text = "Bus", font = ('Monteserrat', 13, "bold"), text_color = "#FFFFFF")
        busRadioLabel.pack(side = "top", padx = 10, pady = 5, fill = "x")
        busTrueRadioButton.pack(side = "left", padx = (30,5), pady = 5, fill = "x")
        busFalseRadioButton.pack(side = "right", padx = (5,0), pady = 5, fill = "x")
        
        self.motorVar = IntVar(value = 1)
        motorTrueRadioButton = CTkRadioButton(motorcycleFrame, variable = self.motorVar, value = 1, text = "Enable", font = ('Monteserrat', 13), text_color = "#FFFFFF")
        motorFalseRadioButton = CTkRadioButton(motorcycleFrame, variable = self.motorVar, value = 0, text = "Disable", font = ('Monteserrat', 13), text_color = "#FFFFFF")
        motorRadioLabel = CTkLabel(motorcycleFrame, text = "Motorcycle", font = ('Monteserrat', 13, "bold"), text_color = "#FFFFFF")
        motorRadioLabel.pack(side = "top", padx = 10, pady = 5, fill = "x")
        motorTrueRadioButton.pack(side = "left", padx = (30,5), pady = 5, fill = "x")
        motorFalseRadioButton.pack(side = "right", padx = (5,0), pady = 5, fill = "x")
        
        self.tricycleVar = IntVar(value = 1)
        tricycleTrueRadioButton = CTkRadioButton(tricycleFrame, variable = self.tricycleVar, value = 1, text = "Enable", font = ('Monteserrat', 13), text_color = "#FFFFFF")
        tricycleFalseRadioButton = CTkRadioButton(tricycleFrame, variable = self.tricycleVar, value = 0, text = "Disable", font = ('Monteserrat', 13), text_color = "#FFFFFF")
        tryclceRadioLabel = CTkLabel(tricycleFrame, text = "Tricycle", font = ('Monteserrat', 13, "bold"), text_color = "#FFFFFF")
        tryclceRadioLabel.pack(side = "top", padx = 10, pady = 5, fill = "x")
        tricycleTrueRadioButton.pack(side = "left", padx = (30,5), pady = 5, fill = "x")
        tricycleFalseRadioButton.pack(side = "right", padx = (5,0), pady = 5, fill = "x")
        
        # -- Third Row -- 
        self.vanVar = IntVar(value = 1)
        vanTrueRadioButton = CTkRadioButton(vanFrame, variable = self.vanVar, value = 1, text = "Enable", font = ('Monteserrat', 13), text_color = "#FFFFFF")
        vanFalseRadioButton = CTkRadioButton(vanFrame, variable = self.vanVar, value = 0, text = "Disable", font = ('Monteserrat', 13), text_color = "#FFFFFF")
        vanRadioLabel = CTkLabel(vanFrame, text = "Van", font = ('Monteserrat', 13, "bold"), text_color = "#FFFFFF")
        vanRadioLabel.pack(side = "top", padx = 10, pady = 5, fill = "x")
        vanTrueRadioButton.pack(side = "left", padx = (30,5), pady = 5, fill = "x")
        vanFalseRadioButton.pack(side = "right", padx = (5,0), pady = 5, fill = "x")
        
        self.taxiVar = IntVar(value = 1)
        taxiTrueRadioButton = CTkRadioButton(taxiFrame, variable = self.taxiVar, value = 1, text = "Enable", font = ('Monteserrat', 13), text_color = "#FFFFFF")
        taxiFalseRadioButton = CTkRadioButton(taxiFrame, variable = self.taxiVar, value = 0, text = "Disable", font = ('Monteserrat', 13), text_color = "#FFFFFF")
        taxiRadioLabel = CTkLabel(taxiFrame, text = "Taxi", font = ('Monteserrat', 13, "bold"), text_color = "#FFFFFF")
        taxiRadioLabel.pack(side = "top", padx = 10, pady = 5, fill = "x")
        taxiTrueRadioButton.pack(side = "left", padx = (30,5), pady = 5, fill = "x")
        taxiFalseRadioButton.pack(side = "right", padx = (5,0), pady = 5, fill = "x")
        
        self.mJeepneyVar = IntVar(value = 1)
        mJeepneyTrueRadioButton = CTkRadioButton(mJeepneyFrame, variable = self.mJeepneyVar, value = 1, text = "Enable", font = ('Monteserrat', 13), text_color = "#FFFFFF")
        mJeepneyFalseRadioButton = CTkRadioButton(mJeepneyFrame, variable = self.mJeepneyVar, value = 0, text = "Disable", font = ('Monteserrat', 13), text_color = "#FFFFFF")
        mJeepneyRadioLabel = CTkLabel(mJeepneyFrame, text = "Modern Jeepney", font = ('Monteserrat', 13, "bold"), text_color = "#FFFFFF")
        mJeepneyRadioLabel.pack(side = "top", padx = 10, pady = 5, fill = "x")
        mJeepneyTrueRadioButton.pack(side = "left", padx = (30,5), pady = 5, fill = "x")
        mJeepneyFalseRadioButton.pack(side = "right", padx = (5,0), pady = 5, fill = "x")
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
        
        # Add new active hours Frame
        addActiveHoursFrame = tk.Frame(mainFrameRight, bg = "#1B2431")
        addActiveHoursFrame.pack(fill = "both", side = "top", padx = 10, pady = (20, 20))
        
        addActiveHoursLabel = CTkLabel(addActiveHoursFrame, text = "Add Active Hours", text_color = "#FFFFFF", font = ('Montserrat', 15), anchor = "w")
        addActiveHoursLabel.pack(fill = "x", padx = 5)
        
        lineSeparator = tk.Frame(addActiveHoursFrame, height = 2, bg = "#FFFFFF")
        lineSeparator.pack(fill = "x", side = "top", pady = 5)
        
        addActiveForm = tk.Frame(addActiveHoursFrame, bg = "#1B2431")
        addActiveForm.pack(fill = "both", side = "top", pady = 5, expand = True, padx = 20)
        
        fromLabel = CTkLabel(addActiveForm, text="From", font=('Montserrat', 15), text_color="#FFFFFF", anchor="w")
        fromLabel.pack(side="left", padx=5)
        
        fromDropDown = CTkComboBox(addActiveForm, values=["1 AM", "2 AM", "3 AM", "4 AM",
                                                             "5 AM", "6 AM", "7 AM", "8 AM",
                                                             "9 AM", "10 AM", "11 AM", "12 PM",
                                                             "1 PM", "2 PM", "3 PM", "4 PM",
                                                             "5 PM", "6 PM", "7 PM", "8 PM",
                                                             "9 PM", "10 PM", "11 PM", "12 AM"],
                                      command=self.fromComboBox_callback,
                                      width = 80)
        fromDropDown.set("1 AM")
        fromDropDown.pack(side="left", padx=5)
        
        toLabel = CTkLabel(addActiveForm, text="To", font=('Montserrat', 15), text_color="#FFFFFF", anchor="w")
        toLabel.pack(side="left", padx=(10, 5))
        
        toDropDown = CTkComboBox(addActiveForm, values=["1 AM", "2 AM", "3 AM", "4 AM",
                                                           "5 AM", "6 AM", "7 AM", "8 AM",
                                                           "9 AM", "10 AM", "11 AM", "12 PM",
                                                           "1 PM", "2 PM", "3 PM", "4 PM",
                                                           "5 PM", "6 PM", "7 PM", "8 PM",
                                                           "9 PM", "10 PM", "11 PM", "12 AM"],
                                    command=self.toComboBox_callback,
                                    width = 80)
        toDropDown.set("1 AM")
        toDropDown.pack(side="left", padx=5)
        
        everyLabel = CTkLabel(addActiveForm, text="Every", font=('Montserrat', 15), text_color="#FFFFFF", anchor="w")
        everyLabel.pack(side="left", padx=(10, 5))
        
        EveryDropDown = CTkComboBox(addActiveForm,
                                       values=["Mondays", "Tuesdays", "Wednesdays", "Thursdays", "Fridays",
                                               "Saturdays", "Sundays"],
                                       command=self.toComboBox_callback,
                                       width = 100)
        EveryDropDown.set("Mondays")
        EveryDropDown.pack(side="left", padx=5)
        
        addButton = CTkButton(addActiveForm,
                                            text = "Add",
                                            text_color = "#000000",
                                            font = ('Montserrat', 15),
                                            fg_color = "#48BFE3",
                                            corner_radius = 15,
                                            command = self.addButton_callback,
                                            border_color = "#48BFE3",
                                            border_width = 2)
        
        addButton.bind("<Enter>", lambda event: addButton.configure(text_color="#48BFE3", fg_color = "#1B2431", border_color = "#48BFE3")) 
        addButton.bind("<Leave>", lambda event: addButton.configure(text_color="#1B2431", fg_color = "#48BFE3", border_color = "#48BFE3"))  
        addButton.pack(padx = 10, pady = 10, side = "right")
        
        self.dateSelectedEntry = CTkEntry(addActiveForm,
                                          placeholder_text = "Date DD/MM/YYYY", 
                                          text_color = "#252422",
                                          font = ('Montserrat', 15),
                                          width = 200,
                                          fg_color = "#FFFFFF",
                                          corner_radius = 15,
                                          border_color = "#FFFFFF"
                                          )
        self.dateSelectedEntry.pack(side="right", padx=(10, 5))
        
        self.timeSelectedEntry = CTkEntry(addActiveForm,
                                          placeholder_text = "Time HH:MM", 
                                          text_color = "#252422",
                                          font = ('Montserrat', 15),
                                          width = 200,
                                          fg_color = "#FFFFFF",
                                          corner_radius = 15,
                                          border_color = "#FFFFFF"
                                          )
        self.timeSelectedEntry.pack(side="right", padx=(10, 5))
        
        startingFromLabel = CTkLabel(addActiveForm, text="Starting From", font=('Montserrat', 15), text_color="#FFFFFF", anchor="w")
        startingFromLabel.pack(side="right", padx=(10, 5))
        
        selectDateTimeButton = CTkButton(addActiveForm,
                                            text = "Select Date-Time",
                                            text_color = "#000000",
                                            font = ('Montserrat', 15),
                                            fg_color = "#48BFE3",
                                            corner_radius = 15,
                                            command = self.selectDateTime,
                                            border_color = "#48BFE3",
                                            border_width = 2)
        
        selectDateTimeButton.bind("<Enter>", lambda event: selectDateTimeButton.configure(text_color="#48BFE3", fg_color = "#1B2431", border_color = "#48BFE3")) 
        selectDateTimeButton.bind("<Leave>", lambda event: selectDateTimeButton.configure(text_color="#1B2431", fg_color = "#48BFE3", border_color = "#48BFE3"))  
        selectDateTimeButton.pack(padx = 10, pady = 10, side = "right")
        # Set Date Settings
        
        '''
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
        '''
        
        # End of new active hours Frame
        
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
        bottomFrame.pack(fill = "x", side = "top", padx = 20, pady = 20)
        
        # Apply Button, function placeholder is print. For the assignee, update the "command"
        # applyButton = CTkButton(bottomFrame,
        #                             text = 'Apply Now', 
        #                             command = self.applyButton_callback,
        #                             font = ('Montserrat', 15, "bold"),
        #                             border_width = 2,
        #                             corner_radius = 15,
        #                             border_color = '#5E60CE',
        #                             text_color = '#090E18',
        #                             fg_color = '#5E60CE',
        #                             height = 30,
        #                             width = 130)
        
        # applyButton.bind("<Enter>", lambda event: applyButton.configure(text_color="#5E60CE", fg_color = "#090E18")) 
        # applyButton.bind("<Leave>", lambda event: applyButton.configure(text_color="#090E18", fg_color = "#5E60CE")) 
        
        # Scheduled Apply Buttom, function placeholder is print. For the assignee, update the "command"
        # scheduledApplyButton = CTkButton(bottomFrame,
        #                         text = 'Scheduled Apply',
        #                         command = self.scheduleApplyButton_callback, 
        #                         font = ('Montserrat', 12),
        #                         border_width = 2,
        #                         corner_radius = 15,
        #                         border_color = '#5E60CE',
        #                         text_color = '#5E60CE',
        #                         fg_color = '#090E18',
        #                         height = 30,
        #                         width = 140)
        
        # scheduledApplyButton.bind("<Enter>", lambda event: scheduledApplyButton.configure(text_color="#090E18", fg_color = "#5E60CE")) 
        # scheduledApplyButton.bind("<Leave>", lambda event: scheduledApplyButton.configure(text_color="#5E60CE", fg_color = "#090E18")) 

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
        
        #applyButton.pack(side = 'right', padx = 10, pady = 10)
        #scheduledApplyButton.pack(side = 'right', padx = 10, pady = 10)
        dashboardButton.pack(side = 'right', padx = 10, pady = 10)
        logoutButton.pack(side = 'right', padx = 10, pady = 10)
        # End of Bottom Frame for navigation Buttons