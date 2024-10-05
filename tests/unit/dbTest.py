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
    @patch('controllers.dbController.DBController.getHashedPassword')
    def test_register_user(self, mock_get_hashed_password, mock_username_exists, mock_email_exists, mock_session):
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
        mock_get_hashed_password.return_value = '1'
        mock_username_exists.return_value = False
        mock_email_exists.return_value = False
        mock_session.add = MagicMock()
        mock_session.commit = MagicMock()

        response = db.registerUser('a@gmail.com', 'a', 'ab', 'cd', '1', True, True, True, True, True)
        self.assertTrue(response.ok)

    @patch('controllers.dbController.DBController.passwordMatches')
    @patch('controllers.dbController.DBController.getUser')
    @patch('controllers.dbController.DBController.usernameExists')
    def test_login_user(self, mock_username_exists, mock_get_user, mock_password_matches):
        '''
        Tests the loginUser method from DBController. Assumes that the username provided is valid, 
        exists, and can be logged in. This test case tests the functionality of the loginUser method 
        in identifying missing credentials and invalid email or username format while mocking database 
        transactions.

        asserts:
        - True => if the passwords match, then the user has successfully logged in
        - False => if the passwords do not match, or the email or username format is invalid
        '''
        mock_password_matches.return_value = True
        mock_username_exists.return_value = True
        mock_get_user.return_value = MagicMock(password='1')

        response = db.loginUser('1', 'a')
        print(response.ok, response.messages)
        self.assertTrue(response.ok)

    @patch('controllers.dbController.Session')
    def test_add_license_plate(self, mock_session):
        '''
        Tests the addLicensePlate method from DBController. Tests the insertion of a new
        license plate number if it does not already exist yet in the DetectedLicensePlate table.

        asserts:
        - True => if the license plate has been added
        - False => if the license plate has not been added
        '''
        mock_session.add = MagicMock()
        mock_session.commit = MagicMock()

        response = db.addLicensePlate(1, 1, 'morayta', 'AAA1111', 'car', 100, 'none')
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

    @patch('controllers.dbController.DBController.passwordMatches')
    @patch('controllers.dbController.DBController.getHashedPassword')
    @patch('controllers.dbController.DBController.getUser')
    @patch('controllers.dbController.Session')
    def test_change_password(self, mock_session, mock_get_user, mock_get_hashed_password, mock_password_matches):
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
        mock_get_hashed_password.return_value = '1'
        mock_password_matches.return_value = False

        response = db.changePassword(email='a@gmail.com', newPassword='124', confirmPassword='124')
        self.assertTrue(response.ok)

    @patch('controllers.dbController.Session')
    @patch('controllers.dbController.DBController.cameraExists')
    def test_register_camera(self, mock_camera_exists, mock_session):
        '''
        Tests the registerCamera method from DBController. Tests the addition of a new
        camera by considering existing cameras with the same IP address or name.

        asserts:
        - True => if the camera registration is successful
        - False => if the camera reigstration is unsuccessful
        '''
        mock_camera_exists.return_value = False
        mock_session.add = MagicMock()
        mock_session.commit = MagicMock()
        
        response = db.registerCamera(ip_addr='1', name='cam1', location='morayta')
        self.assertTrue(response.ok)

    @patch('controllers.dbController.Session')
    @patch('controllers.dbController.DBController.cameraExists')
    def test_edit_camera(self, mock_camera_exists, mock_session):
        '''
        Tests the editCamera method. Tests the editing of an existing camera considering
        whether a camera already exists with the new name.

        asserts:
        - True => if the camera editing is successful
        - False => if the camera editing is unsuccessful
        '''
        mock_camera_exists.return_value = False
        mock_session.add = MagicMock()
        mock_session.commit = MagicMock()

        response = db.editCamera(oldName='cam1', newName='cam2', newLocation='espanya')
        self.assertTrue(response.ok)

    @patch('controllers.dbController.Session')
    @patch('controllers.dbController.DBController.otherEmailExists')
    @patch('controllers.dbController.DBController.otherUsernameExists')
    @patch('controllers.dbController.DBController.getHashedPassword')
    def test_edit_user(self, mock_get_hashed_password, mock_other_username_exists, mock_other_email_exists, mock_session):
        '''
        Tests the editUser method. Tests the editing of an existing user's credentials
        considering the existence of the same username and email for the new username
        and email.

        asserts:
        - True => if the user editing is successful
        - False => if the user editing is unsuccessful
        '''
        mock_get_hashed_password.return_value = '1'
        mock_other_username_exists.return_value = False
        mock_other_email_exists.return_value = False
        mock_session.execute = MagicMock()
        mock_session.commit = MagicMock()

        response = db.editUser('a', 'b', 'b@gmail.com', 'bc', 'de', '123', False, False, True, False, True)
        self.assertTrue(response.ok)
        
if __name__ == '__main__':
    unittest.main()