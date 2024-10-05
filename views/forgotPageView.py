import re
import os
import sys
import time
import tkinter as tk

from tkinter import messagebox
from customtkinter import *
from PIL import Image

current = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current)
sys.path.append(parent_dir)

import controllers.controller as cont

from controllers.controller import AccountController as ac
from controllers.dbController import DBController as db
from controllers.s3controller import S3Controller

class ForgetPasswordPage(tk.Frame):
    # Close Application
    def closeApplication(self):
        self.master.destroy()

    # Minimize or Iconify the Application
    def minimizeApplication(self):
        self.master.iconify()
    
    def __init__(self, parent):
        self.s3 = S3Controller()

        tk.Frame.__init__(self, parent)
        self.initializePage()
        
    def initializePage(self):
        closePhoto = CTkImage(light_image = Image.open(os.path.join(parent_dir, "views/icons/icon_close_darkmode.png")),
                              dark_image = Image.open(os.path.join(parent_dir, "views/icons/icon_close_darkmode.png")),
                              size = (20, 20))

        # Minimize Icon (Currently Set to darkmode, if possible change to lightmode when the changes)
        minimizePhoto = CTkImage(light_image = Image.open(os.path.join(parent_dir, "views/icons/icon_minimize_darkmode.png")),
                              dark_image = Image.open(os.path.join(parent_dir, "views/icons/icon_minimize_darkmode.png")),
                              size = (20, 20))
        
        # Toolbar Frame
        self.toolbarFrame = tk.Frame(self, bg="#090E18", height = 30)
        self.toolbarFrame.pack(side="top", fill="both")

        closeButton = CTkButton(self.toolbarFrame, 
                                image = closePhoto,
                                text = "",
                                width = 20,
                                height = 20,
                                fg_color = "#090E18",
                                bg_color = "#090E18",
                                hover = True,
                                hover_color = "#48BFE3",
                                command = self.closeApplication)
        closeButton.pack(side = "right", padx = 10, pady = 10)

        minimizeButton = CTkButton(self.toolbarFrame, 
                                image = minimizePhoto,
                                text = "",
                                width = 20,
                                height = 20,
                                fg_color = "#090E18",
                                bg_color = "#090E18",
                                hover = True,
                                hover_color = "#48BFE3",
                                command = self.minimizeApplication)
        minimizeButton.pack(side = "right", padx = 0, pady = 10)
        
        # Main Frame
        self.mainFrame = tk.Frame(self, bg = "#090E18")
        self.mainFrame.pack(expand=True, fill="both")
        
        self.innerMainFrame = tk.Frame(self.mainFrame, bg='#090E18')
        self.innerMainFrame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Navbar Frame
        self.navbarFrame = tk.Frame(self, bg="#090E18")
        self.navbarFrame.pack(side="bottom", fill="x")
        
        cancelButton = CTkButton(self.navbarFrame,
                                text = 'Cancel',
                                command = self.cancelButton_callback, 
                                font = ('Montserrat', 15),
                                border_width = 2,
                                corner_radius = 15,
                                border_color = '#5E60CE',
                                text_color = '#5E60CE',
                                fg_color = '#090E18',
                                height = 30,
                                width = 140)
        cancelButton.pack(side = 'right', padx = 10, pady = 10)
        
        cancelButton.bind("<Enter>", lambda event: cancelButton.configure(text_color="#090E18", fg_color = "#5E60CE")) 
        cancelButton.bind("<Leave>", lambda event: cancelButton.configure(text_color="#5E60CE", fg_color = "#090E18")) 

        # Email Entry and Submit Button
        self.show_email()

        self.otp_label = None
        self.otp_entry = None
        self.new_password_label = None
        self.new_password_entry = None
        self.confirm_password_label = None
        self.confirm_password_entry = None
        self.timer_label = None
        self.timer_value = 30 
        self.otp_sent_time = 0

    def show_email(self):
        # Email Entry and Submit Button
        self.email_label = CTkLabel(self.innerMainFrame, text="Email Address", text_color="#FFFFFF", font=('Montserrat', 15))
        self.email_label.pack(pady=(5, 0))

        self.email_entry = CTkEntry(self.innerMainFrame, placeholder_text="juandelacruz@domain.com", text_color="#000000", fg_color="#FFFFFF", corner_radius=15, width=250, height=30)
        self.email_entry.pack(pady=(0, 5))
        self.email_entry.bind("<KeyRelease>", self.validate_email)

        self.submit_button = CTkButton(self.innerMainFrame, text="Submit", state="disabled", command=self.submit_email, corner_radius=15, fg_color="#FFFFFF", text_color="#000000", height=30)
        self.submit_button.pack(pady=(10,5))
    
    def validate_email(self, event):
        email = self.email_entry.get()
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.submit_button.configure(state="normal")
        else:
            self.submit_button.configure(state="disabled")

    def submit_email(self):
        email = self.email_entry.get()
        if self.email_in_database(email):
            if time.time() - self.otp_sent_time >= self.timer_value:
                user = db.getUser(email=email)
                self.s3.updateAuditLog('OTP request', f'User {user.email} requested for OTP', user)
                self.clear_main_widgets()
                self.ask_otp(email, user)
            else:
                messagebox.showerror("Error", "Please wait before requesting another OTP")
        else:
            return

    def clear_main_widgets(self):
        for widget in self.innerMainFrame.winfo_children():
            widget.pack_forget()

    def ask_otp(self, receiver_email, user):
        self.otp = ac.generate_OTP()
        self.otp_sent_time = time.time()  # Record the time when OTP is sent
        ac.send_OTP(receiver_email, self.otp)
        self.otp_label = CTkLabel(self.innerMainFrame, text="Enter OTP:", font=('Montserrat', 15), text_color="#FFFFFF")
        self.otp_label.pack(pady=(5, 0))

        self.otp_entry = CTkEntry(self.innerMainFrame, placeholder_text="123456", text_color='#000000', fg_color='#FFFFFF', corner_radius=15, font=('Montserrat', 12))
        self.otp_entry.pack(pady=(0, 5))

        self.submit_button.configure(text="Submit", command=lambda: self.submit_otp(receiver_email, user))
        self.submit_button.pack()

        # Timer Label
        self.timer_label = CTkLabel(self.innerMainFrame, text="", font=('Montserrat', 12), text_color='#FFFFFF')
        self.timer_label.pack(pady=(10,0))

        # Start the cooldown timer
        self.update_timer()

        # Request Another OTP Button
        self.request_otp_button = CTkButton(self.innerMainFrame, text="Request Another OTP", state="disabled", command=lambda: self.request_another_otp(receiver_email, user), corner_radius=15, text_color='#000000', fg_color='#FFFFFF', height=30)
        self.request_otp_button.pack(pady=(0,5))

    def update_timer(self):
        if self.timer_value > 0:
            self.timer_label.configure(text=f"Time until next OTP: {self.timer_value} seconds")
            self.timer_value -= 1
            self.timer_label.after(1000, self.update_timer)
            # Enable the request_otp_button when the cooldown timer is over
            if self.timer_value == 0:
                self.request_otp_button.configure(state="normal")
        else:
            self.timer_label.configure(text="")
            self.timer_value = 30  # Reset cooldown timer

    def request_another_otp(self, email, user):
        self.clear_main_widgets()
        self.timer_value = 30  # Reset the timer value
        self.ask_otp(email, user)

    def submit_otp(self, email, user):
        otp = self.otp_entry.get()
        if self.otp_matches(otp) and time.time() - self.otp_sent_time <= 300:  # Check if OTP is submitted within 5 minutes
            self.s3.updateAuditLog('OTP match', f'User {user.email} inputted correct OTP', user)
            self.clear_main_widgets()
            self.change_password(email, user)
        else:
            self.s3.updateAuditLog('OTP mismatch', f'User {user.email} inputted incorrect or invalid OTP', user)
            messagebox.showerror("Error", "Invalid OTP or OTP expired")

    def change_password(self, email, user):
        self.new_password_label = CTkLabel(self.innerMainFrame, text="New Password:", font=('Montserrat', 15), text_color='#FFFFFF')
        self.new_password_label.pack(pady=(5, 0))

        self.new_password_entry = CTkEntry(self.innerMainFrame, show="*", font=('Montserrat', 12), text_color='#000000', fg_color='#FFFFFF', corner_radius=15)
        self.new_password_entry.pack(pady=(0, 5))

        self.confirm_password_label = CTkLabel(self.innerMainFrame, text="Confirm Password:", font=('Montserrat', 15), text_color='#FFFFFF')
        self.confirm_password_label.pack(pady=(5, 0))

        self.confirm_password_entry = CTkEntry(self.innerMainFrame, show="*", font=('Montserrat', 12), text_color='#000000', fg_color='#FFFFFF', corner_radius=15)
        self.confirm_password_entry.pack(pady=(0, 5))

        self.submit_button.configure(text="Submit", command=lambda: self.submit_password(email, user))
        self.submit_button.pack(pady=15)

    def submit_password(self, email, user):
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if new_password == confirm_password:
            response = db.changePassword(email, new_password, confirm_password)
            if response.ok:
                self.s3.updateAuditLog('Password change (forgot password)', f'User {user.email} changed password', user)
                messagebox.showinfo("Success", "Password changed successfully")
                self.reset_page()
                self.master.show_frame(self.master.loginFrame)
                cont.cameraEnabled = False
                cont.loggedIn = False
            else:
                messagebox.showerror("Error", (response.messages['password'] or response.messages['error']))
        else:
            messagebox.showerror("Error", "Passwords do not match")

    def email_in_database(self, email):
        result = db.emailExists(email=email)
        if result:
            return True
        else:
            messagebox.showerror("Error", 'Email does not exist.')
            return False

    def otp_matches(self, otp):
        return self.otp == otp
    
    def cancelButton_callback(self):
        self.reset_page()
        self.master.show_frame(self.master.loginFrame)
        cont.cameraEnabled = False
        cont.loggedIn = False
        
    def reset_page(self):
        self.email_entry.delete(0, tk.END)
        self.email_entry.configure(state="normal")
        self.submit_button.configure(state="disabled")
        self.clear_main_widgets()
        self.timer_value = 30
        self.otp_label = None
        self.otp_entry = None
        self.new_password_label = None
        self.new_password_entry = None
        self.confirm_password_label = None
        self.confirm_password_entry = None
        self.timer_label = None
        self.otp_sent_time = 0
        self.show_email()