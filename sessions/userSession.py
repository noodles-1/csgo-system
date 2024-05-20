import pickle
from datetime import datetime

class UserSession:
    @staticmethod
    def loadUserSession():
        '''
        Loads and retrieves a single user session from the userSession binary file.

        returns:
        - session: dict => contains the user ID and credentials of the current user
        session
        - None => if an error is encountered
        '''
        try:
            file = open('userSession', 'rb')
            session = pickle.load(file)
            file.close()
            return session
        except Exception as e:
            now = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
            file.write(f'[{now}] Error at function invocation session/userSession.py loadUserSession() - {repr(e)}\n')
            return None

    @staticmethod
    def storeUserSession(userData: dict):
        '''
        Stores the current user session after being logged in.

        returns:
        - True => if the user session storage was successful
        - False => if the user session storage encountered an error
        '''
        try:
            file = open('userSession', 'wb')
            pickle.dump(userData, file)
            file.close()
            return True
        except Exception as e:
            now = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
            file.write(f'[{now}] Error at function invocation session/userSession.py storeUserSession() - {repr(e)}\n')
            return False