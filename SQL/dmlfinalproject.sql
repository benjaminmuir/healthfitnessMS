-- Insert data into trainer
INSERT INTO trainer (username, password, name) VALUES ('trainer1', 'password1', 'Trainer One');
INSERT INTO trainer (username, password, name) VALUES ('trainer2', 'password2', 'Trainer Two');
INSERT INTO trainer (username, password, name) VALUES ('trainer3', 'password3', 'Trainer Three');

-- Insert data into member
INSERT INTO member (username, password, fName, lName, email, height, weight, age, weightGoal, lapTime, lapTimeGoal, benchMax, benchMaxGoal, squatMax, squatMaxGoal, restingHeartRate) 
VALUES ('member1', 'password1', 'Member', 'One', 'member1@example.com', 1.70, 70, 30, 65, '00:01:39', '00:01:15', 270, 262, 150, 154, 45);
INSERT INTO member (username, password, fName, lName, email, height, weight, age, weightGoal, lapTime, lapTimeGoal, benchMax, benchMaxGoal, squatMax, squatMaxGoal, restingHeartRate) 
VALUES ('member2', 'password2', 'Member', 'Two', 'member2@example.com', 1.63, 65, 35, 75, '00:05:43', '00:05:55', 110, 120, 160, 170, 75);
INSERT INTO member (username, password, fName, lName, email, height, weight, age, weightGoal, lapTime, lapTimeGoal, benchMax, benchMaxGoal, squatMax, squatMaxGoal, restingHeartRate) 
VALUES ('member3', 'password3', 'Member', 'Three', 'member3@example.com', 1.91, 90, 40, 85, '00:03:12', '00:01:32', 120, 130, 190, 180, 80);

-- Insert data into exerciseRoutine
INSERT INTO exerciseRoutine (name, memberID, repetitions) VALUES ('Push Ups', 1, 10);
INSERT INTO exerciseRoutine (name, memberID, repetitions) VALUES ('SitUps', 2, 15);
INSERT INTO exerciseRoutine (name, memberID, repetitions) VALUES ('Lunges', 3, 20);

-- Insert data into class
INSERT INTO class (day, timeStart, timeEnd, classExercise, memberID, trainerID) VALUES ('Monday', '09:00:00', '10:00:00', 'Squats', 1, 1);
INSERT INTO class (day, timeStart, timeEnd, classExercise, memberID, trainerID) VALUES ('Tuesday', '11:00:00', '12:00:00', 'Zumba', 2, 2);
INSERT INTO class (day, timeStart, timeEnd, classExercise, memberID, trainerID) VALUES ('Wednesday', '01:00:00', '03:00:00', 'Gymnastics', 3, 3);

-- Insert data into room
INSERT INTO room (eventName, day, eventStart, eventEnd) VALUES ('Event 1', 'Friday', '01:00:00', '09:00:00');
INSERT INTO room (eventName, day, eventStart, eventEnd) VALUES ('Event 2', 'Tuesday', '10:00:00', '11:00:00');
INSERT INTO room (CID) VALUES (3);

-- Insert data into equipment
INSERT INTO equipment (name, monitorStatus, nextMonitorDate) VALUES ('Push Up Machine', true, 25);
INSERT INTO equipment (name, monitorStatus, nextMonitorDate) VALUES ('Lat Spread Machine', false, 0);
INSERT INTO equipment (name, monitorStatus, nextMonitorDate) VALUES ('Free Weights', true, 36);

-- Insert data into payment
INSERT INTO payment (amount, memberID, paid) VALUES (100, 1, true);
INSERT INTO payment (amount, memberID, paid) VALUES (45, 1, true);
INSERT INTO payment (amount, memberID, paid) VALUES (350, 1, true);
INSERT INTO payment (amount, memberID, paid) VALUES (1000, 1, false);

INSERT INTO payment (amount, memberID, paid) VALUES (200, 2, false);
INSERT INTO payment (amount, memberID, paid) VALUES (32, 1, false);
INSERT INTO payment (amount, memberID, paid) VALUES (1200, 2, true);
INSERT INTO payment (amount, memberID, paid) VALUES (500, 2, true);

INSERT INTO payment (amount, memberID, paid) VALUES (300, 3, true);
INSERT INTO payment (amount, memberID, paid) VALUES (100, 3, true);

-- Insert data into sessions
INSERT INTO session (trainerID, memberID, day, timeStart, timeEnd) VALUES (1, 1, 'Monday', '11:00:00', '15:00:00');
INSERT INTO session (trainerID, memberID, day, timeStart, timeEnd) VALUES (2, 2, 'Tuesday', '13:00:00', '17:00:00');
INSERT INTO session (trainerID, memberID, day, timeStart, timeEnd) VALUES (3, 3, 'Wednesday', '04:00:00', '05:00:00');

-- Insert data into schedules
INSERT INTO schedule (trainerID, day, timeStart, timeEnd) VALUES (1, 'Monday', '09:00:00', '19:00:00');
INSERT INTO schedule (trainerID, day, timeStart, timeEnd) VALUES (1, 'Tuesday', '11:00:00', '15:00:00');
INSERT INTO schedule (trainerID, day, timeStart, timeEnd) VALUES (1, 'Wednesday', '03:00:00', '15:00:00');
INSERT INTO schedule (trainerID, day, timeStart, timeEnd) VALUES (1, 'Thursday', '09:00:00', '17:00:00');

INSERT INTO schedule (trainerID, day, timeStart, timeEnd) VALUES (2, 'Tuesday', '09:00:00', '20:00:00');
INSERT INTO schedule (trainerID, day, timeStart, timeEnd) VALUES (2, 'Saturday', '10:00:00', '19:00:00');

INSERT INTO schedule (trainerID, day, timeStart, timeEnd) VALUES (3, 'Wednesday', '00:00:00', '05:00:00');
INSERT INTO schedule (trainerID, day, timeStart, timeEnd) VALUES (3, 'Friday', '10:30:00', '17:55:00');
INSERT INTO schedule (trainerID, day, timeStart, timeEnd) VALUES (3, 'Sunday', '06:00:00', '10:00:00');

-- Insert data into memberClass
INSERT INTO memberClass (CID, memberID) VALUES (1, 1);
INSERT INTO memberClass (CID, memberID) VALUES (2, 1);

INSERT INTO memberClass (CID, memberID) VALUES (2, 2);
INSERT INTO memberClass (CID, memberID) VALUES (3, 2);

INSERT INTO memberClass (CID, memberID) VALUES (3, 3);
INSERT INTO memberClass (CID, memberID) VALUES (2, 3);
