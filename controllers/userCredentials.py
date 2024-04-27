#function for creating a file containing the credentials
def createFile(filePath, userCredentials): #userCredentials is a variable that contains a dictionary with username and password pairs
    with open(filePath, 'w') as file:
        for userUsername, userPassword in userCredentials.items():
            file.write(f"{userUsername}:{userPassword}\n")

#function for reading the file, used dictionaries for username, email and password sets
def readFile(filePath):
    userCredentials = {}
    with open(filePath, 'r') as file:
        for line in file:
            userUsername, userPassword = line.strip().split(':')
            userCredentials[userUsername] = userPassword
    return userCredentials

#function for updating a user's username
def updateUsername(userCredentials, oldUsername, newUsername):
    if oldUsername in userCredentials:
        password = userCredentials.pop(oldUsername)
        userCredentials[newUsername] = password
        print(f"Username '{oldUsername}' updated to '{newUsername}' successfully.")
    else:
        print(f"Username '{oldUsername}' not found.")

#function for updating a user's password
def updatePassword(userCredentials, userUsername, newPassword):
    if userUsername in userCredentials:
        userCredentials[userUsername] = newPassword
        print(f"Password for user '{userUsername}' updated successfully.")
    else:
        print(f"User '{userUsername}' not found.")