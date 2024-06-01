import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from tkinter import Tk
from customtkinter import CTkEntry, CTkLabel

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
root = os.path.dirname(parent)
sys.path.append(root)

from views.loginPageView import LoginPage
from controllers import dbController as db

'''
Mock Classes:
    > MockDashboardFrame: Simulates the dashboard frame's behavior.
    > MockParent: Simulates the parent application that contains the dashboardFrame and setUser methods.

TestLoginPage Class:
    > setUp: Initializes the test environment by creating a Tk instance, LoginPage, and a mock parent.
    > tearDown: Cleans up the test environment by destroying the Tk instance.
    > test_valid_login:
        & Arrange: Sets up the mock response for a valid login and initializes the necessary UI elements.
        & Action: Calls the verifyCredentials method to test the login functionality.
        & Assert: Verifies that the user data is correctly set and the dashboard frame is displayed.

Notes:
    > MockParent class includes a show_frame method to avoid errors when verifyCredentials calls switch.showDashboardPage.
    > Each step in the test (Arrange, Action, Assert) is clearly labeled for clarity.
'''

class MockDashboardFrame:
    def __init__(self):
        self.is_mapped = False
    
    def tkraise(self):
        self.is_mapped = True

    def winfo_ismapped(self):
        return self.is_mapped

class MockParent:
    def __init__(self):
        self.currUser = None
        self.dashboardFrame = MockDashboardFrame()

    def setUser(self, user):
        self.currUser = user

    def show_frame(self, frame, changeCameraDisplay=None, cap=None, placeholder_label=None):
        frame.tkraise()

class TestLoginPage(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.login_page = LoginPage(self.root)
        self.mock_parent = MockParent()

    def tearDown(self):
        self.root.destroy()

    @patch('controllers.dbController.DBController.loginUser')
    def test_valid_login(self, mock_login_user):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.data = {'username': 'valid_user'}
        mock_login_user.return_value = mock_response
        
        usernameEntry = CTkEntry(self.root)
        passwordEntry = CTkEntry(self.root)
        incorrectLabel = CTkLabel(self.root, text="")
        
        usernameEntry.insert(0, 'valid_user')
        passwordEntry.insert(0, 'valid_password')

        self.login_page.verifyCredentials(self.mock_parent, usernameEntry, passwordEntry, incorrectLabel)
        
        self.assertEqual(self.mock_parent.currUser, {'username': 'valid_user'})
        self.assertTrue(self.mock_parent.dashboardFrame.winfo_ismapped())

if __name__ == '__main__':
    unittest.main()