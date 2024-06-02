import os
import sys
import tkinter as tk

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import controllers.controller as cont
import views.switchView as switch

from datetime import datetime
from customtkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image
from tkcalendar import Calendar
from controllers.dbController import DBController
from controllers.s3controller import S3Controller

class ConfigPage(tk.Frame):
    def closeApplication(self):
        self.master.destroy()
        
    def minimizeApplication(self):
        self.master.iconify()

    def clearInput(self):
        # Config Form 
        self.fromComboBox.set('')
        self.toComboBox.set('')
        self.everyComboBox.set('')
        
        # Config Form 2
        self.dateEntry.delete(0, tk.END)
        self.timeEntry.delete(0, tk.END)
        
        # Price Form
        self.truckVal.set('')
        self.busVal.set('')
        self.motorcycleVal.set('')
        self.carVal.set('')
        
        # Detectables Form
        self.truckComboBox.set('')
        self.busComboBox.set('')
        self.motorcycleComboBox.set('')
        self.carComboBox.set('')
        
    def addNew_callback(self):
        self.rightDatabaseTable.selection_remove(self.rightDatabaseTable.selection())
        self.leftDatabaseTable.selection_remove(self.leftDatabaseTable.selection())
        
        self.clearInput()

    def refresh_callback(self):
        self.rightDatabaseTable.selection_remove(self.rightDatabaseTable.selection())
        self.leftDatabaseTable.selection_remove(self.leftDatabaseTable.selection())
        self.reloadLeftDatabase()
        self.reloadRightDatabase()
        
    def deleteDataFromTable(self, event):
        caller = event.widget
        
        if tk.messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected items?"):                
            if caller == self.leftDatabaseTable:
                for i in self.leftDatabaseTable.selection():
                    values = caller.item(i)['values']
                    id = int(values[0])
                    response = DBController.deleteCurrentSetting(id)
                    if response.ok:
                        self.s3.updateAuditLog('Delete setting', f'Deleted current setting (starting hour={values[1]}, ending hour={values[2]}, day={values[3]})', cont.currUser)
                        self.leftDatabaseTable.delete(i)
                    
            elif caller == self.rightDatabaseTable:
                for i in self.rightDatabaseTable.selection():
                    values = caller.item(i)['values']
                    id = int(values[0])
                    response = DBController.deleteFutureSetting(id)
                    if response.ok:
                        self.s3.updateAuditLog('Delete setting', f'Deleted future setting (starting hour={values[1]}, ending hour={values[2]}, day={values[3]}, starting date={values[4]})', cont.currUser)
                        self.rightDatabaseTable.delete(i)
    
    def cancelButton_callback(self):
        pass

    def reloadLeftDatabase(self):
        for row in self.leftDatabaseTable.get_children():
            self.leftDatabaseTable.delete(row)

        currResponse = DBController.getCurrentSettings()
        if currResponse.ok:
            for row in currResponse.data:
                self.leftDatabaseTable.insert('', 'end', values=(row[0].id, row[0].hourFrom, row[0].hourTo, row[0].day))

    def reloadRightDatabase(self):
        for row in self.rightDatabaseTable.get_children():
            self.rightDatabaseTable.delete(row)

        futureResponse = DBController.getFutureSettings()
        if futureResponse.ok:
            for row in futureResponse.data:
                self.rightDatabaseTable.insert('', 'end', values=(row[0].id, row[0].hourFrom, row[0].hourTo, row[0].day, row[0].startDate))

    def addUpdateButton_callback(self):
        def isPositiveFloat(s: str) -> bool:
            try:
                n = float(s)
                return n >= 0
            except:
                return False

        carDropdown = self.carComboVal.get()
        motorDropdown = self.motorcycleComboVal.get()
        busDropdown = self.busComboVal.get()
        truckDropdown= self.truckComboVal.get()

        carPrice = self.carVal.get()
        motorPrice = self.motorcycleVal.get()
        busPrice = self.busVal.get()
        truckPrice = self.truckVal.get()
        
        hourFrom = self.fromComboVal.get()
        hourTo = self.toComboVal.get()
        dayEntry = self.everyComboVal.get()

        selectedDate = self.dateEntry.get()
        selectedTime = self.timeEntry.get()

        for widget in [carDropdown, motorDropdown, busDropdown, truckDropdown, carPrice, motorPrice, busPrice, truckPrice, hourFrom, hourTo, dayEntry]:
            if not widget:
                self.statusLabel.configure(text='Incomplete fields.', text_color="#d62828")
                self.after(3500, lambda: self.statusLabel.configure(text_color="#1B2431"))
                return
            
        for price in [carPrice, motorPrice, busPrice, truckPrice]:
            if not isPositiveFloat(price):
                self.statusLabel.configure(text='Invalid price.', text_color="#d62828")
                self.after(3500, lambda: self.statusLabel.configure(text_color="#1B2431"))
                return
            
        if (not selectedDate and selectedTime) or (selectedDate and not selectedTime):
            self.statusLabel.configure(text='Either date or time cannot be empty. Leave both fields empty to apply the setting immediately.', text_color="#d62828")
            self.after(3500, lambda: self.statusLabel.configure(text_color="#1B2431"))
            return
    
        hourFrom = datetime.strptime(hourFrom, '%H:%M').time()
        hourTo = datetime.strptime(hourTo, '%H:%M').time()
        
        try:
            selectedDate = datetime.strptime(selectedDate, '%m/%d/%Y').date() if selectedDate else None
            selectedTime = datetime.strptime(selectedTime, '%H:%M').time() if selectedTime else None
        except:
            self.statusLabel.configure(text='Invalid date or time', text_color="#d62828")
            self.after(3500, lambda: self.statusLabel.configure(text_color="#1B2431"))
            return
        
        if selectedDate and selectedDate < datetime.now().date():
            self.statusLabel.configure(text='Date should be the current or future date.', text_color="#d62828")
            self.after(4000, lambda: self.statusLabel.configure(text_color="#1B2431"))
            return
        
        if selectedDate and selectedDate == datetime.now().date() and selectedTime < datetime.now().time():
            self.statusLabel.configure(text='Time should be current or future time.', text_color="#d62828")
            self.after(2000, lambda: self.statusLabel.configure(text_color="#1B2431"))
            return
        
        if hourTo <= hourFrom:
            self.statusLabel.configure(text='Ending hour cannot be less than or equal the starting hour.', text_color="#d62828")
            self.after(4000, lambda: self.statusLabel.configure(text_color="#1B2431"))
            return
        
        if self.chosenId is None:
            if selectedDate and selectedTime:
                response = DBController.addFutureSetting(hourFrom, hourTo, dayEntry, selectedDate, selectedTime, carDropdown == 'Enabled', motorDropdown == 'Enabled', busDropdown == 'Enabled', truckDropdown == 'Enabled', float(carPrice), float(motorPrice), float(busPrice), float(truckPrice))
            else:
                response = DBController.addCurrentSetting(hourFrom, hourTo, dayEntry, carDropdown == 'Enabled', motorDropdown == 'Enabled', busDropdown == 'Enabled', truckDropdown == 'Enabled', float(carPrice), float(motorPrice), float(busPrice), float(truckPrice))
        else:
            response = DBController.editSetting(self.chosenId, hourFrom, hourTo, dayEntry, carDropdown == 'Enabled', motorDropdown == 'Enabled', busDropdown == 'Enabled', truckDropdown == 'Enabled', float(carPrice), float(motorPrice), float(busPrice), float(truckPrice), self.isCurrentSetting, startDate=selectedDate, startTime=selectedTime)

        if response.ok:
            self.s3.updateAuditLog('Update setting', f'Updated settings with new setting (starting hour={hourFrom}, ending hour={hourTo}, day-{dayEntry}, {f"starting date={selectedDate}" if selectedDate else ""}, {f"starting time={selectedTime}" if selectedTime else ""}, can detect cars?={carDropdown}, can detect motorcycles?={motorDropdown}, can detect buses?={busDropdown}, can detect trucks?={truckDropdown}, car charge={carPrice}, motorcycle charge={motorPrice}, bus charge={busPrice}, truck charge={truckPrice})', cont.currUser)
            self.statusLabel.configure(text='Setting successfully saved.', text_color="#25be8e")
            self.after(3000, lambda: self.statusLabel.configure(text_color="#1B2431"))
            self.clearInput()

            self.reloadLeftDatabase()
            self.reloadRightDatabase()
        else:
            self.statusLabel.configure(text=response.messages['error'], text_color="#d62828")
            self.after(3000, lambda: self.statusLabel.configure(text_color="#1B2431"))
    
    def selectDate_callback(self):
        top = tk.Toplevel(bg="#090E18")
        top.title("Select Date/Time")

        # Calendar for date selection
        calendarFrame = tk.Frame(top, bg="#1B2431")
        calendarFrame.pack(padx=10, pady=(10, 2), ipadx=5, ipady=5, expand=True, fill="both")
        cal = Calendar(calendarFrame, selectmode='day', date_pattern='mm/dd/y', foreground="#FFFFFF", background="#1B2431", bordercolor="#1B2431")
        cal.pack(padx=5, pady=5)

        # Frame for time selection
        frame_time = tk.Frame(top, bg="#1B2431")
        frame_time.pack(padx=10, pady=(2, 10), expand=True, fill="x")

        # Spinbox for hours selection
        label_hours = tk.Label(frame_time, text="Hours:", foreground="#FFFFFF", background="#090E18")
        label_hours.grid(row=0, column=0, padx=5, pady=5, sticky = "w")
        spinbox_hours = ttk.Spinbox(frame_time, from_=0, to=23, foreground="#FFFFFF", background="#FFFFFF")
        spinbox_hours.grid(row=0, column=1, padx=5, pady=5, sticky = "ew")

        # Spinbox for minutes selection
        label_minutes = tk.Label(frame_time, text="Minutes:", foreground="#FFFFFF", background="#090E18")
        label_minutes.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        spinbox_minutes = ttk.Spinbox(frame_time, from_=0, to=59, increment=5, foreground="#000000", background="#FFFFFF")
        spinbox_minutes.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        def getSelectedDateTime():
            global selected_date, selected_time
        
            selected_date = cal.get_date()
            selected_hour = spinbox_hours.get().zfill(2)
            selected_minute = spinbox_minutes.get().zfill(2)
            
            selected_time = f"{selected_hour}:{selected_minute}"

            top.destroy()
            self.selected_date = selected_date
            self.selected_time = selected_time
            self.dateEntry.delete(0, tk.END)
            self.dateEntry.insert(0, f"{self.selected_date}")
            self.timeEntry.delete(0, tk.END)
            self.timeEntry.insert(0, f"{self.selected_time}")

        # Button for confirming selection
        button_confirm = tk.Button(top, text="Confirm", command=getSelectedDateTime, foreground="#FFFFFF", background="#090E18")
        button_confirm.pack(pady=10)
    
    def selectDataFromTable(self, event):
        caller = event.widget
        
        # Event handler that unselects the selection from the other table if the user selects from the other table to prevent multiple selection.
        if caller == self.leftDatabaseTable and bool(self.rightDatabaseTable.selection()):
            self.rightDatabaseTable.selection_remove(self.rightDatabaseTable.selection())
            
        elif caller == self.rightDatabaseTable and bool(self.leftDatabaseTable.selection()):
            self.leftDatabaseTable.selection_remove(self.leftDatabaseTable.selection())
        
        selected_items = caller.selection()
        
        if not selected_items or len(selected_items) != 1:
            # Config Form0
            self.fromComboVal.set('')
            self.toComboVal.set('')
            self.everyComboVal.set('')
            
            # Config Form 2
            self.dateEntry.delete(0, tk.END)
            self.timeEntry.delete(0, tk.END)
            
            # Price Form
            self.truckVal.set('')
            self.busVal.set('')
            self.motorcycleVal.set('')
            self.carVal.set('')
            
            # Detectables Form
            self.truckComboVal.set('')
            self.busComboVal.set('')
            self.motorcycleComboVal.set('')
            self.carComboVal.set('')

            self.chosenId = None
            self.isCurrentSetting = None
            return
        
        # These are all the widgets that updates whenever there is a row selection from either table.
        # Config Form
        self.fromComboVal.set('')
        self.toComboVal.set('')
        self.everyComboVal.set('')
        
        # Config Form 2
        self.dateEntry.delete(0, tk.END)
        self.timeEntry.delete(0, tk.END)
        
        # Price Form
        self.truckVal.set('')
        self.busVal.set('')
        self.motorcycleVal.set('')
        self.carVal.set('')
        
        # Detectables Form
        self.truckComboVal.set('')
        self.busComboVal.set('')
        self.motorcycleComboVal.set('')
        self.carComboVal.set('')
        
        for item in selected_items:
            values = caller.item(item)['values']
            
            currDate = datetime.now().date()
            currTime = datetime.now().time()

            if caller == self.leftDatabaseTable and len(values) >= 4:
                self.clearInput()
                self.chosenId = int(values[0])
                self.isCurrentSetting = True

                setting = DBController.getCurrentSetting(self.chosenId)
                
                self.carComboVal.set('Enabled' if setting.detectCar else 'Disabled')
                self.motorcycleComboVal.set('Enabled' if setting.detectMotorcycle else 'Disabled')
                self.busComboVal.set('Enabled' if setting.detectBus else 'Disabled')
                self.truckComboVal.set('Enabled' if setting.detectTruck else 'Disabled')

                self.carVal.set(setting.carPrice)
                self.motorcycleVal.set(setting.motorcyclePrice)
                self.busVal.set(setting.busPrice)
                self.truckVal.set(setting.truckPrice)

                fromTimeStr = str(setting.hourFrom)
                fromTimeObj = datetime.strptime(fromTimeStr, '%H:%M:%S')
                fromTime = fromTimeObj.strftime('%H:%M')

                toTimeStr = str(setting.hourTo)
                toTimeObj = datetime.strptime(toTimeStr, '%H:%M:%S')
                toTime = toTimeObj.strftime('%H:%M')

                self.fromComboVal.set(fromTime)
                self.toComboVal.set(toTime)
                self.everyComboVal.set(values[3])
                
            if caller == self.rightDatabaseTable and len(values) >= 5:
                self.clearInput()
                self.chosenId = int(values[0])
                self.isCurrentSetting = False

                setting = DBController.getFutureSetting(self.chosenId)
                
                self.carComboVal.set('Enabled' if setting.detectCar else 'Disabled')
                self.motorcycleComboVal.set('Enabled' if setting.detectMotorcycle else 'Disabled')
                self.busComboVal.set('Enabled' if setting.detectBus else 'Disabled')
                self.truckComboVal.set('Enabled' if setting.detectTruck else 'Disabled')

                self.carVal.set(setting.carPrice)
                self.motorcycleVal.set(setting.motorcyclePrice)
                self.busVal.set(setting.busPrice)
                self.truckVal.set(setting.truckPrice)

                fromTimeStr = str(setting.hourFrom)
                fromTimeObj = datetime.strptime(fromTimeStr, '%H:%M:%S')
                fromTime = fromTimeObj.strftime('%H:%M')

                toTimeStr = str(setting.hourTo)
                toTimeObj = datetime.strptime(toTimeStr, '%H:%M:%S')
                toTime = toTimeObj.strftime('%H:%M')

                self.fromComboVal.set(fromTime)
                self.toComboVal.set(toTime)
                self.everyComboVal.set(values[3])

                startDateStr = str(setting.startDate)
                startDateObj = datetime.strptime(startDateStr, '%Y-%m-%d')
                startDate = startDateObj.strftime('%m/%d/%Y')

                startTimeStr = str(setting.startTime)
                startTimeObj = datetime.strptime(startTimeStr, '%H:%M:%S')
                startTime = startTimeObj.strftime('%H:%M')

                self.dateEntry.insert(0, startDate)
                self.timeEntry.insert(0, startTime)

    def applyRestrictions(self, user):
        for comboBox in [self.carComboBox, self.motorcycleComboBox, self.busComboBox, self.truckComboBox]:
            comboBox.configure(state='disabled' if not user.canChangeDetect else 'readonly')

        for entry in [self.carEntry, self.motorcycleEntry, self.busEntry, self.truckEntry]:
            entry.configure(state='disabled' if not user.canChangePrice else 'normal')

        for comboBox in [self.fromComboBox, self.toComboBox, self.everyComboBox]:
            comboBox.configure(state='disabled' if not user.canEditHours else 'readonly')

    def logout_callback(self, parent):
        self.addNew_callback()
        cont.loggedIn = False
        cont.cameraEnabled = False
        cont.currUser = None
        parent.show_frame(parent.loginFrame)
    
    def __init__(self, parent):
        self.selected_date = ''
        self.selected_time = ''
        self.chosenId = None
        self.isCurrentSetting = None
        self.s3 = S3Controller()
        
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
                                command = self.minimizeApplication)
        minimizeButton.pack(side = "right", padx = 0, pady = 10)
        
        # Start of Main Content Frame
        mainContentFrame = CTkScrollableFrame(self, fg_color = "#090E18")
        mainContentFrame.pack(fill = 'both', expand = True, side = 'top')
        
        mainTableFrame = tk.Frame(mainContentFrame, bg = '#090E18')
        mainTableFrame.pack(expand = True, fill = 'both', side = 'top', pady = (0, 0))
        
        leftMainTableFrame = CTkFrame(mainTableFrame, fg_color = '#1B2431', corner_radius = 15)
        rightMainTableFrame = CTkFrame(mainTableFrame, fg_color = '#1B2431', corner_radius = 15)
        
        leftMainTableFrame.pack(expand = True, fill = 'both', side = 'left', pady = 10, padx = 5)
        rightMainTableFrame.pack(expand = True, fill = 'both', side = 'left', pady = 10, padx = 5)
        
        leftMainTableLabelFrame = tk.Frame(leftMainTableFrame, bg = '#1B2431')
        leftMainTableLabelFrame.pack(side = 'top', expand = False, fill = 'x', pady = (10, 0))
        
        leftMainTableLabel = CTkLabel(leftMainTableLabelFrame, text = 'Current Settings', font = ('Montserrat', 12), text_color = '#FFFFFF', anchor = 'w')
        leftMainTableLabel.pack(side = 'left', padx = 10, pady = 5)
        
        leftDatabaseTableFrame = tk.Frame(leftMainTableFrame, bg = '#1B2431')
        leftDatabaseTableFrame.pack(side = 'top', expand = True, fill = 'both', pady = (0, 0), padx = 10)
        
        self.leftDatabaseTable = ttk.Treeview(leftDatabaseTableFrame, columns = ('id', 'from', 'to', 'day'), show = "headings", style = 'Custom.Treeview')
        self.leftDatabaseTable.bind('<<TreeviewSelect>>', self.selectDataFromTable)
        self.leftDatabaseTable.bind('<Delete>', self.deleteDataFromTable)
        
        self.leftDatabaseTable.tag_configure('even', background='#2A2D2E', foreground='#FFFFFF')
        self.leftDatabaseTable.tag_configure('odd', background='#343638', foreground='#FFFFFF')
        
        self.leftDatabaseTable.heading('id', text="ID", anchor='center')
        self.leftDatabaseTable.heading('from', text="From", anchor='center')
        self.leftDatabaseTable.heading('to', text="To", anchor='center')
        self.leftDatabaseTable.heading('day', text="Every", anchor='center')
        
        self.leftDatabaseTable.column('id', width=40, anchor='center')
        self.leftDatabaseTable.column('from', width=150, anchor='center')
        self.leftDatabaseTable.column('to', width=150, anchor='center')
        self.leftDatabaseTable.column('day', width=120, anchor='center')
        
        yscrollbar = ttk.Scrollbar(leftDatabaseTableFrame, orient='vertical', command=self.leftDatabaseTable.yview)
        self.leftDatabaseTable.configure(yscrollcommand=yscrollbar.set)
        
        self.leftDatabaseTable.pack(expand=True, fill='both', padx=0, pady=0, side = "left")
        yscrollbar.pack(side='left', fill='both', padx=0, pady=0)
        
        xscrollbar = ttk.Scrollbar(leftMainTableFrame, orient='horizontal', command=self.leftDatabaseTable.xview)
        self.leftDatabaseTable.configure(xscrollcommand=xscrollbar.set)
        xscrollbar.pack(side='top', fill='both', padx=10, pady=(0, 10))

        self.reloadLeftDatabase()
            
        rightMainTableLabelFrame = tk.Frame(rightMainTableFrame, bg = '#1B2431')
        rightMainTableLabelFrame.pack(side = 'top', expand = False, fill = 'x', pady = (10, 0))
        
        rightMainTableLabel = CTkLabel(rightMainTableLabelFrame, text = 'Scheduled To Be Added Settings', font = ('Montserrat', 12), text_color = '#FFFFFF', anchor = 'w')
        rightMainTableLabel.pack(side = 'left', padx = 10, pady = 5)
        
        rightDatabaseTableFrame = tk.Frame(rightMainTableFrame, bg = '#1B2431')
        rightDatabaseTableFrame.pack(side = 'top', expand = True, fill = 'both', pady = (0, 0), padx = 10)
        
        self.rightDatabaseTable = ttk.Treeview(rightDatabaseTableFrame, columns = ('id', 'from', 'to', 'day', 'startDate'), show = "headings", style = 'Custom.Treeview')
        self.rightDatabaseTable.bind('<<TreeviewSelect>>', self.selectDataFromTable)
        self.rightDatabaseTable.bind('<Delete>', self.deleteDataFromTable)
        
        self.rightDatabaseTable.tag_configure('even', background='#2A2D2E', foreground='#FFFFFF')
        self.rightDatabaseTable.tag_configure('odd', background='#343638', foreground='#FFFFFF')
        
        self.rightDatabaseTable.heading('id', text="ID", anchor='center')
        self.rightDatabaseTable.heading('from', text="From", anchor='center')
        self.rightDatabaseTable.heading('to', text="To", anchor='center')
        self.rightDatabaseTable.heading('day', text="Every", anchor='center')
        self.rightDatabaseTable.heading('startDate', text="Start Date", anchor='center')
        
        self.rightDatabaseTable.column('id', width=40, anchor='center')
        self.rightDatabaseTable.column('from', width=150, anchor='center')
        self.rightDatabaseTable.column('to', width=150, anchor='center')
        self.rightDatabaseTable.column('day', width=120, anchor='center')
        self.rightDatabaseTable.column('startDate', width=120, anchor='center')
        
        yscrollbar = ttk.Scrollbar(rightDatabaseTableFrame, orient='vertical', command=self.rightDatabaseTable.yview)
        self.rightDatabaseTable.configure(yscrollcommand=yscrollbar.set)
        
        self.rightDatabaseTable.pack(expand=True, fill='both', padx=0, pady=0, side = "left")
        yscrollbar.pack(side='left', fill='both', padx=0, pady=0)
        
        xscrollbar = ttk.Scrollbar(rightMainTableFrame, orient='horizontal', command=self.rightDatabaseTable.xview)
        self.rightDatabaseTable.configure(xscrollcommand=xscrollbar.set)
        xscrollbar.pack(side='top', fill='both', padx=10, pady=(0, 10))

        self.reloadRightDatabase()
        
        addNewFrame = tk.Frame(mainContentFrame, bg = '#090E18')
        addNewFrame.pack(expand = False, fill = 'x', side = 'top', pady = (0, 10))
        
        refreshButton = CTkButton(addNewFrame,
                                    text = 'Refresh Tables',
                                    command = self.refresh_callback,
                                    text_color = "#000000",
                                    font = ('Montserrat', 12),
                                    fg_color = "#FFFFFF",
                                    corner_radius = 15,
                                    border_color = "#FFFFFF",
                                    border_width = 2)
        refreshButton.bind("<Enter>", lambda event: refreshButton.configure(text_color="#FFFFFF", fg_color = "#090E18", border_color = "#FFFFFF")) 
        refreshButton.bind("<Leave>", lambda event: refreshButton.configure(text_color="#000000", fg_color = "#FFFFFF", border_color = "#FFFFFF"))  
        refreshButton.pack(expand = False, side = 'right', padx = 10, pady = 0)
        
        addNewButton = CTkButton(addNewFrame,
                                    text = 'Add New',
                                    command = self.addNew_callback,
                                    text_color = "#000000",
                                    font = ('Montserrat', 12),
                                    fg_color = "#FFFFFF",
                                    corner_radius = 15,
                                    border_color = "#FFFFFF",
                                    border_width = 2)
        addNewButton.bind("<Enter>", lambda event: addNewButton.configure(text_color="#FFFFFF", fg_color = "#090E18", border_color = "#FFFFFF")) 
        addNewButton.bind("<Leave>", lambda event: addNewButton.configure(text_color="#000000", fg_color = "#FFFFFF", border_color = "#FFFFFF"))  
        addNewButton.pack(expand = False, side = 'right', padx = 10, pady = 0)
        
        selectRowLabel = CTkLabel(addNewFrame,
                                    text = 'Select a row above to edit a setting or',
                                    font = ('Montserrat', 12),
                                    text_color = '#FFFFFF')
        selectRowLabel.pack(expand = False, side = 'right', padx = 5, pady = 0)
        
        delLabel = CTkLabel(addNewFrame,
                                    text = 'Press Del to delete',
                                    font = ('Montserrat', 12),
                                    text_color = '#FFFFFF')
        delLabel.pack(expand = False, side = 'left', padx = 10, pady = 0)
        
        detectablesFrame = CTkFrame(mainContentFrame, fg_color = '#1B2431', corner_radius = 15)
        detectablesFrame.pack(expand = False, fill = 'x', side = 'top', pady = 10)
        
        detectablesLabelFrame = tk.Frame(detectablesFrame, bg = '#1B2431')
        detectablesLabelFrame.pack(expand = False, fill = 'x', side = 'top', padx = 5, pady = 5)
        
        detectablesLabel = CTkLabel(detectablesLabelFrame, text = 'Detectables Vehicles', anchor = 'w', font = ('Montserrat', 12), text_color = '#FFFFFF')
        detectablesLabel.pack(expand = False, fill = 'x', side = 'left', padx = 10, pady = 5)
        
        detectablesContentFrame = tk.Frame(detectablesFrame, bg = '#1B2431')
        detectablesContentFrame.pack(expand = False, fill = 'both', side = 'top', padx = 5, pady = 5)
        
        self.carComboVal = StringVar(value='')
        self.carComboBox = CTkComboBox(detectablesContentFrame, variable=self.carComboVal, values = ['Enabled', 'Disabled'], width = 200, fg_color = '#e5e5e5', dropdown_fg_color = '#e5e5e5', text_color = '#000000', dropdown_text_color = '#000000', border_color = '#FFFFFF', button_color = '#FFFFFF', state='readonly')
        self.carComboBox.pack(side = 'right', padx = (0, 20), pady = 5)
        carLabel = CTkLabel(detectablesContentFrame, text = 'Car', anchor = 'w', font = ('Montserrat', 12), text_color = '#FFFFFF')
        carLabel.pack(side = 'right', padx = 10)
        
        self.motorcycleComboVal = StringVar(value='')
        self.motorcycleComboBox = CTkComboBox(detectablesContentFrame, variable=self.motorcycleComboVal, values = ['Enabled', 'Disabled'], width = 200, fg_color = '#e5e5e5', dropdown_fg_color = '#e5e5e5', text_color = '#000000', dropdown_text_color = '#000000', border_color = '#FFFFFF', button_color = '#FFFFFF', state='readonly')
        self.motorcycleComboBox.pack(side = 'right', padx = (0, 20), pady = 5)
        motorcycleLabel = CTkLabel(detectablesContentFrame, text = 'Motorcycle', anchor = 'w', font = ('Montserrat', 12), text_color = '#FFFFFF')
        motorcycleLabel.pack(side = 'right', padx = 10)
        
        self.busComboVal = StringVar(value='')
        self.busComboBox = CTkComboBox(detectablesContentFrame, variable=self.busComboVal, values = ['Enabled', 'Disabled'], width = 200, fg_color = '#e5e5e5', dropdown_fg_color = '#e5e5e5', text_color = '#000000', dropdown_text_color = '#000000', border_color = '#FFFFFF', button_color = '#FFFFFF', state='readonly')
        self.busComboBox.pack(side = 'right', padx = (0, 20), pady = 5)
        busLabel = CTkLabel(detectablesContentFrame, text = 'Bus', anchor = 'w', font = ('Montserrat', 12), text_color = '#FFFFFF')
        busLabel.pack(side = 'right', padx = 10)
        
        self.truckComboVal = StringVar(value='')
        self.truckComboBox = CTkComboBox(detectablesContentFrame, variable=self.truckComboVal, values = ['Enabled', 'Disabled'], width = 200, fg_color = '#e5e5e5', dropdown_fg_color = '#e5e5e5', text_color = '#000000', dropdown_text_color = '#000000', border_color = '#FFFFFF', button_color = '#FFFFFF', state='readonly')
        self.truckComboBox.pack(side = 'right', padx = (0, 20), pady = 5)
        truckLabel = CTkLabel(detectablesContentFrame, text = 'Truck', anchor = 'w', font = ('Montserrat', 12), text_color = '#FFFFFF')
        truckLabel.pack(side = 'right', padx = 10)
        
        pricePerVehicleFrame = CTkFrame(mainContentFrame, corner_radius = 15, fg_color = '#1B2431')
        pricePerVehicleFrame.pack(expand = False, fill = 'x', side = 'top', pady = 10)
        
        priceLabelFrame = tk.Frame(pricePerVehicleFrame, bg = '#1B2431')
        priceLabelFrame.pack(expand = False, fill = 'x', side = 'top', padx = 5, pady = 5)
        
        priceLabel = CTkLabel(priceLabelFrame, text = 'Price Per Vehicles Type', anchor = 'w', font = ('Montserrat', 12), text_color = '#FFFFFF')
        priceLabel.pack(expand = False, fill = 'x', side = 'left', padx = 10, pady = 5)
        
        priceContentFrame = tk.Frame(pricePerVehicleFrame, bg = '#1B2431')
        priceContentFrame.pack(expand = False, fill = 'both', side = 'top', padx = 5, pady = 5)
        
        self.carVal = StringVar(value='')
        self.carEntry = CTkEntry(priceContentFrame, textvariable=self.carVal, placeholder_text = '0.0', font = ('Montserrat', 12), text_color = '#000000', corner_radius = 15, border_color = '#FFFFFF', fg_color = '#FFFFFF')
        self.carEntry.pack(side = 'right', padx = (0, 20), pady = 5)
        carLabel = CTkLabel(priceContentFrame, text = 'Car', anchor = 'w', font = ('Montserrat', 12), text_color = '#FFFFFF')
        carLabel.pack(side = 'right', padx = 10)
        
        self.motorcycleVal = StringVar(value='')
        self.motorcycleEntry = CTkEntry(priceContentFrame, textvariable=self.motorcycleVal, placeholder_text = '0.0', font = ('Montserrat', 12), text_color = '#000000', corner_radius = 15, border_color = '#FFFFFF', fg_color = '#FFFFFF')
        self.motorcycleEntry.pack(side = 'right', padx = (0, 20), pady = 5)
        motorcycleLabel = CTkLabel(priceContentFrame, text = 'Motorcycle', anchor = 'w', font = ('Montserrat', 12), text_color = '#FFFFFF')
        motorcycleLabel.pack(side = 'right', padx = 10)
        
        self.busVal = StringVar(value='')
        self.busEntry = CTkEntry(priceContentFrame, textvariable=self.busVal, placeholder_text = '0.0', font = ('Montserrat', 12), text_color = '#000000', corner_radius = 15, border_color = '#FFFFFF', fg_color = '#FFFFFF')
        self.busEntry.pack(side = 'right', padx = (0, 20), pady = 5)
        busLabel = CTkLabel(priceContentFrame, text = 'Bus', anchor = 'w', font = ('Montserrat', 12), text_color = '#FFFFFF')
        busLabel.pack(side = 'right', padx = 10)
        
        self.truckVal = StringVar(value='')
        self.truckEntry = CTkEntry(priceContentFrame, textvariable=self.truckVal, placeholder_text = '0.0', font = ('Montserrat', 12), text_color = '#000000', corner_radius = 15, border_color = '#FFFFFF', fg_color = '#FFFFFF')
        self.truckEntry.pack(side = 'right', padx = (0, 20), pady = 5)
        truckLabel = CTkLabel(priceContentFrame, text = 'Truck', anchor = 'w', font = ('Montserrat', 12), text_color = '#FFFFFF')
        truckLabel.pack(side = 'right', padx = 10)
        
        configFrame = CTkFrame(mainContentFrame, fg_color = '#1B2431', corner_radius = 15)
        configFrame.pack(expand = False, fill = 'x', side = 'top', pady = 10)
        
        configScheduleLabelFrame = tk.Frame(configFrame, bg = '#1B2431')
        configScheduleLabelFrame.pack(expand = False, fill = 'x', side = 'top', padx = 5, pady = 5)
        
        configScheduleLabel = CTkLabel(configScheduleLabelFrame, text = 'Config Schedule', anchor = 'w', font = ('Montserrat', 12), text_color = '#FFFFFF')
        configScheduleLabel.pack(expand = False, fill = 'x', side = 'left', padx = 10, pady = 5)
        
        configContentFrame = tk.Frame(configFrame, bg = '#1B2431')
        configContentFrame.pack(side = 'top', expand = False, fill = 'both', padx = 5, pady = 5)
        
        configLeftContent = tk.Frame(configContentFrame, bg = '#1B2431')
        configLeftContent.pack(side = 'left', expand = False, fill = 'both', padx = 10)
        
        fromLabel = CTkLabel(configLeftContent, text = 'From', font = ('Montserrat', 12), anchor = 'w', text_color = '#FFFFFF')
        fromLabel.pack(side = 'left', padx = (10, 5), pady = 10)
        
        self.fromComboVal = StringVar(value='')
        self.fromComboBox = CTkComboBox(configLeftContent, variable=self.fromComboVal, values=[f'{hour:02d}:00' for hour in range(24)],
                                    width = 80,
                                    fg_color = '#e5e5e5', dropdown_fg_color = '#e5e5e5', text_color = '#000000', dropdown_text_color = '#000000', border_color = '#FFFFFF', button_color = '#FFFFFF', state='readonly')
        self.fromComboBox.pack(side = 'left', padx = (0, 10))
        
        toLabel = CTkLabel(configLeftContent, text = 'To', font = ('Montserrat', 12), anchor = 'w', text_color = '#FFFFFF')
        toLabel.pack(side = 'left', padx = (10, 5), pady = 10)
        
        self.toComboVal = StringVar(value='')
        self.toComboBox = CTkComboBox(configLeftContent, variable=self.toComboVal, values=[f'{hour:02d}:00' for hour in range(24)],
                                    width = 80,
                                    fg_color = '#e5e5e5', dropdown_fg_color = '#e5e5e5', text_color = '#000000', dropdown_text_color = '#000000', border_color = '#FFFFFF', button_color = '#FFFFFF', state='readonly')
        self.toComboBox.pack(side = 'left', padx = (0, 10))
        
        everyLabel = CTkLabel(configLeftContent, text = 'Every', font = ('Montserrat', 12), anchor = 'w', text_color = '#FFFFFF')
        everyLabel.pack(side = 'left', padx = (10, 5), pady = 10)
        
        self.everyComboVal = StringVar(value='')
        self.everyComboBox = CTkComboBox(configLeftContent,
                                    variable=self.everyComboVal, values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                                            "Saturday", "Sunday"],
                                    width = 200,
                                    fg_color = '#e5e5e5', dropdown_fg_color = '#e5e5e5', text_color = '#000000', dropdown_text_color = '#000000', border_color = '#FFFFFF', button_color = '#FFFFFF', state='readonly')
        self.everyComboBox.pack(side = 'left', padx = (0, 10))
        
        configRightContent = tk.Frame(configContentFrame, bg = '#1B2431')
        configRightContent.pack(side = 'right', expand = False, fill = 'both', padx = 10)
        
        configRightFirst = tk.Frame(configRightContent, bg = '#1B2431')
        configRightFirst.pack(side = 'top', fill = 'x')
        
        selectDateButton = CTkButton(configRightFirst,
                                    text = 'Select Date & Time',
                                    command = self.selectDate_callback,
                                    text_color = "#000000",
                                    font = ('Montserrat', 12),
                                    fg_color = "#FFFFFF",
                                    corner_radius = 15,
                                    border_color = "#FFFFFF",
                                    border_width = 2)
        selectDateButton.bind("<Enter>", lambda event: selectDateButton.configure(text_color="#FFFFFF", fg_color = "#1B2431", border_color = "#FFFFFF")) 
        selectDateButton.bind("<Leave>", lambda event: selectDateButton.configure(text_color="#000000", fg_color = "#FFFFFF", border_color = "#FFFFFF"))  
        selectDateButton.pack(expand = False, side = 'right', padx = 10, pady = 10)
        
        self.timeEntry = CTkEntry(configRightFirst, placeholder_text = 'HH:MM', corner_radius = 15, border_color = '#FFFFFF', fg_color = '#FFFFFF', text_color = '#000000', font = ('Montserrat', 12))
        self.timeEntry.pack(side = 'right', padx = 10, pady = 10)
        
        self.dateEntry = CTkEntry(configRightFirst, placeholder_text = 'DD/MM/YYYY', corner_radius = 15, border_color = '#FFFFFF', fg_color = '#FFFFFF', text_color = '#000000', font = ('Montserrat', 12))
        self.dateEntry.pack(side = 'right', padx = 10, pady = 10)
        
        startingLabel = CTkLabel(configRightFirst, text = 'Starting', font = ('Montserrat', 12), text_color = '#FFFFFF')
        startingLabel.pack(side = 'right', padx = 10, pady = 10)
        
        configRightSecond = tk.Frame(configRightContent, bg = '#1B2431')
        configRightSecond.pack(side = 'top', fill = 'x')
        
        infoLabel = CTkLabel(configRightSecond, text = 'Leave blank if going to apply immediately', font = ('Montserrat', 10, 'italic'), text_color = '#FFFFFF')
        infoLabel.pack(side = 'top', fill = 'x', expand = True)

        status = tk.Frame(configRightContent, bg = '#1B2431')
        self.statusLabel = CTkLabel(status, text='Settings saved.', font = ('Monteserrat', 13, 'italic'), anchor = "w", text_color = "#1B2431")

        status.pack(side = 'right', expand = False, fill = 'both', padx = 10)
        self.statusLabel.pack(side='left', pady = 10, expand = True, fill = "x")
        
        applicationFrame = tk.Frame(mainContentFrame, bg = '#090E18')
        applicationFrame.pack(expand = False, fill = 'x', pady = 10)
        
        addUpdateButton = CTkButton(applicationFrame,
                                    text = 'Save',
                                    font = ('Montserrat', 12),
                                    text_color = '#000000',
                                    fg_color = '#FFFFFF',
                                    border_color = '#FFFFFF',
                                    border_width = 2,
                                    corner_radius = 15,
                                    command = self.addUpdateButton_callback)
        addUpdateButton.bind("<Enter>", lambda event: addUpdateButton.configure(text_color="#FFFFFF", fg_color = "#090E18", border_color = "#FFFFFF")) 
        addUpdateButton.bind("<Leave>", lambda event: addUpdateButton.configure(text_color="#000000", fg_color = "#FFFFFF", border_color = "#FFFFFF"))  
        addUpdateButton.pack(expand = False, side = 'right', padx = 10, pady = 10)
        
        cancelButton = CTkButton(applicationFrame,
                                    text = 'Cancel',
                                    font = ('Montserrat', 12),
                                    text_color = '#000000',
                                    fg_color = '#FFFFFF',
                                    border_color = '#FFFFFF',
                                    border_width = 2,
                                    corner_radius = 15,
                                    command = self.cancelButton_callback)
        cancelButton.bind("<Enter>", lambda event: cancelButton.configure(text_color="#FFFFFF", fg_color = "#090E18", border_color = "#FFFFFF")) 
        cancelButton.bind("<Leave>", lambda event: cancelButton.configure(text_color="#000000", fg_color = "#FFFFFF", border_color = "#FFFFFF"))  
        cancelButton.pack(expand = False, side = 'right', padx = 10, pady = 10)
        # End of Main Content Frame
        
        # Start of Navigation Frame (Bottom)
        navigationFrame = tk.Frame(self, bg = '#090E18')
        navigationFrame.pack(fill = 'both', side = 'bottom')
        
        dashboardButton = CTkButton(navigationFrame,
                            text = 'Dashboard',
                            command = lambda: switch.showDashboardPage(parent), 
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
        logoutButton = CTkButton(navigationFrame,
                                text = 'Logout',
                                command = lambda: self.logout_callback(parent), 
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
        
        dashboardButton.pack(side = 'right', padx = 10, pady = 10)
        logoutButton.pack(side = 'right', padx = 10, pady = 10)
        
        # Config Form
        self.fromComboBox.set('')
        self.toComboBox.set('')
        self.everyComboBox.set('')
        
        # Detectables Form
        self.truckComboBox.set('')
        self.busComboBox.set('')
        self.motorcycleComboBox.set('')
        self.carComboBox.set('')