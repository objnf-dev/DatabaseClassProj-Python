from flask import Flask
import mysql.connector
import yaml


app = Flask(__name__)
app.secret_key = b'Fzr2lfT#I^x%2NgD80S!fK&oxvf@rU3R'

import ticket

def readConf():
    f = open("config.yaml", "r")
    fileData = yaml.load(f)
    f.close()
    return fileData


if __name__ == '__main__':
    config = readConf()
    app.run(port = config['Web']['port'])