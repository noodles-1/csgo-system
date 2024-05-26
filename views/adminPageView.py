import os
import sys
import tkinter as tk
from customtkinter import *
from tkinter import ttk
from tkcalendar import Calendar
from PIL import Image
import random
import string
import datetime

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

# These are just samples for the database
licensePlates = []
vehicleTypes = {
    'Car': 50,
    'Taxi': 60,
    'Motorcycle': 30,
    'Bus': 100,
    'Tricycle': 40,
    'Jeepney': 70,
    'Modern Jeepney': 80,
    'Van': 90,
    'Truck': 120
}
cameraID = ['Camera 1', 'Camera 2', 'Camera 3', 'Camera 4']
dates = []
times = []
data = []

def generate_license_plate():
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    digits = ''.join(random.choices(string.digits, k=4))
    license_plate = letters + digits
    return license_plate

def generate_random_past_date():
    today = datetime.date.today()
    random_days = random.randint(1, 365)
    random_date = today - datetime.timedelta(days=random_days)
    return random_date

def generate_random_time():
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)
    return f"{random_hour:02d}:{random_minute:02d}"

# Generate 100 Data Entries
for _ in range(100):
    license_plate = generate_license_plate()
    vehicle_type = random.choice(list(vehicleTypes.keys()))
    camera_id = random.choice(cameraID)
    random_date = generate_random_past_date()
    random_time = generate_random_time()
    price = vehicleTypes[vehicle_type]

    data.append((license_plate, vehicle_type, camera_id, random_time, random_date.strftime("%Y-%m-%d"), price))
# -------

class AdminPage(tk.Frame):
    # Close Application
    def closeApplication(self):
        self.master.destroy()

    # Minimize or Iconify the Application
    def minimizeApplicaiton(self):
        self.master.iconify()
    
    # Select User Dropwdown Function
    def selectUserCombo_callback(self, choice):
        # Insert Logic Here
        print("Select User Combo Value: ", choice)
    
    # Add the new user button
    def addUserButton_callback(self):
        print("Add User Button Pressed")
    
    # Clear the field button
    def clearFieldButton_callback(self):
        print("Clear Field Button Pressed")
        self.firstNameEntry.delete(0, "end")
        self.lastNameEntry.delete(0, "end")
        self.emailEntry.delete(0, "end")
        self.passwordEntry.delete(0, "end")
        self.usernameEntry.delete(0, "end")
        self.selectUserComboVar.set("")
    
    # Delete the user once selected
    def deleteUserButton_callback(self):
        # Retrieve the selected user from the dropdown
        selected_user = self.selectUserComboVar.get()

        # Check if a user is selected
        if selected_user:
            # Remove the selected user from the Combobox values
            current_values = list(self.selectUserCombo._values)
            current_values.remove(selected_user)
            
            self.selectUserCombo.configure(values = current_values)
                
            self.selectUserCombo.set('')  # Clear the selection
            self.clearFieldButton_callback()
            print("Deleted User:", selected_user)
        else:
            # If no user is selected, print a message or handle the situation accordingly
            print("No user selected for deletion.")
            
    def vehicleTypeCombo_callback(self, choice):
        print("Filter By: ", choice)
    
    # Apply changes to the field
    def applyUserButton_callback(self):
        pass
    
    # Apply admin restriction to user
    def adminRadioButton_callback(self):
        pass
    
    # Apply change price restriction to user
    def changePriceRadioButton_callback(self):
        pass
    
    # Apply change active hours restriction to user
    def changeActiveHoursRadioButton_callback(self):
        pass
    
    # Apply change detectable vehicles restriction to user
    def changeDetectableRadioButton_callback(self):
        pass
    
    # Apply download csv restriction to user
    def downloadCSVRadioButton_callback(self):
        pass
    
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
            global selected_date, selected_hour_from, selected_hour_to
            
            self.selected_date = cal.get_date()
            selected_hour = spinbox_hours.get()
            self.selected_hour_from = f"{selected_hour}:00"
            self.selected_hour_to = f"{selected_hour}:59"
            
            #tk.messagebox.showinfo("Selected Date/Time", f"Date: {self.selected_date}\nTime: {self.selected_hour_from} - {self.selected_hour_to}")
            top.destroy()
            self.selectedDateTimeLabel.configure(text = f"Selected: {self.selected_date} at {self.selected_hour_from} - {self.selected_hour_to}")
            

        # Button for confirming selection
        button_confirm = tk.Button(top, text="Confirm", command=getSelectedDateTime, foreground="#FFFFFF", background="#090E18")
        button_confirm.pack(pady=10)
        
    def clearFilter_callback(self):
        self.selected_date = ""
        self.selected_hour_from = ""
        self.selected_hour_to = ""
        self.vehicleTypeComboBox.set("")
        self.selectedDateTimeLabel.configure(text = "Select Date-Time")
        
    def goFilter_callback(self):
        pass
    
    def insertDataToTable(self, inputLicensePlate, inputVehicleType, inputCameraID, inputTime, inputDate, inputPrice):
        self.databaseTable.insert(parent = '', index = 0, values = (inputLicensePlate, inputVehicleType, inputCameraID, inputTime, inputDate, inputPrice))
        print(f'Inserted {inputLicensePlate}, {inputVehicleType}, {inputCameraID}, {inputTime}, {inputDate}, {inputPrice}')
    
    def deleteDataFromTable(self, _):
        if tk.messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected items?"):
            for i in self.databaseTable.selection():
                self.databaseTable.delete(i)
    
    def selectDataFromTable(self, _):
        selected_items = self.databaseTable.selection()
        
        if not selected_items:
            self.licensePlateEntry.delete(0, tk.END)
            self.vehicleTypeEntry.delete(0, tk.END)
            self.priceEntry.delete(0, tk.END)
            return
        
        if len(selected_items) != 1:
            self.licensePlateEntry.delete(0, tk.END)
            self.vehicleTypeEntry.delete(0, tk.END)
            self.priceEntry.delete(0, tk.END)
            return
        
        self.licensePlateEntry.delete(0, tk.END)
        self.vehicleTypeEntry.delete(0, tk.END)
        self.priceEntry.delete(0, tk.END)
        
        for item in selected_items:
            values = self.databaseTable.item(item)['values']
            if len(values) >= 6:
                self.licensePlateEntry.insert(0, values[0])
                self.vehicleTypeEntry.insert(0, values[1])
                self.priceEntry.insert(0, values[5])
        
    def discoverCameras_callback(self):
        # This function discovers cameras from the system using ONVIF or SSDP
        # Calls self.discoveredCamerasDrop.configure to config the values of the dropdown
        '''
            Sample for this code:
                self.discoveredCamerasDrop.configure(values = [str1, str2 , str3...])
        '''
        pass
    
    def addCamera_callback(self):
        # This function gets the Assign ID Entry and the current value of the discoveredCamerasDrop
        '''
            Sample for this code:
                self.assignID.get()
                self.discoveredCamerasDrop.get()
        '''
        pass
    
    def deleteSavedCamera_callback(self):
        self.savedCameraID.configure(text = "")
        # This function retrieves the values of savedCameraId and savedCamerasDrop and deletes them from the saved cameras.
        # Then configs the drop down with the updated list of the saved cameras
        print("Delete Saved Camera Button Pressed")
    
    def updateSavedCamera_callback(self):
        print("Update Saved Camera Button Pressed")
        print("Saved Camera ID: ", self.savedCameraID.get())
        print("Saved Camera Drop Item: ",self.savedCamerasDrop.get())
        
    def updateTable_callback(self):
        inputLicensePlate = self.licensePlateEntry.get()
        inputVehicleType = self.vehicleTypeEntry.get()
        inputPrice = self.priceEntry.get()
        
        self.licensePlateEntry.delete(0, tk.END)
        self.vehicleTypeEntry.delete(0, tk.END)
        self.priceEntry.delete(0, tk.END)
        
        '''
            call update row
        '''
        
        
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg = "#090E18")
        
        style = ttk.Style()
        style.theme_use('forest-dark')
        
        self.selected_date = ""
        self.selected_hour_from = ""
        self.selected_hour_to = ""
        
        # Close Icon (Currently Set to darkmode, if possible change to lightmode when the the changes)
        closePhoto = CTkImage(light_image = Image.open("views/icons/icon_close_darkmode.png"),
                              dark_image = Image.open("views/icons/icon_close_darkmode.png"),
                              size = (20, 20))

        # Minimize Icon (Currently Set to darkmode, if possible change to lightmode when the the changes)
        minimizePhoto = CTkImage(light_image = Image.open("views/icons/icon_minimize_darkmode.png"),
                              dark_image = Image.open("views/icons/icon_minimize_darkmode.png"),
                              size = (20, 20))

        # ---- Styles of Widgets ----
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
        # ---- Declaration of Widgets ----
        toolBarFrame = tk.Frame(self, bg = "#090E18",  )
        
        # Close Button
        closeButton = CTkButton(toolBarFrame, 
                                image = closePhoto,
                                text = "",
                                width = 20,
                                height = 20,
                                fg_color = "#090E18",
                                bg_color = "#000000",
                                hover = True,
                                hover_color = "#48BFE3",
                                command = self.closeApplication)


        # Minimize Button
        minimizeButton = CTkButton(toolBarFrame, 
                                image = minimizePhoto,
                                text = "",
                                width = 20,
                                height = 20,
                                fg_color = "#090E18",
                                bg_color = "#000000",
                                hover = True,
                                hover_color = "#48BFE3",
                                command = self.minimizeApplicaiton)
        
        contentFrame = CTkScrollableFrame(self, bg_color = "#090E18", fg_color = "#090E18")
        
        leftContentFrame = tk.Frame(contentFrame, bg = "#090E18")
        # Contents of Left Content Frame
        upperLeftContent = CTkFrame(leftContentFrame, fg_color = "#1B2431", corner_radius = 5)
        addCamerasLabel = CTkLabel(upperLeftContent, text = "Add Camera", font = ('Montserrat', 12, 'bold'), anchor = "w", text_color = "#FFFFFF")
        
        manageCamerasFirstRow = tk.Frame(upperLeftContent, bg = "#1B2431")
        discoverCameraButton = CTkButton(manageCamerasFirstRow, text = "Discover Cameras", font = ('Montserrat', 12, 'bold'), fg_color = "#FFFFFF", text_color = "#000000", corner_radius = 5, command = self.discoverCameras_callback)
        self.discoveredCamerasDrop = CTkComboBox(manageCamerasFirstRow, values = ["Camera 1", "Camera 2", "Camera 3"], font = ('Montserrat', 12), fg_color = "#FFFFFF", dropdown_fg_color = "#FFFFFF", dropdown_text_color = "#000000", border_color = "#FFFFFF", button_color = "#FFFFFF", text_color = "#000000")
        self.assignID = CTkEntry(manageCamerasFirstRow, placeholder_text = "Assign ID", font = ('Montserrat', 12, 'bold'), fg_color = "#FFFFFF", text_color = "#000000", corner_radius = 5)
        self.assignLocation = CTkEntry(manageCamerasFirstRow, placeholder_text = "Assign Location", font = ('Montserrat', 12, 'bold'), fg_color = "#FFFFFF", text_color = "#000000", corner_radius = 5)
        addCameraButton = CTkButton(manageCamerasFirstRow, text = "Add Camera", fg_color = "#FFFFFF", text_color = "#000000", corner_radius = 5, font = ('Montserrat', 12, 'bold'), command = self.addCamera_callback)
        
        manageCamerasLabel = CTkLabel(upperLeftContent, text = "Manage Cameras", font = ('Montserrat', 12, 'bold'), anchor = "w", text_color = "#FFFFFF")
        
        manageCamerasSecondRow = tk.Frame(upperLeftContent, bg = "#1B2431")
        self.savedCamerasDrop = CTkComboBox(manageCamerasSecondRow, values = ["Camera 1", "Camera 2", "Camera 3"], font = ('Montserrat', 12), fg_color = "#FFFFFF", dropdown_fg_color = "#FFFFFF", dropdown_text_color = "#000000", border_color = "#FFFFFF", button_color = "#FFFFFF", text_color = "#000000")
        self.savedCameraID = CTkEntry(manageCamerasSecondRow, placeholder_text = "Assigned ID", font = ('Montserrat', 12, 'bold'), fg_color = "#FFFFFF", text_color = "#000000", corner_radius = 5)
        self.savedCameraLocation = CTkEntry(manageCamerasSecondRow, placeholder_text = "Assigned Location", font = ('Montserrat', 12, 'bold'), fg_color = "#FFFFFF", text_color = "#000000", corner_radius = 5)
        updateSavedCameraButton = CTkButton(manageCamerasSecondRow, text = "Update Camera", font = ('Montserrat', 12, 'bold'), fg_color = "#FFFFFF", text_color = "#000000", corner_radius = 5, command = self.updateSavedCamera_callback)
        deleteSavedCameraButton = CTkButton(manageCamerasSecondRow, text = "Delete Camera", font = ('Montserrat', 12, 'bold'), fg_color = "#D62828", text_color = "#FFFFFF", corner_radius = 5, command = self.deleteSavedCamera_callback)
        
        lowerLeftContent = CTkFrame(leftContentFrame, fg_color = "#1B2431", corner_radius = 5)
        upperLowerLeft = tk.Frame(lowerLeftContent, bg = "#1B2431")
        # Label for context
        filterLabel = CTkLabel(upperLowerLeft, text= "Filter By:", font = ('Montserrat', 12, 'bold'), anchor = "w", text_color = "#FFFFFF")
        # Dropdown for vehicle Type
        self.vehicleTypeComboVar = StringVar()
        self.vehicleTypeComboBox = CTkComboBox(upperLowerLeft,
                                          values = ['', 'Car', 'Taxi', 'Jeepney', 'Modern Jeepney', 'Motorcycle', 'Truck', 'Bus', 'Taxi', 'Tricycle'],
                                          command = self.vehicleTypeCombo_callback,
                                          variable = self.vehicleTypeComboVar,
                                          fg_color = "#FFFFFF",
                                          border_color = "#FFFFFF",
                                          text_color = "#000000",
                                          button_color = "#FFFFFF",
                                          dropdown_fg_color = "#FFFFFF",
                                          dropdown_text_color = "#000000",
                                          dropdown_font = ('Montserrat', 12))
        # Date Time Picker
        dateTimeButton = CTkButton(upperLowerLeft,
                                   text = "Date and Time",
                                   font = ('Montserrat', 12, 'bold'),
                                   text_color = "#000000",
                                   fg_color = "#FFFFFF",
                                   corner_radius = 5,
                                   command = self.selectDateTime)
        # Label for selected Date-Time
        self.selectedDateTimeLabel = CTkLabel(upperLowerLeft, text = "Select Date-Time", font = ('Montserrat', 12, 'bold'), text_color = "#FFFFFF")
        # Go Button
        goFilterButton = CTkButton(upperLowerLeft,
                                   text = "Go",
                                   font = ('Montserrat', 12, 'bold'),
                                   text_color = "#000000",
                                   fg_color = "#FFFFFF",
                                   corner_radius = 5,
                                   command = self.goFilter_callback)
        
        clearFilterButton = CTkButton(upperLowerLeft,
                                      text = "Clear",
                                      font = ('Montserrat', 12, 'bold'),
                                      text_color = "#000000",
                                      fg_color = "#FFFFFF",
                                      corner_radius = 5,
                                      command = self.clearFilter_callback)
        
        lowerLowerLeft = tk.Frame(lowerLeftContent, bg = "#090E18")
        databaseFrame = tk.Frame(lowerLowerLeft, bg = "#090E18")
        self.databaseTable = ttk.Treeview(databaseFrame, columns = ('licensePlate', 'vehicleType', 'cameraID', 'time', 'date', 'price'), show = "headings", style = 'Custom.Treeview')
        
        self.databaseTable.bind('<<TreeviewSelect>>', self.selectDataFromTable)
        self.databaseTable.bind('<Delete>', self.deleteDataFromTable)
        
        for entry in data:
            self.databaseTable.insert('', 'end', values=entry)
        
        self.databaseTable.tag_configure('even', background='#2A2D2E', foreground='#FFFFFF')
        self.databaseTable.tag_configure('odd', background='#343638', foreground='#FFFFFF')
        
        self.databaseTable.heading('licensePlate', text="License Plate", anchor='center')
        self.databaseTable.heading('vehicleType', text="Vehicle Type", anchor='center')
        self.databaseTable.heading('cameraID', text="Camera ID", anchor='center')
        self.databaseTable.heading('time', text="Time", anchor='center')
        self.databaseTable.heading('date', text="Date", anchor='center')
        self.databaseTable.heading('price', text="Price", anchor='center')
        
        self.databaseTable.column('licensePlate', width=150, anchor='center')
        self.databaseTable.column('vehicleType', width=150, anchor='center')
        self.databaseTable.column('cameraID', width=120, anchor='center')
        self.databaseTable.column('time', width=100, anchor='center')
        self.databaseTable.column('date', width=100, anchor='center')
        self.databaseTable.column('price', width=80, anchor='center')
        
        yscrollbar = ttk.Scrollbar(databaseFrame, orient='vertical', command=self.databaseTable.yview)
        self.databaseTable.configure(yscrollcommand=yscrollbar.set)
        
        xscrollbar = ttk.Scrollbar(lowerLowerLeft, orient='horizontal', command=self.databaseTable.xview)
        self.databaseTable.configure(xscrollcommand=xscrollbar.set)
        
        databaseHandlerFrame = tk.Frame(lowerLowerLeft, bg = "#1B2431")
        databaseHandlerRow = tk.Frame(databaseHandlerFrame, bg = "#1B2431")
                
        licensePlateHandlerFrame = tk.Frame(databaseHandlerRow, bg = "#1B2431")
        self.licensePlateLabel = CTkLabel(licensePlateHandlerFrame, text = "License Plate", font = ('Montserrat', 12), text_color = "#FFFFFF", anchor = 'w')
        self.licensePlateEntry = CTkEntry(licensePlateHandlerFrame, text_color = "#000000", fg_color = "#FFFFFF", corner_radius = 5, font = ('Montserrat', 12))
        
        vehicleTypeHandlerFrame = tk.Frame(databaseHandlerRow, bg = "#1B2431")
        self.vehicleTypeLabel = CTkLabel(vehicleTypeHandlerFrame, text = "Vehicle Type", font = ('Montserrat', 12), text_color = "#FFFFFF", anchor = 'w')
        self.vehicleTypeEntry = CTkEntry(vehicleTypeHandlerFrame, text_color = "#000000", fg_color = "#FFFFFF", corner_radius = 5, font = ('Montserrat', 12))
        
        priceHandlerFrame = tk.Frame(databaseHandlerRow, bg = "#1B2431")
        self.priceLabel = CTkLabel(priceHandlerFrame, text = "Price", font = ('Montserrat', 12), text_color = "#FFFFFF", anchor = 'w')
        self.priceEntry = CTkEntry(priceHandlerFrame, text_color = "#000000", fg_color = "#FFFFFF", corner_radius = 5, font = ('Montserrat', 12))
        
        self.updateTableButton = CTkButton(databaseHandlerRow, fg_color = "#FFFFFF", text = "Update", font = ('Montserrat', 12, 'bold'), corner_radius = 5, text_color = "#000000", command = self.updateTable_callback)
        # End of Contents of Left Content Frame
        
        rightContentFrame = CTkFrame(contentFrame, fg_color = "#1B2431", corner_radius = 5)
        # Contents of Right Content Frame
        manageUsers = CTkLabel(rightContentFrame, text = "Manage Users", font = ('Montserrat', 12, 'bold'), anchor = "w", text_color = "#FFFFFF")
        
        upperRight = tk.Frame(rightContentFrame, bg = "#1B2431")
        
        leftUpperRight = tk.Frame(upperRight, bg = "#1B2431")
        selectUserFrame = tk.Frame(leftUpperRight, bg = "#1B2431")
        selectUserLabel = CTkLabel(selectUserFrame, text = "Select User", font = ('Montserrat', 12), anchor = "w", text_color = "#FFFFFF")
        self.selectUserComboVar = StringVar()
        self.selectUserCombo = CTkComboBox(selectUserFrame,
                                      values = ["Pagtalunan", "Roa", "Rayray", "Mendoza"],
                                      command = self.selectUserCombo_callback,
                                      variable = self.selectUserComboVar,
                                      fg_color = "#FFFFFF",
                                      border_color = "#FFFFFF",
                                      text_color = "#000000",
                                      button_color = "#FFFFFF",
                                      dropdown_fg_color = "#FFFFFF",
                                      dropdown_text_color = "#000000",
                                      dropdown_font = ('Montserrat', 12))
        
        rightUpperRight = tk.Frame(upperRight, bg = "#1B2431")
        addUserButton = CTkButton(rightUpperRight, text = "Add User", font = ('Montserrat', 12, 'bold'), text_color = "#000000", fg_color = "#FFFFFF",
                                  command = self.addUserButton_callback, corner_radius = 5)
        clearFieldButton = CTkButton(rightUpperRight, text = "Clear Field", font = ('Montserrat', 12, 'bold'), text_color = "#000000", fg_color = "#FFFFFF",
                               command = self.clearFieldButton_callback, corner_radius = 5)
        
        middleRight = tk.Frame(rightContentFrame, bg = "#1B2431")
        upperMiddleRight = tk.Frame(middleRight, bg = "#1B2431")
        
        userLabel = CTkLabel(upperMiddleRight, text = "User Information", font = ('Montserrat', 12, 'bold'), anchor = "w", text_color = "#FFFFFF")
        
        firstNameOuter = tk.Frame(upperMiddleRight, bg = "#1B2431")
        firstNameInner = tk.Frame(firstNameOuter, bg = "#1B2431")
        firstNameLabel = CTkLabel(firstNameInner, text = "First Name", font = ('Montserrat', 12), text_color = "#FFFFFF", anchor = "w")
        self.firstNameEntry = CTkEntry(firstNameInner, placeholder_text = "Ex. Juan", font = ('Montserrat', 12), text_color = "#000000", fg_color = "#FFFFFF")
        
        lastNameOuter = tk.Frame(upperMiddleRight, bg = "#1B2431")
        lastNameInner = tk.Frame(lastNameOuter, bg = "#1B2431")
        lastNameLabel = CTkLabel(lastNameInner, text = "Last Name", font = ('Montserrat', 12), text_color = "#FFFFFF", anchor = "w")
        self.lastNameEntry = CTkEntry(lastNameInner, placeholder_text = "Ex. Cruz", font = ('Montserrat', 12), text_color = "#000000", fg_color = "#FFFFFF")
        
        emailOuter = tk.Frame(upperMiddleRight, bg = "#1B2431")
        emailInner = tk.Frame(emailOuter, bg = "#1B2431")
        emailLabel = CTkLabel(emailInner, text = "Email", font = ('Montserrat', 12), text_color = "#FFFFFF", anchor = "w")
        self.emailEntry = CTkEntry(emailInner, placeholder_text = "Ex. juancruz@domain.com", font = ('Montserrat', 12), text_color = "#000000", fg_color = "#FFFFFF")
        
        usernamePasswordOuter = tk.Frame(upperMiddleRight, bg = "#1B2431")
        usernameInner = tk.Frame(usernamePasswordOuter, bg = "#1B2431")
        usernameLabel = CTkLabel(usernameInner, text = "Username", font = ('Montserrat', 12), text_color = "#FFFFFF", anchor = "w")
        self.usernameEntry = CTkEntry(usernameInner, font = ('Montserrat', 12), text_color = "#000000", fg_color = "#FFFFFF")
        passwordInner = tk.Frame(usernamePasswordOuter, bg = "#1B2431")
        passwordLabel = CTkLabel(passwordInner, text = "Password", font = ('Montserrat', 12), text_color = "#FFFFFF", anchor = "w")
        self.passwordEntry = CTkEntry(passwordInner, font = ('Montserrat', 12), text_color = "#000000", fg_color = "#FFFFFF", show = "*")
        
        lowerMiddleRight = tk.Frame(middleRight, bg = "#1B2431")
        
        accessLabel = CTkLabel(lowerMiddleRight, text = "Access", font = ('Montserrat', 12, 'bold'), anchor = "w", text_color = "#FFFFFF")
        
        adminFrameOuter = tk.Frame(lowerMiddleRight, bg = "#1B2431")
        leftAdminFrameInner = tk.Frame(adminFrameOuter, bg = "#1B2431")
        adminLabel = CTkLabel(leftAdminFrameInner, text = "Administrator", font = ('Montserrat', 12), text_color = "#FFFFFF", anchor = "w")
        rightAdminFrameInner = tk.Frame(adminFrameOuter, bg = "#1B2431")
        adminVar = IntVar(value = 0)
        adminRadio_yes = CTkRadioButton(rightAdminFrameInner, text = "Yes", variable = adminVar, value = 1, command = self.adminRadioButton_callback)
        adminRadio_no = CTkRadioButton(rightAdminFrameInner, text = "No", variable = adminVar, value = 2, command = self.adminRadioButton_callback)
        
        congestionPriceFrameOuter = tk.Frame(lowerMiddleRight, bg = "#1B2431")
        leftCongestionPriceFrameInner = tk.Frame(congestionPriceFrameOuter, bg = "#1B2431")
        congestionPriceLabel = CTkLabel(leftCongestionPriceFrameInner, text = "Change Congestion Price", font = ('Montserrat', 12), text_color = "#FFFFFF", anchor = "w")
        rightCongestionPriceFrameInner = tk.Frame(congestionPriceFrameOuter, bg = "#1B2431")
        changePriceVar = IntVar(value = 0)
        changePriceRadio_yes = CTkRadioButton(rightCongestionPriceFrameInner, text = "Yes", variable = changePriceVar, value = 1, command = self.changePriceRadioButton_callback)
        changePriceRadio_no = CTkRadioButton(rightCongestionPriceFrameInner, text = "No", variable = changePriceVar, value = 2, command = self.changePriceRadioButton_callback)
        
        activeHoursFrameOuter = tk.Frame(lowerMiddleRight, bg = "#1B2431")
        leftActiveHoursFrameInner = tk.Frame(activeHoursFrameOuter, bg = "#1B2431")
        activeHoursLabel = CTkLabel(leftActiveHoursFrameInner, text = "Change Active Hours", font = ('Montserrat', 12), text_color = "#FFFFFF", anchor = "w")
        rightActiveHoursFrameInner = tk.Frame(activeHoursFrameOuter, bg = "#1B2431")
        activeHoursRadioVar = IntVar(value = 0)
        activeHoursRadio_yes = CTkRadioButton(rightActiveHoursFrameInner, text = "Yes", variable = activeHoursRadioVar, value = 1, command = self.changeDetectableRadioButton_callback)
        activeHoursRadio_no = CTkRadioButton(rightActiveHoursFrameInner, text = "No", variable = activeHoursRadioVar, value = 2, command = self.changeDetectableRadioButton_callback)
        
        detectableFrameOuter = tk.Frame(lowerMiddleRight, bg = "#1B2431")
        leftDetectableFrameInner = tk.Frame(detectableFrameOuter, bg = "#1B2431")
        detectableLabel = CTkLabel(leftDetectableFrameInner, text = "Change Detectable Vehicles", font = ('Montserrat', 12), text_color = "#FFFFFF", anchor = "w")
        rightDetectableFrameInner = tk.Frame(detectableFrameOuter, bg = "#1B2431")
        detectableRadioVar = IntVar(value = 0)
        detectableRadio_yes = CTkRadioButton(rightDetectableFrameInner, text = "Yes", variable = detectableRadioVar, value = 1, command = self.changeDetectableRadioButton_callback)
        detectableRadio_no = CTkRadioButton(rightDetectableFrameInner, text = "No", variable = detectableRadioVar, value = 2, command = self.changeDetectableRadioButton_callback)
        
        downloadFrameOuter = tk.Frame(lowerMiddleRight, bg = "#1B2431")
        leftDownloadFrameInner = tk.Frame(downloadFrameOuter, bg = "#1B2431")
        downloadLabel = CTkLabel(leftDownloadFrameInner, text = "Download CSV", font = ('Montserrat', 12), text_color = "#FFFFFF", anchor = "w")
        rightDownloadFrameInner = tk.Frame(downloadFrameOuter, bg = "#1B2431")
        downloadRadioVar = IntVar(value = 0)
        downloadRadio_yes = CTkRadioButton(rightDownloadFrameInner, text = "Yes", variable = downloadRadioVar, value = 1, command = self.downloadCSVRadioButton_callback)
        downloadRadio_no = CTkRadioButton(rightDownloadFrameInner, text = "No", variable = downloadRadioVar, value = 2, command = self.downloadCSVRadioButton_callback)
        
        lowerRight = tk.Frame(rightContentFrame, bg = "#1B2431")
        deleteUserButton = CTkButton(lowerRight, text = "Delete User", font = ('Montserrat', 12, 'bold'), text_color = "#FFFFFF", fg_color = "#D62828",
                                  command = self.deleteUserButton_callback, corner_radius = 5)
        applyUserButton = CTkButton(lowerRight, text = "Apply", font = ('Montserrat', 12, 'bold'), text_color = "#000000", fg_color = "#FFFFFF",
                               command = self.applyUserButton_callback, corner_radius = 5)
        # End of Contents of Right Content Frame
        
        navigationFrame = tk.Frame(self, bg = "#090E18")
        # Dashboard Button - Navigates to Dashboard
        dashboardButton = CTkButton(navigationFrame,
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
        
        # --------------------------- Packing of Widgets -------------------------------- #
        
        toolBarFrame.pack(side = "top", fill = "x")
        closeButton.pack(side = "right", padx = 10, pady = 10)
        minimizeButton.pack(side = "right", padx = 0, pady = 10)
        
        contentFrame.pack(side = tk.TOP, expand = True, fill = "both")
        
        leftContentFrame.pack(side = "left", expand = True, fill = "both")
        # Contents of Left Content Frame
        upperLeftContent.pack(side = "top", expand = True, fill = "both", padx = 10, pady = 10, ipadx = 10, ipady = 10)
        
        addCamerasLabel.pack(side = "top", fill = "x", padx = 10, pady = (5,0))
        
        manageCamerasFirstRow.pack(side = "top", fill = "x", padx = 10, pady = (2, 10))
        discoverCameraButton.pack(side = "left", fill = "x", expand = True, padx = 15)
        self.discoveredCamerasDrop.pack(side = "left", fill = "x", expand = True, padx = 15)
        self.assignID.pack(side = "left", fill = "x", expand = True, padx = 15)
        self.assignLocation.pack(side = "left", fill = "x", expand = True, padx = 15)
        addCameraButton.pack(side = "left", fill = "x", expand = True, padx = 15)
        
        manageCamerasLabel.pack(side = "top", fill = "x", padx = 10, pady = (5,0))
        
        manageCamerasSecondRow.pack(side = "top", fill = "x", padx = 10, pady = (2, 10))
        self.savedCamerasDrop.pack(side = "left", fill = "x", expand = True, padx = 15)
        self.savedCameraID.pack(side = "left", fill = "x", expand = True, padx = 15)
        self.savedCameraLocation.pack(side = "left", fill = "x", expand = True, padx = 15)
        updateSavedCameraButton.pack(side = "left", fill = "x", expand = True, padx = 15)
        deleteSavedCameraButton.pack(side = "left", fill = "x", expand = True, padx = 15)
        
        lowerLeftContent.pack(side = "top", expand = True, fill = "both", padx = 10, pady = 10, ipadx = 10, ipady = 10)
        
        upperLowerLeft.pack(side = "top", fill = "both", padx = 10, pady = 10)
        # Label for context
        filterLabel.pack(side = "left", padx = 5, pady = 5)
        # Dropdown for vehicle Type
        self.vehicleTypeComboBox.pack(side = "left", padx = 5, pady = 5)
        # Date Time Picker
        dateTimeButton.pack(side = "left", padx = 5, pady = 5)
        # Label for selected Date-Time
        self.selectedDateTimeLabel.pack(side = "left", padx = 5, pady = 5)
        # Go Button
        goFilterButton.pack(side = "right", padx = 5, pady = 5)
        clearFilterButton.pack(side = "right", padx = 5, pady = 5)
        lowerLowerLeft.pack(side = "top", expand = True, fill = "both", padx = 5, pady = 5)
        databaseFrame.pack(side = "top", expand = True, fill = "both", padx = 2, pady = 2)
        self.databaseTable.pack(expand=True, fill='both', padx=0, pady=0, side = "left")
        yscrollbar.pack(side='left', fill='both', padx=0, pady=0)
        xscrollbar.pack(side='top', fill='both', padx=0, pady=0)
        
        databaseHandlerFrame.pack(side = "top", fill = "x")
        databaseHandlerRow.pack(side = "top", fill = "both")
                
        licensePlateHandlerFrame.pack(side = "left", fill = "y", expand = True)
        self.licensePlateLabel.pack(side = "top", fill = "x", padx = 10, expand = True)
        self.licensePlateEntry.pack(side = "top", fill = "x", expand = True)
        
        vehicleTypeHandlerFrame.pack(side = "left", fill = "y", expand = True)
        self.vehicleTypeLabel.pack(side = "top", fill = "x", padx = 10, expand = True)
        self.vehicleTypeEntry.pack(side = "top", fill = "x", expand = True)
        
        priceHandlerFrame.pack(side = "left", fill = "y", expand = True)
        self.priceLabel.pack(side = "top", fill = "x", padx = 10, expand = True)
        self.priceEntry.pack(side = "top", fill = "x", expand = True)
        
        self.updateTableButton.pack(side = "left", fill = "x", expand = True)
        
        # End of Contents of Left Content Frame
        rightContentFrame.pack(side = "left", expand = False, fill = "both", padx = 10, pady = 10, ipadx = 10, ipady = 10)
        
        manageUsers.pack(side = "top", fill = "x", padx = 10, pady = 5)
        
        upperRight.pack(side = "top", expand = False, fill = "both", padx = 10, pady = 2)
        
        leftUpperRight.pack(side = "left", expand = False, fill = "both")
        selectUserFrame.pack(side = "left", expand = True, fill = "x", padx = 20, pady = 20)
        selectUserLabel.pack(side = "left", fill = "both", padx = (10, 5), pady = 2, expand = False)
        self.selectUserCombo.pack(side = "left", fill = "both", padx = (5, 10), pady = 2, expand = False)
        
        rightUpperRight.pack(side = "left", expand = False, fill = "both")
        addUserButton.pack(side = "left", fill = "x", padx = (10, 5), pady = 10, expand = False)
        clearFieldButton.pack(side = "left", fill = "x", padx = (5, 10), pady = 10, expand = False)
        
        middleRight.pack(side = "top", expand = False, fill = "both", padx = 10, pady = 2)
        upperMiddleRight.pack(side = "top", fill = "both", expand = True, padx = 5, pady = 2)
        userLabel.pack(side = "top", fill = "x", padx = 5, pady = 5)
        
        firstNameOuter.pack(side = "top", fill = "both", expand = True, padx = 10, pady = 2)
        firstNameInner.pack(side = "top", padx = 10, pady = 10, fill = "both", expand = False)
        firstNameLabel.pack(side = "top", fill = "x", padx = 20, pady = (5,0))
        self.firstNameEntry.pack(side = "top", fill = "x", padx = 10, pady = (0,5))
        
        lastNameOuter.pack(side = "top", fill = "both", expand = True, padx = 10, pady = 2)
        lastNameInner.pack(side = "top", padx = 10, pady = 10, fill = "both", expand = False)
        lastNameLabel.pack(side = "top", fill = "x", padx = 20, pady = (5,0))
        self.lastNameEntry.pack(side = "top", fill = "x", padx = 10, pady = (0,5))
        
        emailOuter.pack(side = "top", fill = "both", expand = True, padx = 10, pady = 2)
        emailInner.pack(side = "top", padx = 10, pady = 10, fill = "both", expand = False)
        emailLabel.pack(side = "top", fill = "x", padx = 20, pady = (5,0))
        self.emailEntry.pack(side = "top", fill = "x", padx = 10, pady = (0,5))
        
        usernamePasswordOuter.pack(side = "top", fill = "both", expand = True, padx = 10, pady = 2)
        usernameInner.pack(side = "left", padx = 10, pady = 10, fill = "both", expand = True)
        usernameLabel.pack(side = "top", fill = "x", padx = 20, pady = (5,0))
        self.usernameEntry.pack(side = "top", fill = "x", padx = 10, pady = (0,5))
        passwordInner.pack(side = "left", padx = 10, pady = 10, fill = "both", expand = True)
        passwordLabel.pack(side = "top", fill = "x", padx = 20, pady = (5,0))
        self.passwordEntry.pack(side = "top", fill = "x", padx = 10, pady = (0,5))
        
        lowerMiddleRight.pack(side = "top", fill = "both", expand = True, padx = 5, pady = 2)
        accessLabel.pack(side = "top", fill = "x", padx = 5, pady = 5)
         
        adminFrameOuter.pack(side = "top", fill = "both", expand = True, padx = 10, pady = 2)
        leftAdminFrameInner.pack(side = "left", fill = "both", expand = True)
        adminLabel.pack(fill = "x", expand = False)
        rightAdminFrameInner.pack(side = "left", fill = "both", expand = True)
        adminRadio_no.pack(side = "right", padx = 0, pady = 2)
        adminRadio_yes.pack(side = "right", padx = 5, pady = 2)
        
        congestionPriceFrameOuter.pack(side = "top", fill = "both", expand = True, padx = 10, pady = 2)
        leftCongestionPriceFrameInner.pack(side = "left", fill = "both", expand = True)
        congestionPriceLabel.pack(fill = "x", expand = False)
        rightCongestionPriceFrameInner.pack(side = "left", fill = "both", expand = True)
        changePriceRadio_no.pack(side = "right", padx = 0, pady = 2)
        changePriceRadio_yes.pack(side = "right", padx = 5, pady = 2)
        
        activeHoursFrameOuter.pack(side = "top", fill = "both", expand = True, padx = 10, pady = 2)
        leftActiveHoursFrameInner.pack(side = "left", fill = "both", expand = True)
        activeHoursLabel.pack(fill = "x", expand = False)
        rightActiveHoursFrameInner.pack(side = "left", fill = "both", expand = True)
        activeHoursRadio_no.pack(side = "right", padx = 0, pady = 2)
        activeHoursRadio_yes.pack(side = "right", padx = 5, pady = 2)
        
        detectableFrameOuter.pack(side = "top", fill = "both", expand = True, padx = 10, pady = 2)
        leftDetectableFrameInner.pack(side = "left", fill = "both", expand = True)
        detectableLabel.pack(fill = "x", expand = False)
        rightDetectableFrameInner.pack(side = "left", fill = "both", expand = True)
        detectableRadio_no.pack(side = "right", padx = 0, pady = 2)
        detectableRadio_yes.pack(side = "right", padx = 5, pady = 2)
        
        downloadFrameOuter.pack(side = "top", fill = "both", expand = True, padx = 10, pady = 2)
        leftDownloadFrameInner.pack(side = "left", fill = "both", expand = True)
        downloadLabel.pack(fill = "x", expand = False)
        rightDownloadFrameInner.pack(side = "left", fill = "both", expand = True)
        downloadRadio_no.pack(side = "right", padx = 0, pady = 2)
        downloadRadio_yes.pack(side = "right", padx = 5, pady = 2)
        
        lowerRight.pack(side = "top", expand = False, fill = "both", padx = 10, pady = 2)
        applyUserButton.pack(side = "right", expand = False, fill = "x", padx = (5,10), pady = 2)
        deleteUserButton.pack(side = "right", expand = False, fill = "x", padx = (10,5), pady = 2)
                
        navigationFrame.pack(side = "top", fill = "x")
        dashboardButton.pack(side = 'right', padx = 10, pady = 10)