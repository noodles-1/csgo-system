import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from models.connect import Connection
from models.schemas import User
from models.schemas import Camera
from models.schemas import DetectedLicensePlate
from sqlalchemy import select
from sqlalchemy.orm import Session

class DBController:
    @staticmethod
    def registerUser(email, username, fullName, isAdmin, password):
        try:
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
                return True
        except Exception as e:
            print(e)
            return False