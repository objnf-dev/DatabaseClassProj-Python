import mysql.connector
import sys
from . import errno


def noDBConn(username: str, password: str, host: str, port: int):
    try:
        tempDBConn = mysql.connector.connect(user=username, password=password, host=host, port=port)
    except Exception as e:
        print("[-] Unable to connect to database.\n" + str(e))
        sys.exit(errno.DB_CONN_ERROR)
    return tempDBConn


def createDB(Conn: mysql.connector.MySQLConnection):
    cursor = Conn.cursor()
    cursor.execute("SHOW DATABASES;")
    if ("ticket_sys",) in cursor:
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
    cursor = Conn.cursor(buffered=True)
    try:
        cursor.execute("USE ticket_sys;")
        cursor.execute("""
            CREATE TABLE `user`(
                `username` CHAR(20) NOT NULL PRIMARY KEY,
                `password` CHAR(32) NOT NULL,
                `gid` INT,
                `is_admin` TINYINT(1) NOT NULL,
                `balance` FLOAT NOT NULL
            );
        """)
        cursor.execute("""
            CREATE TABLE `train`(
                `train_name` CHAR(10) NOT NULL PRIMARY KEY,
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
                    SIGNAL SQLSTATE 'HY000' SET MESSAGE_TEXT = 'Train time error.';
                END IF;
            END;
        """)
        cursor.execute("""
            CREATE TABLE `order`(
                `oid` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                `username` CHAR(20) NOT NULL,
                FOREIGN KEY (`username`) REFERENCES user(`username`),
                `train` CHAR(10) NOT NULL,
                FOREIGN KEY (`train`) REFERENCES train(`train_name`),
                `gid` INT,
                `price` FLOAT NOT NULL,
                `status` TINYINT(1) NOT NULL
            );
        """)
        cursor.execute("""
            CREATE TRIGGER `check_order` BEFORE INSERT ON `order` FOR EACH ROW
            BEGIN 
                IF NEW.gid IS NOT NULL and NEW.gid NOT IN (SELECT DISTINCT `gid` from `user`) THEN
                    SIGNAL SQLSTATE 'HY000' SET MESSAGE_TEXT = 'Order group info error.';
                END IF;
            END;
        """)
        Conn.commit()
        for i in admin:
            cursor.execute("""
                INSERT INTO user(`username`, `password`, `gid`, `is_admin`, `balance`) VALUES
                (%s, MD5(%s), NULL, 1, 1000.0);
            """, (i, admin[i]))
        Conn.commit()
    except Exception as e:
        print("[-] Create tables error.\n" + str(e))
        sys.exit(errno.TABLE_CREATE_FAILED)
    finally:
        cursor.close()
        Conn.close()
