import unittest
import sys
import os
import cv2

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
root = os.path.dirname(parent)
sys.path.append(root)

from unittest.mock import MagicMock, patch
from controllers.controller import AIController
from controllers.controller import ReportGenerationController
from controllers.controller import AccountController

class TestControllerMethods(unittest.TestCase):
    def setUp(self):
        self.file_path = 'dummy_data/data.csv'

    def test_validate_license(self):
        # Arrange: Define test method to validate license plate
        # before
        # remove - img = cv2.imread('../test_images/1.jpg')
        #after
         # Arrange: Load the image
        img = cv2.imread('test_images/7.jpg')
        img = cv2.resize(img, (0,0), fx=3, fy=3)
        img = cv2.GaussianBlur(img, (5,5), 0)

        predicted = AIController.get_license_number_cnocr(frame=img)
        predicted = predicted[0]['text'].strip()
        predicted = predicted.replace(' ', '')
        self.assertEqual(predicted, 'FAB3478')

    def test_busiest_time_report(self):
        # Action: Call busiestTimeReport function and store returned xData and yData
        x_data, y_data = ReportGenerationController.busiestTimeReport(self.file_path)
        
        # Assert: Check if xData and yData are lists
        self.assertIsInstance(x_data, list)
        self.assertIsInstance(y_data, list)
        
        # Assert: Check if each element in xData is a string
        for x in x_data:
            self.assertIsInstance(x, str)
        
        # Assert: Check if each element in yData is an integer
        for y in y_data:
            self.assertIsInstance(y, int)

    def test_revenue_report(self):
        '''
        This unit testing may need updating in the future. Since the function relies on the Date Today.
        It takes the last 15 days from the Date Today.
        If the CSV is changed. The expected dates and revenues may need updating.
        '''
        # Arrange: Define expected dates and revenues
        expected_dates = ['2024-12-27', '2024-12-25', '2024-12-12', '2024-12-11', '2024-11-19', '2024-11-18', '2024-11-16', '2024-11-12', '2024-11-08', '2024-11-05', '2024-11-04', '2024-11-02', '2024-11-01', '2024-10-31', '2024-10-30']
        expected_revenues = [950, 500, 1200, 1100, 1050, 500, 1800, 550, 900, 1100, 2150, 700, 50, 150, 1850]
        
        # Action: Call revenueReport function
        latest_dates, latest_revenues = ReportGenerationController.revenueReport(self.file_path)
        
        # Assert: Check if the latest dates match the expected dates
        self.assertEqual(latest_dates, expected_dates)
        
        # Assert: Check if the latest revenues match the expected revenues
        self.assertEqual(latest_revenues, expected_revenues)

    def test_vehicles_detected_report(self):
        # Action: Call vehiclesDetectedReport function and store returned xData and yData
        x_data, y_data = ReportGenerationController.vehiclesDetectedReport(self.file_path)
        
        # Assert: Check if xData and yData are lists
        self.assertIsInstance(x_data, list)
        self.assertIsInstance(y_data, list)
        
        # Assert: Check if each element in xData is a string
        for x in x_data:
            self.assertIsInstance(x, str)
        
        # Assert: Check if each element in yData is an integer
        for y in y_data:
            self.assertIsInstance(y, int)

    @patch('controllers.controller.pd.DataFrame')
    @patch('controllers.controller.os')
    @patch('controllers.controller.DBController.getFilteredLicensePlates')    
    def test_successful_download_and_process(self, mock_filtered_license_plates, mock_os, mock_data_frame):
        # Arrange: Create a test CSV file with dummy data
        test_csv_data = "dummy_data/testData.csv"
        with open(test_csv_data, "w") as f:
            f.write("column1,column2\nvalue1,value2\n")
        
        mock_filtered_license_plates.return_value = MagicMock(data=[])
        mock_os.path.join = MagicMock()
        mock_data_frame.to_csv = MagicMock()
        # Action: Call downloadAndProcessCSV method to download and process the test CSV file
        success, _ = ReportGenerationController.downloadAndProcessCSV()

        # Assert: Check if the download and processing were successful
        self.assertTrue(success)
    
    @patch('controllers.controller.psutil.cpu_percent')
    def test_get_cpu_usage(self, mock_cpu_percent):
        # Arrange: Mock the psutil.cpu_percent function
        mock_cpu_percent.return_value = 50  # Simulate 50% CPU usage

        # Action: Call the function
        x_cpu, y_cpu = ReportGenerationController.get_cpu_usage()

        # Assert: Check the results
        self.assertEqual(x_cpu, [])
        self.assertEqual(y_cpu, [50])

    @patch('controllers.controller.psutil.virtual_memory')
    def test_get_memory_usage(self, mock_virtual_memory):
        # Arrange: Mock the psutil.virtual_memory function
        mock_memory = MagicMock()
        mock_memory.percent = 60  # Simulate 60% memory usage
        mock_virtual_memory.return_value = mock_memory

        # Action: Call the function
        x_memory, y_memory = ReportGenerationController.get_memory_usage()

        # Assert: Check the results
        self.assertEqual(x_memory, [])
        self.assertEqual(y_memory, [60])
    
    def test_generate_otp(self):
        '''
        Tests the generate_OTP method of the AccountController class in controller.
        Tests the type of the returned value whether it is a string format with length of 6.

        asserts:
        - True => if the returned string is a string data type and has length 6
        - False => if the returned string is not a string or does not have a length of 6
        '''
        otp = AccountController.generate_OTP()
        self.assertIsInstance(otp, str)
        self.assertEqual(len(otp), 6)

    def test_verify_otp(self):
        '''
        Tests the verify_OTP method of the AccountController class. Tests
        whether the input OTP is equal with the generated OTP.

        asserts:
        - True => if the input OTP and the generated OTP are equal
        - False => if the input OTP and the generated OTP is not equal
        '''
        val = AccountController.verify_OTP('111111', '111111')
        self.assertTrue(val)

if __name__ == '__main__':
    unittest.main()