import unittest
import sys
import os
import cv2

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
root = os.path.dirname(parent)
sys.path.append(root)

from controllers import controller

class TestControllerMethods(unittest.TestCase):
    # checks if an image has vehicles
    def test_has_vehicle(self):
        results = controller.detect_vehicle(frame=cv2.imread('test_images/1.jpg'))
        self.assertTrue(results[0].boxes)
    
    # checks if an image has a license plate
    def test_has_license_plate(self):
        results = controller.detect_license_plate(frame=cv2.imread('test_images/2.jpg'))
        self.assertTrue(results[0].boxes)

    # checks if an input license plate image's number matches with predicted number
    def test_validate_license(self):
        img = cv2.imread('test_images/7.jpg')
        img = cv2.resize(img, (0,0), fx=3, fy=3)
        img = cv2.GaussianBlur(img, (5,5), 0)
        predicted = controller.validate_license_number(frame=img)
        self.assertEqual(predicted.strip(), 'FAB3478')

unittest.main()