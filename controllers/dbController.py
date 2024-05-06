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
            self.messages contains 'error', 'email', 'username', 'fullName', 'isAdmin', and 'password' keys 
            which maps to a string value denoting the message from the corresponding key
            '''
            self.ok: bool = None
            self.messages = defaultdict(str)
            self.data = None

    '''
    Helper functions for database transactions
    '''
    @staticmethod
    def emailExists(email) -> bool:
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
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        return re.fullmatch(regex, email) is not None

    @staticmethod
    def isValidUsername(username) -> bool:
        regex = r'^[a-zA-Z0-9]*$'
        return re.fullmatch(regex, username) is not None
    
    @staticmethod
    def validateMissing(credentials: dict) -> Response:
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