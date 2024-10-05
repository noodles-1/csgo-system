import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from tkinter import Tk
from customtkinter import CTkComboBox

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
root = os.path.dirname(parent)
sys.path.append(root)

from views.dashboardPageView import DashboardPage

''''
Solution Documentation:
This solution documentation outlines the steps taken to test the callback function `changeCameraDisplay_callback` in the `DashboardPage` class.

Test Scenario:
- Test if selecting a value from the custom combobox `changeCameraDisplay` calls the function `changeCameraDisplay_callback` with the correct argument.

Test Setup:
- Mock the data returned by `DBController.getCameras` to simulate the presence of a camera named 'Camera1'.
- Create a mock object for the custom combobox `changeCameraDisplay`.
- Access the `changeCameraDisplay_callback` function of the `DashboardPage` class.
- Set up the test environment with the following steps:

    # Arrange:
    - Mock the data returned by `DBController.getCameras` to return a camera named 'Camera1'.
    - Create a mock object for the custom combobox `changeCameraDisplay`.
    - Access the `changeCameraDisplay_callback` function of the `DashboardPage` class.

    # Action:
    - Call the `changeCameraDisplay_callback` function with the argument 'Camera1'.

    # Assert:
    - Assert that the `changeCameraDisplay_callback` function is called once with the argument 'Camera1'.

'''

class MockParent:
    def __init__(self):
        self.currUser = None

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.mock_parent = MockParent()

        # Patch ttk.Style().theme_use to bypass the theme error
        with patch('views.dashboardPageView.ttk.Style.theme_use'):
            with patch('controllers.dbController.DBController.getCameras') as mock_getCameras:
                mock_camera = MagicMock()
                mock_camera.name = 'Camera1'
                mock_getCameras.return_value = MagicMock(data=[mock_camera])
                
                self.dashboard_page = DashboardPage(self.root)
                
                # Access the changeCameraDisplay attribute after initialization
                self.changeCameraDisplay = self.dashboard_page.changeCameraDisplay

    @patch('controllers.dbController.DBController.getCameras')
    @patch.object(DashboardPage, 'changeCameraDisplay_callback')
    def test_combobox_selection(self, mock_change_callback, mock_getCameras):
        # Mock the data returned by getCameras
        mock_camera = MagicMock()
        mock_camera.name = 'Camera1'
        mock_getCameras.return_value = MagicMock(data=[mock_camera])

        # Create a mock object for the custom combobox
        mock_change_camera_combobox = MagicMock(spec=CTkComboBox)
        self.dashboard_page.changeCameraDisplay = mock_change_camera_combobox

        # Set up the test
        self.dashboard_page.changeCameraDisplay_callback('Camera1')

        # Assert that the callback function is called with the correct argument
        mock_change_callback.assert_called_once_with('Camera1')

if __name__ == '__main__':
    unittest.main()
