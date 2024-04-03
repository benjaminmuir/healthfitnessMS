import psycopg
#connect to the database 
db = psycopg.connect("dbname=finalProject2 host=localhost user=postgres password=jabulani")
#create a cursor
cur = db.cursor()



def userMenu():
    mainMenuChoice = input("""
\n---------------------------------------------------------------------------------------------------
(1) Profile Management (Updating personal info, goals, and health metrics)
                    

(2) Dashboard Display (Displaying exercise routines, fitness acheivements, health stats)
                    

(3) Schedule Management (Schedule personal training sessions or group fitness classes)
---------------------------------------------------------------------------------------------------\n""")
    
    
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
            existing = str(input("\nDo you have an existing account? (Y or N)\n"))

            while existing not in ["Y","N","y","n","yes","no","YES","NO"]:
                print("Please enter a valid answer to the question.\n")
                existing = str(input("\nDo you have an existing account? (Y or N)\n"))

            if existing in ["n", "N", "no", "NO"]: # they are looking to make a new account
                usernameId = str(input("\nPlease sign in with your username:\n"))
                userPassWord = str(input("Password:\n"))
                try:
                    #make new data in the member table and set id username and password for now
                    cur.execute("INSERT INTO member (username, password) VALUES (%s, %s)",
                                (usernameId,userPassWord))
                    
                    #get memberID from this member and set to a variable
                    cur.execute("SELECT memberID FROM member WHERE username = %s AND password = %s",
                                (usernameId,userPassWord)) 
                    memberID = str(cur.fetchone()[0]) #get only the ID 
                    print(f"\nNew member {usernameId} added!\n")
                except:
                    print("Either username or password is the same as an existing member.")
                    memberID = ""
                    userLogin()

            #if the member has an account, simply fetch the relevant data
            elif existing in ["y", "Y", "yes", "YES"]:
                usernameId = str(input("\nPlease sign in with your username:\n"))
                userPassWord = str(input("Password:\n"))
                #get memberID from this member and set to a variable
                cur.execute("SELECT memberID FROM member WHERE username = %s AND password = %s",
                            (usernameId,userPassWord)) 
                #check for non-existing member
                try: 
                    memberID = str(cur.fetchone()[0])
                    print(f"\nWelcome back {usernameId}!\n")
                except:
                    print("No member found with that username and password.")
                    memberID = "" #set to empty string to avoid errors
                    userLogin()
                
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
        case "q":
            print("Exiting the system.")
            db.commit()
            cur.close()
            db.close()
            quit()
        case _:
            while logInType not in {"1","2","3"}:
                print("Please enter a number from 1 to 3.")
                userLogin()
    return usernameId, userPassWord, memberID

def updatePersonalInfo(columnName,memberID):
    cur.execute("UPDATE {columnName} SET {columnName} = %s WHERE memberID = %s",(columnName,memberID))

def profileMenu(memberID):
    col_names = []
    data_rows = []
    choice = input("""\n
---------------------------------------------------------------------------------------------------
Profile Menu:
(1) Update Personal Info
(2) Update Goals
(3) Update Health Metrics
(4) View Profile
---------------------------------------------------------------------------------------------------\n""")
    match choice:
        case "1":
            print("You have chosen to update your personal info!\n")
            cur.execute("SELECT fName,lName,email,height,weight,age FROM member WHERE memberID = %s",(memberID,))
            #storing the column names and corresponding data for printing 
            col_names = ([desc[0] for desc in cur.description])
            for row in cur:
                data_rows.append(row)
            #printing names and data 
            print("Here is your current personal info:\n")
            for data in col_names:
                print(f"{data}: {data_rows[0][col_names.index(data)]}")
            columnUpdate = int(input("""
Which column would you like to update?
(0) First Name
(1) Last Name
(2) Email
(3) Height
(4) Weight
(5) Age
\n"""))
            dataUpdate = input("Please enter the new data:\n")
            for data in col_names:
                print(str(col_names.index(data)) + " " + data)
                if columnUpdate == col_names.index(data):
                    cur.execute(f"UPDATE member SET {data} = %s WHERE memberID = %s",(dataUpdate,memberID))
                    print("Data updated successfully!")
            # cur.execute(f"UPDATE member SET {col_names[columnUpdate]} = %s WHERE memberID = %s",(dataUpdate,memberID))
        case "2":
            print("You have chosen to update your goals!")
            #updateGoals(memberID)
        case "3":
            print("You have chosen to update your health metrics!")
            #updateHealthMetrics(memberID)
        case "4":
            print("You have chosen to view your profile!")
            #viewProfile(memberID)
        case _:
            while choice not in {"1","2","3","4"}:
                print("Please enter a number from 1 to 4.")
                choice = profileMenu(memberID) 

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
            profileMenu(currentMemberID) 
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