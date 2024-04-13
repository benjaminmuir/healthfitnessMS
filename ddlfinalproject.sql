create table trainer 
    (trainerID      serial UNIQUE not null, 
     username       varchar(255) UNIQUE not null, 
     password       varchar(255) UNIQUE not null,
     name           varchar UNIQUE not null,
     primary key (trainerID)
    );

	
create table member 
    (memberID      serial UNIQUE not null, 
     username       varchar(255) UNIQUE not null, 
     password       varchar(255) UNIQUE not null,
     fName           varchar(255) ,
     lName          varchar(255),
     email          varchar(255) ,
     height         numeric CHECK (height > 0),
     weight         numeric CHECK (weight > 0),
     age            integer CHECK (age > 0), 
     weightGoal     numeric CHECK (weightGoal > 0),
     lapTime        time CHECK (lapTime >= '00:00:00'),
     lapTimeGoal        time CHECK (lapTimeGoal >= '00:00:00'),
     benchMax        numeric CHECK (benchMax > 0),
     benchMaxGoal       numeric CHECK (benchMaxGoal > 0),
     squatMax       numeric CHECK (squatMax > 0),
     squatMaxGoal        numeric CHECK (squatMaxGoal > 0),
     restingHeartRate   numeric CHECK (restingHeartRate >= 40 AND restingHeartRate <= 110), 
     bmi            numeric CHECK (bmi > 0),
     primary key (memberID)
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
    (CID        serial UNIQUE not null,
     day        varchar CHECK (day IN ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')),
     timeStart  time CHECK (timeStart >= '00:00:00' and timeStart <= '23:59:59' and timeStart < timeEnd ),
     timeEnd    time CHECK (timeEnd >= '00:00:00' and timeEnd <= '23:59:59' and timeEnd > timeStart ), 
     classExercise  varchar(255),
     memberID integer,
     trainerID integer not null,
     primary key (CID),
     foreign key (memberID) references member (memberID)
        on delete cascade,
     foreign key (trainerID) references trainer (trainerID)
        on delete cascade
    );

create table room
    (roomID serial UNIQUE not null,
     eventName varchar(255),
     day        varchar CHECK (day IN ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')),
     eventStart time CHECK (eventStart >= '00:00:00' and eventStart <= '23:59:59' and eventStart < eventEnd),
     eventEnd time CHECK (eventEnd >= '00:00:00' and eventEnd <= '23:59:59' and eventEnd > eventStart),
     CID integer,
     primary key (roomID),
     foreign key (CID) references class (CID)
        on delete set null
    );   

create table equipment
    (equipmentID serial UNIQUE not null,
     name varchar not null, 
     monitorStatus boolean not null,
     nextMonitorDate integer,
     primary key (equipmentID) 
    );


create table payment
    (billID serial UNIQUE not null,
     amount numeric CHECK (amount > 0) not null, 
     memberID  integer not null, 
     paid   boolean not null,
     primary key (billID),
     foreign key (memberID) references member (memberID)
        on delete cascade
    );

create table session
    (SID        serial UNIQUE not null,
     trainerID  integer not null,
     memberID   integer not null,
     day        varchar CHECK (day IN ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')), 
     timeStart  time CHECK (timeStart >= '00:00:00' and timeStart <= '23:59:59' and timeStart < timeEnd),
     timeEnd    time CHECK (timeEnd >= '00:00:00' and timeEnd <= '23:59:59' and timeEnd > timeStart), 
     primary key (SID, trainerID),
     foreign key (trainerID) references trainer (trainerID)
        on delete cascade,
     foreign key (memberID) references member (memberID)
        on delete cascade
    );	

create table schedule 
    (trainerID integer not null, 
     day        varchar(9) CHECK (day IN ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')),
     timeStart  time CHECK (timeStart >= '00:00:00' and timeStart <= '23:59:59' and timeStart < timeEnd),
     timeEnd    time CHECK (timeEnd >= '00:00:00' and timeEnd <= '23:59:59' and timeEnd > timeStart),
     foreign key (trainerID) references trainer (trainerID)
        on delete cascade
    );    
    
create table memberClass
    (CID        integer,
     memberID        integer,
     primary key (CID, memberID),
     foreign key (CID) references class (CID)
        on delete cascade,
     foreign key (memberID) references member (memberID)
        on delete cascade
    );
    
