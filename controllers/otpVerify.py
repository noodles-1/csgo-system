import random
import smtplib

#function for generating a random 6 digit one-time pin
def otpGenerator():
    onetimePin = format(random.randint(0,999999), "06d")
    return onetimePin

#function for sending the otp to the user
def sendOTP(OTP, inputEmail):
    emailSubject = ("Your OTP - " + OTP)
    emailMessage = ("Hello! Your OTP is " + OTP + ". Use it to verify your account for logging in.")
    emailSent = f"subject:{emailSubject}\n\n{emailMessage}"
    smtpServer.sendmail("csgolpr001@gmail.com",inputEmail,emailSent)

#set up the email server and the sender email (this is just a temporary email with an app password i created at the date i wrote this code)
smtpServer = smtplib.SMTP('smtp.gmail.com',587)
smtpServer.starttls()
smtpServer.login("csgolpr001@gmail.com","dbfi jcfy febq rhba")

#setup for user's email address
userEmail = input("Enter your E-Mail address: ")

#calling the functions to generate an OTP and send the OTP to the user's email
mailOTP = otpGenerator()
sendOTP(mailOTP, userEmail)
print("Your OTP has been sent to your E-Mail!")

#verifying the OTP that the user will input
verifyOTP = input("Please enter your OTP: ")
while verifyOTP != mailOTP:
    verifyOTP = input("Incorrect OTP. Please enter the correct OTP: ")
    if verifyOTP == mailOTP:
        print("Account verified!")
        break