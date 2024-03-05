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
    def test_has_vehicle(self):
        results = controller.detect_vehicle(frame=cv2.imread('<image>'))
        self.assertTrue(results[0].boxes)

    def test_validate_license(self):
        img = cv2.imread('<image>')
        img = cv2.resize(img, (0,0), fx=3, fy=3)
        img = cv2.GaussianBlur(img, (5,5), 0)
        predicted = controller.validate_license_number(frame=img)
        self.assertEqual(predicted.strip(), '<actual license plate number>')

unittest.main()