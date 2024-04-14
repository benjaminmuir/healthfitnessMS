import psycopg
from datetime import datetime
#connect to the database 
db = psycopg.connect("dbname=finalProject2 host=localhost user=postgres password=jabulani")
#create a cursor
cur = db.cursor()



def memberMenu():
    mainMenuChoice = input("""
    ---------------------------------------------------------------------------------------------------
    (1) Profile Management (Updating personal info, goals, and health metrics)
                            
    (2) Dashboard Display (Displaying exercise routines, fitness acheivements, health stats)
                            
    (3) Schedule Management (Schedule personal training sessions or group fitness classes)
                           
    (4) Exit the System
    ---------------------------------------------------------------------------------------------------\n""")
    
    
    return mainMenuChoice

def trainerMenu():
    mainMenuChoice = input("""
    ---------------------------------------------------------------------------------------------------
    (1) Schedule Management
                            
    (2) Member Profile Search 

    (3) Update Trainer Name
                                                              
    (4) Exit the System
    ---------------------------------------------------------------------------------------------------\n""")
    return mainMenuChoice

def adminMenu():
    while True:
        mainMenuChoice = input("""
        ---------------------------------------
        (1) Room Booking Management
                                
        (2) Equipment Maintenance Management
                                
        (3) Class Schedule Management

        (4) Billing and Payment Management                                              

        (5) Exit the System
        --------------------------------------\n""")
        
        if mainMenuChoice == "1":
            roomBookingMenu()
        elif mainMenuChoice == "2":
            equipmentMaintenanceMenu()
        elif mainMenuChoice == "3":
            classScheduleMenu()
        elif mainMenuChoice == "4":
            billingAndPaymentMenu()
        elif mainMenuChoice == "5":
            print("Exiting the admin menu...")
            break
        else:
            print("Please enter a valid option.")
    
def printAllRooms():
    cur.execute("""
    SELECT room.roomNumber, room.eventName, room.day, room.eventStart, room.eventEnd, class.CID, class.day, class.timeStart, class.timeEnd, class.classExercise, trainer.name 
    FROM room 
    LEFT JOIN class ON room.CID = class.CID
    LEFT JOIN trainer ON class.trainerID = trainer.trainerID
    """)
    allRooms = cur.fetchall() 
    for row in allRooms:
        if row[5] is None:
            print(f"Room Number: {row[0]}, Event Name: {row[1]}, Day: {row[2]}, Start Time: {row[3]}, End Time: {row[4]}")
        else:
            print(f"Room Number: {row[0]}, Class ID: {row[5]}, Day: {row[6]}, Start Time: {row[7]}, End Time: {row[8]}, Class Exercise: {row[9]}, Trainer: {row[10]}")


def roomBookingMenu():
    while True:
        try:
            print("\nWelcome to room booking management!")
            adminChoice = input("""
                --------------------------------
                Room Booking Menu:
                (1) Create a new room
                                
                (2) View all rooms
                                
                (3) Update an existing room
                                
                (4) Exit Room Booking Menu
                -------------------------------\n""")
            if adminChoice == "1":
                while True:
                    try:
                        choice = input("\nIs this for a special event (1) or for a group class (2)?\n")
                        if choice == "2":
                            printAllClasses()
                            cID = input("\nPlease input the class ID that is occuring in this room.\n")
                            cur.execute("SELECT CID from room WHERE CID = %s",(cID,))
                            if cur.fetchone() is None:
                                cur.execute("INSERT INTO room (CID) VALUES (%s)", (cID,))
                                db.commit()
                                cur.execute("SELECT * from class WHERE CID = %s", (cID,))
                                print(f"\nRoom created.\n")
                                break
                            else:
                                print("\nClass already exists in a room.\n")
                                break 
                        elif choice == "1":
                            eventName = input("\nPlease enter the name of the event that will occur in this room:\n")
                            print("Here are all the current rooms:")
                            printAllRooms()
                            day = input("Please enter the day of the event:\n")
                            eventStart = input("Please enter the time that the event will start:\n")
                            eventEnd = input("Please enter the time the event will end:\n")
                            cur.execute("INSERT INTO room (eventName,day,eventStart,eventEnd) VALUES (%s,%s,%s,%s)", 
                                        (eventName,day,eventStart,eventEnd))
                            
                            db.commit()
                            print(f"\nThe room has been created.\n")
                            break
                    except ValueError:
                        print("\nPlease enter the right value.\n")
                        db.rollback()
                    except psycopg.errors.InvalidTextRepresentation as f:
                        print("\nThis is in the wrong form.\n")
                        db.rollback()
            elif adminChoice == "2":
                print("\nHere are all the rooms:\n")
                printAllRooms()
            elif adminChoice == "3":
                while True:
                    try:
                        printAllRooms()
                        # Update Existing room
                        roomNumber = str(input("\nPlease select a room that you want to update (Must be the Room Number):\n"))
                        cur.execute("SELECT * FROM room WHERE roomNumber = %s", (roomNumber,))
                        #check if exists first
                        room = cur.fetchone()
                        if room is None:
                            print("\nYou have not yet created a room like that yet, please create it first.")
                            break
                        else:
                            #get CID from roomId 
                            cur.execute("SELECT CID from room WHERE roomNumber = %s",(roomNumber,))
                            cid = cur.fetchone()
                            #if not None, then it is a room with CID (room with class -> room with event)
                            if cid is not None and cid[0] is not None:
                                print("\nYou have decided to switch a room with a class to a special event.\n")
                                eventName = input("\nPlease enter a new name of the event that will occur in this room:\n")
                                day = input("Please enter a new day of the event:\n")
                                eventStart = input("Please enter a new time that the event will start at:\n")
                                eventEnd = input("Please enter a new time the event will end at:\n")
                                cur.execute("UPDATE room SET eventName =%s, day =%s, eventStart=%s, eventEnd=%s, CID = %s WHERE roomNumber = %s", 
                                            (eventName,day,eventStart,eventEnd,None, roomNumber))
                                db.commit()
                            else:
                                print("\nYou have decided to switch a room with a special event to a room with a class.\n")
                                printAllClasses()
                                cId = input("Please enter the cId of the class you are putting into the room:\n")
                                #check if class is in table
                                cur.execute("SELECT CID from room WHERE CID = %s",(cId,))
                                if cur.fetchone() is not None:
                                    print("\nThat class already exists in a room. Please choose another class or make a new one.\n")
                                    break
                                else:
                                    cur.execute("UPDATE room SET CID =%s WHERE roomNumber = %s", 
                                                (cId,roomNumber))
                                    db.commit()
                                    print("\nRoom has been updated.\n")
                            con = input("\nWould you like to update anymore? Yes (1) or No (2):\n")
                            if con == "2":
                                db.commit()
                                break
                            else:
                                print("\nThe room has been updated!\n")
                                db.commit()
                    except ValueError:
                        print("\nPlease enter the proper value.\n")
                        db.rollback()
                    except psycopg.errors.InvalidTextRepresentation as f:
                        print("\nEnsure you are writing a valid input.\n")
                        db.rollback()
                    except psycopg.errors.InvalidDatetimeFormat as e:
                        print("Please ensure the date/time format is correct")
                        db.rollback()

            elif adminChoice == "4":
                print("Exiting...")
                break
        except ValueError:
            print("\nPlease enter the right input.\n")     

def equipmentMaintenanceMenu():
    print("\nWelcome to class schedule management!")
    while True:
        try:
            
            adminChoice = input("""
        --------------------------------
        Equipment Management Menu:
        (1) View All Equipment
                        
        (2) Insert new equipment
                                
        (3) Delete an equipment

        (4) Update Equipment Information
                        
        (5) Exit Equipment menu
        -------------------------------\n""")
            if adminChoice == "1":
                cur.execute("SELECT * FROM equipment")
                equips = cur.fetchall()
                for row in equips:
                    print(f"EquipmentID: {row[0]}, Name: {row[1]}, Monitor Status: {row[2]}, Time before next update: {row[3]}")
            elif adminChoice == "2":
                name = input("Please enter the name of the equipment:\n")
                status = input("Please enter the status of the equipment (True (1) or False (2)):\n")
                time = input("Please enter the time before the next update (in days):\n")
                if status == "1":
                    cur.execute("INSERT INTO equipment (name, monitorStatus, nextMonitorDate) VALUES (%s,%s,%s)", 
                    (name,True,time))
                else:
                    cur.execute("INSERT INTO equipment (name, monitorStatus, nextMonitorDate) VALUES (%s,%s,%s)", 
                    (name,False,time))
                db.commit()
                print(f"\nEquipment {name} has been added to the database!\n")
                
            elif adminChoice == "3":
                while True:
                    cur.execute("SELECT * FROM equipment")
                    equips = cur.fetchall()
                    for row in equips:
                        print(f"EquipmentID: {row[0]}, Name: {row[1]}, Monitor Status: {row[2]}, Time before next update: {row[3]}")
                    equipID = input("\nPlease enter the equipment ID you would like to delete:\n")
                    cur.execute("SELECT * FROM equipment WHERE equipmentID = %s", (equipID,))
                    check = cur.fetchone()
                    if check is None:
                        print("\nThere does not exist an equipment with that ID.\n")
                        break
                    else:
                        cur.execute("DELETE FROM equipment WHERE equipmentID = %s",(equipID,))
                        db.commit()
                        print("\nEquipment deleted\n")
                        con = input("\nWould you like to delete anymore? (1) Yes or (2) No\n")
                        if con == "2":
                            db.commit()
                            break
                        else:
                            db.commit()
            elif adminChoice == "4":
                while True:
                    cur.execute("SELECT * FROM equipment")
                    equips = cur.fetchall()
                    for row in equips:
                        print(f"EquipmentID: {row[0]}, Name: {row[1]}, Monitor Status: {row[2]}, Time before next update: {row[3]}")
                    equipID = input("\nPlease enter the equipment ID you would like to update:\n")
                    cur.execute("SELECT * FROM equipment WHERE equipmentID = %s", (equipID,))
                    if cur.fetchone() is None:
                        print("\nThere does not exist an equipment with that ID.\n")
                        break
                    else:
                        name = input("Please enter the new name of the equipment:\n")
                        status = input("Please enter the new status of the equipment (True (1) or False (2)):\n")
                        time = input("Please enter the new time before the next update (in days):\n")
                        if status == "1":
                            cur.execute("UPDATE equipment SET name = %s, monitorStatus = %s, nextMonitorDate = %s WHERE equipmentID = %s",
                                        (name, True, time, equipID))
                            db.commit()
                        else:
                            cur.execute("UPDATE equipment SET name = %s, monitorStatus = %s, nextMonitorDate = %s WHERE equipmentID = %s",
                                        (name, False, time, equipID))
                            db.commit()
                        print(f"\nEquipment {name} has been updated!\n")
                        con = input("Would you like to update anymore? (1) Yes or (2) No\n")
                        if con == "2":
                            db.commit()
                            break
                        else:
                            db.commit()
                    
            elif adminChoice == "5":
                print("\nExiting...\n")
                break
        except ValueError:
            print("\nPlease enter correct input\n")
        except psycopg.errors.InvalidTextRepresentation as f:
            print("\nThis is in the wrong form.\n")
            db.rollback()
        except psycopg.errors.InvalidDatetimeFormat as e:
            print("\nPlease ensure the date/time format is correct\n")
            db.rollback()

def createClass():
    while True:
        try:
            classExercise = input("Please enter the name of the exercise the class will be doing:\n")
            #user same process as member schedule to get all trainers
            cur.execute("SELECT name FROM trainer")
            allTrainers = cur.fetchall()
            print("Here is the names of our current trainers:")
            for i in allTrainers:
                print(i[0])

            trainerName = input("\nEnter the name of the trainer you would like to host the class:\n")
            cur.execute("SELECT trainerID FROM trainer WHERE name = %s", (trainerName,))
            #get id from name given
            result = cur.fetchone()
            if result is None:
                print("\nThere is no trainer with that name.\n")
                break
            else:
                trainerID = result[0]

            cur.execute("SELECT day,timeStart,timeEnd FROM schedule WHERE trainerID = %s", (trainerID,))
            print(f"\nHere is the schedule for {trainerName}:")
            for row in cur:
                print(f"{row[0]} from {row[1]} - {row[2]}")


            day = input("\nPlease enter the day the class will occur (must be capatalized):\n")
            #get time and end based on trainers schedule
            timeStart = input("Please enter the time for the class to start (HH:MM:SS):\n")
            timeEnd = input("Please enter the time for the class to end (HH:MM:SS):\n")

            #check trainer is available
            cur.execute("SELECT * from schedule WHERE trainerID = %s AND day = %s AND timeStart <= %s AND timeEnd >= %s", 
                            (trainerID, day, timeStart, timeEnd))
            if cur.fetchone() is None:
                print("\nThe trainer does not have availability to host a class at this time or day.\n")
                break
            
            #if there exists a class already that is the same time 
            # Check if there exists a class already that is the same time 
            cur.execute("""
                SELECT * from class 
                WHERE day = %s AND trainerID = %s AND (
                    (timeStart <= %s AND timeEnd > %s) OR 
                    (timeStart < %s AND timeEnd >= %s) OR 
                    (timeStart >= %s AND timeEnd <= %s) OR
                    (timeStart < %s AND timeEnd > %s)
                )
            """, (day, trainerID, timeStart, timeStart, timeStart, timeEnd, timeStart, timeEnd, timeEnd, timeEnd))
            overCheck = cur.fetchone()
            if overCheck is not None:
                print("\nYou have a class that overlaps this one, please check your class list:\n")
                cur.execute("""
                    SELECT class.CID, class.day, class.timeStart, class.timeEnd, trainer.name 
                    FROM class 
                    JOIN trainer ON class.trainerID = trainer.trainerID 
                    WHERE class.day = %s AND class.trainerID = %s
                """, (day, trainerID))
                overlap = cur.fetchall()
                for row in overlap:
                    print(f"Class ID: {row[0]}, Day: {row[1]}, StartTime: {row[2]}, End Time: {row[3]}, Trainer: {row[4]}")
                break
                
            #then check if there exists a session during the same time
            # Check if there exists a session during the same time
            cur.execute("""
                SELECT * from session 
                WHERE day = %s AND trainerID = %s AND (
                    (timeStart <= %s AND timeEnd > %s) OR 
                    (timeStart < %s AND timeEnd >= %s) OR 
                    (timeStart >= %s AND timeEnd <= %s) OR
                    (timeStart < %s AND timeEnd > %s)
                )
            """, (day, trainerID, timeStart, timeStart, timeStart, timeEnd, timeStart, timeEnd, timeEnd, timeEnd))
            overlapCheck = cur.fetchone()
            if overlapCheck is not None:
                print("\nYou have a session that overlaps with this class time/day and trainer, please check the sessions.\n")
                cur.execute("""
                    SELECT session.sID, session.day, session.timeStart, session.timeEnd, trainer.name 
                    FROM session 
                    JOIN trainer ON session.trainerID = trainer.trainerID 
                    WHERE session.day = %s AND session.trainerID = %s
                """, (day, trainerID))
                overlap = cur.fetchall()
                for row in overlap:
                    print(f"Session ID: {row[0]}, Day: {row[1]}, StartTime: {row[2]}, End Time: {row[3]}, Trainer: {row[4]}")
                break  
            else:
                cur.execute("INSERT INTO class (day, timeStart,timeEnd,classExercise,trainerID) VALUES (%s, %s, %s, %s, %s)",
                    (day, timeStart, timeEnd, classExercise, trainerID))
                db.commit()
                print(f"\nClass was created with {trainerName} as a host on {day} at {datetime.strptime(timeStart,'%H:%M:%S').time()}!\n")
                break
        except ValueError:
            print("\nPlease ensure the input is correct\n")
            db.rollback()
        except psycopg.errors.InvalidDatetimeFormat as e:
            print("\nPlease ensure the date/time format is correct\n")
            db.rollback()

def printAllClasses():
    print("\nHere is all the classes:\n")
    cur.execute("""
    SELECT class.CID, class.day, class.timeStart, class.timeEnd, class.classExercise, trainer.name 
    FROM class 
    JOIN trainer ON class.trainerID = trainer.trainerID
    """)
    allClasses = cur.fetchall()
    for row in allClasses:
        print(f"Class ID: {row[0]}, Day: {row[1]}, Start Time: {row[2]}, End Time: {row[3]}, Class Exercise: {row[4]}, Trainer: {row[5]}")
    print("\n")
    

def printAllTrainers():
    #first print out all the trainers so member knows
    cur.execute("SELECT name FROM trainer")
    allTrainers = cur.fetchall()
    print("\nHere is the names of our current trainers:")
    for i in allTrainers:
        print(i[0])

def deleteClass():
    printAllClasses()
    cId = input("\nSelect a class ID you would like to delete:\n")
    cur.execute("SELECT * FROM class WHERE CID = %s",(cId,))
    cidCheck = cur.fetchone()
    if cidCheck is None:
        print("\nThere is no class with that ID.\n")
    else:
        cur.execute("DELETE FROM class WHERE CID = %s", (cId,))
        db.commit()
        print(f"\nThe class has been cancelled. The trainer and members has been notified.\n")

def classScheduleMenu():
    print("\nWelcome to class schedule management!")
    while True:
        try:
            
            adminChoice = input("""
        --------------------------------
        Class Schedule Menu:
        (1) Create a new class
                        
        (2) View all classes
                        
        (3) Update an existing class

        (4) Cancel a class

        (5) Exit Class Schedule Menu
        -------------------------------\n""")
            if adminChoice == "1":
                createClass()
            elif adminChoice == "2":
                printAllClasses()
            elif adminChoice == "3":
                while True:
                    try:
                        printAllClasses()
                        # Update Existing Availability
                        cId = str(input("\nPlease select a class that you want to update (Must be the Class ID):\n"))
                        cur.execute("SELECT * FROM class WHERE CID = %s", (cId,))
                        #check if exists first
                        if cur.fetchone() is None:
                            print("\nYou have not yet created a class like that yet, please create it first.")
                            break
                        
                        printAllTrainers()
                        #get new trainer
                        trainerName = input("\nEnter the name of the trainer you would like to host the class:\n")
                        cur.execute("SELECT trainerID FROM trainer WHERE name = %s", (trainerName,))
                        #get id from name given
                        result = cur.fetchone()
                        if result is None:
                            print("\nThere does not exist a trainer of that name.")
                            break
                        else:
                            trainerID = result[0]

                        cur.execute("SELECT day,timeStart,timeEnd FROM schedule WHERE trainerID = %s", (trainerID,))
                        print(f"\nHere is the schedule for {trainerName}:")
                        for row in cur:
                            print(f"{row[0]} from {row[1]} - {row[2]}")
                        #get the rest of necessary data
                        day = input("\nPlease enter a new day for the class to start:\n")
                        timeStart = input("Please input a new start time for that day in the format hh:mm:ss (24-hour clock):\n")
                        timeEnd = input("Please input a new end time for that day in the format hh:mm::ss (24-hour clock)\n")

                        #first check if the trainer has availability at the time
                        cur.execute("SELECT * from schedule WHERE trainerID = %s AND day = %s AND timeStart <= %s AND timeEnd >= %s", 
                            (trainerID, day, timeStart, timeEnd))
                        if cur.fetchone() is None:
                            print("\nThat trainer does not have availability to host a class at this time or day.\n")

                        else:
                            #then check if there exists a session during the same time
                            cur.execute("""
                                SELECT * from session 
                                WHERE day = %s AND trainerID = %s AND (
                                    (timeStart <= %s AND timeEnd > %s) OR 
                                    (timeStart < %s AND timeEnd >= %s) OR 
                                    (timeStart >= %s AND timeEnd <= %s) OR
                                    (timeStart < %s AND timeEnd > %s)
                                )
                            """, (day, trainerID, timeStart, timeStart, timeStart, timeEnd, timeStart, timeEnd, timeEnd, timeEnd))

                            if cur.fetchone() is not None:
                                print("\nYou have a session that overlaps this class time, please check the sessions here:\n")
                                cur.execute("""
                                    SELECT session.SID, session.day, session.timeStart, session.timeEnd, trainer.name 
                                    FROM session 
                                    JOIN trainer ON session.trainerID = trainer.trainerID 
                                    WHERE session.day = %s AND session.trainerID = %s
                                """, (day, trainerID))
                                overlap = cur.fetchall()
                                for row in overlap:
                                    print(f"Session ID: {row[0]}, Day: {row[1]}, StartTime: {row[2]}, End Time: {row[3]}, Trainer: {row[4]}")
                                break
                            else:

                                startObject = datetime.strptime(timeStart, '%H:%M:%S')
                                endObject = datetime.strptime(timeEnd, '%H:%M:%S')
                                cur.execute("UPDATE class SET trainerID = %s, timeStart = %s, timeEnd = %s, day = %s WHERE CID = %s",
                                            (trainerID,startObject.time(), endObject.time(), day, cId,))
                                print("\nClass has been updated!\n")
                                db.commit()
                                con = input("Would you like to update any others? (1) Yes or (2) No\n")
                                if con == "2":
                                    db.commit()
                                    break
                                else:
                                    db.commit()
                    except ValueError:
                        print("Please enter the proper format")
                        db.rollback()
                    except psycopg.errors.InvalidDatetimeFormat as e:
                        print("Please ensure the date/time formate is correct")
                        db.rollback()
                    

            elif adminChoice == "4":
                deleteClass()       
            elif adminChoice == "5":
                print("\nExiting the menu...\n")
                break
        #except TypeError:
            #print("Please enter the proper format")
        except ValueError:
            print("Please enter in the proper format.")
            db.rollback()
        except psycopg.errors.InvalidTextRepresentation as f:
            print("\nThis is in the wrong format.\n")
            db.rollback()

def printAllBills():
    cur.execute("SELECT * from payment")
    allBills = cur.fetchall()
    for row in allBills:
        if row[3] == True:
            paid = "Paid"
        if row[3] == False:
            paid = "Unpaid"
        print(f"Bill ID: {row[0]}, Amount: {row[1]}, MemberID: {row[2]}, Payment Status: {paid}")

def billingAndPaymentMenu():
    print("\nWelcome to the billing and payment menu!")
    while True:
        try:
            adminChoice = input("""
    --------------------------------
    Bill Payment Menu:
    (1) Update a payment
                    
    (2) View all payments
                    
    (3) Exit the menu
    -------------------------------\n""")
            if adminChoice == "1":
                print("\nHere is all the payment information.")
                printAllBills()
                bill = input("\nChoose the bill ID that you would like to make change.\n")
                cur.execute("SELECT * FROM payment WHERE billID = %s",(bill,))
                billCheck = cur.fetchone()
                if billCheck is None:
                    print("\nThere is no bill with that ID\n")
                    break
                else:
                    amount = input("Choose the new amount of the bill (type same number to not change):\n")
                    paid = input("What is the status of the bill you would like to change to? (1) Paid or (2) Unpaid\n")
                    if paid == "1":
                        cur.execute("UPDATE payment SET amount = %s, paid = %s WHERE billID = %s",
                                    (amount, True,bill))
                        db.commit()
                    elif paid == "2":
                        cur.execute("UPDATE payment SET amount = %s, paid = %s WHERE billID = %s",
                            (amount,False,bill))
                        db.commit()
                    con = input("Would you like to update anymore bills? (1) Yes or (2) No:\n")
                    if con == "2":
                        db.commit()
                        break
                    else:
                        db.commit()
            elif adminChoice == "2":
                print("\nHere is all the payment information.")
                printAllBills()
            elif adminChoice == "3":
                print("\nExiting...\n")
                break
            else:
                print("\nPlease enter a valid number.\n")
                break
        except ValueError:
            print("Please enter the proper input.")
            db.rollback()
        except TypeError:
            print("Please enter the proper input.")
            db.rollback()
        except psycopg.errors.InvalidTextRepresentation as f:
            print("\nPlease enter the proper format.\n")
            db.rollback()


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
            db.rollback()
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
        name = str(input("Enter a name as well for your members to call you by:\n"))
        #make new data in the trainer table and set id username and password for now
        try:
            #set the data for username and password and name only
            cur.execute("INSERT INTO trainer (username, password,name) VALUES (%s, %s,%s)",
                    (usernameId,userPassWord,name))
            
            #get the trainerID of the new trainer
            cur.execute("SELECT trainerID FROM trainer WHERE username = %s AND password = %s AND name = %s" ,
                    (usernameId,userPassWord, name))
            trainerID = str(cur.fetchone()[0])
            print(f"\nNew trainer {usernameId} added!")
            db.commit()
            return usernameId, userPassWord, trainerID
        
        except psycopg.IntegrityError as e:
            print("Either username or password is the same as an existing trainer.")
            db.rollback()
            return usernameId, userPassWord, False
        except psycopg.errors.InvalidDatetimeFormat as e:
            print("Please ensure the date/time formate is correct")
            db.rollback()

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
    print(f"\nHere is your current weight: {weight}kg\n")
     #This will keep asking for lapTime until constraints are met, then exists while loop
    while True:
        try:
            weightGoal = float(input("Please enter your new weight goal (in kgs):\n"))
            cur.execute("UPDATE member SET weightGoal = %s WHERE memberID = %s", (weightGoal,memberID))

            print(f"\nUpdated your weight goal to: {weightGoal}!\n")
            db.commit()
            break
        except ValueError:
            print("\nInvalid input, please enter a number (can include decimals).\n")
           
        except psycopg.IntegrityError as e:
            print("\nInvalid input, please enter a number above 0\n")
        except psycopg.errors.InvalidTextRepresentation as f:
            print("\nPlease enter the proper format.\n")
            db.rollback()
       

def updateLapTimeGoal(memberID):
    cur.execute("SELECT lapTime FROM member WHERE memberID = %s", (memberID,))
    lapTime = cur.fetchone()[0]
    print(f"\nHere is your current lap time: {lapTime}\n")
     #This will keep asking for lapTime until constraints are met, then exists while loop
    while True:
        try:
            lapTimeGoal = input("Please enter your new lap time goal (in HH:MM:SS):\n")
            #update the db
            cur.execute("UPDATE member SET lapTimeGoal = %s WHERE memberID = %s", (lapTimeGoal,memberID))

            print(f"\nUpdated your lap time goal to: {lapTimeGoal}!\n")
            db.commit()
            break
        #makes sure to rollback the previous execute on error
        except ValueError:
            print("\nInvalid input, please enter the proper format.\n")
            
        except psycopg.IntegrityError as e:
            print("\nInvalid input, please enter a number above 0\n")
        except psycopg.errors.InvalidTextRepresentation as f:
            print("\nPlease enter the proper format.\n")
            db.rollback()
        

def updateBenchMaxGoal(memberID):
    cur.execute("SELECT benchMax FROM member WHERE memberID = %s", (memberID,))
    benchMax = cur.fetchone()[0]
    print(f"\nHere is your current bench max: {benchMax}kg\n")
    while True:
        try:
            benchMaxGoal = float(input("Please enter your new bench max goal (in kgs):\n"))
            #update the db
            cur.execute("UPDATE member SET benchMaxGoal = %s WHERE memberID = %s", (benchMaxGoal,memberID))

            print(f"\nUpdated your bench goal to: {benchMaxGoal}!")
            db.commit()
            break
        #makes sure to rollback the previous execute on error
        except ValueError:
            print("\nInvalid input, please enter a number.\n")
            
        except psycopg.IntegrityError as e:
            print("\nInvalid input, please enter a number above 0\n")
        except psycopg.errors.InvalidTextRepresentation as f:
            print("\nPlease enter the proper format.\n")
            db.rollback()
        

def updateSquatGoal(memberID):
    cur.execute("SELECT squatMax FROM member WHERE memberID = %s", (memberID,))
    squatMax = cur.fetchone()[0]
    print(f"\nHere is your current squat max: {squatMax}kg")
    while True:
        try:
            squatMaxGoal = float(input("Please enter your new squat max goal (in kgs):\n"))
            #update the db
            cur.execute("UPDATE member SET squatMaxGoal = %s WHERE memberID = %s", (squatMaxGoal,memberID))

            print(f"\nUpdated your squat goal to: {squatMaxGoal}!\n")
            db.commit()
            break
        #makes sure to rollback the previous execute on error
        except ValueError:
            print("\nInvalid input, please enter a number.\n")
        except psycopg.IntegrityError as e:
            print("\nInvalid input, please enter a number above 0\n")
        except psycopg.errors.InvalidTextRepresentation as f:
            print("\nPlease enter the proper format.\n")
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
    (6) Lap Time (in HH:MM:SS)
    (7) Bench Max (in kilograms)
    (8) Squat Max (in kilograms)
            \n"""))
    
            dataUpdate = input("Please enter the new data or type clear to erase current data:\n")
            for data in cols:
                if columnUpdate == cols.index(data):
                    #if data is int
                    if data == "age":
                        if dataUpdate in ["clear", "c", "Clear", "C"]:
                            cur.execute(f"UPDATE member SET {data} = %s WHERE memberID = %s",(None,memberID))
                            db.commit()
                        else:
                            cur.execute(f"UPDATE member SET {data} = %s WHERE memberID = %s",(int(dataUpdate),memberID))
                            print(f"\nUpdated {data} to {dataUpdate}\n")
                            db.commit()
                    #if data is float
                    elif data == "height" or data == "weight" or data == "squatMax" or data == "benchMax":
                        if dataUpdate in ["clear", "c", "Clear", "C"]:
                            cur.execute(f"UPDATE member SET {data} = %s WHERE memberID = %s",(None,memberID))
                            db.commit()
                        else:
                            cur.execute(f"UPDATE member SET {data} = %s WHERE memberID = %s",(float(dataUpdate),memberID))
                            print(f"\nUpdated {data} to {dataUpdate}\n")
                            db.commit()
                    #if data is other
                    else:
                        if dataUpdate in ["clear", "c", "Clear", "C"]:
                            cur.execute(f"UPDATE member SET {data} = %s WHERE memberID = %s",(None,memberID))
                            db.commit()
                        else:
                            cur.execute(f"UPDATE member SET {data} = %s WHERE memberID = %s",(dataUpdate,memberID))
                            print(f"\nUpdated {data} to {dataUpdate}\n")
                            db.commit()
            db.commit()
            break
        #makes sure to rollback the previous execute on error
        except ValueError:
            print("\nInvalid input, please enter a number.\n")
        except psycopg.IntegrityError as e:
            print("\nInvalid input, please enter a valid number\n")
        except psycopg.errors.InvalidTextRepresentation as f:
            print("\nPlease enter the proper format.\n")
            db.rollback()
        except psycopg.errors.InvalidDatetimeFormat as c:
            print("\nPlease enter a proper time format.\n")
            db.rollback()
        except psycopg.errors.DataError as x:
            print("\nMust be from 00:00:00 to 23:59:59.\n")
            db.rollback()
        except psycopg.errors.DateTimeFieldOverFlow as c:
            print("\nPlease enter a real time from 00:00:00 to 23:59:59.\n")
            db.rollback()
    
def memberScheduleMenu(memberID):
    print("Welcome to your schedule!")
    while True:
        choice = input("""
    -------------------------------------
    Schedule Menu:
    (1) Book a Session with a Trainer
                       
    (2) View Your Sessions
                       
    (3) Cancel a session 
                       
    (4) Join a Group Fitness Class
                       
    (5) View Your Group Fitness Classes
                       
    (6) Drop out of fitness class
                       
    (7) Exit the menu
    -------------------------------------\n""")
        return choice
   
def createSession(memberID):
    while True:
        try:
            printAllTrainers()
            trainerName = input("\nEnter the name of the trainer you would like to train with:\n")
            cur.execute("SELECT trainerID FROM trainer WHERE name = %s", (trainerName,))
            #get id from name given
            result = cur.fetchone()
            if result is None:
                print("\nTrainer does not exist.\n")
                break
            else:
                trainerID = result[0]

            cur.execute("SELECT day,timeStart,timeEnd FROM schedule WHERE trainerID = %s", (trainerID,))
            print(f"\nHere is the schedule for {trainerName}:")
            for row in cur:
                print(f"{row[0]} from {row[1]} - {row[2]}")

            day = input("\nEnter the day for the session (Day of Week, Capatalized):\n")
            timeStart = input("Enter the start time for the session: HH:MM:SS (24-Hour):\n")
            timeEnd = input("Enter the end time for the session: HH:MM:SS (24-Hour):\n")
            #use trainerId and data to get availaiblity of trainer 
            cur.execute("SELECT * from schedule WHERE trainerID = %s AND day = %s AND timeStart <= %s AND timeEnd >= %s", 
                        (trainerID, day, timeStart, timeEnd))
            #check if availability does not line up
            if cur.fetchone() is None:
                print("\nThe trainer does not have availability at this time or day.\n")

            else:
                #if there exists a session already that is the same time 
                cur.execute("""
                    SELECT * from session 
                    WHERE day = %s AND (
                        (timeStart <= %s AND timeEnd > %s) OR 
                        (timeStart < %s AND timeEnd >= %s) OR 
                        (timeStart >= %s AND timeEnd <= %s) OR
                        (timeStart < %s AND timeEnd > %s)
                    )
                """, (day, timeStart, timeStart, timeStart, timeEnd, timeStart, timeEnd, timeEnd, timeEnd))
                if cur.fetchone() is not None:
                    print("\nYou have a session that overlaps this one, please check your session list:\n")
                    cur.execute("""
                        SELECT session.SID, session.day, session.timeStart, session.timeEnd, trainer.name 
                        FROM session 
                        JOIN trainer ON session.trainerID = trainer.trainerID 
                        WHERE session.day = %s AND session.trainerID = %s
                    """, (day, trainerID))
                    overlap = cur.fetchall()
                    for row in overlap:
                        print(f"Session ID: {row[0]}, Day: {row[1]}, StartTime: {row[2]}, End Time: {row[3]}, Trainer: {row[4]}")
                    break
                else:
                    cur.execute("SELECT * FROM session where memberID = %s", (memberID,))
                    #set the time in hours for the entire session (for payment)
                    totalTime = ((datetime.strptime(timeEnd,'%H:%M:%S') - datetime.strptime(timeStart,'%H:%M:%S')).total_seconds())/3600
                    bill = 65 * totalTime
                    print(f"The bill for this session is: ${bill}")
                    billChoice = input("\nWould you like to pay now (1) or in person (2)?\n")

                    if billChoice == "1":
                        #make new bill that is paid for admin to keep track of 
                        cur.execute("INSERT INTO payment (amount, memberID, paid) VALUES (%s, %s, %s)", (bill,memberID,True))
                        db.commit()
                        print("Decision received! Your bill has been paid!")

                    elif billChoice == "2":
                        #make new bill that is not paid
                        cur.execute("INSERT INTO payment (amount, memberID, paid) VALUES (%s, %s, %s)", (bill,memberID,False))
                        db.commit()
                        print("Bill has been set to unpaid for now, please see admins in person to pay the bill.")

                    cur.execute("INSERT INTO session (trainerID, memberID, day, timeStart, timeEnd) VALUES (%s, %s, %s, %s, %s)",
                                (trainerID, memberID, day, timeStart, timeEnd))
                    db.commit()

                    cur.execute("SELECT session.*, trainer.name AS trainerName FROM session JOIN trainer ON session.trainerID = trainer.trainerID WHERE day = %s AND session.trainerID = %s",
                                (day,trainerID))
                    print(f"\nSession was booked with {trainerName} on {day} at {datetime.strptime(timeStart,'%H:%M:%S').time()}!\n")
                    break
        
        except ValueError:
            print("\nPlease enter the proper input.\n")
            db.rollback()
        except psycopg.errors.InvalidDatetimeFormat as e:
            print("\nPlease make sure the time is the correct format.\n")
            db.rollback()

def memberSchedule(memberID, choice):
    while True:
        try:
            if choice == "1":
                try:
                    #get all the session data from member
                    createSession(memberID)
                    break
                
                except psycopg.IntegrityError:
                    print("\nPlease ensure that the time is formatted correctly, and that the name is of an existing trainer.\n")
                    db.rollback()

            elif choice == "2":
                cur.execute("""
                    SELECT session.SID, session.day, session.timeStart, session.timeEnd, trainer.name 
                    FROM session 
                    JOIN trainer ON session.trainerID = trainer.trainerID 
                    WHERE session.memberID = %s
                """, (memberID,))
                print("\nYour current sessions are:")
                for row in cur:
                    print(f"Session ID: {row[0]}, Day: {row[1]}, StartTime: {row[2]}, End Time: {row[3]}, Trainer: {row[4]}")
                break


            elif choice == "3":
                cur.execute("SELECT * FROM session WHERE memberID = %s", (memberID,))
                print("\nYour current sessions are:")
                for row in cur:
                    print(f"Session ID: {row[0]}, Day: {row[3]}, StartTime: {row[4]}, End Time: {row[5]}")
                sID = input("\nEnter the session ID that you want to cancel:\n")
                cur.execute("SELECT * FROM session WHERE SID = %s AND memberID = %s",(sID,memberID))
                check = cur.fetchone()
                if check is None:
                    print("\nThere does not exist a session with that ID\n")
                    break
                else:
                    cur.execute("DELETE FROM session WHERE SID = %s AND memberID = %s", (sID, memberID))
                    db.commit()
                    print(f"\nThe session has been cancelled. The trainer has been notified.\n")
                    break

            elif choice == "4":
                cur.execute("""
                    SELECT class.CID, class.classExercise, class.day, class.timeStart, class.timeEnd, trainer.name 
                    FROM class 
                    JOIN trainer ON class.trainerID = trainer.trainerID
                """)
                allClasses = cur.fetchall()
                print("\nHere are all the classes:")
                for c in allClasses:
                    print(f"Class ID: {c[0]}, Exercise: {c[1]}, Day: {c[2]}, StartTime: {c[3]}, End Time: {c[4]}, Trainer: {c[5]}")


                cID = input("\nEnter the ID of the class you would like to join:\n")

                cur.execute("SELECT * from memberClass WHERE CID = %s AND memberID = %s", 
                    (cID,memberID))
                #check if availability does not line up
                check = cur.fetchone()
                if check is not None:
                    print("\nYou are already enrolled in this class \n")
                    break
                cur.execute("SELECT * FROM class WHERE CID = %s", (cID,))
                twoCheck = cur.fetchone()
                if twoCheck is None:
                    print("\nClass does not exist. \n")
                    break
                else:
                    cur.execute("INSERT INTO memberClass (CID, memberID) VALUES (%s, %s)", (cID, memberID))
                    db.commit()
                    print("\nYou have joined the class!\n")
                    break
                

            elif choice == "5":
                cur.execute("""
                    SELECT memberClass.CID, class.classExercise, class.day, class.timeStart, class.timeEnd, trainer.name 
                    FROM memberClass 
                    JOIN class ON memberClass.CID = class.CID 
                    JOIN trainer ON class.trainerID = trainer.trainerID 
                    WHERE memberClass.memberID = %s
                """, (memberID,))
                print("\nThe classes you are currently registered for:\n")
                for row in cur: 
                    print(f"Class ID: {row[0]}, Exercise: {row[1]}, Day: {row[2]}, StartTime: {row[3]}, End Time: {row[4]}, Trainer: {row[5]}")
                break

            
            elif choice == "6":
                printAllClasses()
                cId = input("\nEnter the class Id of the class you wish to drop from:\n")
                cur.execute("SELECT * from memberClass WHERE cID = %s AND memberID = %s", 
                    (cId,memberID))
                #check if availability does not line up
                if cur.fetchone() is None:
                    print("\nYou are not in any class of that ID\n")
                    break
                else:
                    cur.execute("DELETE FROM memberClass WHERE CID = %s AND memberID = %s", (cId, memberID))
                    db.commit()
                    print("\nYou have left the class!\n")
                    break

            elif choice == "7":
                print("\nExiting the menu...")
                break
            else:
                print("\nPlease enter a valid choice.\n")
                break
        except ValueError:
            print("Please enter a valid input.")
        except psycopg.errors.InvalidDatetimeFormat as e:
            print("Please ensure the date/time format is correct")
            db.rollback()
        except psycopg.errors.InvalidTextRepresentation as f:
            print("\nPlease enter the proper format.\n")
            db.rollback()

def profileMenu(memberID):
    col_names = []
    data_rows = []
    while True:
        choice = input("""
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

                    data_rows = []
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
                        db.commit()
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
                    except psycopg.errors.InvalidDatetimeFormat as e:
                        print("Please ensure the date/time formate is correct")
                        db.rollback()
                        
            case "4":
                #print profile info, goals, and health metrics in seperate sections all titled
                print("Here is your profile information:\n")
                cur.execute("SELECT fName,lName,email,height,weight,age,lapTime,benchMax,squatMax FROM member WHERE memberID = %s",(memberID,))
                
                col_names = ([desc[0] for desc in cur.description])

                data_rows = []
                for row in cur:
                    data_rows.append(row)

                for data in col_names:
                    print(f"{data}: {data_rows[0][col_names.index(data)]}")

                print("\nHere are your fitness goals:\n")
                cur.execute("SELECT weightGoal,lapTimeGoal,squatMaxGoal,benchMaxGoal FROM member WHERE memberID = %s",(memberID,))
                
                col_names = ([desc[0] for desc in cur.description])

                data_rows = [] #make sure to clear data before append new data
                for row in cur:
                    data_rows.append(row)
                
                
                for data in col_names:
                    print(f"{data}: {data_rows[0][col_names.index(data)]}")

                print("\nHere are your health metrics:\n")
                cur.execute("SELECT bmi,restingHeartRate FROM member WHERE memberID = %s",(memberID,))
                
                col_names = ([desc[0] for desc in cur.description])
                
                data_rows = []
                for row in cur:
                    data_rows.append(row)

                for data in col_names:
                    print(f"{data}: {data_rows[0][col_names.index(data)]}")
                
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
    
    gender = input("\nAre you a female (1) or male (2)?\n")
    if gender == "1":
        try:
            if weight < 70.1:
                print(f"\nThe average weight in Canada for a female is 70.1kg You weigh {weight}kg. You are below average.")
            elif weight > 70.1:
                print(f"\nThe average weight in Canada for a female is 70.1kg. You weigh {weight}kg. You are above average.")
            elif weight == 70.1:
                print("\nYou are the average weight for a female in Canada.")
        except TypeError:
            print("\nLooks like your weight was not set up, please see personal information in profile mangement to set it up!\n")
        try:
            if height < 1.62:
                print(f"The average height in Canada for a female is 1.77m. You are {height}m. You are short.")
            elif height > 1.62:
                print(f"The average height in Canada for a female is 1.77m. You are {height}m. You are tall.")
            elif height == 1.62:
                print(f"The average height in Canada for a female is 1.77m. You are {height}m. You are average.")
        except TypeError:
            print("\nLooks like your height was not set up, please see personal information in profile mangement to set it up!\n")
    elif gender == "2":
            try:
                if weight < 84.6:
                    print(f"\nThe average weight in Canada for a male is 84.6kg. You weigh {weight}kg. You are below average.")
                elif weight > 84.6:
                    print(f"\nThe average weight in Canada for a male is 84.6kg. You weigh {weight}kg. You are above average.")
                elif weight == 84.6:
                    print("\nYou are the average weight for a male in Canada.")
            except TypeError:
                print("\nLooks like your weight was not set up, please see personal information in profile mangement to set it up!\n")
            try:
                if height < 1.77:
                    print(f"The average height in Canada for a male is 1.77m. You are {height}m. You are short.")
                if height > 1.77:
                    print(f"The average height in Canada for a male is 1.77m. You are {height}m. You are tall.")
                elif height == 1.77:
                    print(f"The average height in Canada for a male is 1.77m. You are {height}m. You are average.")
            except TypeError:
                print("\nLooks like your height was not set up, please see personal information in profile mangement to set it up!\n")
    try:
        if age < 40:
            print(f"The average age in Ontario is 40. You are {age} and thus less than average!")
        elif age > 40:
            print(f"The average age in Ontario is 40. You are {age} and thus above average!")
        elif age == 40:
            print(f"The average age in Ontario is 40. You are 40 and thus average!")
    except TypeError:
        print("\nLooks like your age was not set up, please see personal information in profile mangement to set it up!\n")
    try:
        if bmi <= 24.9 or bmi >= 18.5:
            print(f"Your BMI is: {bmi}. Which is in a healthy range!\n")
        elif bmi >= 25 or bmi <= 29.9:
            print(f"Your BMI is: {bmi}. Which is in the overweight range!\n")
        elif 30 <= bmi <= 39.9:
            print(f"Your BMI is: {bmi}. Which is in the obesity range!\n")
        elif bmi >= 40:
            print(f"Your BMI is: {bmi}. Which is in the severe obesity range!")
    except TypeError:
        print("\nLooks like your height, weight, or age was not set up, please see personal information in profile mangement to set it up!\n")
    

def viewFitnessAchievements(memberID):
    # This function will fetch and display the fitness achievements of the member
    # from the relevant tables in the database.
    # try:
        
    cur.execute("SELECT lapTime,weight,weightGoal,lapTimeGoal,squatMax,squatMaxGoal,benchMaxGoal,benchMax FROM member WHERE memberID = %s", (memberID,))
    lapTime,weight,weightGoal, lapTimeGoal, squatMax, squatMaxGoal, benchMaxGoal, benchMax = cur.fetchone()
    #get the time difference between the goal and current laptime
    
    #convert to a datetime from a EPOCH timestamp
    try:
        cur.execute("SELECT EXTRACT (EPOCH FROM (lapTime - lapTimeGoal)) FROM member WHERE memberID = %s", (memberID,))
        timeDifference = abs(cur.fetchone()[0])
        formattedTimeDiff = datetime.fromtimestamp(int(timeDifference))
        if(weight < weightGoal):
            print(f"Your current weight goal is {weightGoal}kg. You need to gain {weightGoal-weight}kgs to reach it!")
        elif(weight > weightGoal):
            print(f"Your current weight goal is {weightGoal}kg. You need to lose {weight-weightGoal}kgs to reach it!")
        elif(weight == weightGoal):
            print(f"Your current weight goal of {weightGoal}kg is the same as your weight of {weight}kg! Great Job!")
    except TypeError:
        print("Look like you have not set a value for either weight or a weight goal, please review your information if you wish to see this achievement")
    try:
        if(lapTime <= lapTimeGoal):
            print(f"Your current lap time goal is {lapTimeGoal}. Your best you've ran is {lapTime}, congratulations!")
        elif(lapTime > lapTimeGoal):
            #print in formatted string
            print(f"Your current lap time goal is {lapTimeGoal}. You need to run {formattedTimeDiff.strftime('%M:%S')} faster to reach it!")
    except TypeError:
        print("Look like you have not set a value for either lap time or a lap time goal, please review your information if you wish to see this achievement")

    try:
        if(squatMax < squatMaxGoal):
            print(f"Your current squat max goal is {squatMaxGoal}kg. The best you've lifted is {squatMax}kg, keep it up and get those {squatMaxGoal-squatMax}kgs up!")
        elif(squatMax > squatMaxGoal):
            print(f"Your current squat max goal is {squatMaxGoal}kg. The best you've lifted is {squatMax}kg, congratulations on beating your fitness goal!")
        elif squatMaxGoal == squatMax:
            print(f"Both your squat max goal: {squatMaxGoal}kg and your current best: {squatMax}kg are the same! Congratulations on reaching the goal, now lift that {squatMaxGoal-squatMax}kgs to achieve it!")
    except TypeError:
        print("Look like you have not set a value for either squat max or a squat max goal, please review your information if you wish to see this achievement")

    try:
        if(benchMax < benchMaxGoal):
            print(f"Your current bench max goal is {benchMaxGoal}kg. The best you've lifted is {benchMax}kg, keep it up and get those {benchMaxGoal-benchMax}kgs up!")
        elif(benchMax > benchMaxGoal):
            print(f"Your current bench max goal is {benchMaxGoal}kg. The best you've lifted is {benchMax}kg, congratulations on beating your fitness goal!")
        elif benchMaxGoal == benchMax:
            print(f"Both your bench max goal: {benchMaxGoal}kg and your current best: {benchMax}kg are the same! Congratulations on reaching the goal, now lift that {benchMaxGoal-benchMax}kgs to achieve it!")
    except TypeError:
        print("Look like you have not set a value for either bench max or a bench max goal, please review your information if you wish to see this achievement")

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

def updateTrainerName(trainerID):
    while True:
        try:
            name = input("Please enter your name you would like the members to call you:\n")
            cur.execute("UPDATE trainer set name = %s WHERE trainerID = %s", (name,trainerID))
            db.commit()
            break
        except TypeError:
            print("\nMust be words\n")
            db.rollback()
        except ValueError:
            print("Please enter a valid input.")
            db.rollback()

def scheduleMenu(trainerID):
    print("Welcome to your schedule management!")
    while True:
        choice = input("""
    --------------------------------
    Schedule Menu:
    (1) Create New Availability
                       
    (2) Update Existing Availability
                       
    (3) See your current available Days
                       
    (4) Exit Dashboard
    -------------------------------\n""")
        try:
            if choice == "1":
                while True: #to enable multiple creations in a row 
                    dayWhen = str(input("Please select a day that you are available (Must be Capatalized):\n"))
                    #check if the day already exists for this trainer
                    cur.execute("SELECT * FROM schedule WHERE trainerID = %s AND day = %s", (trainerID,dayWhen))
                    if cur.fetchone() is not None:
                        print("\nAvailability has already been made for that day, please update the existing availability.")
                        break
                    else:
                        timeStart = input("Please input a time to start on that day in the format hh:mm:ss (24-hour clock):\n")
                        timeEnd = input("Please input a time to end on that day in the format hh:mm::ss (24-hour clock)\n")
                        startObject = datetime.strptime(timeStart, '%H:%M:%S')
                        endObject = datetime.strptime(timeEnd, '%H:%M:%S')
                        # cur.execute("INSERT INTO exerciseRoutine (name, repetitions, memberID) VALUES (%s, %s, %s)",
                            # (exercise_name, repetitions, memberID))
                        cur.execute("INSERT INTO schedule (trainerID,day,timeStart,timeEnd) VALUES (%s,%s,%s,%s)",
                                    (trainerID, dayWhen,startObject.time(),endObject.time()))
                        print("\nAvailability has been made!\n")
                        con = input("\nWould you like to make more availability? Yes (1) or No (2)\n")
                        if con == "2":
                            db.commit()
                            break
                        else:
                            db.commit()
            elif choice == "2":
                while True:
                    # Update Existing Availability
                    dayWhen = str(input("Please select a day that you want to update (Must be Capitalized):\n"))
                    cur.execute("SELECT * FROM schedule WHERE trainerID = %s AND day = %s", (trainerID,dayWhen))
                    #check if exists first
                    if cur.fetchone() is None:
                        print("\nYou have not yet created that day yet, please create it first.")
                        break
                    timeStart = input("Please input a new start time for that day in the format hh:mm:ss (24-hour clock):\n")
                    timeEnd = input("Please input a new end time for that day in the format hh:mm::ss (24-hour clock)\n")
                    startObject = datetime.strptime(timeStart, '%H:%M:%S')
                    endObject = datetime.strptime(timeEnd, '%H:%M:%S')
                    cur.execute("UPDATE schedule SET timeStart = %s, timeEnd = %s WHERE trainerID = %s AND day = %s",
                                (startObject.time(), endObject.time(), trainerID, dayWhen))
                    print("Availability has been updated!")
                    db.commit()
                    con = input("Would you like to update any others? (1) Yes or (2) No\n")
                    if con == "2":
                        db.commit()
                        break
                    else:
                        db.commit()
            elif choice == "3":
                # See your current available Days
                cur.execute("SELECT day, timeStart, timeEnd FROM schedule WHERE trainerID = %s ORDER BY day",(trainerID,))
                print("\nYour current available days are:\n")
                for row in cur:
                    print(f"Day: {row[0]}, Start Time: {row[1]}, End Time: {row[2]}")
                break
            elif choice == "4":
                print("\nExiting Dashboard...")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")
        except ValueError:
            print("Please enter in the proper format.")
            db.rollback()
        
def viewMember():
    #vars for storing data
    col_names = []
    data_rows = []
    print("Welcome to the member search!\n")
    while True:
        #get names of member for searching
        memberFirstName = input("Please enter the first name of the member:\n")
        memberLastName = input("Please enter the last name of the member:\n")
        cur.execute("SELECT * FROM member WHERE fName = %s AND lName = %s", 
                    (memberFirstName,memberLastName))
        #check if member exists first
        data_rows = [] #make sure to clear data before append new data
        for row in cur:
            data_rows.append(row)
        if len(data_rows) == 0:
            print("\nThere does not exists a member with those names")
            break
        else:
            #get the names
            print(f"\nHere is the member data for {memberFirstName} {memberLastName}:\n")
            col_names = ([desc[0] for desc in cur.description])
            # get data and print
            for data in col_names:
                print(f"{data}: {data_rows[0][col_names.index(data)]}")

        #ask for continuation
        choice = input("\nWould you like to look up another member? (1) Yes or (2) No\n")
        if choice == "2":
            break
        else:
            pass

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
                    memberMenuChoice = memberMenu()
                    #keep updating current member ID that is logged in
                    if memberMenuChoice == "1":
                        profileMenu(currentMemberID)
                    elif memberMenuChoice == "2":
                        dashBoardDisplay(currentMemberID)
                    elif memberMenuChoice == "3":
                        choice = memberScheduleMenu(currentMemberID)
                        memberSchedule(currentMemberID,choice) 
                    elif memberMenuChoice == "4":
                        print("\nExiting....")
                        db.commit()
                        cur.close()
                        db.close()
                        quit()
                    db.commit()
    
            #login is a trainer
            elif logInType == "2":
                trainer = trainerLogin()

                #check if error occured on login
                if trainer[2] == False:
                    main()
                
                #store trainerID from return value
                currentTrainerID = trainer[2]

                while True:
                    try: 
                        trainerMenuChoice = trainerMenu() 
                        if trainerMenuChoice == "1":
                            scheduleMenu(currentTrainerID)
                        elif trainerMenuChoice == "2":
                            viewMember()
                        elif trainerMenuChoice == "3":
                            updateTrainerName(currentTrainerID)
                        elif trainerMenuChoice == "4":
                            print("Exiting.")
                            db.commit()
                            cur.close()
                            db.close()
                            quit()
                        db.commit()
                    except ValueError:
                        print("Please enter valid input.")
            #login is an admin
            elif logInType == "3":
                adminMenu()
            elif logInType == "4":
                print("Quitting the system...")
                quit()
        except ValueError:
            print("please enter right type")
        except psycopg.errors.InvalidTextRepresentation as f:
            print("\nPlease enter the proper format.\n")
            db.rollback()
        break

    

    

if __name__ == "__main__":
    main()