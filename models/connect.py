from schemas import Base
from sqlalchemy import create_engine

class Connection:
    engine = None

    @staticmethod
    def createConnection(path):
        try:
            Connection.engine = create_engine(f'sqlite:///{path}', echo=True)
            return True
        except Exception as e:
            print(e)
            return False
    
    @staticmethod
    def connect(path):
        if Connection.createConnection(path):
            Base.metadata.create_all(Connection.engine)
            return True
        else:
            return False