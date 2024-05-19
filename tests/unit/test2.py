import unittest
import os
import sys

# Adjust the import path according to your project structure
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
root = os.path.dirname(parent)
sys.path.append(root)

# Import the toggle_classes function
from controllers.vehicleToDetect import toggle_classes

class TestToggleClasses(unittest.TestCase):

    def test_toggle_classes(self):
        classes = ['car', 'motorcycle', 'jeepney', 'bus', 'tricycle', 'van', 'truck', 'taxi', 'modern_jeepney']
        classes_enabled = [False] * 9
        
        # Test case 1: toggle 'car', 'taxi', 'jeepney'
        result = toggle_classes(classes, classes_enabled.copy(), ['car', 'taxi', 'jeepney'])
        self.assertEqual(result, [0, 2, 7])
        
        # Test case 2: toggle 'bus', 'van', 'truck'
        result = toggle_classes(classes, classes_enabled.copy(), ['bus', 'van', 'truck'])
        self.assertEqual(result, [3, 5, 6])
        
        # Test case 3: vehicle not in list
        result = toggle_classes(classes, classes_enabled.copy(), ['plane'])
        self.assertTrue(result.startswith("Error"))

    def test_toggle_invalid_vehicle(self):
        classes = ['car', 'motorcycle', 'jeepney', 'bus', 'tricycle', 'van', 'truck', 'taxi', 'modern_jeepney']
        classes_enabled = [False] * 9
        
        # Test invalid vehicle type
        result = toggle_classes(classes, classes_enabled.copy(), ['bicycle'])
        self.assertTrue(result.startswith("Error"))

    def test_no_vehicle_toggled(self):
        classes = ['car', 'motorcycle', 'jeepney', 'bus', 'tricycle', 'van', 'truck', 'taxi', 'modern_jeepney']
        classes_enabled = [False] * 9
        
        # Test with no vehicles to toggle
        result = toggle_classes(classes, classes_enabled.copy(), [])
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
