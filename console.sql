CREATE DATABASE ticket_sys;

USE ticket_sys;

CREATE TABLE `user`(
    `username` CHAR(20) NOT NULL PRIMARY KEY,
    `password` CHAR(32) NOT NULL,
    `gid` INT,
    `is_admin` TINYINT(1) NOT NULL
);

CREATE TABLE `train`(
    `train_name` CHAR(10) NOT NULL PRIMARY KEY,
    `start_station` CHAR(10) NOT NULL,
    `start_time` DATETIME NOT NULL,
    `stop_station` CHAR(10) NOT NULL,
    `stop_time` DATETIME NOT NULL,
    `capacity` INT NOT NULL,
    `price` FLOAT NOT NULL CHECK(price >= 0.0)
);

CREATE TRIGGER `check_train` BEFORE INSERT ON `train` FOR EACH ROW
BEGIN 
		IF NEW.start_time < SYSDATE() or NEW.stop_time <= NEW.start_time THEN 
				SIGNAL SQLSTATE 'HY000' SET MESSAGE_TEXT = 'Train time error.';
		END IF;
END;

CREATE TABLE `order`(
    `oid` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` CHAR(20) NOT NULL,
    FOREIGN KEY (`username`) REFERENCES user(`username`),
    `train` CHAR(10) NOT NULL,
    FOREIGN KEY (`train`) REFERENCES train(`train_name`),
    `gid` INT,
    `status` TINYINT(1) NOT NULL
);

CREATE TRIGGER `check_order` BEFORE INSERT ON `order` FOR EACH ROW
BEGIN 
    IF NEW.gid IS NOT NULL and NEW.gid NOT IN (SELECT DISTINCT `gid` from `user`) THEN
        SIGNAL SQLSTATE 'HY000' SET MESSAGE_TEXT = 'Order group info error.';
    END IF;
END;


INSERT INTO user(`username`, `password`,`gid`, `is_admin`) VALUES ('superuser', 'test1234', NULL, 1)