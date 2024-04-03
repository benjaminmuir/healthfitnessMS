create table trainer 
    (trainerID      serial UNIQUE not null, 
     username       varchar(18) UNIQUE not null, 
     password       varchar(18) UNIQUE not null,
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
     height         integer ,
     weight         integer ,
     age            integer , 
     weightGoal     integer,
     lapTime        integer,
     averageHeartRate   numeric, 
     bloodOxygen        numeric, 
     primary key (memberID)
    );
	
create table session
    (SID        integer UNIQUE not null,
     trainerID  integer not null,
     day        integer, 
     timeStart  time,
     timeEnd    time, 
     memberID   integer,
     primary key (SID, trainerID),
     foreign key (trainerID) references trainer (trainerID)
        on delete set null,
     foreign key (memberID) references member (memberID)
    );	

create table schedule 
    (trainerID integer not null, 
     day        varchar(9),
     foreign key (trainerID) references trainer (trainerID)
    );    


create table opens 
    (SID        integer,
     trainerID  integer,
     primary key (SID),
     foreign key (SID) references session (SID)
        on delete set null,
     foreign key (trainerID) references trainer (trainerID)
        on delete set null
    );

create table registers 
    (SID        integer,
     memberID  integer,
     primary key (SID),
     foreign key (SID) references session (SID)
        on delete set null,
     foreign key (memberID) references member (memberID)
        on delete set null
    );
    
create table exerciseRoutine 
    (name       varchar(255),
     repetitions integer,
     primary key (name)       
    );

create table class 
    (CID        integer UNIQUE not null,
     day        date,
     timeStart  time,
     timeEnd    time, 
     classExercise  varchar(255),
     primary key (CID),
     foreign key (classExercise) references exerciseRoutine (name)
        on delete set null
    );


    
    
