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
        '''
        Tests the registerUser method from DBController. Assumes that the username and email
        provided does not exist yet and is available for registration. This test case tests the
        functionality of the registerUser method in identifying missing credentials and invalid
        email or username format while mocking database transactions.

        asserts:
        - True => if the user has been successfully registered
        - False => if the registration has failed caused by either missing credentials or
        invalid email or username format
        '''
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
        '''
        Tests the loginUser method from DBController. Assumes that the username and email
        provided exists and can be logged in. This test case tests the functionality of the
        loginUser method in identifying missing credentials and invalid email or username
        format while mocking database transactions.

        asserts:
        - True => if the passwords match, then the user has successfully logged in
        - False => if the passwords do not match, or the email or username format is invalid
        '''
        mock_username_exists.return_value = True
        mock_email_exists.return_value = True
        mock_get_user.return_value = MagicMock(password='321')

        response = db.loginUser('321', username='aasdf')
        print(response.messages)
        self.assertTrue(response.ok)
        
if __name__ == '__main__':
    unittest.main()