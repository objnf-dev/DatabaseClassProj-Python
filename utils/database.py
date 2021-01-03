import mysql.connector
import sys
from datetime import datetime
from hashlib import md5
from . import errno

DBConn = None


def connectDB(username: str, password: str, host: str, port: int, dbname: str):
    try:
        newConn = mysql.connector.connect(user=username, password=password, host=host, port=port, database=dbname)
    except Exception as e:
        print("[-] Unable to connect to database.\n" + str(e))
        sys.exit(errno.DB_CONN_ERROR)
    return newConn


def createUser(Conn: mysql.connector.MySQLConnection, username: str, password: str):
    cursor = Conn.cursor(buffered=True)
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
    cursor = Conn.cursor(buffered=True)
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
    cursor = Conn.cursor(buffered=True)
    try:
        cursor.execute("""
            SELECT `password`, `is_admin` FROM `user` WHERE `username` = %s;
        """, (username,))
        Conn.commit()
        for sqlpwd in cursor:
            if md5(password.encode("ascii")).hexdigest() == sqlpwd[0]:
                print("[+] User {} login successfully.\n".format(username))
                return True, sqlpwd[1]
            else:
                return False, None
    except Exception as e:
        print("[-] Login error.\n" + str(e))
        return False


def checkUserUnique(Conn: mysql.connector.MySQLConnection, username: str):
    cursor = Conn.cursor(buffered=True)
    try:
        cursor.execute("""
            SELECT COUNT(`username`) FROM `user` WHERE `username` = %s;
        """, (username,))
        Conn.commit()
        for count in cursor:
            if int(count[0]):
                return False
            else:
                return True
    except Exception as e:
        print("[-] User not unique.\n" + str(e))
        return False


def queryUser():
    pass


def queryTrain(Conn: mysql.connector.MySQLConnection, info):
    print(info)
    cursor = Conn.cursor(buffered=True)
    try:
        num = 0
        checkList = ["train_name", "start_station", "stop_station"]
        param = ()
        sql = "SELECT * FROM `train` WHERE"
        for item in checkList:
            if item in info:
                if not num:
                    sql += "`{}` = %s".format(item)
                else:
                    sql += "AND `{}` = %s".format(item)
                num = num + 1
                param += (info[item], )
        if "start_time" in info:
            if not num:
                sql += "`start_time` >= %s"
            else:
                sql += "AND `start_time >= %s"
        if "stop_time" in info:
            if not num:
                sql += "`stop_time` <= %s"
            else:
                sql += "AND `stop_time` <= %s"
        sql += ";"
        cursor.execute(sql, param)
        Conn.commit()
        result = {}
        num = 0
        for train in cursor:
            num += 1
            result[str(num)] = train
        return True, result
    except Exception as e:
        print("[-] Check train info error.\n" + str(e))
        return False, None


