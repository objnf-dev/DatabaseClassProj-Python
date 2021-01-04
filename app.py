from flask import Flask
import yaml
import sys
import os
import utils.database, utils.createDB, utils.errno
from routes import *

# App settings
app = Flask(__name__)
# app.secret_key = os.urandom(32)
app.secret_key = "1234"
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.register_blueprint(routes)


# Read configuration file
def readConf():
    try:
        f = open("config.yaml", "r")
        fileData = yaml.safe_load(f)
        f.close()
    except Exception:
        print("[-] Failed to read configuration.")
        sys.exit(utils.errno.CONF_READ_ERROR)
    return fileData


# Start here
if __name__ == '__main__':
    config = readConf()

    # Check install status
    if not os.path.isfile("install.lock"):
        dbConn = utils.createDB.noDBConn(config["Database"]["username"], config["Database"]["password"],
                                         config["Database"]["host"], config["Database"]["port"])
        utils.createDB.createDB(dbConn)
        utils.createDB.createTable(dbConn, config["Admin"])
        with open("install.lock", "w"):
            pass

    # Connect to DB
    utils.database.DBConn = utils.database.connectDB(config["Database"]["username"], config["Database"]["password"],
                                                     config["Database"]["host"],
                                                     config["Database"]["port"], "ticket_sys")

    # Run app
    try:
        app.run(port=config['Web']['port'])
    except Exception as e:
        print("[-] Failed to start web server.\n" + str(e))
        sys.exit(utils.errno.APP_START_ERROR)
