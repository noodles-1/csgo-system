import unittest
import sys
import os
import cv2

# Arrange: Define current and parent directories
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)

# before
# remove - root = os.path.dirname(parent)
# remove - sys.path.append(root)

# before season 2
# remove sys.path.append(parent)

# Arrange: Define root directory and add it to sys.path
root = os.path.dirname(parent)
sys.path.append(root)

# Import the controller module from the controllers package
from controllers import controller

# Instantiate AIController from the controller module
ai = controller.AIController()

class TestControllerMethods(unittest.TestCase):
    # checks if an image has vehicles
   # def test_has_vehicle(self):
    #    results = ai.detect_vehicle(frame=cv2.imread('test_images/1.jpg'))
     #   self.assertTrue(results[0].boxes)
    
    # checks if an image has a license plate
    #def test_has_license_plate(self):
     #   results = ai.detect_license_plate(frame=cv2.imread('test_images/2.jpg'))
      #  self.assertTrue(results[0].boxes)

    # checks if an input license plate image's number matches with predicted number
    def test_validate_license(self):
         # Arrange: Define test method to validate license plate
        # before
        # remove - img = cv2.imread('../test_images/1.jpg')
        #after
         # Arrange: Load the image
        img = cv2.imread('test_images/9.jpg')

        # Action: Preprocess the image
        img = cv2.resize(img, (0,0), fx=3, fy=3)
        img = cv2.GaussianBlur(img, (5,5), 0)
         # Action: Get predicted license plate number using AIController
        predicted = ai.get_license_number_cnocr(frame=img)
        self.assertEqual(predicted.strip(), 'FAB3478')

    def setUp(self):
        # Arrange: Initialize ReportGenerationController instance and set file path
        self.reportController = ctrl.ReportGenerationController()
        self.file_path = "dummy_data/data.csv"

    def test_busiestTimeReport(self):
        # Action: Call busiestTimeReport function and store returned xData and yData
        x_data, y_data = self.reportController.busiestTimeReport(self.file_path)
        
        # Assert: Check if xData and yData are lists
        self.assertIsInstance(x_data, list)
        self.assertIsInstance(y_data, list)
        
        # Assert: Check if each element in xData is a string
        for x in x_data:
            self.assertIsInstance(x, str)
        
        # Assert: Check if each element in yData is an integer
        for y in y_data:
            self.assertIsInstance(y, int)

    def test_revenueReport(self):
        '''
        This unit testing may need updating in the future. Since the function relies on the Date Today.
        It takes the last 15 days from the Date Today.
        If the CSV is changed. The expected dates and revenues may need updating.
        '''
        # Arrange: Define expected dates and revenues
        expected_dates = ['2024-12-27', '2024-12-25', '2024-12-12', '2024-12-11', '2024-11-19', '2024-11-18', '2024-11-16', '2024-11-12', '2024-11-08', '2024-11-05', '2024-11-04', '2024-11-02', '2024-11-01', '2024-10-31', '2024-10-30']
        expected_revenues = [950, 500, 1200, 1100, 1050, 500, 1800, 550, 900, 1100, 2150, 700, 50, 150, 1850]
        
        # Action: Call revenueReport function
        latest_dates, latest_revenues = self.reportController.revenueReport(self.file_path)
        
        # Assert: Check if the latest dates match the expected dates
        self.assertEqual(latest_dates, expected_dates)
        
        # Assert: Check if the latest revenues match the expected revenues
        self.assertEqual(latest_revenues, expected_revenues)

    def test_vehiclesDetectedReport(self):
        # Action: Call vehiclesDetectedReport function and store returned xData and yData
        x_data, y_data = self.reportController.vehiclesDetectedReport(self.file_path)
        
        # Assert: Check if xData and yData are lists
        self.assertIsInstance(x_data, list)
        self.assertIsInstance(y_data, list)
        
        # Assert: Check if each element in xData is a string
        for x in x_data:
            self.assertIsInstance(x, str)
        
        # Assert: Check if each element in yData is an integer
        for y in y_data:
            self.assertIsInstance(y, int)

    def test_successful_download_and_process(self):
        # Arrange: Create a test CSV file with dummy data
        test_csv_data = "dummy_data/testData.csv"
        with open(test_csv_data, "w") as f:
            f.write("column1,column2\nvalue1,value2\n")
        
        # Action: Call downloadAndProcessCSV method to download and process the test CSV file
        report_controller = ctrl.ReportGenerationController()
        success, output_path = report_controller.downloadAndProcessCSV(test_csv_data)

        # Assert: Check if the download and processing were successful
        self.assertTrue(success)
        self.assertTrue(os.path.exists(output_path))

        # Clean up: Remove the test CSV file and the processed output file
        os.remove(test_csv_data)
        os.remove(output_path)
        
    def test_missing_file(self):
        # Arrange: Specify the path to a nonexistent file
        invalid_file_path = "dummy_data/nonexistent.csv"

        # Action and Assert: Check if an exception is raised when attempting to download and process the nonexistent file
        with self.assertRaises(FileNotFoundError):
            # Call downloadAndProcessCSV() with the invalid file path
            success, output_path = self.reportController.downloadAndProcessCSV(invalid_file_path)
    
    @patch('controllers.controller.psutil.cpu_percent')
    def test_get_cpu_usage(self, mock_cpu_percent):
        # Arrange: Mock the psutil.cpu_percent function
        mock_cpu_percent.return_value = 50  # Simulate 50% CPU usage

        # Action: Call the function
        x_cpu, y_cpu = ctrl.get_cpu_usage()

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
        x_memory, y_memory = ctrl.get_memory_usage()

        # Assert: Check the results
        self.assertEqual(x_memory, [])
        self.assertEqual(y_memory, [60])

# Run the test cases
unittest.main()