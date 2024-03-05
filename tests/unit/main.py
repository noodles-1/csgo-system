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

unittest.main()