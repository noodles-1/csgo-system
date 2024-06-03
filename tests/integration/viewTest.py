import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from tkinter import Tk

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
root = os.path.dirname(parent)
sys.path.append(root)

from views import view as v

class TestGUI(unittest.TestCase):
    @patch('controllers.dbController.DBController.getCameras')
    def test_gui_exists(self, mock_get_cameras):
        # Create a MagicMock object to mimic the behavior of cameras.data
        mock_cameras_data = MagicMock()
        mock_cameras_data.data = [(MagicMock(name='Camera1'),), (MagicMock(name='Camera2'),)]  # Example data
        
        # Set the return value of mock_get_cameras to the MagicMock object
        mock_get_cameras.return_value = mock_cameras_data
        
        view = v.MainWindow()
        print(view)
        self.assertIsNotNone(view)   
        
if __name__ == '__main__':
    unittest.main()
