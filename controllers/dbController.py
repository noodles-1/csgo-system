import os
import sys
import re
import csv

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from collections import defaultdict
from datetime import datetime
from models.connect import Connection
from models.schemas import User
from models.schemas import Camera
from models.schemas import DetectedLicensePlate
from models.schemas import Setting
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import or_
from sqlalchemy import and_
from sqlalchemy import desc
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
            with open('logs.txt', 'a') as file:
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
            with open('logs.txt', 'a') as file:
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
            with open('logs.txt', 'a') as file:
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
            with open('logs.txt', 'a') as file:
                now = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                file.write(f'[{now}] Error at function invocation controllers/dbController.py emailExists() - {repr(e)}\n')
            return False
        
    @staticmethod
    def cameraExists(ip_addr='', name='') -> bool:
        try:
            with Session(Connection.engine) as session:
                if name:
                    stmt = select(Camera).where(or_(Camera.id == ip_addr, Camera.name == name))
                else:
                    stmt = select(Camera).where(Camera.id == ip_addr)
                result = session.scalar(stmt)
                return result is not None
        except Exception as e:
            with open('logs.txt', 'a') as file:
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
            with open('logs.txt', 'a') as file:
                now = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                file.write(f'[{now}] Error at function invocation controllers/dbController.py getUser() - {repr(e)}\n')
            return None
        
    @staticmethod
    def getCamera(name: str):
        try:
            with Session(Connection.engine) as session:
                stmt = select(Camera).where(Camera.name == name)
                result = session.scalar(stmt)
                return result
        except Exception as e:
            with open('logs.txt', 'a') as file:
                now = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                file.write(f'[{now}] Error at function invocation controllers/dbController.py getCamera() - {repr(e)}\n')
            return None
        
    @staticmethod
    def getSetting(id: int):
        try:
            with Session(Connection.engine) as session:
                stmt = select(Setting).where(Setting.id == id)
                result = session.scalar(stmt)
                return result
        except Exception as e:
            with open('logs.txt', 'a') as file:
                now = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                file.write(f'[{now}] Error at function invocation controllers/dbController.py getSetting() - {repr(e)}\n')
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
            with open('logs.txt', 'a') as file:
                now = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                file.write(f'[{now}] Error at function invocation controllers/dbController.py licensePlateExists() - {repr(e)}\n')
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
            elif not DBController.usernameExists(username):
                response.ok = False
                response.messages['error'] = 'Username error.'
                response.messages['username'] = 'Username does not exist.'
            else:
                user = DBController.getUser(username=username)
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
    
    @staticmethod
    def addLicensePlate(userId: int, cameraId: int, licenseNumber: str, vehicleType: str, price: float, imageUrl: str) -> Response:
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
            if DBController.licensePlateExists(licenseNumber):
                response.ok = False
                response.messages['error'] = 'License plate already detected.'
            else:
                with Session(Connection.engine) as session:
                    license = DetectedLicensePlate(
                        userId=userId,
                        cameraId=cameraId,
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
            if currPassword and user.password != currPassword:
                response.ok = False
                response.messages['error'] = 'Password error.'
                response.messages['password'] = 'Current password is incorrect.'
                return response
            if newPassword != confirmPassword:
                response.ok = False
                response.messages['error'] = 'Password error.'
                response.messages['password'] = 'Passwords do not match.'
                return response
            if currPassword and currPassword == newPassword:
                response.ok = False
                response.messages['error'] = 'Password error.'
                response.messages['password'] = "New password can't be the current password."
                return response
            with Session(Connection.engine) as session:
                stmt = update(User).where(User.email == email).values(password=newPassword)
                session.execute(stmt)
                session.commit()
                response.ok = True
        except Exception as e:
            response.ok = False
            response.messages['error'] = repr(e)
        
        return response
    
    @staticmethod
    def registerCamera(ip_addr: str, name='', location='') -> Response:
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
                        location=location
                    )
                    session.add(camera)
                    session.commit()
                    response.ok = True
        except Exception as e:
            response.ok = False
            response.messages['error'] = repr(e)
        
        return response
    
    @staticmethod
    def editCamera(oldName: str, newName: str, newLocation: str) -> Response:
        response = DBController.Response()

        try:
            if newName and DBController.cameraExists(name=newName):
                response.ok = False
                response.messages['error'] = 'Camera name already exists.'
            else:
                with Session(Connection.engine) as session:
                    stmt = update(Camera).where(Camera.name == oldName)
                    if newName:
                        stmt = stmt.values(name=newName)
                    if newLocation:
                        stmt = stmt.values(location=newLocation)
                    session.execute(stmt)
                    session.commit()
                    response.ok = True
        except Exception as e:
            response.ok = False
            response.messages['error'] = repr(e)

        return response

    @staticmethod
    def getCameras() -> Response:
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
                        password=newPassword,
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
    def addSetting(hourFrom: datetime.time, hourTo: datetime.time, day: str, startDate: datetime.date, startTime: datetime.time, detectCar: bool, detectMotorcycle: bool, detectBus: bool, detectTruck: bool, carPrice: float, motorcyclePrice: float, busPrice: float, truckPrice: float) -> Response:
        response = DBController.Response()

        try:
            with Session(Connection.engine) as session:
                currDate = datetime.now().date()
                currTime = datetime.now().time()

                # Remove other overlapping intervals
                if currDate == startDate and startTime <= currTime:
                    stmt = select(Setting).where(and_(
                        Setting.day == day, 
                        or_(
                            Setting.startDate < currDate,
                            and_(
                                Setting.startDate == currDate,
                                Setting.startTime <= currTime
                            )
                        )
                    ))
                    results = session.execute(stmt).all()

                    for result in results:
                        hourFrom2, hourTo2 = result[0].hourFrom, result[0].hourTo
                        if hourFrom2 <= hourTo and hourFrom <= hourTo2:
                            session.delete(result[0])
                            session.commit()
                
                setting = Setting(
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
        response = DBController.Response()

        try:
            with Session(Connection.engine) as session:
                currDate = datetime.now().date()
                currTime = datetime.now().time()

                stmt = select(Setting).where(or_(
                    Setting.startDate < currDate,
                    and_(
                        Setting.startDate == currDate,
                        Setting.startTime <= currTime
                    )
                )).order_by(desc(Setting.startDate)).order_by(desc(Setting.startTime))
                results = session.execute(stmt).all()
                response.ok = True
                response.data = results
        except Exception as e:
            response.ok = False
            response.messages['error'] = repr(e)

        return response
    
    @staticmethod
    def getFutureSettings() -> Response:
        response = DBController.Response()

        try:
            with Session(Connection.engine) as session:
                currDate = datetime.now().date()
                currTime = datetime.now().time()

                stmt = select(Setting).where(or_(
                    currDate < Setting.startDate,
                    and_(
                        currDate == Setting.startDate,
                        currTime < Setting.startTime
                    )
                )).order_by(desc(Setting.startDate)).order_by(desc(Setting.startTime))
                results = session.execute(stmt).all()
                response.ok = True
                response.data = results
        except Exception as e:
            response.ok = False
            response.messages['error'] = repr(e)

        return response
    
    @staticmethod
    def editSetting(id: int, hourFrom: datetime.time, hourTo: datetime.time, day: str, startDate: datetime.date, startTime: datetime.time, detectCar: bool, detectMotorcycle: bool, detectBus: bool, detectTruck: bool, carPrice: float, motorcyclePrice: float, busPrice: float, truckPrice: float) -> Response:
        response = DBController.Response()

        try:
            with Session(Connection.engine) as session:
                stmt = select(Setting).where(Setting.id == id)
                res = session.scalar(stmt)
                session.delete(res)
                session.commit()

                response = DBController.addSetting(hourFrom, hourTo, day, startDate, startTime, detectCar, detectMotorcycle, detectBus, detectTruck, carPrice, motorcyclePrice, busPrice, truckPrice)
        except Exception as e:
            response.ok = False
            response.messages['error'] = repr(e)

        return response