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

Fticket = Blueprint('Fticket', __name__)

# Route pour la page pour voir les tickets
@Fticket.route('/tickets')
def tickets():

    # Vérification de la connexion de l'utilisateur
    if session['loggedin'] == True and session['istech'] == True:
        
        priorite = request.args.get("priorite")
        if priorite == "basse":
            # Création d'un curseur pour interagir avec la base de données
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            # Récupération des tickets ayant un statut "En attente" ou "En cours"
            cursor.execute('SELECT * FROM ticket WHERE priorite = "Basse" AND ( status = "En attente" OR status = "En cours" ) ')
            all_tickets = cursor.fetchall()

            # Envoi des tickets récupérés à la vue pour affichage
            return render_template('ticket/all_ticket.html', title="Ticket", username=session['username'], tickets=all_tickets)

        elif priorite == "normale":
            # Création d'un curseur pour interagir avec la base de données
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            # Récupération des tickets ayant un statut "En attente" ou "En cours"
            cursor.execute('SELECT * FROM ticket WHERE priorite = "Normale" AND ( status = "En attente" OR status = "En cours" ) ')
            all_tickets = cursor.fetchall()

            # Envoi des tickets récupérés à la vue pour affichage
            return render_template('ticket/all_ticket.html', title="Ticket", username=session['username'], tickets=all_tickets)

        elif priorite == "elevee":
            # Création d'un curseur pour interagir avec la base de données
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            # Récupération des tickets ayant un statut "En attente" ou "En cours"
            cursor.execute('SELECT * FROM ticket WHERE priorite = "Élevée" AND ( status = "En attente" OR status = "En cours" ) ')
            all_tickets = cursor.fetchall()

            # Envoi des tickets récupérés à la vue pour affichage
            return render_template('ticket/all_ticket.html', title="Ticket", username=session['username'], tickets=all_tickets)
        
        else:
            # Création d'un curseur pour interagir avec la base de données
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            # Récupération des tickets ayant un statut "En attente" ou "En cours"
            cursor.execute('SELECT * FROM ticket WHERE status = "En attente" OR status = "En cours"')
            all_tickets = cursor.fetchall()

            # Envoi des tickets récupérés à la vue pour affichage
            return render_template('ticket/all_ticket.html', title="Tickets", username=session['username'], tickets=all_tickets)
    # Redirection vers la page de connexion si l'utilisateur n'est pas connecté
    return redirect(url_for('Fauth.login'))

# Route pour la page pour voir les tickets
@Fticket.route('/empl/tickets')
def tickets_empl():

    # Vérification de la connexion de l'utilisateur
    if session['loggedin'] == True:

        # Création d'un curseur pour interagir avec la base de données
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Récupération des tickets correspondant à l'utilisateur connecté
        cursor.execute('SELECT * FROM ticket WHERE user = %s', [session['username']])
        all_tickets = cursor.fetchall()

        # Envoi des tickets récupérés à la vue pour affichage
        return render_template('mobile/ticketsme.html', title="Tickets", username=session['username'], tickets=all_tickets)

    # Redirection vers la page de connexion si l'utilisateur n'est pas connecté
    return redirect(url_for('Fauth.login_empl'))


# Route pour la page pour voir les tickets fini
@Fticket.route('/tickets/resolu')
def tickets_f():

    # Vérification de la connexion de l'utilisateur
    if session['loggedin'] == True and session['istech'] == True:

        # Création d'un curseur pour interagir avec la base de données
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Récupération des tickets ayant un statut "Fini"
        cursor.execute('SELECT * FROM ticket WHERE status = "Fini"')
        all_tickets = cursor.fetchall()

        # Envoi des tickets récupérés à la vue pour affichage
        return render_template('ticket/all_ticket.html', title="Tickets", username=session['username'], tickets=all_tickets)

    # Redirection vers la page de connexion si l'utilisateur n'est pas connecté
    return redirect(url_for('Fauth.login'))



# Route pour la page pour voir un ticket
@Fticket.route('/tickets/ticket')
def ticket():

    # Vérification de la connexion de l'utilisateur
    if session['loggedin'] == True and session['istech'] == True:

        # Récupération de l'ID du ticket à afficher
        ticket_id = request.args.get("ticket_id")

        # Création d'un curseur pour interagir avec la base de données
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Récupération des données du ticket correspondant à l'ID spécifié
        cursor.execute('SELECT * FROM ticket WHERE ID = %s', [ticket_id])
        ticket = cursor.fetchone()

        # Formatage de la date de création du ticket
        date1_1 = str(ticket['creation'])
        date1_2 = datetime.strptime(date1_1, "%Y-%m-%d").date()
        ticket_creation = str('{:02d}'.format(date1_2.day)) +"-"+str('{:02d}'.format(date1_2.month))+"-"+str(date1_2.year)

        # Verification si l'utilisateur est un administrateur ou pas
        if session['id'] == 1:

            # Affichage du bouton de suppression pour les administrateurs
            return render_template('ticket/ticket.html', username=session['username'], title="Ticket", ticket=ticket, creation=ticket_creation, delete= True) 
        else:

            # Affichage sans le bouton de suppression pour les utilisateurs
            return render_template('ticket/ticket.html', username=session['username'], title="Ticket", ticket=ticket, delete = False) 
   
    # Redirection vers la page de connexion si l'utilisateur n'est pas connecté
    return redirect(url_for('Fauth.login'))



# Route pour la page pour creer un ticket
@Fticket.route('/empl/creation_ticket', methods=['GET', 'POST'])
def create_ticket():

    # Vérification de la connexion de l'utilisateur
    if session['loggedin'] == True:
        if session['istech'] == False:

            # Création d'un curseur pour interagir avec la base de données
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            # Récupération de tous les appareils de la base de données
            cursor.execute('SELECT * FROM device')
            all_device = cursor.fetchall()

            if request.method == 'POST' and 'desc' in request.form:

                # Récupération des champs du formulaire
                ticket_username = session['username']
                priorite = request.form['priorite']
                ticket_device_id = request.form['device_id']
                ticket_objet = request.form['objet']
                ticket_desc = request.form['desc']
                ticket_status = "En attente"

                # Récupération de la date actuelle
                date = datetime.now()

                # Conversion de la date de création au format "YYYY-MM-DD"
                ticket_creation = str(date.year) +"-"+str(date.month)+"-"+str(date.day)

                # Ajout des données du ticket à la base de données
                cursor.execute('INSERT INTO ticket VALUES (NULL, %s, %s, %s, %s, %s, %s, "En attente")', (ticket_username, ticket_objet, ticket_desc, ticket_status, priorite, ticket_creation))
                mysql.connection.commit()
                email = session['email']
                create_ticket_mail(email, ticket_username, priorite, ticket_device_id, ticket_objet, ticket_desc)
            elif request.method == 'POST':
                flash("Remplissez le formulaire!", "danger")

            # Affichage du template pour créer un ticket avec les appareils récupérés
            return render_template('mobile/creertk.html', username=session['username'],title="Créer un ticket", device=all_device)

        # Redirection vers la page de connexion si l'utilisateur n'est pas connecté
        return redirect(url_for('Fhome.home'))

    # Redirection vers la page de connexion si l'utilisateur n'est pas connecté
    return redirect(url_for('Fauth.login_empl'))

# Route pour la page pour supprimer un ticket
@Fticket.route('/suppression_ticket', methods=['GET', 'POST'])
def delete_ticket():

    # Vérification de la connexion de l'utilisateur
    if session['loggedin'] == True and session['istech'] == True:

        # Récupération de l'ID du ticket à supprimer
        ticket_id_args = request.args.get("tickettodelete")

        # Création d'un curseur pour interagir avec la base de données
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Suppression du ticket correspondant à l'ID spécifié
        cursor.execute('DELETE FROM `ticket` WHERE `id` = %s', [ticket_id_args])
        mysql.connection.commit()

        # Affichage d'un message de succès
        flash("Le ticket a été supprimé avec succès!", "success")

        # Redirection vers la page des tickets
        return redirect(url_for('Fticket.tickets'))

    # Redirection vers la page de connexion si l'utilisateur n'est pas connecté
    return redirect(url_for('Fauth.login'))



# Route pour la page pour les notifications de ticket
@Fticket.route("/notif_ticket")
def notif_ticket():

    # Création d'un curseur pour interagir avec la base de données
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Récupération de tous les tickets en attente
    cursor.execute('SELECT * FROM ticket WHERE status = "En attente"')

    all_tickets1 = cursor.fetchall()
    # Inversion de l'ordre des tickets pour avoir le dernier ticket en premier

    all_tickets = all_tickets1[::-1]
    # Affichage du template de notification avec les tickets récupérés
    
    # Affichage du template pour les notifications
    return render_template("includes/notification.html", all_tickets=all_tickets)



# Route pour la page de status de ticket
@Fticket.route("/change_status", methods=['GET', 'POST'])
def change_status():

    # Récupération de l'ID du ticket à changer
    ticket_id = request.values.get("ticketidtochange")

    # Récupération du statut du ticket
    status = request.values.get("status")

    # Création d'un curseur pour interagir avec la base de données
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Si le statut est 'encours'
    if status == "encours":

        # Mise à jour du statut du ticket en 'En cours'
        cursor.execute('UPDATE ticket SET status = "En cours" WHERE ID = %s', [ticket_id])
        cursor.execute('UPDATE ticket SET encharge = %s WHERE ID = %s', [session['username'], ticket_id])

        # Commit des changements à la base de données
        mysql.connection.commit()

    # Si le statut est 'effectue'
    elif status == "effectue":

        # Mise à jour du statut du ticket en 'Fini'
        cursor.execute('UPDATE ticket SET status = "Fini" WHERE ID = %s', [ticket_id])
        cursor.execute('UPDATE ticket SET encharge = %s WHERE ID = %s', [session['username'], ticket_id])

        # Commit des changements à la base de données
        mysql.connection.commit()

    # Redirection vers la page du ticket avec l'ID mis à jour
    return redirect(url_for('Fticket.ticket', ticket_id=ticket_id))