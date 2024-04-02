

def userMenu():
    mainMenuChoice = int(input("""
---------------------------------------------------------------------------------------------------
(1) Profile Management (Updating personal info, goals, and health metrics)
                    

(2) Dashboard Display (Displaying exercise routines, fitness acheivements, health stats)
                    

(3) Schedule Management (Schedule personal training sessions or group fitness classes)
---------------------------------------------------------------------------------------------------"""))
    return mainMenuChoice
#comment out for testing
# password = input("Enter Password:\n)

def userLogin():
    usernameId = ""
    userPassWord = ""
    logInType = 0
    logInType = int(input("""
------------------------------------------------------------------
Welcome to the Health and Fitness Club Management System!\n

Are you a Member (1), Trainer (2), or Adminstration (3)?\n  
------------------------------------------------------------------"""))
    print(logInType)
    if logInType == 1:
        usernameId = str(input("Please sign in with your username:\n"))
        userPassWord = str(input("Password:\n"))
    if logInType == 2:
        usernameId = str(input("Please sign in with your username:\n"))
        userPassWord = str(input("Password:\n"))
    if logInType == 3:
        usernameId = str(input("Please sign in with your username:\n"))
        userPassWord = str(input("Password:\n"))
    return usernameId, userPassWord

def main():
    userType = userLogin()
    userMenuChoice = userMenu()
    while userType != 1 and userType != 2 and userType != 3:
        print("Invalid User Type")
        userType = userLogin()
    while userMenuChoice != 1 and userMenuChoice != 2 and userMenuChoice != 3:
        print("Invalid Menu Choice")
        userMenuChoice = userMenu()
    

if __name__ == "__main__":
    main()