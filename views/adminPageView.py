import os
import sys
import datetime
import tkinter as tk
import tk_async_execute as tk_async

current = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current)
sys.path.append(parent_dir)

import views.switchView as switch
import controllers.controller as cont

from customtkinter import *
from tkinter import ttk
from tkcalendar import Calendar
from PIL import Image
from controllers.dbController import DBController
from controllers.rtspController import RTSPController
from controllers.s3controller import S3Controller
from controllers.googleController import GoogleController
from views.tooltip import ToolTip as tt

class AdminPage(tk.Frame):
    # Close Application
    def closeApplication(self):
        self.master.destroy()

    # Minimize or Iconify the Application
    def minimizeApplicaiton(self):
        self.master.iconify()
    
    # Select User Dropwdown Function
    def selectUserCombo_callback(self, choice):
        user = DBController.getUser(username=choice)
        self.firstNameVar.set(user.firstName)
        self.lastNameVar.set(user.lastName)
        self.emailVar.set(user.email)
        self.usernameVar.set(user.username)
        self.adminVar.set(1 if user.isAdmin else 2)
        self.changePriceVar.set(1 if user.canChangePrice else 2)
        self.downloadRadioVar.set(1 if user.canDownload else 2)
        self.detectableRadioVar.set(1 if user.canChangeDetect else 2)
        self.activeHoursRadioVar.set(1 if user.canEditHours else 2)
    
    # Clear the field button
    def clearFieldButton_callback(self):
        self.firstNameVar.set('')
        self.lastNameVar.set('')
        self.emailVar.set('')
        self.passwordVar.set('')
        self.usernameVar.set('')
        self.selectUserComboVar.set("")
        self.adminVar.set(0)
        self.changePriceVar.set(0)
        self.downloadRadioVar.set(0)
        self.detectableRadioVar.set(0)
        self.activeHoursRadioVar.set(0)
    
    # Add the new user button
    def addUserButton_callback(self):
        firstName = self.firstNameVar.get()
        lastName = self.lastNameVar.get()
        email = self.emailVar.get()
        username = self.usernameVar.get()
        password = self.passwordVar.get()
        confirmPassword = self.confirmPasswordVar.get()

        isAdmin = self.adminVar.get() != 0
        canChangePrice = self.changePriceVar.get() != 0
        canDownload = self.downloadRadioVar.get() != 0
        canChangeDetect = self.detectableRadioVar.get() != 0
        canEditHours = self.activeHoursRadioVar.get() != 0

        if not firstName or not lastName or not email or not username or not password or not confirmPassword or not isAdmin or not canChangePrice or not canDownload or not canChangeDetect or not canEditHours:
            self.editUserStatusLabel.configure(text='Incomplete fields.', text_color="#d62828")
            self.after(2000, lambda: self.editUserStatusLabel.configure(text_color="#1B2431"))
            return
        
        if password != confirmPassword:
            self.editUserStatusLabel.configure(text='Passwords does not match.', text_color="#d62828")
            self.after(2000, lambda: self.editUserStatusLabel.configure(text_color="#1B2431"))
            return
        
        isAdmin = self.adminVar.get() == 1
        canChangePrice = self.changePriceVar.get() == 1
        canDownload = self.downloadRadioVar.get() == 1
        canChangeDetect = self.detectableRadioVar.get() == 1
        canEditHours = self.activeHoursRadioVar.get() == 1
        
        response = DBController.registerUser(email, username, firstName, lastName, password, isAdmin, canChangePrice, canDownload, canChangeDetect, canEditHours)

        if response.ok:
            self.editUserStatusLabel.configure(text='User successfully edited.', text_color='#25be8e')
            self.after(3000, lambda: self.editUserStatusLabel.configure(text_color='#1b2431'))
            users = DBController.getUsers()
            self.selectUserCombo.configure(values=[user[0].username for user in users.data])
            self.clearFieldButton_callback()
            self.s3.updateAuditLog('Register user', f'Registered new user (email={email}, username={username}, full name={f"{firstName} {lastName}"}, is admin?={isAdmin}, can change vehicle price?={canChangePrice}, can download CSV?={canDownload}, can change vehicles to detect?={canChangeDetect}, can edit hours in settings?={canEditHours})', cont.currUser)
        else:
            self.editUserStatusLabel.configure(text=(response.messages['email'] or response.messages['username'] or response.messages['error']), text_color="#d62828")
            self.after(2000, lambda: self.editUserStatusLabel.configure(text_color="#1B2431"))
    
    # Apply changes to the field
    def applyUserButton_callback(self):
        user = self.selectUserCombo.get()
        firstName = self.firstNameVar.get()
        lastName = self.lastNameVar.get()
        email = self.emailVar.get()
        username = self.usernameVar.get()
        password = self.passwordVar.get()

        isAdmin = self.adminVar.get() == 1
        canChangePrice = self.changePriceVar.get() == 1
        canDownload = self.downloadRadioVar.get() == 1
        canChangeDetect = self.detectableRadioVar.get() == 1
        canEditHours = self.activeHoursRadioVar.get() == 1

        if not user or not firstName or not lastName or not email or not username or not password:
            self.editUserStatusLabel.configure(text='Incomplete fields.', text_color="#d62828")
            self.after(2000, lambda: self.editUserStatusLabel.configure(text_color="#1B2431"))
            return
        
        response = DBController.editUser(user, username, email, firstName, lastName, password, isAdmin, canChangeDetect, canChangePrice, canEditHours, canDownload)

        if response.ok:
            self.editUserStatusLabel.configure(text='User successfully updated.', text_color='#25be8e')
            self.after(3000, lambda: self.editUserStatusLabel.configure(text_color='#1b2431'))
            users = DBController.getUsers()
            self.selectUserCombo.configure(values=[user[0].username for user in users.data])
            self.clearFieldButton_callback()
            self.s3.updateAuditLog('Edit user', f'Edited new user (old username={user}, email={email}, new username={username}, full name={f"{firstName} {lastName}"}, is admin?={isAdmin}, can change vehicle price?={canChangePrice}, can download CSV?={canDownload}, can change vehicles to detect?={canChangeDetect}, can edit hours in settings?={canEditHours})', cont.currUser)
        else:
            self.editUserStatusLabel.configure(text=(response.messages['email'] or response.messages['username'] or response.messages['error']), text_color="#d62828")
            self.after(2000, lambda: self.editUserStatusLabel.configure(text_color="#1B2431"))
    
    # Delete the user once selected
    def deleteUserButton_callback(self):
        user = self.selectUserComboVar.get()

        if not user:
            self.editUserStatusLabel.configure(text='Incomplete fields.', text_color="#d62828")
            self.after(2000, lambda: self.editUserStatusLabel.configure(text_color="#1B2431"))
            return

        response = DBController.deleteUser(username=user)

        if response.ok:
            self.editUserStatusLabel.configure(text='User successfully deleted.', text_color='#25be8e')
            self.after(3000, lambda: self.editUserStatusLabel.configure(text_color='#1b2431'))
            users = DBController.getUsers()
            self.selectUserCombo.configure(values=[user[0].username for user in users.data])
            self.clearFieldButton_callback()
            self.s3.updateAuditLog('Delete user', f'Deleted registered user (username={user})', cont.currUser)
        else:
            self.editUserStatusLabel.configure(text=response.messages['error'], text_color="#d62828")
            self.after(2000, lambda: self.editUserStatusLabel.configure(text_color="#1B2431"))
    
    # Apply admin restriction to user
    def adminRadioButton_callback(self):
        if self.adminVar.get() == 1:
            self.changePriceVar.set(1)
            self.downloadRadioVar.set(1)
            self.detectableRadioVar.set(1)
            self.activeHoursRadioVar.set(1)
    
    # Apply change price restriction to user
    def changePriceRadioButton_callback(self):
        if self.adminVar.get() == 1:
            self.adminVar.set(2)
    
    # Apply change active hours restriction to user
    def changeActiveHoursRadioButton_callback(self):
        if self.adminVar.get() == 1:
            self.adminVar.set(2)
    
    # Apply change detectable vehicles restriction to user
    def changeDetectableRadioButton_callback(self):
        if self.adminVar.get() == 1:
            self.adminVar.set(2)
    
    # Apply download csv restriction to user
    def downloadCSVRadioButton_callback(self):
        if self.adminVar.get() == 1:
            self.adminVar.set(2)
    
    def selectDateTime(self):
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

        def getSelectedDateTime():
            global selected_date, selected_hour_from, selected_hour_to
            
            self.selected_date = cal.get_date()
            self.selected_hour = spinbox_hours.get()
            self.selected_hour_from = f"{self.selected_hour}:00"
            self.selected_hour_to = f"{self.selected_hour}:59"
            
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
        vehicleType = self.vehicleTypeComboVar.get()
        selectedDate = self.selected_date
        hourFrom = self.selected_hour_from
        hourTo = self.selected_hour_to

        if selectedDate and len(hourFrom) <= 3:
            self.filterStatusLabel.configure(text='Invalid hours.', text_color="#d62828")
            self.after(2000, lambda: self.filterStatusLabel.configure(text_color="#1B2431"))
            return
        
        for row in self.databaseTable.get_children():
            self.databaseTable.delete(row)

        date = datetime.datetime.strptime(selectedDate, '%m/%d/%Y').date() if selectedDate else None
        hourFrom = datetime.datetime.strptime(hourFrom, '%H:%M').time() if selectedDate else None
        hourTo = datetime.datetime.strptime(hourTo, '%H:%M').time() if selectedDate else None

        self.prevVehicleType = vehicleType
        self.prevDate = date
        self.prevHourFrom = hourFrom
        self.prevHourTo = hourTo

        filterResponse = DBController.getFilteredLicensePlates(vehicleType=vehicleType.lower(), date=date, hourFrom=hourFrom, hourTo=hourTo)
        
        if filterResponse.ok:
            self.filterStatusLabel.configure(text='Filter applied.', text_color="#25be8e")
            self.after(3000, lambda: self.filterStatusLabel.configure(text_color="#1B2431"))

            for row in filterResponse.data:
                self.databaseTable.insert('', 'end', values=(row[0].licenseNumber, row[0].vehicleType, row[0].location, row[0].time, row[0].date, row[0].price))
        else:
            self.filterStatusLabel.configure(text=filterResponse.messages['error'], text_color="#d62828")
            self.after(2000, lambda: self.filterStatusLabel.configure(text_color="#1B2431"))

        self.clearFilter_callback()
    
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
                self.licensePlate = values[0]
                self.licensePlateEntry.insert(0, values[0])
                self.vehicleTypeEntry.insert(0, values[1])
                self.priceEntry.insert(0, values[5])

    async def searchCameras(self):
        for ip, _ in RTSPController.scanNetwork():
            if RTSPController.checkRtsp(ip=ip) and RTSPController.validateRtsp(ip=ip) and not DBController.cameraExists(ip_addr=ip):
                self.ip_cameras.add(ip)
        
    async def discoverCameras(self):
        tk_async.tk_execute(self.discoverCameraButton.configure, state='disabled', text='Discovering Cameras...')
        tk_async.tk_execute(self.discoveredCamerasDrop.configure, state='disabled', values=[''])
        tk_async.tk_execute(self.discoveredCamerasDrop.set, '')
        tk_async.tk_execute(self.addCameraButton.configure, state='disabled')

        await self.searchCameras()

        tk_async.tk_execute(self.discoverCameraButton.configure, state='normal', text='Discover Cameras')
        tk_async.tk_execute(self.discoveredCamerasDrop.configure, state='readonly', values=list(self.ip_cameras))
        tk_async.tk_execute(self.discoveredCamerasDrop.set, '')
        tk_async.tk_execute(self.addCameraButton.configure, state='normal')

        if self.ip_cameras:
            tk_async.tk_execute(self.addCameraStatusLabel.configure, text='New IP camera(s)', text_color='#25be8e')
            self.s3.updateAuditLog('Discover camera', 'Discovered new IP camera(s)', cont.currUser)
        else:
            tk_async.tk_execute(self.addCameraStatusLabel.configure, text='No IP cameras found.', text_color='#d62828')
            self.s3.updateAuditLog('Discover camera', 'Did not discover new IP cameras', cont.currUser)

    def discoverCameras_callback(self):
        tk_async.async_execute(self.discoverCameras(), visible=False)
        self.after(2000, lambda: self.addCameraStatusLabel.configure(text_color='#1B2431'))

    def addCamera_callback(self):
        cameraIpAddr = self.discoveredCamerasDrop.get()
        cameraName = self.assignID.get()
        cameraLocation = self.assignLocation.get()
        firstLat = self.firstCoordinateNEntry.get()
        firstLng = self.firstCoordinateEEntry.get()
        secondLat = self.secondCoordinateNEntry.get()
        secondLng = self.secondCoordinateEEntry.get()

        if not cameraIpAddr or not cameraName or not cameraLocation or not firstLat or not firstLng or not secondLat or not secondLng:
            self.addCameraStatusLabel.configure(text='Incomplete fields.', text_color="#d62828")
            self.after(2000, lambda: self.addCameraStatusLabel.configure(text_color="#1B2431"))
            return
        
        originCoords = f'{firstLat}, {firstLng}'
        destCoords = f'{secondLat}, {secondLng}'
        
        googleResponse = GoogleController.getDistanceMatrix(originCoords, destCoords)

        if 'error' in googleResponse:
            self.addCameraStatusLabel.configure(text=googleResponse['error'], text_color="#d62828")
            self.after(2000, lambda: self.addCameraStatusLabel.configure(text_color="#1B2431"))
            return

        response = DBController.registerCamera(ip_addr=cameraIpAddr, name=cameraName, location=cameraLocation, originCoords=originCoords, destCoords=destCoords)

        if response.ok:
            self.addCameraStatusLabel.configure(text='Camera successfully added.', text_color="#25be8e")
            self.after(3000, lambda: self.addCameraStatusLabel.configure(text_color="#1B2431"))
            cameras = DBController.getCameras()
            values = [camera[0].name for camera in cameras.data]
            self.savedCamerasDrop.set('')
            self.savedCamerasDrop.configure(values=values)
            self.ip_cameras.remove(cameraIpAddr)
            self.discoveredCamerasDrop.set('')
            self.discoveredCamerasDrop.configure(values=list(self.ip_cameras))
            self.changeCameraDisplay.set('(NONE)')
            self.changeCameraDisplay.configure(values=values)
            self.s3.updateAuditLog('Register camera', f'Registered new camera (name={cameraName}, location={cameraLocation})', cont.currUser)
            if self.cap:
                self.cap.release()
                self.placeholder_label.configure(text='(Change cameras below)')
        else:
            self.addCameraStatusLabel.configure(text=response.messages['error'], text_color="#d62828")
            self.after(2000, lambda: self.addCameraStatusLabel.configure(text_color="#1B2431"))

        self.assignID.delete(0, 'end')
        self.assignLocation.delete(0, 'end')
        self.assignLocation.delete(0, 'end')
        self.firstCoordinateNEntry.delete(0, 'end')
        self.firstCoordinateEEntry.delete(0, 'end')
        self.secondCoordinateNEntry.delete(0, 'end')
        self.secondCoordinateEEntry.delete(0, 'end')

    def savedCamerasDropCallback(self, choice):
        camera = DBController.getCamera(name=choice)
        firstLat, firstLng = camera.originCoords.split(', ')
        secondLat, secondLng = camera.destCoords.split(', ')
        self.savedCameraNameVar.set(camera.name)
        self.savedCameraLocationVar.set(camera.location)
        self.firstLatEntryVar.set(firstLat)
        self.firstLngEntryVar.set(firstLng)
        self.secondLatEntryVar.set(secondLat)
        self.secondLngEntryVar.set(secondLng)
    
    def updateSavedCamera_callback(self):
        cameraOldName = self.savedCamerasDrop.get()
        cameraNewName = self.savedCameraID.get()
        cameraNewLocation = self.savedCameraLocation.get()
        firstLat = self.savedFirstCoordinateNEntry.get()
        firstLng = self.savedFirstCoordinateEEntry.get()
        secondLat = self.savedSecondCoordinateNEntry.get()
        secondLng = self.savedSecondCoordinateEEntry.get()

        if not cameraOldName:
            self.secondRowStatusLabel.configure(text='No camera chosen.', text_color="#d62828")
            self.after(2000, lambda: self.secondRowStatusLabel.configure(text_color="#1B2431"))
            return
        
        if not cameraNewName or not cameraNewLocation or not firstLat or not firstLng or not secondLat or not secondLng:
            self.secondRowStatusLabel.configure(text='Incomplete field(s).', text_color="#d62828")
            self.after(2000, lambda: self.secondRowStatusLabel.configure(text_color="#1B2431"))
            return
        
        originCoords = f'{firstLat}, {firstLng}'
        destCoords = f'{secondLat}, {secondLng}'
        
        googleResponse = GoogleController.getDistanceMatrix(originCoords, destCoords)

        if 'error' in googleResponse:
            self.secondRowStatusLabel.configure(text=googleResponse['error'], text_color="#d62828")
            self.after(2000, lambda: self.secondRowStatusLabel.configure(text_color="#1B2431"))
            return
        
        response = DBController.editCamera(oldName=cameraOldName, newName=cameraNewName, newLocation=cameraNewLocation, newOriginCoords=originCoords, newDestCoords=destCoords)

        if response.ok:
            self.secondRowStatusLabel.configure(text='Camera successfully updated.', text_color='#25be8e')
            self.after(3000, lambda: self.secondRowStatusLabel.configure(text_color='#1b2431'))
            cameras = DBController.getCameras()
            values = [camera[0].name for camera in cameras.data]
            self.savedCamerasDrop.set('')
            self.savedCamerasDrop.configure(values=values)
            self.changeCameraDisplay.set('(NONE)')
            self.changeCameraDisplay.configure(values=values)
            self.s3.updateAuditLog('Edit camera', f'Edited registered camera (old name={cameraOldName}, new name={cameraNewName}, new location={cameraNewLocation})', cont.currUser)
            if self.cap:
                self.cap.release()
                self.placeholder_label.configure(text='(Change cameras below)')
        else:
            self.secondRowStatusLabel.configure(text=response.messages['error'], text_color="#d62828")
            self.after(2000, lambda: self.secondRowStatusLabel.configure(text_color="#1B2431"))

        self.savedCamerasDrop.set('')
        self.savedCameraID.delete(0, 'end')
        self.savedCameraLocation.delete(0, 'end')
        self.firstLatEntryVar.set('')
        self.firstLngEntryVar.set('')
        self.secondLatEntryVar.set('')
        self.secondLngEntryVar.set('')

    def deleteSavedCamera_callback(self):
        cameraToDelete = self.savedCamerasDrop.get()

        if not cameraToDelete:
            self.secondRowStatusLabel.configure(text='No camera chosen.', text_color='#d62828')
            self.after(2000, lambda: self.secondRowStatusLabel.configure(text_color='#1b2431'))
            return
        
        response = DBController.deleteCamera(name=cameraToDelete)

        if response.ok:
            self.secondRowStatusLabel.configure(text='Camera successfully deleted.', text_color='#25be8e')
            self.after(3000, lambda: self.secondRowStatusLabel.configure(text_color='#1b2431'))
            cameras = DBController.getCameras()
            values = [camera[0].name for camera in cameras.data]
            self.savedCamerasDrop.set('')
            self.savedCamerasDrop.configure(values=values)
            self.changeCameraDisplay.set('(NONE)')
            self.changeCameraDisplay.configure(values=values)
            self.s3.updateAuditLog('Delete camera', f'Deleted registered camera (name={cameraToDelete})', cont.currUser)
            if self.cap:
                self.cap.release()
                self.placeholder_label.configure(text='(Change cameras below)')
        else:
            self.secondRowStatusLabel.configure(text=response.messages['error'], text_color="#d62828")
            self.after(2000, lambda: self.secondRowStatusLabel.configure(text_color="#1B2431"))

        self.savedCamerasDrop.set('')
        self.savedCameraID.delete(0, 'end')
        self.savedCameraLocation.delete(0, 'end')
        self.firstLatEntryVar.set('')
        self.firstLngEntryVar.set('')
        self.secondLatEntryVar.set('')
        self.secondLngEntryVar.set('')
    
    def updateTable_callback(self):
        def isPositiveFloat(s: str) -> bool:
            try:
                n = float(s)
                return n >= 0
            except:
                return False

        licensePlate = self.licensePlate
        newLicensePlate = self.licensePlateEntry.get()
        newVehicleType = self.vehicleTypeEntry.get()
        newPrice = self.priceEntry.get()

        if not newLicensePlate or not newVehicleType or not newPrice:
            self.updateStatusLabel.configure(text='No camera chosen.', text_color='#d62828')
            self.after(2000, lambda: self.updateStatusLabel.configure(text_color='#1b2431'))
            return
        
        if newVehicleType.lower() not in {'car', 'motorcycle', 'bus', 'truck'}:
            self.updateStatusLabel.configure(text='Invalid vehicle type.', text_color='#d62828')
            self.after(2000, lambda: self.updateStatusLabel.configure(text_color='#1b2431'))
            return
        
        if not isPositiveFloat(newPrice):
            self.updateStatusLabel.configure(text='Invalid price.', text_color='#d62828')
            self.after(2000, lambda: self.updateStatusLabel.configure(text_color='#1b2431'))
            return
        
        response = DBController.editLicensePlate(licensePlate, newLicensePlate, newVehicleType.lower(), newPrice)

        if response.ok:
            self.updateStatusLabel.configure(text='Successfully updated.', text_color='#25be8e')
            self.after(3000, lambda: self.updateStatusLabel.configure(text_color='#1b2431'))
            self.s3.updateAuditLog('Edit detected license plate', f'Edited detected license plate (old license plate={licensePlate}, new license plate={newLicensePlate}, new vehicle type={newVehicleType.lower()}, new price={newPrice})', cont.currUser)
            for row in self.databaseTable.get_children():
                self.databaseTable.delete(row)

            filterResponse = DBController.getFilteredLicensePlates(vehicleType=self.prevVehicleType.lower(), date=self.prevDate, hourFrom=self.prevHourFrom, hourTo=self.prevHourTo)
            
            if filterResponse.ok:
                for row in filterResponse.data:
                    self.databaseTable.insert('', 'end', values=(row[0].licenseNumber, row[0].vehicleType, row[0].cameraId, row[0].time, row[0].date, row[0].price))
        else:
            self.updateStatusLabel.configure(text=response.messages['error'], text_color="#d62828")
            self.after(2000, lambda: self.updateStatusLabel.configure(text_color="#1B2431"))

        self.licensePlateEntry.delete(0, 'end')
        self.vehicleTypeEntry.delete(0, 'end')
        self.priceEntry.delete(0, 'end')
    
    def setCameraDisplay(self, changeCameraDisplay, cap, placeholder_label):
        self.changeCameraDisplay = changeCameraDisplay
        self.placeholder_label = placeholder_label
        self.cap = cap
        
    def __init__(self, parent):
        self.ip_cameras = set()
        self.changeCameraDisplay = None
        self.placeholder_label = None
        self.cap = None
        self.s3 = S3Controller()

        tk.Frame.__init__(self, parent, bg = "#090E18")
        
        style = ttk.Style()
        style.theme_use('forest-dark')
        
        self.selected_date = ""
        self.selected_hour_from = ""
        self.selected_hour_to = ""
        
        # Close Icon (Currently Set to darkmode, if possible change to lightmode when the the changes)
        closePhoto = CTkImage(light_image = Image.open(os.path.join(parent_dir, "views/icons/icon_close_darkmode.png")),
                              dark_image = Image.open(os.path.join(parent_dir, "views/icons/icon_close_darkmode.png")),
                              size = (20, 20))

        # Minimize Icon (Currently Set to darkmode, if possible change to lightmode when the the changes)
        minimizePhoto = CTkImage(light_image = Image.open(os.path.join(parent_dir, "views/icons/icon_minimize_darkmode.png")),
                              dark_image = Image.open(os.path.join(parent_dir, "views/icons/icon_minimize_darkmode.png")),
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
        self.discoverCameraButton = CTkButton(manageCamerasFirstRow, text = "Discover Cameras", font = ('Montserrat', 12, 'bold'), fg_color = "#FFFFFF", text_color = "#000000", corner_radius = 5, command = self.discoverCameras_callback)
        self.discoveredCamerasDrop = CTkComboBox(manageCamerasFirstRow, values = [], font = ('Montserrat', 12), fg_color = "#FFFFFF", dropdown_fg_color = "#FFFFFF", dropdown_text_color = "#000000", border_color = "#FFFFFF", button_color = "#FFFFFF", text_color = "#000000", state='readonly')
        self.assignID = CTkEntry(manageCamerasFirstRow, placeholder_text = "Assign Name", font = ('Montserrat', 12, 'bold'), fg_color = "#FFFFFF", text_color = "#000000", corner_radius = 5)
        self.addCameraButton = CTkButton(manageCamerasFirstRow, text = "Add Camera", fg_color = "#FFFFFF", text_color = "#000000", corner_radius = 5, font = ('Montserrat', 12, 'bold'), command = self.addCamera_callback)
        self.assignLocation = CTkEntry(manageCamerasFirstRow, placeholder_text = "Assign Location", font = ('Montserrat', 12, 'bold'), fg_color = "#FFFFFF", text_color = "#000000", corner_radius = 5)
        
        manageCamerasFirstRowCoordFrame = tk.Frame(upperLeftContent, bg="#1B2431")
        tooltipImage = CTkImage(light_image = Image.open(os.path.join(parent_dir, "views/icons/icons_info.png")),
                            dark_image = Image.open(os.path.join(parent_dir, "views/icons/icons_info.png")),
                            size = (15, 15))
        tooltipLabel = CTkLabel(manageCamerasFirstRowCoordFrame, image=tooltipImage, text = "")
        tooltipLabel.image = tooltipImage
        self.tooltip = tt(tooltipLabel, "Coordinates are used for the Dynamic Congestion Pricing Window Setting. The 2 Coordinates must be 500 meters apart. Leave blank if not going to use.", bg = "#FFFFFF", fg = "#000000")
        self.firstCoordinateNEntry = CTkEntry(manageCamerasFirstRowCoordFrame, placeholder_text = "First Coordinate N", font = ('Montserrat', 12, 'bold'), fg_color = "#FFFFFF", text_color = "#000000", corner_radius = 5)
        self.firstCoordinateEEntry = CTkEntry(manageCamerasFirstRowCoordFrame, placeholder_text = "First Coordinate E", font = ('Montserrat', 12, 'bold'), fg_color = "#FFFFFF", text_color = "#000000", corner_radius = 5)
        self.secondCoordinateNEntry = CTkEntry(manageCamerasFirstRowCoordFrame, placeholder_text = "Second Coordinate N", font = ('Montserrat', 12, 'bold'), fg_color = "#FFFFFF", text_color = "#000000", corner_radius = 5)
        self.secondCoordinateEEntry = CTkEntry(manageCamerasFirstRowCoordFrame, placeholder_text = "Second Coordinate E", font = ('Montserrat', 12, 'bold'), fg_color = "#FFFFFF", text_color = "#000000", corner_radius = 5)

        manageCamerasFirstRowStatus = tk.Frame(upperLeftContent, bg="#1B2431")
        self.addCameraStatusLabel = CTkLabel(manageCamerasFirstRowStatus, text='Camera successfully added.', font = ('Monteserrat', 13, 'italic'), anchor = "w", text_color = "#1B2431")

        manageCamerasLabel = CTkLabel(upperLeftContent, text = "Manage Cameras", font = ('Montserrat', 12, 'bold'), anchor = "w", text_color = "#FFFFFF")
        
        cameras = DBController.getCameras()

        manageCamerasSecondRow = tk.Frame(upperLeftContent, bg = "#1B2431")
        
        self.savedCamerasDrop = CTkComboBox(manageCamerasSecondRow, values=[camera[0].name for camera in cameras.data], font = ('Montserrat', 12), fg_color = "#FFFFFF", dropdown_fg_color = "#FFFFFF", dropdown_text_color = "#000000", border_color = "#FFFFFF", button_color = "#FFFFFF", text_color = "#000000", state='readonly', command=self.savedCamerasDropCallback)
        # Used for Testing without connection to DB
        # self.savedCamerasDrop = CTkComboBox(manageCamerasSecondRow, values=['(NONE)'], font = ('Montserrat', 12), fg_color = "#FFFFFF", dropdown_fg_color = "#FFFFFF", dropdown_text_color = "#000000", border_color = "#FFFFFF", button_color = "#FFFFFF", text_color = "#000000", state='readonly')
        self.savedCameraNameVar = StringVar(value='')
        self.savedCameraLocationVar = StringVar(value='')
        self.savedCameraID = CTkEntry(manageCamerasSecondRow, textvariable=self.savedCameraNameVar, placeholder_text = "Change Name", font = ('Montserrat', 12, 'bold'), fg_color = "#FFFFFF", text_color = "#000000", corner_radius = 5)
        self.savedCameraLocation = CTkEntry(manageCamerasSecondRow, textvariable=self.savedCameraLocationVar, placeholder_text = "Change Location", font = ('Montserrat', 12, 'bold'), fg_color = "#FFFFFF", text_color = "#000000", corner_radius = 5)
        
        updateSavedCameraButton = CTkButton(manageCamerasSecondRow, text = "Update Camera", font = ('Montserrat', 12, 'bold'), fg_color = "#FFFFFF", text_color = "#000000", corner_radius = 5, command = self.updateSavedCamera_callback)
        deleteSavedCameraButton = CTkButton(manageCamerasSecondRow, text = "Delete Camera", font = ('Montserrat', 12, 'bold'), fg_color = "#D62828", text_color = "#FFFFFF", corner_radius = 5, command = self.deleteSavedCamera_callback)
        
        manageCamerasSecondRowCoordFrame = tk.Frame(upperLeftContent, bg="#1B2431")
        self.firstLatEntryVar = StringVar(value='')
        self.firstLngEntryVar = StringVar(value='')
        self.secondLatEntryVar = StringVar(value='')
        self.secondLngEntryVar = StringVar(value='')
        self.savedFirstCoordinateNEntry = CTkEntry(manageCamerasSecondRowCoordFrame, textvariable=self.firstLatEntryVar, placeholder_text = "First Coordinate N", font = ('Montserrat', 12, 'bold'), fg_color = "#FFFFFF", text_color = "#000000", corner_radius = 5)
        self.savedFirstCoordinateEEntry = CTkEntry(manageCamerasSecondRowCoordFrame, textvariable=self.firstLngEntryVar, placeholder_text = "First Coordinate E", font = ('Montserrat', 12, 'bold'), fg_color = "#FFFFFF", text_color = "#000000", corner_radius = 5)
        self.savedSecondCoordinateNEntry = CTkEntry(manageCamerasSecondRowCoordFrame, textvariable=self.secondLatEntryVar, placeholder_text = "Second Coordinate N", font = ('Montserrat', 12, 'bold'), fg_color = "#FFFFFF", text_color = "#000000", corner_radius = 5)
        self.savedSecondCoordinateEEntry = CTkEntry(manageCamerasSecondRowCoordFrame, textvariable=self.secondLngEntryVar, placeholder_text = "Second Coordinate E", font = ('Montserrat', 12, 'bold'), fg_color = "#FFFFFF", text_color = "#000000", corner_radius = 5)

        manageCamerasSecondRowStatus = tk.Frame(upperLeftContent, bg="#1B2431")
        self.secondRowStatusLabel = CTkLabel(manageCamerasSecondRowStatus, text='Camera successfully added.', font = ('Monteserrat', 13, 'italic'), anchor = "w", text_color = "#1B2431")

        lowerLeftContent = CTkFrame(leftContentFrame, fg_color = "#1B2431", corner_radius = 5)
        upperLowerLeft = tk.Frame(lowerLeftContent, bg = "#1B2431")
        # Label for context
        filterLabel = CTkLabel(upperLowerLeft, text= "Filter By:", font = ('Montserrat', 12, 'bold'), anchor = "w", text_color = "#FFFFFF")
        # Dropdown for vehicle Type
        self.vehicleTypeComboVar = StringVar()
        self.vehicleTypeComboBox = CTkComboBox(upperLowerLeft,
                                          values = ['', 'Car', 'Motorcycle', 'Bus', 'Truck'],
                                          variable = self.vehicleTypeComboVar,
                                          fg_color = "#FFFFFF",
                                          border_color = "#FFFFFF",
                                          text_color = "#000000",
                                          button_color = "#FFFFFF",
                                          dropdown_fg_color = "#FFFFFF",
                                          dropdown_text_color = "#000000",
                                          dropdown_font = ('Montserrat', 12),
                                          state='readonly')
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
        
        filterStatus = tk.Frame(upperLowerLeft, bg="#1B2431")
        self.filterStatusLabel = CTkLabel(filterStatus, text='Invalid hours.', font = ('Monteserrat', 13, 'italic'), anchor = "w", text_color = "#1B2431")
        
        lowerLowerLeft = tk.Frame(lowerLeftContent, bg = "#090E18")
        databaseFrame = tk.Frame(lowerLowerLeft, bg = "#090E18")
        self.databaseTable = ttk.Treeview(databaseFrame, columns = ('licensePlate', 'vehicleType', 'location', 'time', 'date', 'price'), show = "headings", style = 'Custom.Treeview')
        
        filterResponse = DBController.getFilteredLicensePlates()
        if filterResponse.ok:
            for row in filterResponse.data:
                self.databaseTable.insert('', 'end', values=(row[0].licenseNumber, row[0].vehicleType, row[0].location, row[0].time, row[0].date, row[0].price))

        self.databaseTable.bind('<<TreeviewSelect>>', self.selectDataFromTable)
        self.databaseTable.bind('<Delete>', self.deleteDataFromTable)
        
        self.databaseTable.tag_configure('even', background='#2A2D2E', foreground='#FFFFFF')
        self.databaseTable.tag_configure('odd', background='#343638', foreground='#FFFFFF')
        
        self.databaseTable.heading('licensePlate', text="License Plate", anchor='center')
        self.databaseTable.heading('vehicleType', text="Vehicle Type", anchor='center')
        self.databaseTable.heading('location', text="Location", anchor='center')
        self.databaseTable.heading('time', text="Time", anchor='center')
        self.databaseTable.heading('date', text="Date", anchor='center')
        self.databaseTable.heading('price', text="Charge", anchor='center')
        
        self.databaseTable.column('licensePlate', width=150, anchor='center')
        self.databaseTable.column('vehicleType', width=150, anchor='center')
        self.databaseTable.column('location', width=120, anchor='center')
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
        self.priceLabel = CTkLabel(priceHandlerFrame, text = "Charge", font = ('Montserrat', 12), text_color = "#FFFFFF", anchor = 'w')
        self.priceEntry = CTkEntry(priceHandlerFrame, text_color = "#000000", fg_color = "#FFFFFF", corner_radius = 5, font = ('Montserrat', 12))
        
        self.updateTableButton = CTkButton(databaseHandlerRow, fg_color = "#FFFFFF", text = "Update", font = ('Montserrat', 12, 'bold'), corner_radius = 5, text_color = "#000000", command = self.updateTable_callback)
        # End of Contents of Left Content 
        
        updateStatus = tk.Frame(databaseHandlerRow, bg = "#1B2431")
        self.updateStatusLabel = CTkLabel(updateStatus, text='Data successfully updated.', font = ('Monteserrat', 13, 'italic'), anchor = "w", text_color = "#1B2431")
        
        rightContentFrame = CTkFrame(contentFrame, fg_color = "#1B2431", corner_radius = 5)
        # Contents of Right Content Frame
        manageUsers = CTkLabel(rightContentFrame, text = "Manage Users", font = ('Montserrat', 12, 'bold'), anchor = "w", text_color = "#FFFFFF")
        
        upperRight = tk.Frame(rightContentFrame, bg = "#1B2431")
        
        leftUpperRight = tk.Frame(upperRight, bg = "#1B2431")
        selectUserFrame = tk.Frame(leftUpperRight, bg = "#1B2431")
        selectUserLabel = CTkLabel(selectUserFrame, text = "Select User", font = ('Montserrat', 12), anchor = "w", text_color = "#FFFFFF")
        self.selectUserComboVar = StringVar()

        users = DBController.getUsers()
        if users is not None and users.data is not None:
            # Proceed with creating the CTkComboBox
            self.selectUserCombo = CTkComboBox(selectUserFrame,
                                        values=[user[0].username for user in users.data],
                                        command=self.selectUserCombo_callback,
                                        variable=self.selectUserComboVar,
                                        fg_color="#FFFFFF",
                                        border_color="#FFFFFF",
                                        text_color="#000000",
                                        button_color="#FFFFFF",
                                        dropdown_fg_color="#FFFFFF",
                                        dropdown_text_color="#000000",
                                        dropdown_font=('Montserrat', 12))
        else:
            self.selectUserCombo = CTkComboBox(selectUserFrame,
                                        values=['None'],
                                        command=self.selectUserCombo_callback,
                                        variable=self.selectUserComboVar,
                                        fg_color="#FFFFFF",
                                        border_color="#FFFFFF",
                                        text_color="#000000",
                                        button_color="#FFFFFF",
                                        dropdown_fg_color="#FFFFFF",
                                        dropdown_text_color="#000000",
                                        dropdown_font=('Montserrat', 12))
        
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
        self.firstNameVar = StringVar(value='')
        self.firstNameEntry = CTkEntry(firstNameInner, textvariable=self.firstNameVar, placeholder_text = "Ex. Juan", font = ('Montserrat', 12), text_color = "#000000", fg_color = "#FFFFFF")
        
        lastNameOuter = tk.Frame(upperMiddleRight, bg = "#1B2431")
        lastNameInner = tk.Frame(lastNameOuter, bg = "#1B2431")
        lastNameLabel = CTkLabel(lastNameInner, text = "Last Name", font = ('Montserrat', 12), text_color = "#FFFFFF", anchor = "w")
        self.lastNameVar = StringVar(value='')
        self.lastNameEntry = CTkEntry(lastNameInner, textvariable=self.lastNameVar, placeholder_text = "Ex. Cruz", font = ('Montserrat', 12), text_color = "#000000", fg_color = "#FFFFFF")
        
        emailOuter = tk.Frame(upperMiddleRight, bg = "#1B2431")
        emailInner = tk.Frame(emailOuter, bg = "#1B2431")
        emailLabel = CTkLabel(emailInner, text = "Email", font = ('Montserrat', 12), text_color = "#FFFFFF", anchor = "w")
        self.emailVar = StringVar(value='')
        self.emailEntry = CTkEntry(emailInner, textvariable=self.emailVar, placeholder_text = "Ex. juancruz@domain.com", font = ('Montserrat', 12), text_color = "#000000", fg_color = "#FFFFFF")
        
        usernameOuter = tk.Frame(upperMiddleRight, bg = "#1B2431")
        usernameInner = tk.Frame(usernameOuter, bg = "#1B2431")
        usernameLabel = CTkLabel(usernameInner, text = "Username", font = ('Montserrat', 12), text_color = "#FFFFFF", anchor = "w")
        self.usernameVar = StringVar(value='')
        self.usernameEntry = CTkEntry(usernameInner, textvariable=self.usernameVar, placeholder_text = "Ex. juancruz@domain.com", font = ('Montserrat', 12), text_color = "#000000", fg_color = "#FFFFFF")

        passwordOuter = tk.Frame(upperMiddleRight, bg = "#1B2431")
        passwordInner = tk.Frame(passwordOuter, bg = "#1B2431")
        passwordLabel = CTkLabel(passwordInner, text = "Password", font = ('Montserrat', 12), text_color = "#FFFFFF", anchor = "w")
        self.passwordVar = StringVar(value='')
        self.passwordEntry = CTkEntry(passwordInner, textvariable=self.passwordVar, font = ('Montserrat', 12), text_color = "#000000", fg_color = "#FFFFFF", show = "*")

        confirmPasswordInner = tk.Frame(passwordOuter, bg = "#1B2431")
        confirmPasswordLabel = CTkLabel(confirmPasswordInner, text = "Confirm Password", font = ('Montserrat', 12), text_color = "#FFFFFF", anchor = "w")
        self.confirmPasswordVar = StringVar(value='')
        self.confirmPasswordEntry = CTkEntry(confirmPasswordInner, textvariable=self.confirmPasswordVar, font = ('Montserrat', 12), text_color = "#000000", fg_color = "#FFFFFF", show = "*")
        
        lowerMiddleRight = tk.Frame(middleRight, bg = "#1B2431")
        
        accessLabel = CTkLabel(lowerMiddleRight, text = "Access", font = ('Montserrat', 12, 'bold'), anchor = "w", text_color = "#FFFFFF")
        
        adminFrameOuter = tk.Frame(lowerMiddleRight, bg = "#1B2431")
        leftAdminFrameInner = tk.Frame(adminFrameOuter, bg = "#1B2431")
        adminLabel = CTkLabel(leftAdminFrameInner, text = "Administrator", font = ('Montserrat', 12), text_color = "#FFFFFF", anchor = "w")
        rightAdminFrameInner = tk.Frame(adminFrameOuter, bg = "#1B2431")
        self.adminVar = IntVar(value = 0)
        adminRadio_yes = CTkRadioButton(rightAdminFrameInner, text = "Yes", variable = self.adminVar, value = 1, command = self.adminRadioButton_callback)
        adminRadio_no = CTkRadioButton(rightAdminFrameInner, text = "No", variable = self.adminVar, value = 2, command = self.adminRadioButton_callback)
        
        congestionPriceFrameOuter = tk.Frame(lowerMiddleRight, bg = "#1B2431")
        leftCongestionPriceFrameInner = tk.Frame(congestionPriceFrameOuter, bg = "#1B2431")
        congestionPriceLabel = CTkLabel(leftCongestionPriceFrameInner, text = "Change Congestion Charge", font = ('Montserrat', 12), text_color = "#FFFFFF", anchor = "w")
        rightCongestionPriceFrameInner = tk.Frame(congestionPriceFrameOuter, bg = "#1B2431")
        self.changePriceVar = IntVar(value = 0)
        changePriceRadio_yes = CTkRadioButton(rightCongestionPriceFrameInner, text = "Yes", variable = self.changePriceVar, value = 1, command = self.changePriceRadioButton_callback)
        changePriceRadio_no = CTkRadioButton(rightCongestionPriceFrameInner, text = "No", variable = self.changePriceVar, value = 2, command = self.changePriceRadioButton_callback)
        
        activeHoursFrameOuter = tk.Frame(lowerMiddleRight, bg = "#1B2431")
        leftActiveHoursFrameInner = tk.Frame(activeHoursFrameOuter, bg = "#1B2431")
        activeHoursLabel = CTkLabel(leftActiveHoursFrameInner, text = "Change Active Hours", font = ('Montserrat', 12), text_color = "#FFFFFF", anchor = "w")
        rightActiveHoursFrameInner = tk.Frame(activeHoursFrameOuter, bg = "#1B2431")
        self.activeHoursRadioVar = IntVar(value = 0)
        activeHoursRadio_yes = CTkRadioButton(rightActiveHoursFrameInner, text = "Yes", variable = self.activeHoursRadioVar, value = 1, command = self.changeDetectableRadioButton_callback)
        activeHoursRadio_no = CTkRadioButton(rightActiveHoursFrameInner, text = "No", variable = self.activeHoursRadioVar, value = 2, command = self.changeDetectableRadioButton_callback)
        
        detectableFrameOuter = tk.Frame(lowerMiddleRight, bg = "#1B2431")
        leftDetectableFrameInner = tk.Frame(detectableFrameOuter, bg = "#1B2431")
        detectableLabel = CTkLabel(leftDetectableFrameInner, text = "Change Detectable Vehicles", font = ('Montserrat', 12), text_color = "#FFFFFF", anchor = "w")
        rightDetectableFrameInner = tk.Frame(detectableFrameOuter, bg = "#1B2431")
        self.detectableRadioVar = IntVar(value = 0)
        detectableRadio_yes = CTkRadioButton(rightDetectableFrameInner, text = "Yes", variable = self.detectableRadioVar, value = 1, command = self.changeDetectableRadioButton_callback)
        detectableRadio_no = CTkRadioButton(rightDetectableFrameInner, text = "No", variable = self.detectableRadioVar, value = 2, command = self.changeDetectableRadioButton_callback)
        
        downloadFrameOuter = tk.Frame(lowerMiddleRight, bg = "#1B2431")
        leftDownloadFrameInner = tk.Frame(downloadFrameOuter, bg = "#1B2431")
        downloadLabel = CTkLabel(leftDownloadFrameInner, text = "Download CSV", font = ('Montserrat', 12), text_color = "#FFFFFF", anchor = "w")
        rightDownloadFrameInner = tk.Frame(downloadFrameOuter, bg = "#1B2431")
        self.downloadRadioVar = IntVar(value = 0)
        downloadRadio_yes = CTkRadioButton(rightDownloadFrameInner, text = "Yes", variable = self.downloadRadioVar, value = 1, command = self.downloadCSVRadioButton_callback)
        downloadRadio_no = CTkRadioButton(rightDownloadFrameInner, text = "No", variable = self.downloadRadioVar, value = 2, command = self.downloadCSVRadioButton_callback)
        
        editUserStatus = tk.Frame(lowerMiddleRight, bg = "#1B2431")
        self.editUserStatusLabel = CTkLabel(editUserStatus, text='User successfully edited.', font = ('Monteserrat', 13, 'italic'), anchor = "w", text_color = "#1B2431")

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
        manageCamerasFirstRowCoordFrame.pack(side = "top", fill = "x", padx = 10, pady = (2, 10))
        manageCamerasFirstRowStatus.pack(side = "top", fill = "x", padx = 15, pady = (2))

        self.discoverCameraButton.pack(side = "left", fill = "x", expand = True, padx = 15)
        self.discoveredCamerasDrop.pack(side = "left", fill = "x", expand = True, padx = 15)
        self.assignID.pack(side = "left", fill = "x", expand = True, padx = 15)

        self.assignLocation.pack(side = "left", fill = "x", expand = True, padx = 15)
        self.addCameraButton.pack(side = "left", fill = "x", expand = True, padx = 15)
        
        tooltipLabel.pack(side = 'left', fill = 'x', expand = False, padx = (15, 5))
        self.firstCoordinateNEntry.pack(side='left', pady = 10, expand = True, fill = "x", padx = 15)
        self.firstCoordinateEEntry.pack(side='left', pady = 10, expand = True, fill = "x", padx = 15)
        self.secondCoordinateNEntry.pack(side='left', pady = 10, expand = True, fill = "x", padx = 15)
        self.secondCoordinateEEntry.pack(side='left', pady = 10, expand = True, fill = "x", padx = 15)
        
        self.addCameraStatusLabel.pack(side='left', pady = 10, expand = True, fill = "x")
        
        manageCamerasLabel.pack(side = "top", fill = "x", padx = 10, pady = (5,0))
        
        manageCamerasSecondRow.pack(side = "top", fill = "x", padx = 10, pady = (2, 10))
        manageCamerasSecondRowCoordFrame.pack(side = "top", fill = "x", padx = 10, pady = (2, 10))
        manageCamerasSecondRowStatus.pack(side = "top", fill = "x", padx = 15, pady = (2))

        self.savedCamerasDrop.pack(side = "left", fill = "x", expand = True, padx = 15)
        self.savedCameraID.pack(side = "left", fill = "x", expand = True, padx = 15)
        self.savedCameraLocation.pack(side = "left", fill = "x", expand = True, padx = 15)
        updateSavedCameraButton.pack(side = "left", fill = "x", expand = True, padx = 15)
        deleteSavedCameraButton.pack(side = "left", fill = "x", expand = True, padx = 15)
        
        self.savedFirstCoordinateNEntry.pack(side='left', pady = 10, expand = True, fill = "x", padx = 15)
        self.savedFirstCoordinateEEntry.pack(side='left', pady = 10, expand = True, fill = "x", padx = 15)
        self.savedSecondCoordinateNEntry.pack(side='left', pady = 10, expand = True, fill = "x", padx = 15)
        self.savedSecondCoordinateEEntry.pack(side='left', pady = 10, expand = True, fill = "x", padx = 15)

        self.secondRowStatusLabel.pack(side='left', pady = 10, expand = True, fill = "x")

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

        filterStatus.pack(side = "top", fill = "both", expand = True, padx = 10, pady = 2)
        self.filterStatusLabel.pack(side='left', pady = 10, expand = True, fill = "x")

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

        updateStatus.pack(side = "top", fill = "both", expand = True, padx = 10, pady = 2)
        self.updateStatusLabel.pack(side='left', pady = 10, expand = True, fill = "x")
        
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
        
        usernameOuter.pack(side = "top", fill = "both", expand = True, padx = 10, pady = 2)
        usernameInner.pack(side = "top", padx = 10, pady = 10, fill = "both", expand = False)
        usernameLabel.pack(side = "top", fill = "x", padx = 20, pady = (5,0))
        self.usernameEntry.pack(side = "top", fill = "x", padx = 10, pady = (0,5))

        passwordOuter.pack(side = "top", fill = "both", expand = True, padx = 10, pady = 2)

        passwordInner.pack(side = "left", padx = 10, pady = 10, fill = "both", expand = True)
        passwordLabel.pack(side = "top", fill = "x", padx = 20, pady = (5,0))
        self.passwordEntry.pack(side = "top", fill = "x", padx = 10, pady = (0,5))

        confirmPasswordInner.pack(side = "left", padx = 10, pady = 10, fill = "both", expand = True)
        confirmPasswordLabel.pack(side = "top", fill = "x", padx = 20, pady = (5,0))
        self.confirmPasswordEntry.pack(side = "top", fill = "x", padx = 10, pady = (0,5))
        
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

        editUserStatus.pack(side = "top", fill = "both", expand = True, padx = 10, pady = 2)
        self.editUserStatusLabel.pack(side='left', pady = 10, expand = True, fill = "x")
        
        lowerRight.pack(side = "top", expand = False, fill = "both", padx = 10, pady = 2)
        applyUserButton.pack(side = "right", expand = False, fill = "x", padx = (5,10), pady = 2)
        deleteUserButton.pack(side = "right", expand = False, fill = "x", padx = (10,5), pady = 2)
                
        navigationFrame.pack(side = "top", fill = "x")
        dashboardButton.pack(side = 'right', padx = 10, pady = 10)