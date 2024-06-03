# Import necessary modules
import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from tkinter import ttk
import os
import sys

# Append the root directory to the sys path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
root = os.path.dirname(parent)
sys.path.append(root)

# Import the module to be tested
from views.adminPageView import AdminPage

# Define test class
class TestAdminPage(unittest.TestCase):

    # Set up the test environment
    @patch('controllers.dbController.DBController.editUser')
    @patch('controllers.dbController.DBController.isValidEmail')
    @patch('controllers.dbController.DBController.isValidUsername')
    @patch('controllers.dbController.DBController.otherEmailExists')
    @patch('controllers.dbController.DBController.otherUsernameExists')
    @patch('controllers.dbController.DBController.validateMissing')
    @patch('controllers.dbController.DBController.getCameras')
    @patch('tkinter.ttk.Style.theme_use', lambda *args: None)
    def setUp(self, MockGetCameras, MockValidateMissing, MockOtherUsernameExists, MockOtherEmailExists, MockIsValidUsername, MockIsValidEmail, MockEditUser):
        """
        Set up the test environment.

        - Patch necessary functions with MagicMock.
        - Create a Tkinter root window.
        - Mock the response of getCameras.
        - Mock variables and GUI elements.
        """
        # Assign mock objects to instance variables
        self.MockEditUser = MockEditUser
        self.MockIsValidEmail = MockIsValidEmail
        self.MockIsValidUsername = MockIsValidUsername
        self.MockOtherEmailExists = MockOtherEmailExists
        self.MockOtherUsernameExists = MockOtherUsernameExists
        self.MockValidateMissing = MockValidateMissing
        
        # Create a Tkinter root window
        self.root = tk.Tk()
        
        # Mock getCameras response
        mock_camera = MagicMock()
        mock_camera.name = "Camera1"
        MockGetCameras.return_value.ok = True
        
        # Create an instance of AdminPage
        self.admin_page = AdminPage(self.root)

        # Mock the variables and GUI elements
        self.admin_page.selectUserCombo = MagicMock(spec=ttk.Combobox)
        self.admin_page.firstNameVar = MagicMock(spec=tk.StringVar)
        self.admin_page.lastNameVar = MagicMock(spec=tk.StringVar)
        self.admin_page.emailVar = MagicMock(spec=tk.StringVar)
        self.admin_page.usernameVar = MagicMock(spec=tk.StringVar)
        self.admin_page.passwordVar = MagicMock(spec=tk.StringVar)
        self.admin_page.adminVar = MagicMock(spec=tk.IntVar)
        self.admin_page.changePriceVar = MagicMock(spec=tk.IntVar)
        self.admin_page.downloadRadioVar = MagicMock(spec=tk.IntVar)
        self.admin_page.detectableRadioVar = MagicMock(spec=tk.IntVar)
        self.admin_page.activeHoursRadioVar = MagicMock(spec=tk.IntVar)
        self.admin_page.editUserStatusLabel = MagicMock(spec=tk.Label)

    # Test case for applyUserButton callback with incomplete fields
    def test_applyUserButton_callback_incomplete_fields(self):
        """
        Test the behavior of applyUserButton_callback when there are incomplete fields.

        - Set one of the fields to be empty.
        - Mock the response of the internal method.
        - Call the method.
        - Check if the status label is updated correctly.
        """
        # Set one of the fields to be empty
        self.admin_page.selectUserCombo.get.return_value = ''
        self.admin_page.firstNameVar.get.return_value = 'John'
        self.admin_page.lastNameVar.get.return_value = 'Doe'
        self.admin_page.emailVar.get.return_value = 'john.doe@example.com'
        self.admin_page.usernameVar.get.return_value = 'johndoe'
        self.admin_page.passwordVar.get.return_value = 'password'

        # Mock the internal method responses
        self.MockValidateMissing.return_value.ok = False

        # Call the method
        self.admin_page.applyUserButton_callback()

        # Check if the status label is updated correctly
        self.admin_page.editUserStatusLabel.configure.assert_called_with(text='Incomplete fields.', text_color="#d62828")

    # Clean up after the test
    def tearDown(self):
        """
        Clean up after the test by destroying the Tkinter root window.
        """
        self.root.destroy()

# Run the tests if the script is executed directly
if __name__ == '__main__':
    unittest.main()
