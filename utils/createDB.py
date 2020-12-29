import mysql.connector
import sys

from mysql.connector import cursor
from . import errno

def noDBConn(username: str, password: str, host: str, port: int):
    try:
        tempDBConn = mysql.connector.connect(username, password, host, port)
    except Exception:
        print("Unable to connect to database.")
        sys.exit(errno.DB_CONN_ERROR)
    return tempDBConn


def createDB(Conn: mysql.connector.MySQLConnection, tableName: str):
    cursor = Conn.cursor()
    dbList = cursor.execute("SHOW DATABASES;")
    if tableName in dbList:
        print("[+] Drop the old database and create a new one.")
        try:
            cursor.execute("DROP DATABASE %s", (tableName, ))
        except Exception:
            print("Drop database failed.")
            sys.exit(errno.DB_DROP_FAILED)
    try:
        cursor.execute("CREATE DATABASE %s", (tableName, ))
    except Exception:
        print("Create database failed.")
        sys.exit(errno.DB_CREATE_FAILED)


def createTable(Conn: mysql.connector.MySQLConnection, tableName: str):
    cursor = Conn.cursor()
    try:
        cursor.execute("USE DATABASE %s;", (tableName, ))
        cursor.execute("""
            CREATE TABLE `user`(
                `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                `gid` INT,
                `username` CHAR(20) NOT NULL,
                `password` CHAR(60) NOT NULL,
                `is_admin` TINYINT(1) NOT NULL
            );
        """)
        cursor.execute("""
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
        """)
        cursor.execute("""
            CREATE TRIGGER `check_train` BEFORE INSERT ON `train` FOR EACH ROW
            BEGIN 
		        IF NEW.start_time < SYSDATE() or NEW.stop_time <= NEW.start_time THEN 
				    SIGNAL SQLSTATE "HY000" SET MESSAGE_TEXT = "Train time error.";
		        END IF;
            END;
        """)
        cursor.execute("""
            CREATE TABLE `order`(
                `oid` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                `uid` INT NOT NULL,
                FOREIGN KEY (`uid`) REFERENCES user(`id`),
                `gid` INT,
                `status` TINYINT(1) NOT NULL
            );
        """)
        cursor.execute("""
            CREATE TRIGGER `check_order` BEFORE INSERT ON `order` FOR EACH ROW
            BEGIN 
                IF NEW.gid != NULL and NEW.gid NOT IN (SELECT DISTINCT `gid` from `user`) THEN
                    SIGNAL SQLSTATE "HY000" SET MESSAGE_TEXT = "Order group info error.";
                END IF;
            END;
        """)
    except Exception:
        print("Create tables error.")
        sys.exit()
