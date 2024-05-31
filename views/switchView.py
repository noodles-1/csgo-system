import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import controllers.controller as cont

def showSettingsPage(parentFrame):
    parentFrame.show_frame(parentFrame.configFrame)
    cont.cameraEnabled = False

def showAdminPage(parentFrame, changeCameraDisplay, cap, placeholder_label):
    parentFrame.show_frame(parentFrame.adminFrame, changeCameraDisplay, cap, placeholder_label)
    cont.cameraEnabled = False

def showAnalyticsPage(parentFrame):
    parentFrame.show_frame(parentFrame.analyticsFrame)
    cont.cameraEnabled = False

def showDashboardPage(parentFrame):
    parentFrame.show_frame(parentFrame.dashboardFrame)
    cont.cameraEnabled = True

def showLoginPage(parentFrame):
    parentFrame.show_frame(parentFrame.loginFrame)
    cont.loggedIn = False
    cont.cameraEnabled = False
    
def showForgotPasswordPage(parentFrame):
    parentFrame.show_frame(parentFrame.forgotFrame)
    cont.loggedIn = False
    cont.cameraEnabled = False