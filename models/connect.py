from .schemas import Base
from sqlalchemy import create_engine

class Connection:
    '''
    Connection class to establish connection and build ORM with the database.
    '''
    engine = None

    @staticmethod
    def createConnection(path) -> bool:
        '''
        Creates a connection between the system and the database.

        params:
        - path: str => the path of the database (.db) file relative to the project's root directory

        returns:
        - True => if connection is successfully established
        - False => if connection failed to establish
        '''
        try:
            print(path)
            Connection.engine = create_engine(f'sqlite:///{path}', echo=True)
            return True
        except Exception as e:
            print(e)
            return False
    
    @staticmethod
    def connect(path) -> bool:
        '''
        Establishes a connection first. If successful, creates ORM and maps the tables 
        from models/schemas.py to the database.

        params:
        - path: str => the path of the database (.db) file relative to the project's root directory

        returns:
        - True => if connection is successfully established
        - False => if connection failed to establish 
        '''
        if Connection.createConnection(path):
            Base.metadata.create_all(Connection.engine)
            return True
        else:
            return False