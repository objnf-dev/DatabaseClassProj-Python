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
            INSERT INTO user(`username`, `password`, `gid`, `is_admin`, `is_group_admin`, `balance`) VALUES
            (%s, MD5(%s), NULL, 0, 0, 100.0);
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


def queryAllUser(Conn: mysql.connector.MySQLConnection):
    cursor = Conn.cursor(buffered=True)
    try:
        cursor.execute("""
            SELECT `username` FROM `user` WHERE `is_admin` = 0;
        """)
        Conn.commit()
        res = {}
        num = 0
        for user in cursor:
            num = num + 1
            res[str(num)] = user[0]
        return True, res
    except Exception as e:
        print("[-] User query failed.\n" + str(e))
        return False, None


def queryTrain(Conn: mysql.connector.MySQLConnection, info):
    cursor = Conn.cursor(buffered=True)
    try:
        num = 0
        checkList = ["train_name", "start_station", "stop_station"]
        param = ()
        sql = "SELECT * FROM `train`"
        for item in checkList:
            if item in info:
                if not num:
                    sql += "WHERE `{}` = %s ".format(item)
                else:
                    sql += "AND `{}` = %s ".format(item)
                num = num + 1
                param += (info[item], )
        if "start_time" in info:
            if not num:
                sql += "WHERE `start_time` >= %s "
            else:
                sql += "AND `start_time >= %s "
            param += (info["start_time"], )
        if "stop_time" in info:
            if not num:
                sql += "WHERE `stop_time` <= %s "
            else:
                sql += "AND `stop_time` <= %s "
            param += (info["stop_time"], )
        sql += "ORDER BY `start_time`;"
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


def placeOrder(Conn: mysql.connector.MySQLConnection, username: str, train: str, status: int):
    cursor = Conn.cursor(buffered=True)
    try:
        sql = """
            SET @price = (SELECT `price` FROM `train` WHERE `train_name` = %s);
            SET @remain = (SELECT `balance` FROM `user` WHERE `username` = %s);
        """
        if status:
            sql += "UPDATE `user` SET `price` = @remain - @price;"
        sql += """INSERT INTO `order`(`username`, `train`, `gid`, `price`, `status`) VALUES
                    (%s, %s, NULL, @price, %s);"""
        cursor.execute(sql, (train, username, username, train, status))
        return True
    except Exception as e:
        print("[-] Failed to place order.\n" + str(e))
        return False


def placeGroupOrder(Conn: mysql.connector.MySQLConnection, usernameList: list, train: str, gid: int, status: int):
    pass


def removeOrder(Conn: mysql.connector.MySQLConnection, oid: int, username: str):
    cursor = Conn.cursor(buffered=True)
    try:
        cursor.execute("""
            SET @price = (SELECT `price` FROM `order` WHERE `oid` = %s);
            SET @remain = (SELECT `balance` FROM `user` WHERE `username` = %s);
            SET @capa = (SELECT `capacity` FROM `train` WHERE `train_name` = (SELECT `train` FROM `order` WHERE `oid` = %s));
            UPDATE `user` SET `price` = @remain + @price;
            UPDATE `train` SET `capacity` = @capa + 1;
            DELETE FROM `order` WHERE `oid` = %s;
        """, (oid, username, oid ))
        return True
    except Exception as e:
        print("[-] Delete order failed.\n" + str(e))
        return False


def removeGroupOrder(Conn: mysql.connector.MySQLConnection):
    pass


def payOrder(Conn: mysql.connector.MySQLConnection, oid: int, username: str):
    cursor = Conn.cursor(buffered=True)
    try:
        cursor.execute("""
            SET @price = (SELECT `price` FROM `order` WHERE `oid` = %s);
            SET @remain = (SELECT `balance` FROM `user` WHERE `username` = %s);
            UPDATE `user` SET `price` = @remain - @price;
            UPDATE `order` SET `status` = 1 WHERE `oid` = %s;
        """, (oid, username, oid))
        return True
    except Exception as e:
        print("[-] Pay for order failed.\n" + str(e))
        return False
