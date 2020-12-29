import mysql.connector
import sys
from . import errno

def connectDB(username: str, password: str, host: str, port: int, dbname: str):
    try:
        dbConn = mysql.connector.connect(user = username, password = password, host = host, port = port, database = dbname)
    except Exception:
        print("Unable to connect to database.")
        sys.exit(errno.DB_CONN_ERROR)
    return dbConn

def createUser(): 
    pass

