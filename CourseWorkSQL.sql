CREATE DATABASE spaceMissions;

CREATE TABLE mission
(
	missionNo int NOT NULL PRIMARY KEY,
	agencyNo int FOREIGN KEY REFERENCES agency(agencyNo),
	missionData date,
	equipmentMissionNo int FOREIGN KEY REFERENCES equipmentJunction(equipmentMissionNo),
	totalWeight int
);

CREATE TABLE agency 
(
	agencyNo int NOT NULL PRIMARY KEY,
	leadAgency varchar(255),
	country varchar(255)
);

CREATE TABLE equipmentJunction
(
	equipmentMissionNo int NOT NULL PRIMARY KEY,
	equipmentNo int FOREIGN KEY REFERENCES equipment(equipmentNo)
);

CREATE TABLE equipment
(
	equipmentNo int NOT NULL PRIMARY KEY,
	equipment varchar(255),
	qty int,
	itemWeight int
);

INSERT INTO mission (missionNo,agencyNo,missionData,equipmentMissionNo,totalWeight) VALUES 
	('2237','178','2013-12-14','011','211'),
	('3664','526','16-01-2014','012','1.20'),
	('2356','167','12-02-2014','013','69'),
	('1234','032','16-04-2014','014','2.5');

INSERT INTO agency (agencyNo,leadAgency,country) VALUES	
	('178','JAXA','Japan')
	('526','ESA','EU')
	('167','NASA','USA')
	('032','Roscosmos','Russia');
	
INSERT INTO equipmentJunction (equipmentMissionNo,equipmentNo) VALUES
	('011','001'),
	('011','002'),
	('011','003'),
	('012','004'),
	('013','003'),
	('013','005'),
	('013','006'),
	('013','007'),
	('014','003'),
	('014','002');
	
INSERT INTO equipment (equipmentNo,equipment,qty,itemWeight) VALUES
	('001','Potable water dispenser','2','100'),
	('002','Flexible air duct','6','0.5'),
	('003','Small storage rack','4','2'),
	('004','Bio filter','6','0.20');