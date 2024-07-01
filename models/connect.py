import os
import sys

from .schemas import Base
from sqlalchemy import create_engine

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(parent, '.env'))
RDS_ENDPOINT = os.getenv('RDS_ENDPOINT')
RDS_PORT = os.getenv('RDS_PORT')
RDS_DB = os.getenv('RDS_DB')
RDS_USER = os.getenv('RDS_USER')
RDS_PASSWORD = os.getenv('RDS_PASSWORD')

class Connection:
    '''
    Connection class to establish connection and build ORM with the database.
    '''
    engine = None

    @staticmethod
    def createConnection() -> bool:
        '''
        Creates a connection between the system and the database.

        returns:
        - True => if connection is successfully established
        - False => if connection failed to establish
        '''
        try:
            url = f'mysql+pymysql://{RDS_USER}:{RDS_PASSWORD}@{RDS_ENDPOINT}/{RDS_DB}'
            Connection.engine = create_engine(url, echo=True)
            return True
        except Exception as e:
            print(e)
            return False
    
    @staticmethod
    def connect() -> bool:
        '''
        Establishes a connection first. If successful, creates ORM and maps the tables 
        from models/schemas.py to the database.

        returns:
        - True => if connection is successfully established
        - False => if connection failed to establish 
        '''
        if Connection.createConnection():
            Base.metadata.create_all(Connection.engine)
            return True
        else:
            return False