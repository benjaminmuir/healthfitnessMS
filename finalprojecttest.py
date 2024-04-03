import psycopg
#create the database 
db = psycopg.connect("dbname=finalProject2 user=postgres password=jabulani")
#create a cursor
cur = db.cursor()
def userMenu():
    mainMenuChoice = (input("""
\n---------------------------------------------------------------------------------------------------
(1) Profile Management (Updating personal info, goals, and health metrics)
                    

(2) Dashboard Display (Displaying exercise routines, fitness acheivements, health stats)
                    

(3) Schedule Management (Schedule personal training sessions or group fitness classes)
---------------------------------------------------------------------------------------------------\n"""))
    
    
    return mainMenuChoice


def userLogin():
    usernameId = ""
    userPassWord = ""
    logInType = (input("""
------------------------------------------------------------------
\nWelcome to the Health and Fitness Club Management System!

Are you a Member (1), Trainer (2), or Adminstration (3)? (Quit at any time with q)\n  
------------------------------------------------------------------\n"""))
    
    match logInType:
        case "1":
            usernameId = str(input("\nPlease sign in with your username:\n"))
            userPassWord = str(input("Password:\n"))
            #make new data in the member table and set id username and password for now
            cur.execute("INSERT INTO member (username, password) VALUES (%s, %s)",
                        (usernameId,userPassWord))
            
            #get memberID from this member and set to a variable
            cur.execute("SELECT memberID FROM member WHERE username = %s AND password = %s",
                        (usernameId,userPassWord)) 
            memberID = str(cur.fetchone()[0])

            print("\nNew member added!\n")
        case "2":
            print("I will implement this later")
            return
            # usernameId = str(input("Please sign in with your username:\n"))
            # userPassWord = str(input("Password:\n"))
        case "3":
            print("I will implement this later")
            return
            # usernameId = str(input("Please sign in with your username:\n"))
            # userPassWord = str(input("Password:\n"))
        case _:
            while logInType not in {"1","2","3"}:
                print("Please enter a number from 1 to 3.")
                userLogin()
    return usernameId, userPassWord, memberID

def profileMenu():
    return 

def dashBoardDisplay():
    return 

def scheduleMenu():
    return

def main():
    userType = userLogin()
    userMenuChoice = userMenu()
    #get the memberID from the user who logged in
    #to reference in the other functions
    currentMemberID = userType[2]
    match userMenuChoice:
        case "1":
            print("You have chosen the profile menu!")
            profileMenu() 
        case "2":
            print("You have chosen the dashboard menu!")
            dashBoardDisplay() 
        case "3":
            print("You have chosen the schedule menu!")
            scheduleMenu() 
        case "q":
            print("Exiting the system.")
            db.commit()
            cur.close()
            db.close()
            quit()
        case _:
            while userMenuChoice not in {"1","2","3","q"}:
                print("Please enter a number from 1 to 3.")
                userMenuChoice = userMenu()
    #ensure we commit cursor changes and close db
    cur.close()
    db.commit()
    db.close()

if __name__ == "__main__":
    main()