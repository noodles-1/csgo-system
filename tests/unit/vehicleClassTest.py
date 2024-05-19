import unittest
import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
root = os.path.dirname(parent)
sys.path.append(root)

from controllers.controller import AIController

class TestVehicleChange(unittest.TestCase):
    def test_add_class(self):
        '''
        Tests whether the ID of the vehicle has been added in the classes to detect by
        the vehicle detection model.

        asserts:
        - True => if the ID of the vehicle is in the classes
        - False => if the ID of the vehicle is not in the classes
        '''
        vehicleId = 0
        AIController.setVehicleClasses(vehicleId, True)
        self.assertIn(vehicleId, AIController.vehicleClasses)

    def test_remove_class(self):
        '''
        Tests whether the ID of the vehicle has been removed in the classes to detect by
        the vehicle detection model.

        asserts:
        - True => if the ID of the vehicle is not in the classes
        - False => if the ID of the vehicle is in the classes
        '''
        vehicleId = 0
        AIController.setVehicleClasses(vehicleId, False)
        self.assertNotIn(vehicleId, AIController.vehicleClasses)

if __name__ == '__main__':
    unittest.main()