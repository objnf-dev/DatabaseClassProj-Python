from flask import Flask
import yaml
import sys
import errno
from utils import database
from routes import *


app = Flask(__name__)
app.secret_key = b'Fzr2lfT#I^x%2NgD80S!fK&oxvf@rU3R'

app.register_blueprint(routes)

def readConf():
    try:
        f = open("config.yaml", "r")
        fileData = yaml.load(f)
        f.close()
    except Exception:
        print("Failed to read configuration.")
        sys.exit(errno.CONF_READ_ERROR)
    return fileData


if __name__ == '__main__':
    config = readConf()
    dbConn = database.connectDB(config["Database"]["username"], config["Database"]["password"], config["Database"]["host"], 
        config["Database"]["port"], config["Database"]["dbname"])
    try:
        app.run(port = config['Web']['port'])
    except Exception:
        print("Failed to start web server.")
        sys.exit(errno.APP_START_ERROR)