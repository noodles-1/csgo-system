import os
import re
import bcrypt  # Import bcrypt for password hashing
import hmac

# Placeholder dictionary to simulate user passwords in the database
user_passwords = {
    "1": bcrypt.hashpw("password1".encode(), bcrypt.gensalt()),
    "2": bcrypt.hashpw("password2".encode(), bcrypt.gensalt()),
    "3": bcrypt.hashpw("password3".encode(), bcrypt.gensalt()),
    "4": bcrypt.hashpw("password4".encode(), bcrypt.gensalt()),
    "5": bcrypt.hashpw("password5".encode(), bcrypt.gensalt()),
    # Add more user passwords as needed
}

def changePassword(currentPassword, newPassword, userId):
    try:
        # Connect to your authentication system (will be changed with actual implementation)
        storedHashedPassword = getHashedPassword(userId)

        # Verify the entered current password against the stored hash
        if not verifyPassword(currentPassword, storedHashedPassword):
            return False, "Incorrect current password"

        # Hash the new password
        hashedNewPassword = hashPassword(newPassword)

        # Update the user's password in the authentication system
        updateUserPassword(userId, hashedNewPassword)

        return True, "Password changed successfully"
    except Exception as e:
        return False, f"An error occurred: {e}"

def verifyNewPassword(password):
    # Password requirements: at least 1 uppercase letter, 1 number, 1 special character, and minimum length of 8 characters
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[!@#$%^&*()-_+=]', password):
        return False
    return True

def verifyPassword(password, storedHashedPassword):
    # Use a secure comparison function (e.g., constant_time_compare)
    print("Stored: ", storedHashedPassword)
    password = password.encode("utf-8")
    return bcrypt.checkpw(password, storedHashedPassword)


def hashPassword(password): 
    # Use bcrypt to hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password

# Function to input new password twice for verification
def inputNewPassword():
    while True:
        newPassword = input("Enter new password: ")
        confirmPassword = input("Confirm new password: ")
        if newPassword == confirmPassword:
            return newPassword
        else:
            print("Passwords do not match. Please try again.")

# Function that will interact with the database
def getHashedPassword(userId):
    # Placeholder implementation to retrieve hashed password from the dictionary
    return user_passwords.get(userId)

def updateUserPassword(userId, hashedPassword):
    # Placeholder implementation to update hashed password in the dictionary
    user_passwords[userId] = hashedPassword

# Main function to change password
def main(): 
    userId = input("Enter user ID: ")
    currentPassword = input("Enter current password: ")
    newPassword = inputNewPassword()

    # Check if the user exists
    storedHashedPassword = getHashedPassword(userId)
    if storedHashedPassword is None:
        print("User does not exist.")
        return

    success, message = changePassword(currentPassword, newPassword, userId)
    if success:
        print(message)
    else:
        print("Password change failed:", message)

if __name__ == "__main__":
    main()