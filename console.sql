CREATE DATABASE ticket_sys;

USE ticket_sys;

CREATE TABLE `user`(
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `gid` INT,
    `username` CHAR(20) NOT NULL,
    `password` CHAR(60) NOT NULL,
    `is_admin` TINYINT(1) NOT NULL
);

CREATE TABLE `train`(
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `train_name` CHAR(10) NOT NULL,
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
				SIGNAL SQLSTATE "HY000" SET MESSAGE_TEXT = "Train time error.";
		END IF;
END;

CREATE TABLE `order`(
    `oid` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `uid` INT NOT NULL,
    FOREIGN KEY (`uid`) REFERENCES user(`id`),
    `gid` INT,
    `status` TINYINT(1) NOT NULL
);

CREATE TRIGGER `check_order` BEFORE INSERT ON `order` FOR EACH ROW
BEGIN 
    IF NEW.gid != NULL and NEW.gid NOT IN (SELECT DISTINCT `gid` from `user`) THEN
        SIGNAL SQLSTATE "HY000" SET MESSAGE_TEXT = "Order group info error.";
    END IF;
END;
