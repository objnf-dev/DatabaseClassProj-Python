import mysql.connector
import sys
from datetime import datetime
from hashlib import md5
from . import errno


def connectDB(username: str, password: str, host: str, port: int, dbname: str):
    try:
        newConn = mysql.connector.connect(user = username, password = password, host = host, port = port, database = dbname)
    except Exception as e:
        print("[-] Unable to connect to database.\n" + str(e))
        sys.exit(errno.DB_CONN_ERROR)
    return newConn


def createUser(Conn: mysql.connector.MySQLConnection, username: str, password: str):
    cursor = Conn.cursor(buffered = True) 
    try: 
        cursor.execute("""
            INSERT INTO user(`username`, `password`, `gid`, `is_admin`) VALUES
            (%s, MD5(%s), NULL, 0);
        """, (username, password))
        Conn.commit()
        cursor.close()
        return True
    except Exception as e:
        print("[-] Add user failed." + str(e))
        cursor.close()
        return False


def createTrain(Conn: mysql.connector.MySQLConnection, trainName: str, startStat: str, 
    startTime: datetime, endStat: str, endTime: datetime, capacity: int, price: float):
    cursor = Conn.cursor(buffered = True)
    try:
        cursor.execute("""
            INSERT INTO train(`train_name`, `start_station`, `start_time`, `stop_station`, 
                `stop_time`, `capacity`, `price`) VALUES
            (%s, %s, %s, %s, %s, %s, %s);
        """, (trainName, startStat, startTime, endStat, endTime, capacity, price))
        Conn.commit()
        cursor.close()
        return True
    except Exception as e:
        print("[-] Add train failed.\n" + str(e))
        cursor.close()
        return False


def checkLogin(Conn: mysql.connector.MySQLConnection, username: str, password: str):
    cursor = Conn.cursor(buffered = True)
    try:
        cursor.execute("""
            SELECT `password` FROM `user` WHERE `username` = %s;
        """, (username, ))
        Conn.commit()
        if md5(password.encode("ascii")).hexdigest() == cursor["password"]:
            print("[+] User {} login successfully.\n".format(username))
            return True
        else:
            return False
    except Exception as e:
        print("[-] Login error.\n" + str(e))
        return False


def queryUser():
    pass


def queryTrainByName():
    pass


def queryTrainByStation():
    pass


def queryTrainByTime():
    pass



