import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from tkinter import Tk
from customtkinter import CTkEntry, CTkButton, CTkLabel

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
root = os.path.dirname(parent)
sys.path.append(root)

from views.forgotPageView import ForgetPasswordPage

class TestForgetPasswordPage(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.root.show_frame = MagicMock()  # Mock the show_frame method
        self.root.loginFrame = MagicMock()  # Mock the loginFrame attribute
        self.page = ForgetPasswordPage(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_validate_email_valid(self):
        self.page.email_entry.insert(0, 'valid@example.com')
        self.page.validate_email(None)
        self.assertEqual(self.page.submit_button.cget('state'), 'normal')

    def test_validate_email_invalid(self):
        self.page.email_entry.insert(0, 'invalid-email')
        self.page.validate_email(None)
        self.assertEqual(self.page.submit_button.cget('state'), 'disabled')

    @patch('controllers.dbController.DBController.emailResponse')
    @patch('controllers.controller.AccountController.send_OTP')
    @patch('controllers.controller.AccountController.generate_OTP')
    def test_submit_email_valid(self, mock_generate_otp, mock_send_otp, mock_email_response):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_email_response.return_value = mock_response
        mock_generate_otp.return_value = '123456'
        
        self.page.email_entry.insert(0, 'valid@example.com')
        self.page.submit_email()
        
        self.assertEqual(self.page.otp, '123456')
        self.assertIsNotNone(self.page.otp_label)
        self.assertIsNotNone(self.page.otp_entry)

    @patch('controllers.dbController.DBController.emailResponse')
    def test_submit_email_invalid(self, mock_email_response):
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.messages = {'email': 'Email not found'}
        mock_email_response.return_value = mock_response
        
        self.page.email_entry.insert(0, 'invalid@example.com')
        self.page.submit_email()
        
        self.assertIsNone(self.page.otp_label)
        self.assertIsNone(self.page.otp_entry)

    def test_submit_otp_valid(self):
        self.page.otp = '123456'
        self.page.otp_entry = CTkEntry(self.page.innerMainFrame)
        self.page.otp_entry.insert(0, '123456')
        
        self.page.submit_otp('valid@example.com')
        
        self.assertIsNone(self.page.new_password_entry)
        self.assertIsNone(self.page.confirm_password_entry)

    def test_submit_otp_invalid(self):
        self.page.otp = '123456'
        self.page.otp_entry = CTkEntry(self.page.innerMainFrame)
        self.page.otp_entry.insert(0, '654321')
        
        with patch('tkinter.messagebox.showerror') as mock_showerror:
            self.page.submit_otp('valid@example.com')
            mock_showerror.assert_called_with("Error", "Invalid OTP or OTP expired")

    @patch('controllers.dbController.DBController.changePassword')
    def test_submit_passwords_matching(self, mock_change_password):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_change_password.return_value = mock_response
        
        self.page.new_password_entry = CTkEntry(self.page.innerMainFrame, show="*")
        self.page.confirm_password_entry = CTkEntry(self.page.innerMainFrame, show="*")
        self.page.new_password_entry.insert(0, 'newpassword')
        self.page.confirm_password_entry.insert(0, 'newpassword')
        
        with patch('tkinter.messagebox.showinfo') as mock_showinfo:
            self.page.submit_password('valid@example.com')
            mock_showinfo.assert_called_with("Success", "Password changed successfully")

    @patch('controllers.dbController.DBController.changePassword')
    def test_submit_passwords_not_matching(self, mock_change_password):
        self.page.new_password_entry = CTkEntry(self.page.innerMainFrame, show="*")
        self.page.confirm_password_entry = CTkEntry(self.page.innerMainFrame, show="*")
        self.page.new_password_entry.insert(0, 'newpassword')
        self.page.confirm_password_entry.insert(0, 'differentpassword')
        
        with patch('tkinter.messagebox.showerror') as mock_showerror:
            self.page.submit_password('valid@example.com')
            mock_showerror.assert_called_with("Error", "Passwords do not match")

if __name__ == '__main__':
    unittest.main()
