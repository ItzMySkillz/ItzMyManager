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

# Variable de l'application
app = Flask(__name__)
Mobility(app)


# Chargement du fichier config.ini et du contenu
config_object = ConfigParser()
config_object.read("config.ini")
sql_server = config_object["SQL_SERVER"]
app_information = config_object["APP_INFORMATION"]
UPLOAD_FOLDER = app_information["upload_folder"]

# Code secret de l'application    
app.secret_key = app_information["secret_password"]

# Détail de la base de donée
app.config['MYSQL_HOST'] = sql_server["host"]
app.config['MYSQL_USER'] = sql_server["user"]
app.config['MYSQL_PASSWORD'] = sql_server["password"]
app.config['MYSQL_DB'] = sql_server["database"]


mysql.init_app(app)

# Ajout du chemin d'accès pour les photo de profil
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Importation et chargement de la partie connexion avec blueprint
from app_file.auth import Fauth as Fauth_blueprint
app.register_blueprint(Fauth_blueprint)

# Importation et chargement de la partie ticket avec blueprint
from app_file.ticket import Fticket as Fticket_blueprint
app.register_blueprint(Fticket_blueprint)

# Importation et chargement de la profile connexion avec blueprint
from app_file.profile import Fprofile as Fprofile_blueprint
app.register_blueprint(Fprofile_blueprint)

# Importation et chargement de la partie erreur avec blueprint
from app_file.erreur import Ferreur as Ferreur_blueprint
app.register_blueprint(Ferreur_blueprint)

# Importation et chargement de la partie accueil avec blueprint
from app_file.home import Fhome as Fhome_blueprint
app.register_blueprint(Fhome_blueprint)

# Creation de l'application ( developpement )
if __name__ =='__main__':
    app.run(Debug=True)