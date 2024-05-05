from schemas import Base
from sqlalchemy import create_engine

class Connection:
    def __init__(self):
        self.engine = None

    def createConnection(self, path):
        try:
            self.engine = create_engine(f'sqlite:///{path}', echo=True)
            return True
        except:
            return False
    
    def connect(self, path):
        if self.createConnection(path):
            Base.metadata.create_all(self.engine)
            return True
        else:
            return False