from flask import Flask
import yaml
import sys
import os
import errno
from utils import createDB
from utils.database import connectDB
from routes import *


app = Flask(__name__)
app.secret_key = os.urandom(32)

app.register_blueprint(routes)


def readConf():
    try:
        f = open("config.yaml", "r")
        fileData = yaml.safe_load(f)
        f.close()
    except Exception:
        print("[-] Failed to read configuration.")
        sys.exit(errno.CONF_READ_ERROR)
    return fileData


if __name__ == '__main__':
    config = readConf()
    if not os.path.isfile("install.lock"):
        dbConn = createDB.noDBConn(config["Database"]["username"], config["Database"]["password"], 
            config["Database"]["host"], config["Database"]["port"])
        createDB.createDB(dbConn)
        createDB.createTable(dbConn, config["Admin"])
        with open("install.lock", "w"):
            pass

    dbConn = connectDB(config["Database"]["username"], config["Database"]["password"], config["Database"]["host"], 
        config["Database"]["port"], "ticket_sys")
    try:
        app.run(port = config['Web']['port'])
    except Exception as e:
        print("[-] Failed to start web server.\n" + str(e))
        sys.exit(errno.APP_START_ERROR)
