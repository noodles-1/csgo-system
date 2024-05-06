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
from sqlalchemy.orm import Session

class DBController:
    class Response:
        def __init__(self):
            '''
            self.messages contains 'error', 'email', 'username', 'fullName', 'isAdmin', and 'password' keys 
            which maps to a string value denoting the message from the corresponding key
            '''
            self.ok: bool = None
            self.messages = defaultdict(str) 

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
    def isValidEmail(email) -> bool:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        return re.fullmatch(regex, email) is not None

    @staticmethod
    def isValidUsername(username) -> bool:
        regex = r'^[a-zA-Z0-9]*$'
        return re.fullmatch(regex, username) is not None
    
    @staticmethod
    def registerUser(email, username, fullName, password, isAdmin=False) -> Response:
        response = DBController.Response()

        credentialMapping = {'email': email, 'username': username, 'fullName': fullName, 'password': password}

        # validate if credentials are non-empty strings
        hasMissing = False
        for credential, value in credentialMapping.items():
            if not value:
                response.ok = False
                response.messages['error'] = 'Some fields are empty.'
                response.messages[credential] = 'Empty field.'
                hasMissing = True
        
        if hasMissing:
            return response
        
        try:
            if DBController.emailExists(email):
                response.ok = False
                response.messages['error'] = 'Email error.'
                response.messages['email'] = 'Email already exists.'
            elif DBController.usernameExists(username):
                response.ok = False
                response.messages['error'] = 'Username error.'
                response.messages['username'] = 'Username already exists.'
            elif not DBController.isValidEmail(email):
                response.ok = False
                response.messages['error'] = 'Email error.'
                response.messages['email'] = 'Invalid email.'
            elif not DBController.isValidUsername(username):
                response.ok = False
                response.messages['error'] = 'Username error.'
                response.messages['username'] = 'Username should be alphanumeric only.'
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
            response.errorMessage = repr(e)

        return response