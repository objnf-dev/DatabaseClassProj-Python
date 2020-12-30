from flask import Flask
import yaml
import sys
import os
from utils import createDB, errno, DBConn
from utils.database import connectDB
from routes import *

# App settings
app = Flask(__name__)
app.secret_key = os.urandom(32)

app.register_blueprint(routes)


# Read configuration file
def readConf():
    try:
        f = open("config.yaml", "r")
        fileData = yaml.safe_load(f)
        f.close()
    except Exception:
        print("[-] Failed to read configuration.")
        sys.exit(errno.CONF_READ_ERROR)
    return fileData


# Start here
if __name__ == '__main__':
    global DBConn
    config = readConf()

    # Check install status
    if not os.path.isfile("install.lock"):
        dbConn = createDB.noDBConn(config["Database"]["username"], config["Database"]["password"],
                                   config["Database"]["host"], config["Database"]["port"])
        createDB.createDB(dbConn)
        createDB.createTable(dbConn, config["Admin"])
        with open("install.lock", "w"):
            pass

    # Connect to DB
    DBConn = connectDB(config["Database"]["username"], config["Database"]["password"], config["Database"]["host"],
                       config["Database"]["port"], "ticket_sys")

    # Run app
    try:
        app.run(port=config['Web']['port'])
    except Exception as e:
        print("[-] Failed to start web server.\n" + str(e))
        sys.exit(errno.APP_START_ERROR)
