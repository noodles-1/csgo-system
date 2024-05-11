import random
import smtplib

#function for generating a random 6 digit one-time pin
def otpGenerator():
    oneTimePin = format(random.randint(0,999999), "06d")
    return oneTimePin

#function for sending the otp to the user and setting up the email server and sender address (this is just a temporary email with an app password i created at the date i wrote this code)
def sendOTP(OTP, inputEmail):
    emailSubject = ("Your OTP - " + OTP)
    emailMessage = ("Hello! Your OTP is " + OTP + ". Use it to verify your account for logging in.")
    emailSent = f"subject:{emailSubject}\n\n{emailMessage}"
    smtpServer = smtplib.SMTP('smtp.gmail.com',587)
    smtpServer.starttls()
    smtpServer.login("csgolpr001@gmail.com","dbfi jcfy febq rhba")
    smtpServer.sendmail("csgolpr001@gmail.com",inputEmail,emailSent)
    print("Your OTP has been sent to your E-Mail!")

#function for verifying the OTP that the user will input
def verifyOTP(inputOTP, receivedOTP):
    while True:
        if inputOTP == receivedOTP:
            print("Account verified!")
            break
        else:
            inputOTP = input("Invalid OTP. Please input the correct OTP: ")
            continue
