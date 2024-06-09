import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from datetime import datetime
from controllers.dbController import DBController


class PollController:
    currSetting = None
    analyticsShown = False
    
    @staticmethod
    def updateFutureSettings():
        response = DBController.updateFutureSettings()
        
        if not response.ok:
            with open(os.path.join(parent, 'logs.txt', 'a')) as file:
                now = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                file.write(f'[{now}] Error at function invocation controllers/pollController.py updateFutureSettings() - {repr(response.messages["error"])}\n')
    
    @staticmethod
    def updateActiveSetting():
        PollController.currSetting = DBController.getActiveSetting()