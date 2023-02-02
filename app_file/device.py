from flask import Blueprint, Flask, render_template, request, redirect, url_for, session,flash
from .db import mysql
from flask_mobility import Mobility
import MySQLdb.cursors
import re
import os
import uuid
import hashlib
import random
import string
from configparser import ConfigParser
from .mail_model import *
import time
from datetime import datetime
from time import strftime

Fdevice = Blueprint('Fdevice', __name__)

# Route pour la page d'ajout d'imprimante
@Fdevice.route('/add_printer', methods=['GET', 'POST'])
def add_printer():
    # Vérifie si l'utilisateur est connecté en vérifiant la valeur de la clé 'loggedin' dans le dictionnaire de session
    if session['loggedin'] == True :

        # Si l'utilisateur a soumis un formulaire
        if request.method == 'POST' and 'name' in request.form and 'ip' in request.form and 'location' in request.form:
            name = request.form['name']
            ip = request.form['ip']
            location = request.form['location']

            # Crée un curseur pour une connexion MySQL
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            cursor.execute( "SELECT * FROM printer WHERE ip LIKE %s OR name LIKE %s", (ip, name))
            printer = cursor.fetchone()
            if printer:
                flash("L'imprimante existe déjà!", "danger")
            else:
                cursor.execute('INSERT INTO printer VALUES (NULL, %s, %s, %s)', (name, ip, location))
                mysql.connection.commit()
                flash("Votre imprimante à été ajouté avec succès", "success")

        elif request.method == 'POST':
            # Affiche un message si le formulaire est incomplet
            flash("Remplissez le formulaire !", "danger")

        return render_template('home/add_printer.html', username=session['username'], title="Imprimante")
    
    # Si l'utilisateur n'est pas connecté, redirige vers la page de connexion
    return redirect(url_for('Fauth.login'))


# Route pour la page d'ajout d'imprimante
@Fdevice.route('/printers', methods=['GET', 'POST'])
def printers():
    # Vérifie si l'utilisateur est connecté en vérifiant la valeur de la clé 'loggedin' dans le dictionnaire de session
    if session['loggedin'] == True :
        # Crée un curseur pour une connexion MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute( "SELECT * FROM printer")
        all_printers = cursor.fetchall()

        return render_template('home/printers.html', username=session['username'], title="Imprimante", all_printers = all_printers)
    
    # Si l'utilisateur n'est pas connecté, redirige vers la page de connexion
    return redirect(url_for('Fauth.login'))