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
from pythonping import ping

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
                cursor.execute('INSERT INTO printer VALUES (NULL, %s, %s, %s, %s)', (name, ip, location,"down"))
                mysql.connection.commit()
                flash("Votre imprimante à été ajouté avec succès", "success")

        elif request.method == 'POST':
            # Affiche un message si le formulaire est incomplet
            flash("Remplissez le formulaire !", "danger")

        return render_template('home/add_printer.html', username=session['username'], title="Imprimante")
    
    # Si l'utilisateur n'est pas connecté, redirige vers la page de connexion
    return redirect(url_for('Fauth.login'))


# Route pour la page de tout profile de l'employer
@Fdevice.route('/device', methods=['GET', 'POST'])
def device():

    # Vérifie si l'utilisateur est connecté en vérifiant la valeur de la clé 'loggedin' dans le dictionnaire de session
    if session['loggedin'] == True :

        # Récupère l'ID de l'utilisateur à partir de la requête
        deivce_id = request.values.get("device_id")
        device_id_args = request.args.get("device_id")
        print(device_id_args)

        # Crée un curseur pour une connexion MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Exécute une requête pour sélectionner l'entrée de la table 'employee' correspondant à l'ID de l'utilisateur
        cursor.execute('SELECT * FROM device WHERE ID = %s', [device_id_args])

        # Récupère les résultats de la requête
        device = cursor.fetchone()

        device_ram_prct1 = 100 * float(device['ram_us'])/float(device['ram_tot'])
        device_disk_prct1 = 100 * float(device['disk_us'])/float(device['disk_tot'])
        device_disk_prct = round(device_disk_prct1, 1)
        device_ram_prct = round(device_ram_prct1, 1)
        
        # Rend la template "other_profile.html" avec les arguments appropriés
        return render_template('home/device.html', username=session['username'], title="Post de travail", device=device, device_ram=device_ram_prct, device_disk=device_disk_prct) 

    # Si l'utilisateur n'est pas connecté, redirige vers la page de connexion
    return redirect(url_for('Fauth.login'))


# Route pour la page d'affichage des posts de travaille
@Fdevice.route('/devices', methods=['GET', 'POST'])
def devices():
    # Vérifie si l'utilisateur est connecté en vérifiant la valeur de la clé 'loggedin' dans le dictionnaire de session
    if session['loggedin'] == True :
        # Crée un curseur pour une connexion MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            
        cursor.execute( "SELECT * FROM device")
        all_device = cursor.fetchall()

        return render_template('home/devices.html', username=session['username'], title="Post de travaille", all_device = all_device)
    
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
        printers = cursor.fetchall()

        for printer in printers:
            resp = ping(printer['ip'], count=1)

            if resp.success():
                print("up")
                cursor.execute('UPDATE printer SET ping = %s WHERE ip = %s', ("up", printer['ip']))
                mysql.connection.commit()
            else:
                print("down")
                cursor.execute('UPDATE printer SET ping = %s WHERE ip = %s', ("down", printer['ip']))
                mysql.connection.commit()
            
        cursor.execute( "SELECT * FROM printer")
        all_printers = cursor.fetchall()
        


        return render_template('home/printers.html', username=session['username'], title="Imprimante", all_printers = all_printers)
    
    # Si l'utilisateur n'est pas connecté, redirige vers la page de connexion
    return redirect(url_for('Fauth.login'))