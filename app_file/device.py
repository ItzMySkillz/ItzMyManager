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
from blabel import LabelWriter
import qrcode
import qrcode.image.pil

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


# Route pour la page du post de travail séléctionner
@Fdevice.route('/device', methods=['GET', 'POST'])
def device():

    # Vérifie si l'utilisateur est connecté en vérifiant la valeur de la clé 'loggedin' dans le dictionnaire de session
    if session['loggedin'] == True :

        # Récupère l'ID du post de travail à partir de la requête
        deivce_id = request.values.get("device_id")
        device_id_args = request.args.get("device_id")
        print(device_id_args)

        # Crée un curseur pour une connexion MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Exécute une requête pour sélectionner l'entrée de la table 'device' correspondant à l'ID du post de travail
        cursor.execute('SELECT * FROM device WHERE ID = %s', [device_id_args])

        # Récupère les résultats de la requête
        device = cursor.fetchone()

        device_ram_prct1 = 100 * float(device['ram_us'])/float(device['ram_tot'])
        device_disk_prct1 = 100 * float(device['disk_us'])/float(device['disk_tot'])
        device_disk_prct = round(device_disk_prct1, 1)
        device_ram_prct = round(device_ram_prct1, 1)

        qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
        )

        qr.add_data("https://www.itzmyweb.be")
        qr.make(fit=True)
        image = qr.make_image(image_factory=qrcode.image.pil.PilImage)
        image.save("static\\label\\qrcode\\{val}.png".format(val = device['node']))

        label_writer = LabelWriter("templates/label/device.html", default_stylesheets=("static/bootstrap/css/style.css",))
        target = "static\\label\\{val}.pdf".format(val = device['node'])
        qrcodepng = "http://192.168.68.157:5000/device_info?device={val}".format(val = device['node'])
        records = [
            dict(id=device['id'], hote=device['node'],qrcodepng=qrcodepng)
        ]
        label_writer.write_labels(records, target="C:\\Users\\bogda\\Documents\\GitHub\\ItzMyManager\\static\\label\\{val}.pdf".format(val = device['node']))
        
        # Rend la template "device.html" avec les arguments appropriés
        return render_template('home/device.html', username=session['username'], title="Post de travail", device=device, device_ram=device_ram_prct, device_disk=device_disk_prct, target = target, qrcodepng=qrcodepng) 

    # Si l'utilisateur n'est pas connecté, redirige vers la page de connexion
    return redirect(url_for('Fauth.login'))


# Route pour la page d'affichage des posts de travails
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
        all_printers = cursor.fetchall()
        


        return render_template('home/printers.html', username=session['username'], title="Imprimante", all_printers = all_printers)
    
    # Si l'utilisateur n'est pas connecté, redirige vers la page de connexion
    return redirect(url_for('Fauth.login'))

# Route pour la page de l'imprimante séléctionner
@Fdevice.route('/printer', methods=['GET', 'POST'])
def printer():

    # Vérifie si l'utilisateur est connecté en vérifiant la valeur de la clé 'loggedin' dans le dictionnaire de session
    if session['loggedin'] == True :

        # Récupère l'ID de l'imprimante à partir de la requête
        deivce_id = request.values.get("printer_id")
        device_id_args = request.args.get("printer_id")
        print(device_id_args)

        # Crée un curseur pour une connexion MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Exécute une requête pour sélectionner l'entrée de la table 'printer' correspondant à l'ID de l'imprimante
        cursor.execute('SELECT * FROM printer WHERE ID = %s', [device_id_args])

        # Récupère les résultats de la requête
        printer = cursor.fetchone()

        label_writer = LabelWriter("templates/label/device.html", default_stylesheets=("static/bootstrap/css/style.css",))
        records = [
            dict(id=printer['id'], hote=printer['name']),
        ]
        target = "static\\label\\printer\\{val}.pdf".format(val = printer['name'])
        label_writer.write_labels(records, target="C:\\Users\\bogda\\Documents\\GitHub\\ItzMyManager\\static\\label\\printer\\{val}.pdf".format(val = printer['name']))
        
        # Rend la template "printer.html" avec les arguments appropriés
        return render_template('home/printer.html', username=session['username'], title="Imprimante", printer=printer,target = target) 

    # Si l'utilisateur n'est pas connecté, redirige vers la page de connexion
    return redirect(url_for('Fauth.login'))

# Route pour la page d'affichage de l'information de la machine
@Fdevice.route('/device_info', methods=['GET', 'POST'])
def device_info():

    # Récupère l'hote de la machine à partir de la requête
    device = request.values.get("device")
    device_args = request.args.get("device")
    print(device_args)

    # Crée un curseur pour une connexion MySQL
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Exécute une requête pour sélectionner l'entrée de la table 'device' correspondant à l'hote de la machine
    cursor.execute('SELECT * FROM device WHERE node = %s', [device_args])

    # Récupère les résultats de la requête
    device = cursor.fetchone()
        
    # Rend la template "device_info.html" avec les arguments appropriés
    return render_template('home/device_info.html', title="Informations", device=device) 