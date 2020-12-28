import mysql.connector
import sys
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
    dbList = cursor().execute("SHOW DATABASES;")
    if tableName in dbList:
        print("[+] Drop the old database and create a new one.")
        try:
            cursor().execute("DROP DATABASE %s", (tableName, ))
        except Exception:
            print("Drop database failed.")
            sys.exit(errno.DB_DROP_FAILED)
    try:
        cursor.execute("CREATE DATABASE %s", (tableName, ))
    except Exception:
        print("Create database failed.")
        sys.exit(errno.DB_CREATE_FAILED)


def createTable(Conn: mysql.connector.MySQLConnection):
    pass