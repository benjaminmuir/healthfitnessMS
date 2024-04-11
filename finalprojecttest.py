import psycopg
#connect to the database 
db = psycopg.connect("dbname=finalProject2 host=localhost user=postgres password=jabulani")
#create a cursor
cur = db.cursor()



def userMenu():
    mainMenuChoice = input("""
    ---------------------------------------------------------------------------------------------------
    (1) Profile Management (Updating personal info, goals, and health metrics)
                            
    (2) Dashboard Display (Displaying exercise routines, fitness acheivements, health stats)
                            
    (3) Schedule Management (Schedule personal training sessions or group fitness classes)
                           
    (4) Exit the System
    ---------------------------------------------------------------------------------------------------\n""")
    
    
    return mainMenuChoice

def memberLogin():
    usernameId = ""
    userPassWord = ""
    
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
            print(f"\nNew member {usernameId} added!")
            db.commit()
            return usernameId, userPassWord, memberID
        
        except:
            print("Either username or password is the same as an existing member.")
            return usernameId, userPassWord, False

    #if the member has an account, simply fetch the relevant data
    if existing in ["y", "Y", "yes", "YES"]:
        usernameId = str(input("\nPlease sign in with your username:\n"))
        userPassWord = str(input("Password:\n"))
        #get memberID from this member and set to a variable
        
        #check for non-existing member
        try: 
            cur.execute("SELECT memberID FROM member WHERE username = %s AND password = %s",
                    (usernameId,userPassWord)) 
            #keep track of memberID
            memberID = str(cur.fetchone()[0])
            print(f"\nWelcome back {usernameId}!")
            db.commit()
            return usernameId, userPassWord, memberID
        except:
            print("No member found with that username and password.")
            #make sure to rollback on error 
            db.rollback()
            return usernameId, userPassWord, False

def trainerLogin():
    usernameId = ""
    userPassWord = ""
    
    existing = str(input("\nDo you have an existing account? (Y or N)\n"))

    #input check
    while existing not in ["Y","N","y","n","yes","no","YES","NO"]:
        print("Please enter a valid answer to the question.\n")
        existing = str(input("\nDo you have an existing account? (Y or N)\n"))

    # they are looking to make a new account
    if existing in ["n", "N", "no", "NO"]: 
        usernameId = str(input("\nPlease sign in with your username:\n"))
        userPassWord = str(input("Password:\n"))
        #make new data in the trainer table and set id username and password for now
        try:
            #set the data for username and password only
            cur.execute("INSERT INTO trainer (username, password) VALUES (%s, %s)",
                    (usernameId,userPassWord))
            
            #get the trainerID of the new trainer
            cur.execute("SELECT trainerID FROM trainer WHERE username = %s AND password = %s",
                    (usernameId,userPassWord))
            trainerID = str(cur.fetchone()[0])
            print(f"\nNew trainer {usernameId} added!")
            db.commit()
            return usernameId, userPassWord, trainerID
        
        except psycopg.IntegrityError as e:
            print("Either username or password is the same as an existing trainer.")
            db.rollback()
            return usernameId, userPassWord, False

    #if the trainer has an account, simply fetch the relevant data
    if existing in ["y", "Y", "yes", "YES"]:
        usernameId = str(input("\nPlease sign in with your username:\n"))
        userPassWord = str(input("Password:\n"))
        
        try: 
            cur.execute("SELECT trainerID FROM trainer WHERE username = %s AND password = %s",
                    (usernameId,userPassWord)) 
            #keep track of trainerID
            trainerID = str(cur.fetchone()[0])
            print(f"\nWelcome back {usernameId}!")
            db.commit()
            return usernameId, userPassWord, trainerID
        except TypeError:
            print("No trainer found with that username and password.")
            return usernameId, userPassWord, False
        

def userLogin():
    
    logInType = (input("""
    ------------------------------------------------------------------
    Welcome to the Health and Fitness Club Management System!
                        
    Are you a Member (1), Trainer (2), or Adminstration (3)? (Quit at any time with 4)  
    ------------------------------------------------------------------\n"""))

    return logInType

def updateWeightGoal(memberID):
    cur.execute("SELECT weight FROM member WHERE memberID = %s", (memberID,))
    weight = cur.fetchone()[0]
    print(f"Here is your current weight: {weight}kg")
     #This will keep asking for lapTime until constraints are met, then exists while loop
    while True:
        try:
            weightGoal = float(input("Please enter your new weight goal (in kgs):\n"))
            cur.execute("UPDATE member SET weightGoal = %s WHERE memberID = %s", (weightGoal,memberID))

            print(f"Updated your weight goal to: {weightGoal}!\n")
            db.commit()
            break
        except ValueError:
            print("Invalid input, please enter a number (can include decimals).\n")
            db.rollback()
        except psycopg.IntegrityError as e:
            print("Invalid input, please enter a number above 0\n")
            db.rollback()
       

def updateLapTimeGoal(memberID):
    cur.execute("SELECT lapTime FROM member WHERE memberID = %s", (memberID,))
    lapTime = cur.fetchone()[0]
    print(f"Here is your current lap time: {lapTime}mins")
     #This will keep asking for lapTime until constraints are met, then exists while loop
    while True:
        try:
            lapTimeGoal = float(input("Please enter your new lap time goal (in minutes):\n"))
            #update the db
            cur.execute("UPDATE member SET lapTimeGoal = %s WHERE memberID = %s", (lapTimeGoal,memberID))

            print(f"Updated your lap time goal to: {lapTimeGoal}!\n")
            db.commit()
            break
        #makes sure to rollback the previous execute on error
        except ValueError:
            print("Invalid input, please enter a number.\n")
            db.rollback()
        except psycopg.IntegrityError as e:
            print("Invalid input, please enter a number above 0\n")
            db.rollback()
        

def updateBenchMaxGoal(memberID):
    cur.execute("SELECT benchMax FROM member WHERE memberID = %s", (memberID,))
    benchMax = cur.fetchone()[0]
    print(f"Here is your current bench max: {benchMax}kg")
    while True:
        try:
            benchMaxGoal = float(input("Please enter your new bench max goal (in kgs):\n"))
            #update the db
            cur.execute("UPDATE member SET benchMaxGoal = %s WHERE memberID = %s", (benchMaxGoal,memberID))

            print(f"Updated your bench goal to: {benchMaxGoal}!")
            db.commit()
            break
        #makes sure to rollback the previous execute on error
        except ValueError:
            print("Invalid input, please enter a number.\n")
            db.rollback()
        except psycopg.IntegrityError as e:
            print("Invalid input, please enter a number above 0\n")
            db.rollback()
        

def updateSquatGoal(memberID):
    cur.execute("SELECT squatMax FROM member WHERE memberID = %s", (memberID,))
    squatMax = cur.fetchone()[0]
    print(f"Here is your current squat max: {squatMax}kg")
    while True:
        try:
            squatMaxGoal = float(input("Please enter your new squat max goal (in kgs):\n"))
            #update the db
            cur.execute("UPDATE member SET squatMaxGoal = %s WHERE memberID = %s", (squatMaxGoal,memberID))

            print(f"Updated your squat goal to: {squatMaxGoal}!\n")
            db.commit()
            break
        #makes sure to rollback the previous execute on error
        except ValueError:
            print("Invalid input, please enter a number.\n")
            db.rollback()
        except psycopg.IntegrityError as e:
            print("Invalid input, please enter a number above 0\n")
            db.rollback()

def updatePersonalInfo(memberID, cols):
    while True:
        try:
            columnUpdate = int(input("""
    Which column would you like to update?
    (0) First Name
    (1) Last Name
    (2) Email
    (3) Height (in meters)
    (4) Weight (in kilograms)
    (5) Age
    (6) Lap Time (in minutes)
    (7) Bench Max (in kilograms)
    (8) Squat Max (in kilograms)
            \n"""))
    
            dataUpdate = input("Please enter the new data or type clear to erase current data:\n")
            for data in cols:
                if int(columnUpdate) == cols.index(data):
                    #if data is int
                    if data == "age":
                        if dataUpdate in ["clear", "c", "Clear", "C"]:
                            cur.execute(f"UPDATE member SET {data} = %s WHERE memberID = %s",(None,memberID))
                            db.commit()
                        else:
                            cur.execute(f"UPDATE member SET {data} = %s WHERE memberID = %s",(int(dataUpdate),memberID))
                            print(f"Updated {data} to {dataUpdate}")
                            db.commit()
                    #if data is float
                    elif data == "height" or data == "weight" or data == "lapTime" or data == "squatMax" or data == "benchMax":
                        if dataUpdate in ["clear", "c", "Clear", "C"]:
                            cur.execute(f"UPDATE member SET {data} = %s WHERE memberID = %s",(None,memberID))
                            db.commit()
                        else:
                            cur.execute(f"UPDATE member SET {data} = %s WHERE memberID = %s",(float(dataUpdate),memberID))
                            print(f"Updated {data} to {dataUpdate}")
                            db.commit()
                    #if data is other
                    else:
                        if dataUpdate in ["clear", "c", "Clear", "C"]:
                            cur.execute(f"UPDATE member SET {data} = %s WHERE memberID = %s",(None,memberID))
                            db.commit()
                        else:
                            cur.execute(f"UPDATE member SET {data} = %s WHERE memberID = %s",(dataUpdate,memberID))
                            print(f"Updated {data} to {dataUpdate}")
                            db.commit()
            break
        #makes sure to rollback the previous execute on error
        except ValueError:
            print("Invalid input, please enter a number.")
            db.rollback()
        except psycopg.IntegrityError as e:
            print("Invalid input, please enter a valid number")
            db.rollback()
    
"""
Prints the profile menu for any member. 
Has options:
    Update Personal Info:
        Will update age,fname,lname,email,height,weight 
    Update Goals:
        Used to update weightGoal, lapTime (and others)
    Update Health Metrics:
        Used to update bmi, averageHeartRate 
Params: memberID
    Takes current memberID of the member that is currently logged on. 
"""
def profileMenu(memberID):
    col_names = []
    data_rows = []
    while True:
        choice = input("""\n
    --------------------------------
    Profile Menu:
    (1) Update Personal Info
                       
    (2) Update Fitness Goals
                       
    (3) Update Health Metrics
                       
    (4) View Profile Info and Health Statistics/Metrics
                       
    (5) Exit Profile Menu
    -------------------------------\n""")
        match choice:
            case "1":
                while True:
                    print("You have chosen to update your personal info!\n")
                    cur.execute("SELECT fName,lName,email,height,weight,age,lapTime,benchMax,squatMax FROM member WHERE memberID = %s",(memberID,))
                    #storing the column names and corresponding data for printing 
                    col_names = ([desc[0] for desc in cur.description])

                    for row in cur:
                        data_rows.append(row)

                    #printing names and data 
                    print("Here is your current personal info:\n")
                    for data in col_names:
                        print(f"{data}: {data_rows[0][col_names.index(data)]}")

                    #call helper function to update the db 
                    updatePersonalInfo(memberID, col_names)
                    cc = input("Would you like to update anything else? (1) Yes or (2) No\n")
                    if(cc == "2"):
                        break
                    else:
                        db.commit()

            case "2":
                print("You have chosen to update your goals!\n")
                #Take input for all goals from user
                updateWeightGoal(memberID)
                updateLapTimeGoal(memberID)
                updateBenchMaxGoal(memberID)
                updateSquatGoal(memberID)
                #Change the goal values in the db 
                print("\nUpdated your goals!\n")
            
            case "3":
                print("You have chosen to update your health metrics!\n")
                while True:
                    try:
                        #it is important that this (and any others) remain as (memberID,) if memberID only var 
                        cur.execute("SELECT height FROM member WHERE memberID = %s", (memberID,)) 
                        #need to store height and weight as variables for calculation of BMI 
                        height = float(cur.fetchone()[0])
                        weight = cur.execute("SELECT weight FROM member WHERE memberID = %s", (memberID,))
                        weight = int(cur.fetchone()[0])
                        bmi = round(weight / ((height)**2), 1)
                        averageHeartRate = float(input("Please enter your new resting heart rate:\n"))
                        
                        cur.execute("UPDATE member SET bmi = %s, restingHeartRate = %s WHERE memberID = %s",
                                    (bmi,averageHeartRate,memberID))
                        print("Updated your health metrics!")
                        db.commit()
                        break
                    except ValueError:
                            print("\nInvalid input, please enter a number.")
                            db.rollback()
                    except psycopg.IntegrityError as e:
                        print("\nInvalid input, please enter a number between 39 and 111")
                        db.rollback()
            case "4":
                #print profile info, goals, and health metrics in seperate sections all titled
                print("Here is your profile information:\n")
                cur.execute("SELECT fName,lName,email,height,weight,age,lapTime,benchMax,squatMax FROM member WHERE memberID = %s",(memberID,))
                col_names = ([desc[0] for desc in cur.description])

                for row in cur:
                    data_rows.append(row)

                for data in col_names:
                    print(f"{data}: {data_rows[0][col_names.index(data)]}")

                print("\nHere are your fitness goals:\n")
                cur.execute("SELECT weightGoal,lapTimeGoal,squatMaxGoal,benchMaxGoal FROM member WHERE memberID = %s",(memberID,))
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
            case "5":
                print("Exiting the profile menu")
                break
            case _:
                print("Please enter a number from 1 to 4.")

def createExerciseRoutine(memberID):
    # This function will interact with the user to create a new exercise routine
    # and insert it into the exerciseRoutine table in the database.
    exercise_name = input("Please enter the name of the exercise: ")
    repetitions = int(input("Please enter the number of repetitions: "))
    cur.execute("INSERT INTO exerciseRoutine (name, repetitions, memberID) VALUES (%s, %s, %s)",
                (exercise_name, repetitions, memberID))
    db.commit()
    print(f"Exercise routine '{exercise_name}' with {repetitions} repetitions has been created.")

def viewHealthStatistics(memberID):
    # This function will fetch and display the health statistics of the member
    # from the member table in the database.
    cur.execute("SELECT height, weight, age, bmi FROM member WHERE memberID = %s", (memberID,))
    height, weight, age, bmi = cur.fetchone()
    print(f"Height: {height} m")
    print(f"Weight: {weight} kg")
    print(f"Age: {age} years")
    print(f"BMI: {bmi}")

def viewFitnessAchievements(memberID):
    # This function will fetch and display the fitness achievements of the member
    # from the relevant tables in the database.
    try:
        cur.execute("SELECT lapTime,weight,weightGoal,lapTimeGoal,squatMax,squatMaxGoal,benchMaxGoal,benchMax FROM member WHERE memberID = %s", (memberID,))
        lapTime,weight,weightGoal, lapTimeGoal, squatMax, squatMaxGoal, benchMaxGoal, benchMax = cur.fetchone()
        if(weight < weightGoal):
            print(f"Your current weight goal is {weightGoal}kg. You need to gain {weightGoal-weight}kgs to reach it!")
        elif(weight > weightGoal):
            print(f"Your current weight goal is {weightGoal}kg. You need to lose {weight-weightGoal}kgs to reach it!")
        elif(weight == weightGoal):
            print(f"Your current weight goal of {weightGoal}kg is the same as your weight of {weight}kg! Great Job!")
        
        if(lapTime <= lapTimeGoal):
            print(f"Your current lap time goal is {lapTimeGoal}mins. Your best you've ran is {lapTime}mins, congratulations!")
        elif(lapTime > lapTimeGoal):
            print(f"Your current lap time goal is {lapTimeGoal}mins. You need to run {lapTime-lapTimeGoal}mins faster to reach it!")

        if(squatMax < squatMaxGoal):
            print(f"Your current squat max  goal is {squatMaxGoal}kg. The best you've lifted is {squatMax}kg, keep it up and get those {squatMaxGoal-squatMax}kgs up!")
        elif(squatMax > squatMaxGoal):
            print(f"Your current squat max  goal is {squatMaxGoal}kg. The best you've lifted is {squatMax}kg, congratulations on beating your fitness goal!")
        elif squatMaxGoal == squatMax:
            print(f"Both your squat max goal: {squatMaxGoal}kg and your current best: {squatMax}kg are the same! Congratulations on reaching the goal, now lift that {squatMaxGoal-squatMax}kgs to achieve it!")
        
        if(benchMax < benchMaxGoal):
            print(f"Your current bench max goal is {benchMaxGoal}kg. The best you've lifted is {benchMax}kg, keep it up and get those {benchMaxGoal-benchMax}kgs up!")
        elif(benchMax > benchMaxGoal):
            print(f"Your current bench max goal is {benchMaxGoal}kg. The best you've lifted is {benchMax}kg, congratulations on beating your fitness goal!")
        elif benchMaxGoal == benchMax:
            print(f"Both your bench max goal: {benchMaxGoal}kg and your current best: {benchMax}kg are the same! Congratulations on reaching the goal, now lift that {benchMaxGoal-benchMax}kgs to achieve it!")
    except TypeError:
        print("Look like you have not set a value for either a goal or personal info, please review your information if you wish to see this achievement")

def viewExerciseRoutines(memberID):
    # This function will fetch and display the exercise routines of the member
    # from the exerciseRoutine table in the database.
    cur.execute("SELECT name, repetitions FROM exerciseRoutine WHERE memberID = %s", (memberID,))
    routines = cur.fetchall()
    #if no routines
    if not routines:
        print("You have no routines.")
    else:
        for name, repetitions in routines:
            print(f"Exercise: {name}, Repetitions: {repetitions}")

def dashBoardDisplay(memberID):
    print("\nWelcome to your own personalized dashboard!\n")
    while True:
        choice = input("""\n
    --------------------------------
    Dashboard Menu:
    (1) Create exercise routines
                       
    (2) View health statistics
                       
    (3) See your current fitness achievements 
                       
    (4) View all of your exercise routines
                       
    (5) Exit Dashboard
    -------------------------------\n""")
        match choice: 
            case "1":
                createExerciseRoutine(memberID)
            case "2":
                viewHealthStatistics(memberID)
            case "3":
                viewFitnessAchievements(memberID)
            case "4":
                viewExerciseRoutines(memberID)
            case "5":
                print("\n Exiting dashboard.")
                break
            case _:
                print("Please enter a number from 1 to 5.")
def scheduleMenu():
    return

def main():
    logInType = userLogin()
    while True:
        try:
            #login is a member
            if logInType == "1":
                member = memberLogin()
                if member[2] == False:
                    main()
                currentMemberID = member[2]
                while True:
                    try: 
                        userMenuChoice = userMenu()
                        #keep updating current member ID that is logged in
                        if userMenuChoice == "1":
                            profileMenu(currentMemberID)
                        elif userMenuChoice == "2":
                            dashBoardDisplay(currentMemberID)
                        elif userMenuChoice == "3":
                            scheduleMenu()
                        elif userMenuChoice == "4":
                            print("Exiting.")
                            db.commit()
                            cur.close()
                            db.close()
                            quit()
                        db.commit()
                    except ValueError:
                        print("Please enter valid input.")
            elif logInType == "2":
                trainer = trainerLogin()
                if trainer[2] == False:
                    main()
                currentTrainerID = trainer[2]
                break
        except ValueError:
            print("Please enter valid input.")

    

    

if __name__ == "__main__":
    main()