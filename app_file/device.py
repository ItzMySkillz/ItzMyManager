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
import requests
import nmap

Fdevice = Blueprint('Fdevice', __name__)
port = 6446
nmap = nmap.PortScanner()

# Route pour la page d'ajout d'imprimante
@Fdevice.route('/ajout_imprimante', methods=['GET', 'POST'])
def add_printer():
    # Vérifie si l'utilisateur est connecté en vérifiant la valeur de la clé 'loggedin' dans le dictionnaire de session
    if session['loggedin'] == True and session['istech'] == True:

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
@Fdevice.route('/poste', methods=['GET', 'POST'])
def device():

    # Vérifie si l'utilisateur est connecté en vérifiant la valeur de la clé 'loggedin' dans le dictionnaire de session
    if session['loggedin'] == True and session['istech'] == True:

        # Récupère l'ID du post de travail à partir de la requête
        deivce_id = request.values.get("device_id")
        device_id_args = request.args.get("device_id")
        device_refresh = request.args.get("device_refresh", None)
        print(device_id_args)
        

        # Crée un curseur pour une connexion MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Exécute une requête pour sélectionner l'entrée de la table 'device' correspondant à l'ID du post de travail
        cursor.execute('SELECT * FROM device WHERE ID = %s', [device_id_args])

        # Récupère les résultats de la requête
        device = cursor.fetchone()

        if device_refresh == "1":
            requests.get("http://{val}:6446/api/update".format(val = device['ip']))
        else:
            pass

        device_disk_prct1 = 100 * float(device['disk_us'])/float(device['disk_tot'])
        device_disk_prct = round(device_disk_prct1, 1)

        device_ram_prct1 = 100 * float(device['ram_us'])/float(device['ram_tot'])
        device_ram_prct = round(device_ram_prct1, 1)

        qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
        )

        label_writer = LabelWriter("templates/label/device.html", default_stylesheets=("static/bootstrap/css/style.css",))
        target = "static\\label\\{val}.pdf".format(val = device['node'])
        qrcodepng = "panel.itzmyweb.be/info_poste?device={val}".format(host= request.host_url, val = device['node'])
        records = [
            dict(id=device['id'], hote=device['node'], mac=device['mac'], qrcodepng=qrcodepng)
        ]
        label_writer.write_labels(records, target="static\\label\\{val}.pdf".format(val = device['node']))
        
        # Rend la template "device.html" avec les arguments appropriés
        return render_template('home/device.html', username=session['username'], title="Post de travail", device=device, device_disk=device_disk_prct, device_ram=device_ram_prct, target = target, qrcodepng=qrcodepng) 

    # Si l'utilisateur n'est pas connecté, redirige vers la page de connexion
    return redirect(url_for('Fauth.login'))

# Route pour la page du post de travail séléctionner
@Fdevice.route('/server', methods=['GET', 'POST'])
def server():

    # Vérifie si l'utilisateur est connecté en vérifiant la valeur de la clé 'loggedin' dans le dictionnaire de session
    if session['loggedin'] == True and session['istech'] == True:

        # Récupère l'ID du post de travail à partir de la requête
        server_id = request.values.get("server_id")
        server_id_args = request.args.get("server_id")
        server_refresh = request.args.get("server_refresh", None)
        print(server_id_args)
        

        # Crée un curseur pour une connexion MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Exécute une requête pour sélectionner l'entrée de la table 'server' correspondant à l'ID du post de travail
        cursor.execute('SELECT * FROM server WHERE ID = %s', [server_id_args])

        # Récupère les résultats de la requête
        server = cursor.fetchone()

        if server_refresh == "1":
            requests.get("http://{val}:6446/api-caller".format(val = server['ip']))
        else:
            pass

        server_disk_prct1 = 100 * float(server['disk_us'])/float(server['disk_tot'])
        server_disk_prct = round(server_disk_prct1, 1)

        server_ram_prct1 = 100 * float(server['ram_us'])/float(server['ram_tot'])
        server_ram_prct = round(server_ram_prct1, 1)

        qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
        )

        label_writer = LabelWriter("templates/label/device.html", default_stylesheets=("static/bootstrap/css/style.css",))
        target = "static\\label\\{val}.pdf".format(val = server['node'])
        qrcodepng = "panel.itzmyweb.be/info_poste?device={val}".format(host= request.host_url, val = server['node'])
        records = [
            dict(id=server['id'], hote=server['node'], mac=server['mac'], qrcodepng=qrcodepng)
        ]
        label_writer.write_labels(records, target="static\\label\\{val}.pdf".format(val = server['node']))
        
        # Rend la template "server.html" avec les arguments appropriés
        return render_template('home/server.html', username=session['username'], title="Serveur", server=server, server_disk=server_disk_prct, server_ram=server_ram_prct, target = target, qrcodepng=qrcodepng) 

    # Si l'utilisateur n'est pas connecté, redirige vers la page de connexion
    return redirect(url_for('Fauth.login'))

# Route pour la page d'affichage des posts de travails
@Fdevice.route('/postes', methods=['GET', 'POST'])
def devices():
    # Vérifie si l'utilisateur est connecté en vérifiant la valeur de la clé 'loggedin' dans le dictionnaire de session
    if session['loggedin'] == True and session['istech'] == True:
        # Crée un curseur pour une connexion MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                
        cursor.execute( "SELECT * FROM device")
        all_device = cursor.fetchall()
        return render_template('home/devices.html', username=session['username'], title="Post de travaille", all_device = all_device)
    
    # Si l'utilisateur n'est pas connecté, redirige vers la page de connexion
    return redirect(url_for('Fauth.login'))

# Route pour la page d'affichage des posts de travails
@Fdevice.route('/servers', methods=['GET', 'POST'])
def servers():
    # Vérifie si l'utilisateur est connecté en vérifiant la valeur de la clé 'loggedin' dans le dictionnaire de session
    if session['loggedin'] == True and session['istech'] == True:
        # Crée un curseur pour une connexion MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                
        cursor.execute( "SELECT * FROM server")
        all_server = cursor.fetchall()
        return render_template('home/servers.html', username=session['username'], title="Serveurs", all_server = all_server)
    
    # Si l'utilisateur n'est pas connecté, redirige vers la page de connexion
    return redirect(url_for('Fauth.login'))

# Route pour la page d'ajout d'imprimante
@Fdevice.route('/imprimantes', methods=['GET', 'POST'])
def printers():
    # Vérifie si l'utilisateur est connecté en vérifiant la valeur de la clé 'loggedin' dans le dictionnaire de session
    if session['loggedin'] == True and session['istech'] == True:
        # Crée un curseur pour une connexion MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute( "SELECT * FROM printer")
        all_printers = cursor.fetchall()
        


        return render_template('home/printers.html', username=session['username'], title="Imprimante", all_printers = all_printers)
    
    # Si l'utilisateur n'est pas connecté, redirige vers la page de connexion
    return redirect(url_for('Fauth.login'))

# Route pour la page de l'imprimante séléctionner
@Fdevice.route('/imprimante', methods=['GET', 'POST'])
def printer():

    # Vérifie si l'utilisateur est connecté en vérifiant la valeur de la clé 'loggedin' dans le dictionnaire de session
    if session['loggedin'] == True and session['istech'] == True:

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

        label_writer = LabelWriter("templates/label/printer.html", default_stylesheets=("static/bootstrap/css/style.css",))
        records = [
            dict(id=printer['id'], hote=printer['name'], ip=printer['ip']),
        ]
        target = "static\\label\\printer\\{val}.pdf".format(val = printer['name'])
        label_writer.write_labels(records, target="static\\label\\printer\\{val}.pdf".format(val = printer['name']))
        
        # Rend la template "printer.html" avec les arguments appropriés
        return render_template('home/printer.html', username=session['username'], title="Imprimante", printer=printer,target = target) 

    # Si l'utilisateur n'est pas connecté, redirige vers la page de connexion
    return redirect(url_for('Fauth.login'))

# Route pour la page d'affichage de l'information de la machine
@Fdevice.route('/info_poste', methods=['GET', 'POST'])
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

# Route pour la page d'affichage de l'information de la machine
@Fdevice.route('/reseau', methods=['GET', 'POST'])
def reseau():

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # Exécute une requête pour sélectionner l'entrée de la table 'device' correspondant à l'hote de la machine
    cursor.execute('SELECT * FROM network')
    # Récupère les résultats de la requête
    network_device = cursor.fetchall()

    # Rend la template "device_info.html" avec les arguments appropriés
    return render_template('home/network.html', title="Informations", network_device=network_device)

# Route pour la page d'affichage de l'information de la machine
@Fdevice.route('/reseau_update', methods=['GET', 'POST'])
def reseau_update():

    # Si l'utilisateur a soumis un formulaire
    if request.method == 'POST' and 'network' in request.form:
        network = request.form["network"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('TRUNCATE TABLE network')

        flash("Requete en cours veuillez attendre !", "success")
        nmap.scan(f'{network}', '6446')

        l2 = []

        for host in nmap.all_hosts():
            port_state = nmap[host]['tcp'][port]['state']
            if port_state == "open":
                r = requests.get(f"http://{host}:6446/get-host")
                host_r = r.text

                # Crée un curseur pour une connexion MySQL
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

                cursor.execute( "SELECT * FROM device WHERE node LIKE %s", [host_r[1:-1]])
                device = cursor.fetchone()
                
                if device:
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('INSERT INTO network VALUES (%s, %s, %s, %s)', (port, port_state, host,"True"))
                    mysql.connection.commit()
                    l1 = {'port': port, 'port_state': port_state, 'host': host, 'control': True}
                    l2.append(l1)
                else:
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('INSERT INTO network VALUES (%s, %s, %s, %s)', (port, port_state, host,"False"))
                    mysql.connection.commit()
                    l1 = {'port': port, 'port_state': port_state, 'host': host, 'control': False}
                    l2.append(l1)
            else: pass
        
        return redirect(url_for('Fdevice.reseau'))
        
    elif request.method == 'POST':
        # Affiche un message si le formulaire est incomplet
        flash("Remplissez le formulaire !", "danger")
    # Rend la template "device_info.html" avec les arguments appropriés
    return redirect(url_for('Fdevice.reseau'))

# Route pour la page d'affichage de l'information de la machine
@Fdevice.route('/poste_add', methods=['GET', 'POST'])
def poste_add():
    host = request.values.get("host")

    flash("Poste ajouter sur ItzMyManager avec succèss !", "success")
    fff = f'http://{host}:6446/api/init'
    print(fff)

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE network SET control = %s WHERE host = %s', ("True", host))
    mysql.connection.commit()

    requests.get(f'http://{host}:6446/api/init')

    return redirect(url_for('Fdevice.reseau'))

# Route pour la page d'affichage de l'information de la machine
@Fdevice.route('/poste_upd', methods=['GET', 'POST'])
def poste_upd():
    host = request.values.get("host")

    flash("Poste mise à jour avec succèss !", "success")

    requests.get(f'http://{host}:6446/api/update')

    return redirect(url_for('Fdevice.reseau'))