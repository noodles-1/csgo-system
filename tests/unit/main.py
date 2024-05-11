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
         # Assert: Verify the predicted license plate number
        self.assertEqual(predicted[0]['text'], 'FAA 9637')

# Run the test cases
unittest.main()