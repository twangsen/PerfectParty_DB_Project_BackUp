-- Initialize the database.
-- Drop any existing data and create tables.

DROP DATABASE IF EXISTS perfectparty;
CREATE DATABASE perfectparty;
\connect perfectparty;

create table Client(
	ClientID SERIAL primary key,
	ClientFirstName varchar(20) not null,
    ClientLastName varchar(20),
    ClientPassword varchar(20) not null,
    ClientEmail varchar(30)
);

INSERT INTO Client (ClientFirstName, ClientLastName, ClientPassword, ClientEmail)
VALUES ('Stephen', 'D''Souza', 'test1', 'test01@gmail.com'),
    ('Su', 'Liang', 'test2', 'user2@gmail.com'),
    ('terry', 'Park', 'test3', 'test3@hotmail.com'),
    ('Deric', 'Zhang', 'test4', 'test4@uwaterloo.ca'),
    ('Peter', 'Reissne', 'test5', 'user5@uwaterloo.ca'),
    ('Alex', 'Sergee', 'test6', 'test06@gmail.com'),
    ( 'Kevin', 'Gao', 'test7', 'test07@qq.com'),
    ('Mike', 'Sande', 'test8', 'user8@uwaterloo.ca'),
    ( 'Brian', 'Stonehouse', 'test9', 'test9@hotmail.com'),
    ('Madison', 'Akins', 'test10', 'test10@gmail.com'),
    ('Too', 'Hana', 'test11', 'test11@gmail.com'),
    ('Tina', 'Wong', 'test12', 'test12@hotmail.com'),
    ('Blaine', 'Jamison', 'test13', 'user13@jamison.com'),
    ('Nick', 'Berci', 'test14', 'user14@berci.com'),
    ('Doris', 'Lin', 'test15', 'test15@lin.com');

create table Location(
	LocationID SERIAL
    primary key,
	StreetAddress varchar(100),
	ApartmentNumber varchar(20) default NULL,
	City varchar(50),
	State varchar(25),
	ZipCode varchar(10),
	Capacity  integer,
	constraint capacity_check check(Capacity >= 1 and Capacity <= 100000),
	LocationType varchar(20)
);

Insert INTO Location (StreetAddress, ApartmentNumber, City, State, ZipCode, Capacity, LocationType)
VALUES ('Phillip Street', '100', 'Montreal', 'QC', 'K2L S1E', 80000, 'Stadium'),
    ('Spadina Avenue', '88', 'Toronto', 'ON', 'M5T 4A6', 7000, 'Hall'),
    ('Eglinton Avenue', '1', 'Toronto', 'ON', 'M4T 7B1', 10000, 'Stadium'),
    ('Sunview Drive', '120', 'Waterloo', 'ON', 'N2L 0E1', 5000, 'Hall'),
    ('Bay Street', '1', 'Vancouver', 'BC', 'J2K 4V7', 10000, 'Stadium'),
    ('James Street', '788', 'Toronto', 'ON', 'M8N 0B2', 9500, 'Stadium'),
    ('Carton Avenue', '1008', 'Hamilton', 'ON', 'L7N 1C2', 6800, 'Hall');

create table Event (
	EventID SERIAL
    primary key,
	ClientID int,
	LocationID int,
    Budget decimal(9,2),
    StartDate timestamp,
    EndDate timestamp,
    EventType varchar(20),
    Organizer varchar(20),
    foreign key (ClientID) references Client (ClientID),
    foreign key (LocationID) references Location (LocationID)
);

Insert INTO Event (ClientID, LocationID, Budget, StartDate, EndDate, EventType, Organizer)
VALUES (3, 2, 4300000.00, '2019-08-12 10:30:30', '2019-08-12 19:30:30', 'Wedding', 'Organizer A'),
    (1, 3, 1200000.00, '2019-08-12 16:30:00', '2019-08-12 21:00:00', 'Celebration', 'Organizer B'),
    (5, 3, 2170000.00, '2019-08-14 17:38:30', '2019-08-14 21:40:00', 'Dinner', 'Organizer C'),
    (2, 6, 1782000.00, '2019-07-30 11:40:00', '2019-07-30 14:10:00', 'Dinner', 'Organizer D'),
    (6, 1, 2000000.00, '2019-07-27 14:25:00', '2019-07-30 17:00:00', 'Wedding', 'Organizer E'),
    (4, 3, 3160000.00, '2019-09-16 09:20:00', '2019-09-16 13:26:55', 'Celebration', 'Organizer F'),
    (3, 2, 2950000.00, '2019-08-13 10:30:00', '2019-08-13 21:38:41', 'Celebration', 'Organizer A'),
    (2, 4, 1486000.00, '2019-08-13 09:45:00', '2019-08-15 12:35:00', 'Wedding', 'Organizer D'),
    (3, 2, 3330000.00, '2019-10-12 11:00:00', '2019-10-12 13:05:32', 'Celebration', 'Organizer A'),
    (8, 5, 1001000.00, '2019-11-02 12:10:00', '2019-11-02 15:45:00', 'Wedding', 'Organizer G'),
    (5, 3, 7100000.00, '2019-08-15 14:50:00', '2019-08-15 23:27:22', 'Dinner', 'Organizer C'),
    (5, 1, 2390000.00, '2019-09-03 10:30:00', '2019-09-03 12:30:00', 'Dinner', 'Organizer C'),
    (3, 4, 2700000.00, '2019-09-16 11:00:00', '2019-09-17 14:15:04', 'Celebration', 'Organizer A'),
    (14, 6, 3120000.00, '2019-12-31 11:35:00', '2019-12-31 22:25:30', 'Wedding', 'Organizer H'),
    (3, 5, 1600000.00, '2020-01-02 09:10:00', '2020-01-03 08:00:00', 'Dinner', 'Organizer A'),
    (12, 2, 9100020.00, '2012-01-16 10:50:00', '2012-01-20 09:00:45', 'Celebration', 'Organizer J');

create table Supplier(
	SupplierID SERIAL primary key,
	Price int,
	SupplierType varchar(10) not null
);

Insert INTO Supplier (Price, SupplierType)
VALUES (12,'Catering'),
    (170,'Decor'),
    (26,'Catering'),
    (10,'Catering'),
    (3290,'Entertain'),
    (341,'Entertain'),
    (23,'Catering'),
    (65,'Decor'),
    (566,'Entertain'),
    (420,'Entertain'),
    (71,'Decor');


create table Catering(
	SupplierID int
    primary key references Supplier(SupplierID),
	CateringName varchar(10),
	CateringType varchar(10)
);

Insert INTO Catering (SupplierID, CateringName, CateringType)
VALUES (1, 'Cake', 'dessert'),
    (3, 'Lobster', 'main'),
    (4, 'Coco', 'drink'),
    (7, 'Crab', 'main');

create table Decor(
	SupplierID int
    primary key references Supplier(SupplierID),
    DecorName varchar(10),
    DecorType varchar(10)
);

Insert INTO Decor (SupplierID, DecorName, DecorType)
VALUES (2, 'Rose', 'Flower'),
    (8, 'Table', 'Furniture'),
    (11, 'Chair', 'Furniture');


create table Entertain(
	SupplierID int
 	primary key references Supplier(SupplierID),
 	EntertainName varchar(20),
	EntertainType varchar(20)
);

INSERT INTO Entertain (SupplierID, EntertainName, EntertainType)
VALUES (5, 'Sing', 'Sing 1'),
    (6, 'Magic', 'Magic Show 1'),
    (9, 'Sing', 'Sing 2'),
    (10, 'Action Show', 'Action Show 1');

create table Supply(
	SupplierID int,
	EventID int,
	Amount INT,
    foreign key (SupplierID) references Supplier (SupplierID),
    foreign key (EventID) references Event (EventID)
);

INSERT INTO Supply (SupplierID, EventID, Amount)
VALUES (4, 1,1000),
(2, 1, 2000),
(6, 1, 3000),
(10, 1, 2352),
(1, 2, 561),
(4, 3, 152),
(3, 3, 123),
(8, 3, 5900),
(2, 3, 3200),
(6, 4, 760),
(3, 5, 1200),
(1, 6, 322),
(8, 6, 1600),
(2, 7, 2130),
(5, 7, 340),
(8, 7, 1232),
(4, 8, 510),
(7, 8, 520),
(6, 9, 3120),
(1, 9, 219),
(11, 9, 320),
(11, 10, 4440),
(9, 11, 2121),
(2, 11, 3410),
(7, 11, 2390),
(11, 12, 480),
(10, 13, 4850),
(4, 14, 4840);
