import mysql.connector
import sys
from hashlib import md5
from . import errno

def noDBConn(username: str, password: str, host: str, port: int):
    try:
        tempDBConn = mysql.connector.connect(user = username, password = password, host = host, port = port)
    except Exception as e:
        print("[-] Unable to connect to database.\n" + str(e))
        sys.exit(errno.DB_CONN_ERROR)
    return tempDBConn


def createDB(Conn: mysql.connector.MySQLConnection):
    cursor = Conn.cursor()
    cursor.execute("SHOW DATABASES;")
    if ("ticket_sys", ) in cursor:
        print("[+] Drop the old database and create a new one.")
        try:
            cursor.execute("DROP DATABASE ticket_sys;")
        except Exception as e:
            print("[-] Drop database failed.\n" + str(e))
            sys.exit(errno.DB_DROP_FAILED)
    try:
        cursor.execute("CREATE DATABASE ticket_sys;")
    except Exception as e:
        print("[-] Create database failed.\n" + str(e))
        sys.exit(errno.DB_CREATE_FAILED)


def createTable(Conn: mysql.connector.MySQLConnection, admin: dict):
    cursor = Conn.cursor(buffered = True)
    try:
        cursor.execute("USE ticket_sys;")
        cursor.execute("""
            CREATE TABLE `user`(
                `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                `gid` INT,
                `username` CHAR(20) NOT NULL,
                `password` CHAR(32) NOT NULL,
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
        Conn.commit()
        for i in admin:
            cursor.execute("""
                INSERT INTO user(`gid`, `username`, `password`, `is_admin`) VALUES
                (NULL, %s, MD5(%s), 1);
            """, (i, admin[i]))
        Conn.commit()
    except Exception as e:
        print("[-] Create tables error.\n" + str(e))
        sys.exit(errno.TABLE_CREATE_FAILED)
    finally:
        cursor.close()
        Conn.close()
