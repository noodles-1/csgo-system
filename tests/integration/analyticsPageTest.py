import os
import sys
import unittest
from unittest.mock import patch
import tkinter as tk
import pandas as pd

# Append the root directory to the sys path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
root = os.path.dirname(parent)
sys.path.append(root)

# Import the module to be tested
from views.analyticsPageView import AnalyticsPage

# Define test class
class TestIntegration(unittest.TestCase):

    # Set up the test environment
    @patch('views.analyticsPageView.DBController')
    @patch('views.analyticsPageView.PollController')
    @patch('tkinter.ttk.Style.theme_use', lambda *args: None)
    def setUp(self, MockPollController, MockDBController):
        """
        Set up the test environment for integration testing.

        - Patch necessary controllers with MagicMock.
        - Create a Tkinter root window.
        - Create an instance of AnalyticsPage.
        """
        # Assign mock objects to instance variables
        self.MockDBController = MockDBController
        self.MockPollController = MockPollController
        self.root = tk.Tk()
        self.analytics_page = AnalyticsPage(self.root)
    
    # Test case for downloadCSV method
    def test_downloadCSV(self):
        """
        Test the downloadCSV method.

        - Mock the rgctrl module.
        - Call the method.
        - Check if the correct function in rgctrl is called.
        """
        with patch('views.analyticsPageView.rgctrl') as mock_rgctrl:
            self.analytics_page.downloadCSV()
            mock_rgctrl.downloadAndProcessCSV.assert_called_once()

    # Test case for processDataDetected method
    def test_processDataDetected(self):
        """
        Test the processDataDetected method.

        - Create sample data and DataFrame.
        - Call the method.
        - Check the length of the result.
        """
        data = {
            'date': ['2023-06-01', '2023-06-01'],
            'time': ['12:00:00', '13:00:00']
        }
        df = pd.DataFrame(data)
        hours = 24

        result = self.analytics_page.processDataDetected(df, hours)
        self.assertEqual(len(result), 25)  # Check if it returns 25 hourly entries (including empty hours)

    # Test case for processDataBusiest method
    def test_processDataBusiest(self):
        """
        Test the processDataBusiest method.

        - Create sample data and DataFrame.
        - Call the method.
        - Check the length of the result.
        """
        data = {
            'date': ['2023-06-01', '2023-06-01'],
            'time': ['12:00:00', '12:01:00']
        }
        df = pd.DataFrame(data)
        hours = 2

        result = self.analytics_page.processDataBusiest(df, hours)
        self.assertEqual(len(result), 121)  # Check if it returns 121 minute entries (including empty minutes)

    # Clean up after the test
    def tearDown(self):
        """
        Clean up after the test by destroying the Tkinter root window.
        """
        self.root.destroy()

# Run the tests if the script is executed directly
if __name__ == '__main__':
    unittest.main()
