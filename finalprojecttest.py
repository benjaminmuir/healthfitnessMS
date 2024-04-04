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

            #input check
            while existing not in ["Y","N","y","n","yes","no","YES","NO"]:
                print("Please enter a valid answer to the question.\n")
                existing = str(input("\nDo you have an existing account? (Y or N)\n"))

            # they are looking to make a new account
            if existing in ["n", "N", "no", "NO"]: 
                usernameId = str(input("\nPlease sign in with your username:\n"))
                userPassWord = str(input("Password:\n"))
                #make new data in the member table and set id username and password for now
                try:
                    #set the data for username and password only
                    cur.execute("INSERT INTO member (username, password) VALUES (%s, %s)",
                            (usernameId,userPassWord))
                    
                    #get the memberID of the new member
                    cur.execute("SELECT memberID FROM member WHERE username = %s AND password = %s",
                            (usernameId,userPassWord))
                    memberID = str(cur.fetchone()[0])
                    print(f"\nNew member {usernameId} added!\n")
                    db.commit()
                    return usernameId, userPassWord, memberID
                
                except:
                    print("Either username or password is the same as an existing member.")
                    return False

            #if the member has an account, simply fetch the relevant data
            if existing in ["y", "Y", "yes", "YES"]:
                usernameId = str(input("\nPlease sign in with your username:\n"))
                userPassWord = str(input("Password:\n"))
                #get memberID from this member and set to a variable
                
                #check for non-existing member
                try: 
                    cur.execute("SELECT memberID FROM member WHERE username = %s AND password = %s",
                            (usernameId,userPassWord)) 
                    memberID = str(cur.fetchone()[0])
                    print(f"\nWelcome back {usernameId}!\n")
                    db.commit()
                    return usernameId, userPassWord, memberID
                except:
                    print("No member found with that username and password.")
                    return False
                
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
                return False

    return usernameId, userPassWord, memberID



"""
Prints the profile menu for any member. 
Has options:
    Update Personal Info:
        Will update age,fname,lname,email,height,weight 
    Update Goals:
        Used to update weightGoal, lapTime (and others)
    Update Health Metrics:
        Used to update bloodoxygen, averageHeartRate 
Params: memberID
    Takes current memberID of the member that is currently logged on. 
"""
def profileMenu(memberID):
    col_names = []
    data_rows = []
    choice = input("""\n
--------------------------------
Profile Menu:
(1) Update Personal Info
(2) Update Fitness Goals
(3) Update Health Metrics
(4) View Profile Info and Health Statistics/Metrics
-------------------------------\n""")
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
            columnUpdate = (input("""
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
                if int(columnUpdate) == col_names.index(data):
                    if data == "age" or data == "height" or data == "weight":
                        cur.execute(f"UPDATE member SET {data} = %s WHERE memberID = %s",(int(dataUpdate),memberID))
                        print(f"Updated {data} to {dataUpdate}")
                        db.commit()
                    else:
                        cur.execute(f"UPDATE member SET {data} = %s WHERE memberID = %s",(dataUpdate,memberID))
                        print(f"Updated {data} to {dataUpdate}")
                        db.commit()
                    
            # cur.execute(f"UPDATE member SET {col_names[columnUpdate]} = %s WHERE memberID = %s",(dataUpdate,memberID))
        case "2":
            print("You have chosen to update your goals!\n")
            weightGoal = input("Please enter your new weight goal (in lbs):\n")
            lapTime = input("Please enter your new lap time goal (in minutes.seconds):\n")
            deadliftMax = input("Please enter your new deadlift max (in lbs):\n")
            squatMax = input("Please enter your new squat max (in lbs):\n")
            benchMax = input("Please enter your new bench max (in lbs):\n")
            swimTime = input("Please enter your new swim time (in minutes.seconds):\n")
            cur.execute("UPDATE member SET weightGoal = %s, lapTime = %s, deadliftMax = %s, squatMax = %s, benchMax = %s, swimTime = %s WHERE memberID = %s",
                        (weightGoal,lapTime,deadliftMax,squatMax,benchMax,swimTime,memberID))
            print("Updated your goals!")
            db.commit()
            #updateGoals(memberID)
        case "3":
            print("You have chosen to update your health metrics!\n")
            bmi = input("Please enter your new BMI level:\n")
            averageHeartRate = input("Please enter your new resting heart rate:\n")
            
            cur.execute("UPDATE member SET bmi = %s, restingHeartRate = %s WHERE memberID = %s",
                        (bmi,averageHeartRate,memberID))
            print("Updated your health metrics!")
            db.commit()
            #updateHealthMetrics(memberID)
        case "4":
            #print profile info, goals, and health metrics in seperate sections all titled
            print("Here is your profile information:\n")
            cur.execute("SELECT fName,lName,email,height,weight,age FROM member WHERE memberID = %s",(memberID,))
            col_names = ([desc[0] for desc in cur.description])
            for row in cur:
                data_rows.append(row)
            for data in col_names:
                print(f"{data}: {data_rows[0][col_names.index(data)]}")
            print("\nHere are your fitness goals:\n")
            cur.execute("SELECT weightGoal,lapTime,deadliftMax,squatMax,benchMax,swimTime FROM member WHERE memberID = %s",(memberID,))
            col_names = ([desc[0] for desc in cur.description])
            for row in cur:
                data_rows.append(row)
            for data in col_names:
                print(f"{data}: {data_rows[1][col_names.index(data)]}")
            print("\nHere are your health metrics:\n")
            cur.execute("SELECT bmi,restingHeartRate FROM member WHERE memberID = %s",(memberID,))
            col_names = ([desc[0] for desc in cur.description])
            for row in cur:
                data_rows.append(row)
            for data in col_names:
                print(f"{data}: {data_rows[2][col_names.index(data)]}")
            db.commit()
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
    #ensure we are storing the memberID of the user if anything goes wrong
    while userType == False:
        userType = userLogin()

    #now we ask for menu options 
    userMenuChoice = userMenu()
    while userMenuChoice not in {"q","Q","quit","Quit"}:
        #keep updating current member ID that is logged in
        currentMemberID = userType[2]
        if userMenuChoice == "1":
            profileMenu(currentMemberID)
        elif userMenuChoice == "2":
            dashBoardDisplay()
        elif userMenuChoice == "3":
            scheduleMenu()
        db.commit()
        userMenuChoice = userMenu()


    print("Exiting the system.")
    db.commit()
    cur.close()
    db.close()
    quit()

if __name__ == "__main__":
    main()