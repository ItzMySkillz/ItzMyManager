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

#Création d'un blueprint pour la partie accueil
Fhome = Blueprint('Fhome', __name__)

#Route pour la page d'accueil
@Fhome.route('/home')
def home():

    #Vérifie si l'utilisateur est connecté
    if session['loggedin'] == True :

        #Création d'un curseur pour la connexion à la base de données MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        #Compte le nombre total d'utilisateurs dans les deux tables "accounts" et "employee"
        total_accounts1 = cursor.execute('SELECT * FROM `accounts`')
        total_accounts2 = cursor.execute('SELECT * FROM `employee`')
        session['total_accounts'] = total_accounts1 + total_accounts2

        #Initialisation des variables de session pour les statistiques de tickets pour chaque mois
        session['new_janvier'] = 0
        session['new_fevrier'] = 0
        session['new_mars'] = 0
        session['new_avril'] = 0
        session['new_mai'] = 0
        session['new_juin'] = 0
        session['new_juillet'] = 0
        session['new_aout'] = 0
        session['new_septembre'] = 0
        session['new_novembre'] = 0
        session['retard_janvier'] = 0
        session['fini_janvier'] = 0
        session['retard_fevrier'] = 0
        session['fini_fevrier'] = 0
        session['retard_mars'] = 0
        session['fini_mars'] = 0
        session['retard_avril'] = 0
        session['fini_avril'] = 0
        session['retard_mai'] = 0
        session['fini_mai'] = 0
        session['retard_juin'] = 0
        session['fini_juin'] = 0
        session['retard_juillet'] = 0
        session['fini_juillet'] = 0
        session['retard_aout'] = 0
        session['fini_aout'] = 0
        session['retard_septembre'] = 0
        session['fini_septembre'] = 0
        session['retard_octobre'] = 0
        session['fini_octobre'] = 0
        session['retard_novembre'] = 0
        session['fini_novembre'] = 0
        session['retard_decembre'] = 0
        session['fini_decembre'] = 0

        #Récupère tous les tickets de la base de données
        tickets_stats = cursor.execute('SELECT * FROM `ticket`')
        tickets_stats2 = cursor.fetchall()

        #Boucle à travers tous les tickets pour mettre à jour les statistiques
        for ticket in tickets_stats2:
            
            #Recuperation de la date
            date_tic = str(ticket['creation'])
            date = datetime.strptime(date_tic, "%Y-%m-%d").date()

            #Si le mois de création du ticket est janvier
            if date.month == 1:
                #Incrémente le nombre de tickets nouveaux
                session['new_janvier'] = session['new_janvier'] + 1
                #Si le status du ticket est "En retard"
                if ticket['status'] == "En retard":
                    #Incrémente le nombre de tickets en retard
                    session['retard_janvier'] = session['retard_janvier'] + 1
                #Si le status du ticket est "Fini"
                elif ticket['status'] == "Fini":
                    #Incrémente le nombre de tickets finis
                    session['fini_janvier'] = session['fini_janvier'] + 1

            #Même chose pour les autres mois
            elif date.month == 2:
                session['new_fevrier'] = session['new_fevrier'] + 1
                if ticket['status'] == "En retard":
                    session['retard_fevrier'] = session['retard_fevrier'] + 1
                elif ticket['status'] == "Fini":
                    session['fini_fevrier'] = session['fini_fevrier'] + 1

            elif date.month == 3:
                session['new_mars'] = session['new_mars'] + 1
                if ticket['status'] == "En retard":
                    session['retard_mars'] = session['retard_mars'] + 1
                elif ticket['status'] == "Fini":
                    session['fini_mars'] = session['fini_mars'] + 1

            elif date.month == 4:
                session['new_avril'] = session['new_avril'] + 1
                if ticket['status'] == "En retard":
                    session['retard_avril'] = session['retard_avril'] + 1
                elif ticket['status'] == "Fini":
                    session['fini_avril'] = session['fini_avril'] + 1

            elif date.month == 5:
                session['new_mai'] = session['new_mai'] + 1
                if ticket['status'] == "En retard":
                    session['retard_mai'] = session['retard_mai'] + 1
                elif ticket['status'] == "Fini":
                    session['fini_mai'] = session['fini_mai'] + 1

            elif date.month == 6:
                session['new_juin'] = session['new_juin'] + 1
                if ticket['status'] == "En retard":
                    session['retard_juin'] = session['retard_juin'] + 1
                elif ticket['status'] == "Fini":
                    session['fini_juin'] = session['fini_juin'] + 1

            elif date.month == 7:
                session['new_juillet'] = session['new_juillet'] + 1
                if ticket['status'] == "En retard":
                    session['retard_juillet'] = session['retard_juillet'] + 1
                elif ticket['status'] == "Fini":
                    session['fini_juillet'] = session['fini_juillet'] + 1

            elif date.month == 8:
                session['new_aout'] = session['new_aout'] + 1
                if ticket['status'] == "En retard":
                    session['retard_aout'] = session['retard_aout'] + 1
                elif ticket['status'] == "Fini":
                    session['fini_aout'] = session['fini_aout'] + 1

            elif date.month == 9:
                session['new_septembre'] = session['new_septembre'] + 1
                if ticket['status'] == "En retard":
                    session['retard_septembre'] = session['retard_septembre'] + 1
                elif ticket['status'] == "Fini":
                    session['fini_septembre'] = session['fini_septembre'] + 1

            elif date.month == 10:
                session['new_octobre'] = session['new_octobre'] + 1
                if ticket['status'] == "En retard":
                    session['retard_octobre'] = session['retard_octobre'] + 1
                elif ticket['status'] == "Fini":
                    session['fini_octobre'] = session['fini_octobre'] + 1

            elif date.month == 11:
                session['new_novembre'] = session['new_novembre'] + 1
                if ticket['status'] == "En retard":
                    session['retard_novembre'] = session['retard_novembre'] + 1
                elif ticket['status'] == "Fini":
                    session['fini_novembre'] = session['fini_novembre'] + 1

            elif date.month == 12:
                session['new_decembre'] = session['new_decembre'] + 1
                if ticket['status'] == "En retard":
                    session['retard_decembre'] = session['retard_decembre'] + 1
                elif ticket['status'] == "Fini":
                    session['fini_decembre'] = session['fini_decembre'] + 1

        #Selection des tout les tickets en attente afin de afficher le nombre
        tickets_wait = cursor.execute('SELECT * FROM `ticket` WHERE status = "En attente"')
        session['ticket_wait'] = tickets_wait

        #Selection des tout les tickets en cours afin de afficher le nombre
        ticket_progress = cursor.execute('SELECT * FROM `ticket` WHERE status = "En cours"')
        session['ticket_progress'] = ticket_progress

        #Selection des tout les tickets en retard afin de afficher le nombre
        ticket_late = cursor.execute('SELECT * FROM `ticket` WHERE status = "En retard"')
        session['ticket_late'] = ticket_late

        #Selection des tout les tickets fini afin de afficher le nombre
        ticket_finish = cursor.execute('SELECT * FROM `ticket` WHERE status = "Fini"')
        session['ticket_finish'] = ticket_finish

        #Selection des tout les imprimantes afin de afficher le nombre
        printers = cursor.execute('SELECT * FROM `printer`')
        session['printers'] = printers

        #Selection des tout les postes de travail afin de afficher le nombre
        devices = cursor.execute('SELECT * FROM `device`')
        session['devices'] = devices

        #Affichage la template de la page d'accueil avec les donnéer dessus
        return render_template('home/home.html', username=session['username'],title="Accueil")

    #Redirection à la page d'accueil si l'utilisateur est pas connecté
    return redirect(url_for('Fauth.login'))  