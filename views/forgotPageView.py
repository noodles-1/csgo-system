import tkinter as tk
from tkinter import messagebox
import re
import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from controllers.dbController import DBController as db
from sessions.userSession import UserSession
import controllers.controller as cont
from controllers.controller import AccountController as ac
import views.switchView as switch

class ForgetPasswordPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg="blue")
        self.parent = parent
        self.otp = None
        
        self.email_label = tk.Label(self, text="Enter Email Address:")
        self.email_label.pack()
        
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()
        self.email_entry.bind("<KeyRelease>", self.validate_email)
        
        self.submit_button = tk.Button(self, text="Submit", state="disabled", command=self.submit_email)
        self.submit_button.pack()
        
    def validate_email(self, event):
        email = self.email_entry.get()
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.submit_button.config(state="normal")
        else:
            self.submit_button.config(state="disabled")
            
    def submit_email(self):
        email = self.email_entry.get()
        if self.email_in_database(email):
            self.clear_widgets()
            self.ask_otp(email)
        else:
            return
        
    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.pack_forget()
            
    def ask_otp(self, receiver_email):
        self.otp = ac.generate_OTP()
        ac.send_OTP(receiver_email, self.otp)
        self.otp_label = tk.Label(self, text="Enter OTP:")
        self.otp_label.pack()
        
        self.otp_entry = tk.Entry(self)
        self.otp_entry.pack()
        
        self.submit_button.config(text="Submit", command=lambda: self.submit_otp(receiver_email))
        self.submit_button.pack()
        
    def submit_otp(self, email):
        otp = self.otp_entry.get()
        if self.otp_matches(otp):
            self.clear_widgets()
            self.change_password(email)
        else:
            messagebox.showerror("Error", "Invalid OTP")
            
    def change_password(self, email):
        self.new_password_label = tk.Label(self, text="New Password:")
        self.new_password_label.pack()
        
        self.new_password_entry = tk.Entry(self, show="*")
        self.new_password_entry.pack()
        
        self.confirm_password_label = tk.Label(self, text="Confirm Password:")
        self.confirm_password_label.pack()
        
        self.confirm_password_entry = tk.Entry(self, show="*")
        self.confirm_password_entry.pack()
        
        self.submit_button.config(text="Submit", command=lambda: self.submit_password(email))
        self.submit_button.pack()
        
    def submit_password(self, email):
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        if new_password == confirm_password:
            response = db.changePassword(email, new_password, confirm_password)
            if response.ok:
                messagebox.showinfo("Success", "Password changed successfully")
                self.master.show_frame(self.master.loginFrame)
                cont.cameraEnabled = False
                cont.loggedIn = False
            else:
                messagebox.showerror("Error", response.messages['error'])
        else:
            messagebox.showerror("Error", "Passwords do not match")

    def email_in_database(self, email):
        response = db.emailResponse(email)
        if response.ok:
            return True
        else:
            messagebox.showerror("Error", response.messages['email'])
            return False

    def otp_matches(self, otp):
        return self.otp == otp