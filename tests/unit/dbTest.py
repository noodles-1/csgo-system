import os
import sys
import unittest

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
root = os.path.dirname(parent)
sys.path.append(root)

from unittest.mock import patch, MagicMock
from controllers.dbController import DBController as db

class TestDBControllerMethods(unittest.TestCase):
    @patch('controllers.dbController.Session')
    @patch('controllers.dbController.DBController.emailExists')
    @patch('controllers.dbController.DBController.usernameExists')
    def test_register_user(self, mock_username_exists, mock_email_exists, mock_session):
        mock_username_exists.return_value = False
        mock_email_exists.return_value = False
        mock_session.add = MagicMock()
        mock_session.commit = MagicMock()

        response = db.registerUser('a@gmail.com', 'a', 'abcd', '123', False)
        self.assertTrue(response.ok)

    @patch('controllers.dbController.DBController.getUser')
    @patch('controllers.dbController.DBController.emailExists')
    @patch('controllers.dbController.DBController.usernameExists')
    def test_login_user(self, mock_username_exists, mock_email_exists, mock_get_user):
        mock_username_exists = False
        mock_email_exists = False
        mock_get_user.return_value = MagicMock(password='321')

        response = db.loginUser('321', username='aasdf')
        self.assertTrue(response.ok)
        
if __name__ == '__main__':
    unittest.main()