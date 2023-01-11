from flask import Flask, render_template, request, redirect, url_for, session,flash
from app_file.db import mysql
from flask_mobility import Mobility
import MySQLdb.cursors
import re
import os
import uuid
import hashlib
import random
import string
from configparser import ConfigParser
import time
from datetime import datetime
from time import strftime


app = Flask(__name__)
Mobility(app)

config_object = ConfigParser()
config_object.read("config.ini")

sql_server = config_object["SQL_SERVER"]
app_information = config_object["APP_INFORMATION"]

    # Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = app_information["secret_password"]

    # Enter your database connection details below
app.config['MYSQL_HOST'] = sql_server["host"]
app.config['MYSQL_USER'] = sql_server["user"]
app.config['MYSQL_PASSWORD'] = sql_server["password"]
app.config['MYSQL_DB'] = sql_server["database"]


mysql.init_app(app)

UPLOAD_FOLDER = app_information["upload_folder"]

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from app_file.auth import Fauth as Fauth_blueprint
app.register_blueprint(Fauth_blueprint)

from app_file.ticket import Fticket as Fticket_blueprint
app.register_blueprint(Fticket_blueprint)

from app_file.profile import Fprofile as Fprofile_blueprint
app.register_blueprint(Fprofile_blueprint)

from app_file.erreur import Ferreur as Ferreur_blueprint
app.register_blueprint(Ferreur_blueprint)

from app_file.home import Fhome as Fhome_blueprint
app.register_blueprint(Fhome_blueprint)



if __name__ =='__main__':
    app.run(Debug=True)