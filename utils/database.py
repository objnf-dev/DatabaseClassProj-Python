import mysql.connector
import sys
from datetime import datetime
from . import errno


def connectDB(username: str, password: str, host: str, port: int, dbname: str):
    try:
        dbConn = mysql.connector.connect(user = username, password = password, host = host, port = port, database = dbname)
    except Exception as e:
        print("[-] Unable to connect to database.\n" + str(e))
        sys.exit(errno.DB_CONN_ERROR)
    return dbConn


def createUser(Conn: mysql.connector.MySQLConnection, username: str, password: str):
    cursor = Conn.cursor(buffered = True) 
    try: 
        cursor.execute("""
            INSERT INTO user(`username`, `password`, `gid`, `is_admin`) VALUES
            (%s, MD5(%s), NULL, 0);
        """, (username, password))
        Conn.commit()
        Conn.close()
        return True
    except Exception as e:
        print("[-] Add user failed." + str(e))
        Conn.close()
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
        Conn.close()
        return True
    except Exception as e:
        print("[-] Add train failed.\n" + str(e))
        Conn.close()
        return False


def checkLogin(Conn: mysql.connector.MySQLConnection, username: str, password: str):
    cursor = Conn.cursor(buffered = True)
    try:
        cursor.execute("""
            SELECT `password` FROM `user` WHERE `username` = %s;
        """, (username, ))


def queryUser():
    pass


def queryTrainByName():
    pass


def queryTrainByStation():
    pass


def queryTrainByTime():
    pass



