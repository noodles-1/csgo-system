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
    @patch('controllers.dbController.DBController.usernameExists')
    def test_login_user(self, mock_username_exists, mock_get_user):
        '''
        Tests the loginUser method from DBController. Assumes that the username provided is valid, 
        exists, and can be logged in. This test case tests the functionality of the loginUser method 
        in identifying missing credentials and invalid email or username format while mocking database 
        transactions.

        asserts:
        - True => if the passwords match, then the user has successfully logged in
        - False => if the passwords do not match, or the email or username format is invalid
        '''
        mock_username_exists.return_value = True
        mock_get_user.return_value = MagicMock(password='321')

        response = db.loginUser('321', username='aasdf')
        self.assertTrue(response.ok)

    @patch('controllers.dbController.Session')
    @patch('controllers.dbController.DBController.licensePlateExists')
    def test_add_license_plate(self, mock_license_exists, mock_session):
        '''
        Tests the addLicensePlate method from DBController. Tests the insertion of a new
        license plate number if it does not already exist yet in the DetectedLicensePlate table.

        asserts:
        - True => if the license plate has been added
        - False => if the license plate has not been added
        '''
        mock_license_exists.return_value = False
        mock_session.add = MagicMock()
        mock_session.commit = MagicMock()

        response = db.addLicensePlate(1, 1, 1, 'AAA1111')
        self.assertTrue(response.ok)

    @patch('controllers.dbController.Session')
    @patch('controllers.dbController.DBController.licensePlateExists')
    def test_delete_license_plate(self, mock_license_exists, mock_session):
        '''
        Tests the deleteLicensePlate method from DBController. Tests the deletion of an already
        existing license plate number in the DetectedLicensePlate table.

        asserts:
        - True => if the license plate has been deleted
        - False => if the license plate has not been deleted
        '''
        mock_license_exists.return_value = True
        mock_session.delete = MagicMock()
        mock_session.commit = MagicMock()

        response = db.deleteLicensePlate('AAA1111')
        self.assertTrue(response.ok)

    @patch('controllers.dbController.Session')
    def test_edit_vehicle_price(self, mock_session):
        '''
        Tests the editVehiclePrice method from DBController. Tests the price update
        of the vehicle type where the price should be a positive number.

        asserts:
        - True => if the price update is successful
        - False => if the price update is unsuccessful
        '''
        mock_session.execute = MagicMock()
        mock_session.commit = MagicMock()

        response = db.editVehiclePrice(id=1, newPrice=500)
        self.assertTrue(response.ok)

    @patch('controllers.dbController.DBController.getUser')
    @patch('controllers.dbController.Session')
    def test_change_password(self, mock_session, mock_get_user):
        '''
        Tests the changePassword method from DBController. Tests the password change
        of an account considering that the new password and confirm password fields
        are non-empty and matching.

        asserts:
        - True => if the password change is successful
        - False => if the password change is unsuccessful
        '''
        mock_session.execute = MagicMock()
        mock_session.commit = MagicMock()
        mock_get_user.return_value = MagicMock(password='123')

        response = db.changePassword(email='a@gmail.com', newPassword='124', confirmPassword='124', currPassword='123')
        self.assertTrue(response.ok)
        
if __name__ == '__main__':
    unittest.main()