import os
import sys
import re
import csv
import bcrypt

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from collections import defaultdict
from datetime import datetime
from datetime import timedelta
from models.connect import Connection
from models.schemas import User
from models.schemas import Camera
from models.schemas import DetectedLicensePlate
from models.schemas import CurrentSetting
from models.schemas import FutureSetting
from models.schemas import Congestion
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import or_
from sqlalchemy import and_
from sqlalchemy import asc
from sqlalchemy import desc
from sqlalchemy import text
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
            with open(os.path.join(parent, 'logs.txt'), 'a') as file:
                now = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                file.write(f'[{now}] Error at function invocation controllers/dbController.py emailExists() - {repr(e)}\n')
            return False
        
    @staticmethod
    def otherEmailExists(username, newEmail) -> bool:
        '''
        Checks if another email already exists in the User table in database aside from 
        the current user's email.

        params:
        - email: str => the email which will be checked for existence in the database

        returns:
        - True => if the executed query contains a User data
        - False => if the executed query does contain a User data
        '''
        try:
            user = DBController.getUser(username=username)
            with Session(Connection.engine) as session:
                stmt = select(User).where(and_(User.id != user.id, User.email == newEmail))
                result = session.scalar(stmt)
                return result is not None
        except Exception as e:
            with open(os.path.join(parent, 'logs.txt'), 'a') as file:
                now = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                file.write(f'[{now}] Error at function invocation controllers/dbController.py emailExists() - {repr(e)}\n')
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
            with open(os.path.join(parent, 'logs.txt'), 'a') as file:
                now = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                file.write(f'[{now}] Error at function invocation controllers/dbController.py usernameExists() - {repr(e)}\n')
            return False
        
    @staticmethod
    def otherUsernameExists(username, newUsername) -> bool:
        '''
        Checks if another username already exists in the User table in database
        aside from the current user's username.

        params:
        - username: str => the username which will be checked for existence in the database

        returns:
        - True => if the executed query contains a User data
        - False => if the executed query does contain a User data
        '''
        try:
            user = DBController.getUser(username=username)
            with Session(Connection.engine) as session:
                stmt = select(User).where(and_(User.id != user.id, User.username == newUsername))
                result = session.scalar(stmt)
                return result is not None
        except Exception as e:
            with open(os.path.join(parent, 'logs.txt'), 'a') as file:
                now = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                file.write(f'[{now}] Error at function invocation controllers/dbController.py emailExists() - {repr(e)}\n')
            return False
        
    @staticmethod
    def cameraExists(ip_addr='', name='') -> bool:
        '''
        Checks if a camera already exists with a specified IP address.

        params:
        - ip_addr (Optional): str => the IP address of the camera which will be checked for existence
        - name (Optional): str => the name of the camera which will be checked for existence

        returns:
        - True => if the executed query contains a Camera data
        - False => if the executed query does not contain a Camera data
        '''
        try:
            with Session(Connection.engine) as session:
                if name:
                    stmt = select(Camera).where(or_(Camera.id == ip_addr, Camera.name == name))
                else:
                    stmt = select(Camera).where(Camera.id == ip_addr)
                result = session.scalar(stmt)
                return result is not None
        except Exception as e:
            with open(os.path.join(parent, 'logs.txt'), 'a') as file:
                now = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                file.write(f'[{now}] Error at function invocation controllers/dbController.py cameraExists() - {repr(e)}\n')
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
            with open(os.path.join(parent, 'logs.txt'), 'a') as file:
                now = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                file.write(f'[{now}] Error at function invocation controllers/dbController.py getUser() - {repr(e)}\n')
            return None
        
    @staticmethod
    def getCamera(id=None, name=None):
        '''
        Retrieves the Camera data based from either the camera's IP address or name.

        params:
        - id (Optional): int => the id of the camera
        - name (Optional): str => the name of the camera

        returns:
        - result => the result containing the Camera data
        - None => if the query encountered an exception
        '''
        try:
            with Session(Connection.engine) as session:
                stmt = select(Camera)
                if name:
                    stmt = stmt.where(Camera.name == name)
                if id:
                    stmt = stmt.where(Camera.id == id)
                result = session.scalar(stmt)
                return result
        except Exception as e:
            with open(os.path.join(parent, 'logs.txt'), 'a') as file:
                now = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                file.write(f'[{now}] Error at function invocation controllers/dbController.py getCamera() - {repr(e)}\n')
            return None
        
    @staticmethod
    def getCurrentSetting(id: int):
        '''
        Acquires a CurrentSetting data based on its ID.

        params:
        - id: int => the ID of the current setting to acquire

        returns:
        - result => the result containing the CurrentSetting data
        - None => if the query encountered an exception
        '''
        try:
            with Session(Connection.engine) as session:
                stmt = select(CurrentSetting).where(CurrentSetting.id == id)
                result = session.scalar(stmt)
                return result
        except Exception as e:
            with open(os.path.join(parent, 'logs.txt'), 'a') as file:
                now = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                file.write(f'[{now}] Error at function invocation controllers/dbController.py getCurrentSetting() - {repr(e)}\n')
            return None
    
    @staticmethod
    def getActiveSetting():
        '''
        Retrieves the current active setting for the current date and time.

        returns:
        - result => the result containing the CurrentSetting data for the current date and time
        - None => if there is no CurrentSetting data for the current time or the query
        encountered an exception
        '''
        try:
            with Session(Connection.engine) as session:
                currTime = datetime.now().time()
                currDay = datetime.now().strftime('%A')

                stmt = select(CurrentSetting).where(and_(
                    CurrentSetting.day == currDay,
                    CurrentSetting.hourFrom <= currTime,
                    currTime <= CurrentSetting.hourTo
                ))
                result = session.scalar(stmt)
                return result
        except Exception as e:
            with open(os.path.join(parent, 'logs.txt'), 'a') as file:
                now = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                file.write(f'[{now}] Error at function invocation controllers/dbController.py getCurrentSetting() - {repr(e)}\n')
            return None

    @staticmethod
    def getFutureSetting(id: int):
        '''
        Retrieves the FutureSetting data from its ID.

        params:
        - id: int => the ID of the FutureSetting

        returns:
        - result => the result containing the FutureSetting data
        - None => if the query encountered an exception
        '''
        try:
            with Session(Connection.engine) as session:
                stmt = select(FutureSetting).where(FutureSetting.id == id)
                result = session.scalar(stmt)
                return result
        except Exception as e:
            with open(os.path.join(parent, 'logs.txt'), 'a') as file:
                now = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                file.write(f'[{now}] Error at function invocation controllers/dbController.py getFutureSetting() - {repr(e)}\n')
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
    
    @staticmethod
    def licensePlateExists(licenseNumber: str) -> bool:
        '''
        Checks if the license plate number already exists in the database.

        params:
        - licenseNumber: str => the license number which will be checked for existence in the database

        returns:
        - True => if the executed query contains a license plate data
        - False => if the executed query does contain a license plate data
        '''
        try:
            with Session(Connection.engine) as session:
                stmt = select(DetectedLicensePlate).where(DetectedLicensePlate.licenseNumber == licenseNumber)
                result = session.scalar(stmt)
                return result is not None
        except Exception as e:
            with open(os.path.join(parent, 'logs.txt'), 'a') as file:
                now = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                file.write(f'[{now}] Error at function invocation controllers/dbController.py licensePlateExists() - {repr(e)}\n')
            return False
        
    @staticmethod
    def getHashedPassword(password: str) -> str:
        '''
        Hashes a password and returns it.

        params:
        - password: str => the password to be hashed

        returns:
        - hashedPassword: str => the hashed password from the password parameter
        '''
        salt = bcrypt.gensalt()
        hashedPassword = bcrypt.hashpw(password.encode(), salt)
        return hashedPassword
    
    @staticmethod
    def passwordMatches(id: int, inputPassword: str) -> bool:
        '''
        Checks if an input password matches the password of the user from its ID.

        params:
        - id: int => the ID of the user, which will be checked if its password matches with the input password
        - inputPassword: str => the input password that will be compared with the hashed password of the user

        returns:
        - True => 
        '''
        try:
            with Session(Connection.engine) as session:
                stmt = select(User).where(User.id == id)
                user = session.scalar(stmt)
                inputPassword = inputPassword.encode()
                return bcrypt.checkpw(inputPassword, user.password.encode())
        except Exception as e:
            with open(os.path.join(parent, 'logs.txt'), 'a') as file:
                now = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                file.write(f'[{now}] Error at function invocation controllers/dbController.py passwordMatches() - {repr(e)}\n')
            return False
        
    '''
    Database transaction methods
    '''
    @staticmethod
    def registerUser(email: str, username: str, firstName: str, lastName: str, password: str, isAdmin=False, canChangePrice=False, canDownload=False, canChangeDetect=False, canEditHours=False) -> Response:
        '''
        Inserts a new row (if it doesn't already exist yet) in the User table containing the 
        auto-generated ID, email, username, full name, is admin, and password. Corresponding
        error messages are stored for invalid input.

        params:
        - email: str => the email inputted by the user for registration
        - username: str => the username inputted for registration
        - firstName: str => the first name inputted for registration
        - lastName: str => the last name inputted for registration
        - password: str => the password inputted for registration
        - isAdmin: bool => True if the user has admin privileges, and False otherwise

        returns:
        - response: Response => contains the response status and messages
        '''
        credentials = {'email': email, 'username': username, 'firstName': firstName, 'lastName': lastName, 'password': password}
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
                        firstName=firstName,
                        lastName=lastName,
                        isAdmin=isAdmin,
                        canChangeDetect=canChangeDetect,
                        canChangePrice=canChangePrice,
                        canEditHours=canEditHours,
                        canDownload=canDownload,
                        password=DBController.getHashedPassword(password)
                    )
                    session.add(user)
                    session.commit()
                    response.ok = True
        except Exception as e:
            response.ok = False
            response.messages['error'] = repr(e)

        return response
    
    @staticmethod
    def loginUser(password: str, username: str) -> Response:
        '''
        Checks for the existence of the User provided the username, checks whether the username 
        is in valid format, and compares the inputted hashed password with the hashed password 
        of the User in the database.

        params:
        - password: str => the hashed password from the input of the user
        - username: str => the username provided by the user

        returns:
        - response: Response => contains the response status, (error) messages, and User data that
        matched with the username provided by the user (considering that the passwords match)
        '''
        credentials = {'password': password, 'username': username}
        response = DBController.validateMissing(credentials)

        if not response.ok:
            return response
        
        try:
            if not DBController.isValidUsername(username):
                response.ok = False
                response.messages['error'] = 'Username error.'
                response.messages['username'] = 'Username should be alphanumeric only.'
                return response
            if not DBController.usernameExists(username):
                response.ok = False
                response.messages['error'] = 'Username error.'
                response.messages['username'] = 'Username does not exist.'
                return response
            user = DBController.getUser(username=username)
            if not DBController.passwordMatches(user.id, password):
                response.ok = False
                response.messages['error'] = 'Password error.'
                response.messages['password'] = 'Invalid username or password.'
                return response
            
            response.ok = True
            response.data = user
        except Exception as e:
            response.ok = False
            response.messages['error'] = repr(e)

        return response
    
    @staticmethod
    def addLicensePlate(userId: int, settingId: int, location: str, licenseNumber: str, vehicleType: str, price: float, imageUrl: str) -> Response:
        '''
        Adds a recognized license plate number from the object detection module to the database, 
        accompanied with the user ID, camera ID, vehicle type, and the time and date when the 
        detection occurred.

        params:
        - userId: str => the ID of the logged in user that detected the license plate
        - cameraId: str => the ID of the camera used in the detection of the license plate
        - priceId: str => the ID of the vehicle type with the variable price
        - licenseNubmer: str => the license plate number extracted using the OCR

        returns:
        - response: Response => contains the response status and error messages if any
        '''
        response = DBController.Response()

        try:
            with Session(Connection.engine) as session:
                license = DetectedLicensePlate(
                    userId=userId,
                    settingId=settingId,
                    location=location.lower(),
                    licenseNumber=licenseNumber,
                    vehicleType=vehicleType,
                    price=price,
                    date=datetime.now().date(),
                    time=datetime.now().time(),
                    image=imageUrl
                )
                session.add(license)
                session.commit()
                response.ok = True
        except Exception as e:
            response.ok = False
            response.messages['error'] = repr(e)

        return response
    
    @staticmethod
    def deleteLicensePlate(licenseNumber: str) -> Response:
        '''
        Deletes an already existing detected license plate from the database.

        params:
        - licenseNubmer: str => the license plate number to be deleted

        returns:
        - response: Response => contains the response status and error messages if any
        '''
        response = DBController.Response()

        try:
            if not DBController.licensePlateExists(licenseNumber):
                response.ok = False
                response.messages['error'] = 'Detected license plate number does not exist.'
            else:
                with Session(Connection.engine) as session:
                    stmt = select(DetectedLicensePlate).where(DetectedLicensePlate.licenseNumber == licenseNumber)
                    result = session.scalar(stmt)
                    session.delete(result)
                    session.commit()
                    response.ok = True
        except Exception as e:
            response.ok = False
            response.messages['error'] = repr(e)

        return response
    
    @staticmethod
    def getFilteredLicensePlates(vehicleType=None, date=None, hourFrom=None, hourTo=None):
        '''
        Retrieves the license plates based on a filter. Filter is optional and so will return the entire
        list in DetectedLicensePlate table.

        params:
        - vehicleType (Optional): str => the vehicle type that will be used for filtering results
        - date (Optional): date => the date filter
        - hourFrom (Optional): time => the lower bound time
        - hourTo (Optional): time => the upper bound time

        returns:
        - response: Response => contains the status of the response and error messages (if any)
        '''
        response = DBController.Response()
        
        try:
            with Session(Connection.engine) as session:
                stmt = select(DetectedLicensePlate)
                if vehicleType:
                    stmt = stmt.where(DetectedLicensePlate.vehicleType == vehicleType)
                if date and hourFrom and hourTo:
                    stmt = stmt.where(and_(
                        DetectedLicensePlate.date == date,
                        DetectedLicensePlate.time >= hourFrom,
                        DetectedLicensePlate.time <= hourTo
                    ))
                stmt = stmt.order_by(desc(DetectedLicensePlate.date)).order_by(desc(DetectedLicensePlate.time))
                results = session.execute(stmt).all()
                response.ok = True
                response.data = results
        except Exception as e:
            response.ok = False
            response.messages['error'] = repr(e)

        return response
    
    @staticmethod
    def editLicensePlate(licensePlate: str, newLicensePlate: str, vehicleType: str, price: float) -> Response:
        '''
        Edits a DetectedLicensePlate data.

        params:
        - licensePlate: str => the license plate data to be edited
        - newLicensePlate: str => the new license plate number to be replaced with the old license plate
        - vehicleType: str => the new vehicle type to be replaced with the old vehicle type
        - price: float => the new price to be replaced with the old price

        returns:
        - response: Response => contains the status of the response and error messages (if any)
        '''
        response = DBController.Response()

        try:
            with Session(Connection.engine) as session:
                stmt = update(DetectedLicensePlate).where(DetectedLicensePlate.licenseNumber == licensePlate).values(
                    licenseNumber=newLicensePlate,
                    vehicleType=vehicleType,
                    price=price
                )
                session.execute(stmt)
                session.commit()
                response.ok = True
        except Exception as e:
            response.ok = False
            response.messages['error'] = repr(e)

        return response
    
    @staticmethod
    def generateTemporaryCSV() -> Response:
        '''
        Generates a temporary CSV file polled every few constant minutes to be used for report generation
        methods found on controllers/controller.py.

        returns:
        - response: Response => contains the response status and error messages if any
        '''
        response = DBController.Response()

        try:
            with Session(Connection.engine) as session:
                stmt = select(DetectedLicensePlate)
                results = session.execute(stmt).all()
                with open('tempReports/temp.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['License Plate', 'Camera ID', 'Price ID', 'Time', 'Date'])
                    for result in results:
                        res = result[0]
                        writer.writerow([res.licenseNumber, res.cameraId, res.priceId, res.time, res.date])
                response.ok = True
        except Exception as e:
            response.ok = False
            response.messages['error'] = repr(e)

        return response
    
    @staticmethod
    def changePassword(email: str, newPassword: str, confirmPassword: str, currPassword=None) -> Response:
        '''
        Changes the password of the account associated with the email.

        params:
        - email: str => the email of the associated account
        - newPassword: str => the new password of the account
        - confirmPassword: str => verification of the new password
        - currPassword (Optional): str => the current password of the user

        returns:
        - response: Response => contains the response status and error messages if any
        '''
        credentials = {'newPassword': newPassword, 'confirmPassword': confirmPassword}
        if currPassword:
            credentials['currPassword'] = currPassword
        response = DBController.validateMissing(credentials)

        if not response.ok:
            return response
        
        try:
            user = DBController.getUser(email=email)
            if newPassword != confirmPassword:
                response.ok = False
                response.messages['error'] = 'Password error.'
                response.messages['password'] = 'Passwords do not match.'
                return response
            if DBController.passwordMatches(user.id, newPassword):
                response.ok = False
                response.messages['error'] = 'Password error.'
                response.messages['password'] = "New password can't be the current password."
                return response
            with Session(Connection.engine) as session:
                stmt = update(User).where(User.email == email).values(password=DBController.getHashedPassword(newPassword))
                session.execute(stmt)
                session.commit()
                response.ok = True
        except Exception as e:
            response.ok = False
            response.messages['error'] = repr(e)
        
        return response
    
    @staticmethod
    def registerCamera(ip_addr: str, name: str, location: str, originCoords: str, destCoords: str) -> Response:
        '''
        Registers a new camera with its IP address, camera name, and location.

        params:
        - ip_addr: str => the IP address for the new camera
        - name: str => the name for the new camera
        - location: str => the location where the new camera is placed

        returns:
        - response: Response => contains the response status and error messages if any
        '''
        response = DBController.Response()

        try:
            if DBController.cameraExists(name=name):
                response.ok = False
                response.messages['error'] = 'Camera name already exists.'
            else:
                with Session(Connection.engine) as session:
                    camera = Camera(
                        id=ip_addr,
                        name=name,
                        location=location.lower(),
                        originCoords=originCoords,
                        destCoords=destCoords
                    )
                    session.add(camera)
                    session.commit()
                    response.ok = True
        except Exception as e:
            response.ok = False
            response.messages['error'] = repr(e)
        
        return response
    
    @staticmethod
    def editCamera(oldName: str, newName: str, newLocation: str, newOriginCoords: str, newDestCoords: str) -> Response:
        '''
        Edits an existing camera with a new camera name and location.

        params:
        - oldName: str => the old name of the camera to be replaced
        - newName: str => the new name of the camera that will replace the old name
        - newLocation: str => the new location of the camera

        returns:
        - response: Response => contains the response status and error messages if any
        '''
        response = DBController.Response()

        try:
            if DBController.cameraExists(name=newName) and newName != DBController.getCamera(name=oldName).name:
                response.ok = False
                response.messages['error'] = 'Camera name already exists.'
            else:
                with Session(Connection.engine) as session:
                    stmt = update(Camera).where(Camera.name == oldName).values(
                        name=newName,
                        location=newLocation.lower(),
                        originCoords=newOriginCoords,
                        destCoords=newDestCoords
                    )
                    session.execute(stmt)
                    session.commit()
                    response.ok = True
        except Exception as e:
            response.ok = False
            response.messages['error'] = repr(e)

        return response

    @staticmethod
    def getCameras() -> Response:
        '''
        Retrieves all the cameras registered in the database.

        returns:
        - response: Response => contains the response status, cameras, and error messages if any
        '''
        response = DBController.Response()

        try:
            with Session(Connection.engine) as session:
                stmt = select(Camera)
                res = session.execute(stmt).all()
                response.ok = True
                response.data = res
        except Exception as e:
            response.ok = False
            response.messages['error'] = repr(e)
        
        return response
    
    @staticmethod
    def deleteCamera(name: str) -> Response:
        '''
        Deletes an already existing camera from the database.

        params:
        - name: str => the name of the camera to be deleted

        returns:
        - Response: Response => contains the response status and error messages if any
        '''
        response = DBController.Response()

        try:
            with Session(Connection.engine) as session:
                stmt = select(Camera).where(Camera.name == name)
                result = session.scalar(stmt)
                session.delete(result)
                session.commit()
                response.ok = True
        except Exception as e:
            response.ok = False
            response.messages['error'] = repr(e)
        
        return response
    
    @staticmethod
    def getUsers() -> Response:
        '''
        Retrieves all users in the User table.
        
        returns:
        - response: Response => contains the response status, users, and error messages if any
        '''
        response = DBController.Response()

        try:
            with Session(Connection.engine) as session:
                stmt = select(User)
                result = session.execute(stmt).all()
                response.ok = True
                response.data = result
        except Exception as e:
            response.ok = False
            response.messages['error'] = repr(e)
        
        return response
    
    @staticmethod
    def editUser(username: str, newUsername: str, newEmail: str, newFirstName: str, newLastName: str, newPassword: str, isAdmin: bool, canChangeDetect: bool, canChangePrice: bool, canEditHours: bool, canDownload: bool):
        '''
        Edits a user information with new credentials and permissions.

        params:
        - username: str => the username of the user to be edited
        - newUsername: str => the new username of the user
        - newEmail: str => the new email of the user
        - newFirstName: str => the new first name of the user
        - newLastName: str => the new last name of the user
        - newPassword: str => the new password of the user
        - isAdmin: bool => sets the administrative rights of a user
        - canChangeDetect: bool => sets the change detection right of a user
        - canChangePrice: bool => sets the change price right of a user
        - canEditHours: bool => sets the hour editing right of a user
        - canDownload: bool => sets the download right of a user

        returns:
        - response: Response => contains the response status and error messages if any
        '''
        credentials = {'username': newUsername, 'email': newEmail, 'firstName': newFirstName, 'lastName': newLastName, 'password': newPassword}
        response = DBController.validateMissing(credentials)

        if not response.ok:
            return response
        
        try:
            if not DBController.isValidEmail(newEmail):
                response.ok = False
                response.messages['error'] = 'Email error.'
                response.messages['email'] = 'Invalid email.'
            elif not DBController.isValidUsername(newUsername):
                response.ok = False
                response.messages['error'] = 'Username error.'
                response.messages['username'] = 'Username should be alphanumeric only.'
            elif DBController.otherEmailExists(username, newEmail):
                response.ok = False
                response.messages['error'] = 'Email error.'
                response.messages['email'] = 'Email already exists.'
            elif DBController.otherUsernameExists(username, newUsername):
                response.ok = False
                response.messages['error'] = 'Username error.'
                response.messages['username'] = 'Username already exists.'
            elif len(newUsername) > 50:
                response.ok = False
                response.messages['error'] = 'Username error.'
                response.messages['username'] = 'Length should be less than 50 characters.'
            else:
                with Session(Connection.engine) as session:
                    stmt = update(User).where(User.username == username).values(
                        username=newUsername,
                        email=newEmail,
                        firstName=newFirstName,
                        lastName=newLastName,
                        password=DBController.getHashedPassword(newPassword),
                        isAdmin=isAdmin,
                        canChangeDetect=canChangeDetect,
                        canChangePrice=canChangePrice,
                        canDownload=canDownload,
                        canEditHours=canEditHours
                    )
                    session.execute(stmt)
                    session.commit()
                    response.ok = True
        except Exception as e:
            response.ok = False
            response.messages['error'] = repr(e)

        return response
    
    @staticmethod
    def deleteUser(username: str) -> Response:
        '''
        Deletes an existing user based on its username.

        params:
        - username: str => the username of the user to be deleted

        returns:
        - response: Response => contains the response status and error messages if any
        '''
        response = DBController.Response()

        try:
            with Session(Connection.engine) as session:
                stmt = select(User).where(User.username == username)
                user = session.scalar(stmt)
                session.delete(user)
                session.commit()
                response.ok = True
        except Exception as e:
            response.ok = False
            response.messages['error'] = repr(e)

        return response
    
    @staticmethod
    def addCurrentSetting(hourFrom: datetime.time, hourTo: datetime.time, day: str, detectCar: bool, detectMotorcycle: bool, detectBus: bool, detectTruck: bool, carPrice: float, motorcyclePrice: float, busPrice: float, truckPrice: float) -> Response:
        '''
        Adds a new setting to be applied immediately. The new setting will overwrite existing current settings
        that have conflict with the said setting.

        params:
        - hourFrom: time => the lower bound time
        - hourTo: time => the upper bound time
        - day: str => specifies the day in a week
        - detectCar: bool => specifies whether the setting detects cars
        - detectMotorcycle: bool => specifies whether the setting detects motorcycles
        - detectBus: bool => specifies whether the setting detects buses
        - detectTruck: bool => specifies whether the setting detects trucks
        - carPrice: float => the price charged to a detected car
        - motorcyclePrice: float => the price charged to a detected motorcycle
        - busPrice: float => the price charged to a detected bus
        - truckPrice: float => the price charged to a detected truck

        returns:
        - response: Response => contains the response status and error messages if any
        '''
        response = DBController.Response()

        try:
            with Session(Connection.engine) as session:
                stmt = select(CurrentSetting).where(CurrentSetting.day == day)
                results = session.execute(stmt).all()

                for result in results:
                    hourFrom2, hourTo2 = result[0].hourFrom, result[0].hourTo
                    if hourFrom2 <= hourTo and hourFrom <= hourTo2:
                        session.delete(result[0])
                        session.commit()
                
                setting = CurrentSetting(
                    hourFrom=hourFrom,
                    hourTo=hourTo,
                    day=day,
                    detectCar=detectCar,
                    detectMotorcycle=detectMotorcycle,
                    detectBus=detectBus,
                    detectTruck=detectTruck,
                    carPrice=carPrice,
                    motorcyclePrice=motorcyclePrice,
                    busPrice=busPrice,
                    truckPrice=truckPrice
                )
                session.add(setting)
                session.commit()
                response.ok = True
        except Exception as e:
            response.ok = False
            response.messages['error'] = repr(e)

        return response
    
    @staticmethod
    def addFutureSetting(hourFrom: datetime.time, hourTo: datetime.time, day: str, startDate: datetime.date, startTime: datetime.time, detectCar: bool, detectMotorcycle: bool, detectBus: bool, detectTruck: bool, carPrice: float, motorcyclePrice: float, busPrice: float, truckPrice: float) -> Response:
        '''
        Adds a new setting to be applied in the future.

        params:
        - hourFrom: time => the lower bound time
        - hourTo: time => the upper bound time
        - day: str => specifies the day in a week
        - startDate: date => the date when the setting will be applied
        - startTime: time => the time the startDate in 24-hour format when the setting will be applied
        - detectCar: bool => specifies whether the setting detects cars
        - detectMotorcycle: bool => specifies whether the setting detects motorcycles
        - detectBus: bool => specifies whether the setting detects buses
        - detectTruck: bool => specifies whether the setting detects trucks
        - carPrice: float => the price charged to a detected car
        - motorcyclePrice: float => the price charged to a detected motorcycle
        - busPrice: float => the price charged to a detected bus
        - truckPrice: float => the price charged to a detected truck

        returns:
        - response: Response => contains the response status and error messages if any
        '''
        response = DBController.Response()

        try:
            with Session(Connection.engine) as session:
                setting = FutureSetting(
                    hourFrom=hourFrom,
                    hourTo=hourTo,
                    day=day,
                    startDate=startDate,
                    startTime=startTime,
                    detectCar=detectCar,
                    detectMotorcycle=detectMotorcycle,
                    detectBus=detectBus,
                    detectTruck=detectTruck,
                    carPrice=carPrice,
                    motorcyclePrice=motorcyclePrice,
                    busPrice=busPrice,
                    truckPrice=truckPrice
                )
                session.add(setting)
                session.commit()
                response.ok = True
        except Exception as e:
            response.ok = False
            response.messages['error'] = repr(e)

        return response
    
    @staticmethod
    def getCurrentSettings() -> Response:
        '''
        Acquires all the settings that have already been applied.

        returns:
        - response: Response => contains the response status, current applied settings, and error messages if any
        '''
        response = DBController.Response()

        try:
            with Session(Connection.engine) as session:
                stmt = select(CurrentSetting)
                results = session.execute(stmt).all()
                response.ok = True
                response.data = results
        except Exception as e:
            response.ok = False
            response.messages['error'] = repr(e)

        return response
    
    @staticmethod
    def getFutureSettings() -> Response:
        '''
        Acquires all the settings to be applied in the future.

        returns:
        - response: Response => contains the response status, future settings to be applied, and error messages if any
        '''
        response = DBController.Response()

        try:
            with Session(Connection.engine) as session:
                stmt = select(FutureSetting).order_by(asc(FutureSetting.startDate)).order_by(asc(FutureSetting.startTime))
                results = session.execute(stmt).all()
                response.ok = True
                response.data = results
        except Exception as e:
            response.ok = False
            response.messages['error'] = repr(e)

        return response
    
    @staticmethod
    def updateFutureSettings() -> Response:
        '''
        Updates the future settings to check whether their start date and time have
        already passed, and so will be added in the current settings.

        returns:
        - response: Response => contains the response status and error messages if any
        '''
        response = DBController.Response()

        try:
            with Session(Connection.engine) as session:
                currDate = datetime.now().date()
                currTime = datetime.now().time()

                stmt = select(FutureSetting).where(or_(
                    FutureSetting.startDate < currDate,
                    and_(
                        FutureSetting.startDate == currDate,
                        FutureSetting.startTime <= currTime
                    )
                )).order_by(asc(FutureSetting.id))
                results = session.execute(stmt).all()

                for result in results:
                    setting = result[0]
                    session.delete(setting)
                    session.commit()
                    response = DBController.addCurrentSetting(setting.hourFrom, setting.hourTo, setting.day, setting.detectCar, setting.detectMotorcycle, setting.detectBus, setting.detectTruck, setting.carPrice, setting.motorcyclePrice, setting.busPrice, setting.busPrice)
                    if not response.ok:
                        break
                response.ok = True
        except Exception as e:
            response.ok = False
            response.messages['error'] = repr(e)

        return response
    
    @staticmethod
    def editSetting(id: int, hourFrom: datetime.time, hourTo: datetime.time, day: str, detectCar: bool, detectMotorcycle: bool, detectBus: bool, detectTruck: bool, carPrice: float, motorcyclePrice: float, busPrice: float, truckPrice: float, isCurrentSetting: bool, startDate=None, startTime=None) -> Response:
        '''
        Edits a setting with new configurations.

        params:
        - hourFrom: time => the new lower bound time
        - hourTo: time => the new upper bound time
        - day: str => specifies the new day in a week
        - detectCar: bool => specifies whether the new setting detects cars
        - detectMotorcycle: bool => specifies whether the new setting detects motorcycles
        - detectBus: bool => specifies whether the new setting detects buses
        - detectTruck: bool => specifies whether the new setting detects trucks
        - carPrice: float => the price charged to a detected car
        - motorcyclePrice: float => the price charged to a detected motorcycle
        - busPrice: float => the price charged to a detected bus
        - truckPrice: float => the price charged to a detected truck
        - startDate (Optional): date => the new date when the setting will be applied
        - startTime (Optional): time => the new time the startDate in 24-hour format when the setting will be applied

        returns:
        - response: Response => contains the response status and error messages if any
        '''
        response = DBController.Response()

        try:
            with Session(Connection.engine) as session:
                if isCurrentSetting:
                    setting = DBController.getCurrentSetting(id)
                else:
                    setting = DBController.getFutureSetting(id)
                session.delete(setting)
                session.commit()
                if startDate and startTime:
                    response = DBController.addFutureSetting(hourFrom, hourTo, day, startDate, startTime, detectCar, detectMotorcycle, detectBus, detectTruck, carPrice, motorcyclePrice, busPrice, truckPrice)
                else:
                    response = DBController.addCurrentSetting(hourFrom, hourTo, day, detectCar, detectMotorcycle, detectBus, detectTruck, carPrice, motorcyclePrice, busPrice, truckPrice)
        except Exception as e:
            response.ok = False
            response.messages['error'] = repr(e)

        return response
    
    @staticmethod
    def deleteCurrentSetting(id: int) -> Response:
        '''
        Deletes a current setting with the specified setting ID.

        params:
        - id: int => the ID of the current setting which will be deleted

        returns:
        - response: Response => contains the response status and error messages if any
        '''
        response = DBController.Response()

        try:
            with Session(Connection.engine) as session:
                stmt = select(CurrentSetting).where(CurrentSetting.id == id)
                result = session.scalar(stmt)
                session.delete(result)
                session.commit()
                response.ok = True
        except Exception as e:
            response.ok = False
            response.messages['error'] = repr(e)

        return response
    
    @staticmethod
    def deleteFutureSetting(id: int) -> Response:
        '''
        Deletes a future setting with the specified setting ID.

        params:
        - id: int => the ID of the future setting which will be deleted

        returns:
        - response: Response => contains the response status and error messages if any
        '''
        response = DBController.Response()

        try:
            with Session(Connection.engine) as session:
                stmt = select(FutureSetting).where(FutureSetting.id == id)
                result = session.scalar(stmt)
                session.delete(result)
                session.commit()
                response.ok = True
        except Exception as e:
            response.ok = False
            response.messages['error'] = repr(e)

        return response
    
    @staticmethod
    def getLicenseData(location: str, hours: int) -> Response:
        '''
        Retrieves detected vehicles 2 hours from the current time on a
        location where they were detected.

        params:
        - location: str => the location where the vehicles have been detected

        returns:
        - response: Response => contains the response status, detected vehicles 2 hours from now, and error messages if any
        '''
        response = DBController.Response()

        try:
            with Session(Connection.engine) as session:
                time_24_hours_ago = (datetime.now() - timedelta(hours=hours)).strftime('%Y-%m-%d %H:%M:%S')
                stmt = select(DetectedLicensePlate).filter(
                    text(f"STR_TO_DATE(CONCAT(date, ' ', time), '%Y-%m-%d %H:%i:%s') >= '{time_24_hours_ago}'"),
                ).where(DetectedLicensePlate.location == location)
                results = session.execute(stmt).all()
                response.ok = True
                response.data = results
        except Exception as e:
            response.ok = False
            response.messages['error'] = repr(e)
        
        return response
    
    @staticmethod
    def getLocations() -> Response:
        '''
        Retrieves the unique locations of each camera.

        returns:
        - response: Response => contains the response status, location names, and error messages if any
        '''
        response = DBController.Response()

        try:
            with Session(Connection.engine) as session:
                stmt = select(Camera.location).group_by(Camera.location)
                results = session.execute(stmt).all()
                response.ok = True
                response.data = results
        except Exception as e:
            response.ok = False
            response.messages['error'] = repr(e)

        return response
    
    @staticmethod
    def addCongestion(location: str, congestion: float):
        '''
        Adds a congestion/traffic ratio on a location at the current date and time.

        params:
        - location: str => the location of the traffic
        - congestion: float => the traffic ratio between 0 to 1, where values closer to 0 denotes lighter traffic,
        and values closer 1 denotes heavier traffic

        returns:
        - response: Response => contains the response status
        '''
        response = DBController.Response()

        try:
            with Session(Connection.engine) as session:
                congestion = Congestion(
                    location=location,
                    congestion=congestion,
                    date=datetime.now().date(),
                    time=datetime.now().time()
                )
                session.add(congestion)
                session.commit()
                response.ok = True
        except Exception as e:
            response.ok = False
            response.messages['error'] = repr(e)
        
        return response