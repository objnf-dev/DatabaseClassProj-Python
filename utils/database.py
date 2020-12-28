import mysql.connector
import sys
from . import errno

def connectDB(username, password, host, port, dbname):
    try:
        dbConn = mysql.connector.connect(user = username, password = password, host = host, port = port, dbname = dbname)
    except Exception:
        print("Unable to connect to database.")
        sys.exit(errno.DB_CONN_ERROR)
    return dbConn

