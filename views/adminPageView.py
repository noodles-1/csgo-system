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
        
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg = "#090E18")
        
        style = ttk.Style()
        style.theme_use('forest-dark')
        
        self.selected_date = ""
        self.selected_hour_from = ""
        self.selected_hour_to = ""
        
        # Close Icon (Currently Set to darkmode, if possible change to lightmode when the the changes)
        closePhoto = CTkImage(light_image = Image.open("views/icons/icon_close_lightmode.png"),
                              dark_image = Image.open("views/icons/icon_close_darkmode.png"),
                              size = (20, 20))

        # Minimize Icon (Currently Set to darkmode, if possible change to lightmode when the the changes)
        minimizePhoto = CTkImage(light_image = Image.open("views/icons/icon_minimize_lightmode.png"),
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
        toolBarFrame = tk.Frame(self, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        
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

        contentFrame = tk.Frame(self, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        
        
        leftContentFrame = tk.Frame(contentFrame, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        # Contents of Left Content Frame
        upperLeftContent = tk.Frame(leftContentFrame, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        manageCamerasLabel = CTkLabel(upperLeftContent, text = "Manage Cameras", font = ('Montserrat', 12, 'bold'), anchor = "w", text_color = "#FFFFFF")
        
        lowerLeftContent = tk.Frame(leftContentFrame, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        upperLowerLeft = tk.Frame(lowerLeftContent, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
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
        
        lowerLowerLeft = tk.Frame(lowerLeftContent, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        databaseFrame = tk.Frame(lowerLowerLeft, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        databaseTable = ttk.Treeview(databaseFrame, columns = ('licensePlate', 'vehicleType', 'cameraID', 'time', 'date', 'price'), show = "headings", style = 'Custom.Treeview')
        
        for entry in data:
            databaseTable.insert('', 'end', values=entry)
        
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
        
        yscrollbar = ttk.Scrollbar(databaseFrame, orient='vertical', command=databaseTable.yview)
        databaseTable.configure(yscrollcommand=yscrollbar.set)
        
        xscrollbar = ttk.Scrollbar(lowerLowerLeft, orient='horizontal', command=databaseTable.xview)
        databaseTable.configure(xscrollcommand=xscrollbar.set)
        # End of Contents of Left Content Frame
        
        rightContentFrame = tk.Frame(contentFrame, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        # Contents of Right Content Frame
        manageUsers = CTkLabel(rightContentFrame, text = "Manage Users", font = ('Montserrat', 12, 'bold'), anchor = "w", text_color = "#FFFFFF")
        
        upperRight = tk.Frame(rightContentFrame, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        
        leftUpperRight = tk.Frame(upperRight, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        selectUserFrame = tk.Frame(leftUpperRight, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
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
        
        rightUpperRight = tk.Frame(upperRight, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        addUserButton = CTkButton(rightUpperRight, text = "Add User", font = ('Montserrat', 12, 'bold'), text_color = "#000000", fg_color = "#FFFFFF",
                                  command = self.addUserButton_callback, corner_radius = 5)
        clearFieldButton = CTkButton(rightUpperRight, text = "Clear Field", font = ('Montserrat', 12, 'bold'), text_color = "#000000", fg_color = "#FFFFFF",
                               command = self.clearFieldButton_callback, corner_radius = 5)
        
        middleRight = tk.Frame(rightContentFrame, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        upperMiddleRight = tk.Frame(middleRight, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        
        userLabel = CTkLabel(upperMiddleRight, text = "User Information", font = ('Montserrat', 12, 'bold'), anchor = "w", text_color = "#FFFFFF")
        
        firstNameOuter = tk.Frame(upperMiddleRight, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        firstNameInner = tk.Frame(firstNameOuter, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        firstNameLabel = CTkLabel(firstNameInner, text = "First Name", font = ('Montserrat', 12), text_color = "#FFFFFF", anchor = "w")
        self.firstNameEntry = CTkEntry(firstNameInner, placeholder_text = "Ex. Juan", font = ('Montserrat', 12), text_color = "#000000", fg_color = "#FFFFFF")
        
        lastNameOuter = tk.Frame(upperMiddleRight, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        lastNameInner = tk.Frame(lastNameOuter, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        lastNameLabel = CTkLabel(lastNameInner, text = "Last Name", font = ('Montserrat', 12), text_color = "#FFFFFF", anchor = "w")
        self.lastNameEntry = CTkEntry(lastNameInner, placeholder_text = "Ex. Cruz", font = ('Montserrat', 12), text_color = "#000000", fg_color = "#FFFFFF")
        
        emailOuter = tk.Frame(upperMiddleRight, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        emailInner = tk.Frame(emailOuter, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        emailLabel = CTkLabel(emailInner, text = "Email", font = ('Montserrat', 12), text_color = "#FFFFFF", anchor = "w")
        self.emailEntry = CTkEntry(emailInner, placeholder_text = "Ex. juancruz@domain.com", font = ('Montserrat', 12), text_color = "#000000", fg_color = "#FFFFFF")
        
        usernamePasswordOuter = tk.Frame(upperMiddleRight, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        usernameInner = tk.Frame(usernamePasswordOuter, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        usernameLabel = CTkLabel(usernameInner, text = "Username", font = ('Montserrat', 12), text_color = "#FFFFFF", anchor = "w")
        self.usernameEntry = CTkEntry(usernameInner, font = ('Montserrat', 12), text_color = "#000000", fg_color = "#FFFFFF")
        passwordInner = tk.Frame(usernamePasswordOuter, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        passwordLabel = CTkLabel(passwordInner, text = "Password", font = ('Montserrat', 12), text_color = "#FFFFFF", anchor = "w")
        self.passwordEntry = CTkEntry(passwordInner, font = ('Montserrat', 12), text_color = "#000000", fg_color = "#FFFFFF", show = "*")
        
        lowerMiddleRight = tk.Frame(middleRight, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        
        accessLabel = CTkLabel(lowerMiddleRight, text = "Access", font = ('Montserrat', 12, 'bold'), anchor = "w", text_color = "#FFFFFF")
        
        adminFrameOuter = tk.Frame(lowerMiddleRight, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        leftAdminFrameInner = tk.Frame(adminFrameOuter, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        adminLabel = CTkLabel(leftAdminFrameInner, text = "Administrator", font = ('Montserrat', 12), text_color = "#FFFFFF", anchor = "w")
        rightAdminFrameInner = tk.Frame(adminFrameOuter, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        adminVar = IntVar(value = 0)
        adminRadio_yes = CTkRadioButton(rightAdminFrameInner, text = "Yes", variable = adminVar, value = 1, command = self.adminRadioButton_callback)
        adminRadio_no = CTkRadioButton(rightAdminFrameInner, text = "No", variable = adminVar, value = 2, command = self.adminRadioButton_callback)
        
        congestionPriceFrameOuter = tk.Frame(lowerMiddleRight, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        leftCongestionPriceFrameInner = tk.Frame(congestionPriceFrameOuter, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        congestionPriceLabel = CTkLabel(leftCongestionPriceFrameInner, text = "Change Congestion Price", font = ('Montserrat', 12), text_color = "#FFFFFF", anchor = "w")
        rightCongestionPriceFrameInner = tk.Frame(congestionPriceFrameOuter, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        changePriceVar = IntVar(value = 0)
        changePriceRadio_yes = CTkRadioButton(rightCongestionPriceFrameInner, text = "Yes", variable = changePriceVar, value = 1, command = self.changePriceRadioButton_callback)
        changePriceRadio_no = CTkRadioButton(rightCongestionPriceFrameInner, text = "No", variable = changePriceVar, value = 2, command = self.changePriceRadioButton_callback)
        
        activeHoursFrameOuter = tk.Frame(lowerMiddleRight, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        leftActiveHoursFrameInner = tk.Frame(activeHoursFrameOuter, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        activeHoursLabel = CTkLabel(leftActiveHoursFrameInner, text = "Change Active Hours", font = ('Montserrat', 12), text_color = "#FFFFFF", anchor = "w")
        rightActiveHoursFrameInner = tk.Frame(activeHoursFrameOuter, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        activeHoursRadioVar = IntVar(value = 0)
        activeHoursRadio_yes = CTkRadioButton(rightActiveHoursFrameInner, text = "Yes", variable = activeHoursRadioVar, value = 1, command = self.changeDetectableRadioButton_callback)
        activeHoursRadio_no = CTkRadioButton(rightActiveHoursFrameInner, text = "No", variable = activeHoursRadioVar, value = 2, command = self.changeDetectableRadioButton_callback)
        
        detectableFrameOuter = tk.Frame(lowerMiddleRight, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        leftDetectableFrameInner = tk.Frame(detectableFrameOuter, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        detectableLabel = CTkLabel(leftDetectableFrameInner, text = "Change Detectable Vehicles", font = ('Montserrat', 12), text_color = "#FFFFFF", anchor = "w")
        rightDetectableFrameInner = tk.Frame(detectableFrameOuter, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        detectableRadioVar = IntVar(value = 0)
        detectableRadio_yes = CTkRadioButton(rightDetectableFrameInner, text = "Yes", variable = detectableRadioVar, value = 1, command = self.changeDetectableRadioButton_callback)
        detectableRadio_no = CTkRadioButton(rightDetectableFrameInner, text = "No", variable = detectableRadioVar, value = 2, command = self.changeDetectableRadioButton_callback)
        
        downloadFrameOuter = tk.Frame(lowerMiddleRight, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        leftDownloadFrameInner = tk.Frame(downloadFrameOuter, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        downloadLabel = CTkLabel(leftDownloadFrameInner, text = "Download CSV", font = ('Montserrat', 12), text_color = "#FFFFFF", anchor = "w")
        rightDownloadFrameInner = tk.Frame(downloadFrameOuter, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        downloadRadioVar = IntVar(value = 0)
        downloadRadio_yes = CTkRadioButton(rightDownloadFrameInner, text = "Yes", variable = downloadRadioVar, value = 1, command = self.downloadCSVRadioButton_callback)
        downloadRadio_no = CTkRadioButton(rightDownloadFrameInner, text = "No", variable = downloadRadioVar, value = 2, command = self.downloadCSVRadioButton_callback)
        
        lowerRight = tk.Frame(rightContentFrame, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
        deleteUserButton = CTkButton(lowerRight, text = "Delete User", font = ('Montserrat', 12, 'bold'), text_color = "#FFFFFF", fg_color = "#D62828",
                                  command = self.deleteUserButton_callback, corner_radius = 5)
        applyUserButton = CTkButton(lowerRight, text = "Apply", font = ('Montserrat', 12, 'bold'), text_color = "#000000", fg_color = "#FFFFFF",
                               command = self.applyUserButton_callback, corner_radius = 5)
        # End of Contents of Right Content Frame
        
        navigationFrame = tk.Frame(self, bg = "#090E18", highlightbackground = "#FFFFFF", highlightthickness = 2)
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
        
        # ---------------------------- Packing of Widgets -------------------------------- #
        
        toolBarFrame.pack(side = "top", fill = "x")
        closeButton.pack(side = "right", padx = 10, pady = 10)
        minimizeButton.pack(side = "right", padx = 0, pady = 10)
                
        contentFrame.pack(side = "top", expand = True, fill = "both")
        
        leftContentFrame.pack(side = "left", expand = True, fill = "both")
        # Contents of Left Content Frame
        upperLeftContent.pack(side = "top", expand = True, fill = "both", padx = 10, pady = 10)
        
        manageCamerasLabel.pack(side = "top", fill = "x", padx = 10, pady = 5)
        
        lowerLeftContent.pack(side = "top", expand = True, fill = "both", padx = 10, pady = 10)
        
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
        databaseTable.pack(expand=True, fill='both', padx=0, pady=0, side = "left")
        yscrollbar.pack(side='left', fill='both', padx=0, pady=0)
        xscrollbar.pack(side='top', fill='both', padx=0, pady=0)
        # End of Contents of Left Content Frame
        rightContentFrame.pack(side = "left", expand = False, fill = "both")
        
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