create table trainer 
    (trainerID      serial UNIQUE not null, 
     username       varchar(255) UNIQUE not null, 
     password       varchar(255) UNIQUE not null,
     name           varchar(255),
     primary key (trainerID)
    );
	
create table member 
    (memberID      serial UNIQUE not null, 
     username       varchar(18) UNIQUE not null, 
     password       varchar(18) UNIQUE not null,
     fName           varchar(255) ,
     lName          varchar(255),
     email          varchar(255) ,
     height         numeric CHECK (height > 0),
     weight         numeric CHECK (weight > 0),
     age            integer CHECK (age > 0), 
     weightGoal     numeric CHECK (weightGoal > 0),
     lapTime        numeric CHECK (lapTime > 0),
     lapTimeGoal        numeric CHECK (lapTimeGoal > 0),
     benchMax        numeric CHECK (benchMax > 0),
     benchMaxGoal       numeric CHECK (benchMaxGoal > 0),
     squatMax       numeric CHECK (squatMax > 0),
     squatMaxGoal        numeric CHECK (squatMaxGoal > 0),
     restingHeartRate   numeric CHECK (restingHeartRate >= 40 AND restingHeartRate <= 110), 
     bmi            numeric CHECK (bmi > 0),
     primary key (memberID)
    );

create table room
    (roomID serial UNIQUE not null,
     eventName varchar(255),
     eventStart time CHECK (timeStart > '00:00:00' and timeStart < '24:00:00'),
     eventEnd time CHECK (timeStart > '00:00:00' and timeStart < '24:00:00'),
     capacity integer CHECK (capacity > 0),
     CID integer,
     primary key (roomID)
     foreign key (CID) references class (CID)
        on delete set null
    );    
	
create table session
    (SID        integer UNIQUE not null,
     trainerID  integer not null,
     memberID   integer not null,
     day        integer CHECK (day > 0 and day < 32), 
     timeStart  time CHECK (timeStart > '00:00:00' and timeStart < '24:00:00'),
     timeEnd    time CHECK (timeEnd > '00:00:00' and timeEnd < '24:00:00'), 
     roomID     integer, 
     primary key (SID, trainerID),
     foreign key (trainerID) references trainer (trainerID)
        on delete cascade,
     foreign key (memberID) references member (memberID)
        on delete cascade,
     foreign key (roomID) references room (roomID)
        on delete cascade
    );	

create table schedule 
    (trainerID integer not null, 
     day        varchar(9) CHECK (day IN ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')),
     timeStart  time CHECK (timeStart > '00:00:00' and timeStart < '24:00:00'),
     timeEnd    time CHECK (timeEnd > '00:00:00' and timeEnd < '24:00:00'),
     foreign key (trainerID) references trainer (trainerID)
        on delete set cascade
    );    


create table opens 
    (SID        integer,
     trainerID  integer,
     primary key (SID, trainerID),
     foreign key (SID) references session (SID)
        on delete set null,
     foreign key (trainerID) references trainer (trainerID)
        on delete set null
    );

create table registers 
    (SID        integer,
     memberID  integer,
     primary key (SID, memberID),
     foreign key (SID) references session (SID)
        on delete set null,
     foreign key (memberID) references member (memberID)
        on delete set null
    );
    
create table exerciseRoutine 
    (routineID serial UNIQUE not null,
     name       varchar(255),
     memberID integer not null,
     repetitions integer CHECK (repetitions > 0),
     primary key (routineID),
     foreign key (memberID) references member (memberID)
        on delete cascade       
    );

create table class 
    (CID        integer UNIQUE not null,
     day        date,
     timeStart  time CHECK (timeStart > '00:00:00' and timeStart < '24:00:00'),
     timeEnd    time CHECK (timeEnd > '00:00:00' and timeEnd < '24:00:00'), 
     classExercise  integer UNIQUE,
     memberID integer,
     trainerID integer UNIQUE,
     roomID     integer,
     primary key (CID),
     foreign key (classExercise) references exerciseRoutine (routineID)
        on delete set null,
     foreign key (roomID) references room (roomID)
        on delete cascade,
     foreign key (memberID) references member (memberID)
        on delete cascade,
     foreign key (trainerID) references trainer (trainerID)
    );

create table memberClass
    (CID        integer,
     memberID        integer,
     primary key (CID, memberID),
     foreign key (CID) references class (CID)
        on delete set null
    foreign key (memberID) references member (memberID)
    );
    
