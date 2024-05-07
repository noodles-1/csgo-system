import os
import sys
import re

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from collections import defaultdict
from models.connect import Connection
from models.schemas import User
from models.schemas import Camera
from models.schemas import DetectedLicensePlate
from sqlalchemy import select
from sqlalchemy import or_
from sqlalchemy.orm import Session

class DBController:
    '''
    Response class to contain response status and messages from database transactions performed
    '''
    class Response:
        def __init__(self):
            '''
            vars:

            - self.ok: bool => specifies whether the response is successful (OK) or not

            - self.messages: dict => contains 'error', 'email', 'username', 'fullName', 'isAdmin', and 'password' keys 
            which maps to a string value denoting the message from the corresponding key

            - self.data => contains the result of the executed query statement
            '''
            self.ok: bool = None
            self.messages = defaultdict(str)
            self.data = None

    '''
    Helper functions for database transactions
    '''
    @staticmethod
    def emailExists(email) -> bool:
        '''
        Checks if the email already exists in the User table in database.

        params:
        - email: str => the email which will be checked for existence in the database

        returns:
        - True => if the executed query contains a User data
        - False => if the executed query does contain a User data
        '''
        try:
            with Session(Connection.engine) as session:
                stmt = select(User).where(User.email == email)
                result = session.scalar(stmt)
                return result is not None
        except Exception as e:
            print(repr(e))
            return False
        
    @staticmethod
    def usernameExists(username) -> bool:
        '''
        Checks if the username already exists in the User table in database.

        params:
        - username: str => the username which will be checked for existence in the database

        returns:
        - True => if the executed query contains a User data
        - False => if the executed query does contain a User data
        '''
        try:
            with Session(Connection.engine) as session:
                stmt = select(User).where(User.username == username)
                result = session.scalar(stmt)
                return result is not None
        except Exception as e:
            print(repr(e))
            return False
        
    @staticmethod
    def getUser(email='', username=''):
        '''
        Retrieves the row from the User table that matches with the email or username.

        params:
        - email (Optional): str => the email which will be checked in the database
        - username (Optional): str => the username which will be checked in the database

        returns:
        - result => the result containing the User data that matched with either the email or username
        - None => if the query encountered an exception
        '''
        try:
            with Session(Connection.engine) as session:
                stmt = select(User).where(or_(User.email == email, User.username == username))
                result = session.scalar(stmt)
                return result
        except Exception as e:
            print(repr(e))
            return None
        
    @staticmethod
    def isValidEmail(email) -> bool:
        '''
        Checks if the email provided is in valid email format.

        params:
        - email: str => the email which will be checked whether it conforms with the regular expression

        returns:
        - True => if the email conforms with the regular expression, and follows a valid email format
        - False => if the email is not in a valid email format
        '''
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        return re.fullmatch(regex, email) is not None

    @staticmethod
    def isValidUsername(username) -> bool:
        '''
        Checks if the username provided is in valid format. Valid username should only consist of
        alphanumeric characters.

        params:
        - email: str => the username which will be checked whether it conforms with the regular expression

        returns:
        - True => if the username conforms with the regular expression, and follows the valid username format
        - False => if the username is not in a valid username format
        '''
        regex = r'^[a-zA-Z0-9]*$'
        return re.fullmatch(regex, username) is not None
    
    @staticmethod
    def validateMissing(credentials: dict) -> Response:
        '''
        Checks each credential whether they are non-empty strings and provides an error message
        for fields that are empty.

        params:
        - credentials: dict => contains the credentials inputted by the user regardless of login
        or register input

        returns:
        - response: Response => contains the response status and messages
        '''
        response = DBController.Response()
        response.ok = True

        for credential, value in credentials.items():
            if not value:
                response.ok = False
                response.messages['error'] = 'Some fields are empty.'
                response.messages[credential] = 'Empty field.'

        return response
    
    '''
    Database transaction methods
    '''
    @staticmethod
    def registerUser(email, username, fullName, password, isAdmin=False) -> Response:
        '''
        Inserts a new row (if it doesn't already exist yet) in the User table containing the 
        auto-generated ID, email, username, full name, is admin, and password. Corresponding
        error messages are stored for invalid input.

        params:
        - email: str => the email inputted by the user for registration
        - username: str => the username inputted for registration
        - fullName: str => the full name inputted for registration
        - password: str => the password inputted for registration
        - isAdmin: bool => True if the user has admin privileges, and False otherwise

        returns:
        - response: Response => contains the response status and messages
        '''
        credentials = {'email': email, 'username': username, 'fullName': fullName, 'password': password}
        response = DBController.validateMissing(credentials)

        if not response.ok:
            return response
        
        try:
            if not DBController.isValidEmail(email):
                response.ok = False
                response.messages['error'] = 'Email error.'
                response.messages['email'] = 'Invalid email.'
            elif not DBController.isValidUsername(username):
                response.ok = False
                response.messages['error'] = 'Username error.'
                response.messages['username'] = 'Username should be alphanumeric only.'
            elif DBController.emailExists(email):
                response.ok = False
                response.messages['error'] = 'Email error.'
                response.messages['email'] = 'Email already exists.'
            elif DBController.usernameExists(username):
                response.ok = False
                response.messages['error'] = 'Username error.'
                response.messages['username'] = 'Username already exists.'
            elif len(username) > 50:
                response.ok = False
                response.messages['error'] = 'Username error.'
                response.messages['username'] = 'Length should be less than 50 characters.'
            else:
                with Session(Connection.engine) as session:
                    user = User(
                        email=email, 
                        username=username,
                        fullName=fullName,
                        isAdmin=isAdmin,
                        password=password
                    )
                    session.add(user)
                    session.commit()
                    response.ok = True
        except Exception as e:
            response.ok = False
            response.messages['error'] = repr(e)

        return response
    
    @staticmethod
    def loginUser(password, email='', username='') -> Response:
        '''
        Checks for the existence of the User provided the email or username, and
        compares the inputted hashed password with the hashed password of the User
        in the database. This method assumes that an input field accepts either an
        email or username for logging the user in.

        params:
        - password: str => the hashed password from the input of the user
        - email (Optional): str => the email provided by the user
        - username (Optional): str => the username provided by the user

        returns:
        - response: Response => contains the response status, (error) messages, and User data that
        matched with the email or username provided by the user (considering that the passwords match)
        '''
        credentials = {'password': password}
        if email:
            credentials['email'] = email
        else:
            credentials['username'] = username

        response = DBController.validateMissing(credentials)

        if not response.ok:
            return response
        
        try:
            if (email and not DBController.isValidEmail(email)) or (username and not DBController.isValidUsername(username)):
                response.ok = False
                response.messages['error'] = 'Email or username error.'
                response.messages['email'] = 'Invalid email or username.'
                response.messages['username'] = 'Invalid email or username.'
            elif (email and not DBController.emailExists(email)):
                response.ok = False
                response.messages['error'] = 'Email error.'
                response.messages['email'] = 'Email does not exist.'
            elif (username and not DBController.usernameExists(username)):
                response.ok = False
                response.messages['error'] = 'Username error.'
                response.messages['username'] = 'Username does not exist.'
            else:
                user = DBController.getUser(email=email, username=username)

                if user.password != password:
                    response.ok = False
                    response.messages['error'] = 'Password error.'
                    response.messages['password'] = 'Passwords do not match.'
                else:
                    response.ok = True
                    response.data = user
        except Exception as e:
            response.ok = False
            response.messages['error'] = repr(e)

        return response