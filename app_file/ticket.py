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

@Fticket.route('/tickets')
def tickets():
    if session['loggedin'] == True :
        if request.MOBILE == True:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM ticket WHERE user = %s', [session['username']])
            all_tickets = cursor.fetchall()

            return render_template('mobile/ticketsme.html', title="Ticket", username=session['username'], tickets=all_tickets)
            
        elif request.MOBILE == False:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM ticket WHERE status = "En attente" OR status = "En cours"')
            all_tickets = cursor.fetchall()

            return render_template('ticket/all_ticket.html', title="Ticket", username=session['username'], tickets=all_tickets)
            
    return redirect(url_for('Fauth.login'))

@Fticket.route('/tickets_r')
def tickets_r():
    if session['loggedin'] == True :
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM ticket WHERE status = "En retard"')
        all_tickets = cursor.fetchall()

        return render_template('ticket/all_ticket.html', title="Ticket", username=session['username'], tickets=all_tickets)

    return redirect(url_for('Fauth.login'))

@Fticket.route('/tickets_f')
def tickets_f():
    if session['loggedin'] == True :
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM ticket WHERE status = "Fini"')
        all_tickets = cursor.fetchall()

        return render_template('ticket/all_ticket.html', title="Ticket", username=session['username'], tickets=all_tickets)

    return redirect(url_for('Fauth.login'))

@Fticket.route('/ticket')
def ticket():
    if session['loggedin'] == True :
        ticket_id = request.args.get("ticket_id")
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM ticket WHERE ID = %s', [ticket_id])
        ticket = cursor.fetchone()
        date1_1 = str(ticket['creation'])
        date1_2 = datetime.strptime(date1_1, "%Y-%m-%d").date()
        ticket_creation = str('{:02d}'.format(date1_2.day)) +"-"+str('{:02d}'.format(date1_2.month))+"-"+str(date1_2.year)

        date2_1 = str(ticket['limite'])
        date2_2 = datetime.strptime(date2_1, "%Y-%m-%d").date()
        ticket_limite = str('{:02d}'.format(date2_2.day)) +"-"+str('{:02d}'.format(date2_2.month))+"-"+str(date2_2.year)

        if session['id'] == 1:
            print("Admin")
            return render_template('ticket/ticket.html', username=session['username'], title="Ticket", ticket=ticket, creation=ticket_creation, limite=ticket_limite, delete= True) 
        else:
            print("User")
            return render_template('ticket/ticket.html', username=session['username'], title="Ticket", ticket=ticket, delete = False) 

        return render_template('ticket/ticket.html', username=session['username'], title="Ticket", ticket=ticket)
    
    return redirect(url_for('Fauth.login'))

@Fticket.route('/create_ticket', methods=['GET', 'POST'])
def create_ticket():
    if session['loggedin'] == True :
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM device')
        all_device = cursor.fetchall()


        if request.method == 'POST' and 'desc' in request.form:
            ticket_username = session['username']
            limite = request.form['limite']
            ticket_device_id = request.form['device_id']
            ticket_objet = request.form['objet']
            ticket_desc = request.form['desc']
            ticket_status = "En attente"

            ticket_limite = datetime.strptime(limite, '%Y-%m-%d').date()
            date = datetime.now()

            print(date)
            ticket_creation = str(date.year) +"-"+str(date.month)+"-"+str(date.day)

            cursor.execute('INSERT INTO ticket VALUES (NULL, %s, %s, %s, %s, %s, %s, "En attente")', (ticket_username, ticket_objet, ticket_desc, ticket_status, ticket_limite, ticket_creation))
            mysql.connection.commit()
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            flash("Remplissez le formulaire !", "danger")
        # User is loggedin show them the home page
        return render_template('mobile/creertk.html', username=session['username'],title="Créer un ticket", device=all_device)
    # User is not loggedin redirect to login page
    return redirect(url_for('Fauth.login'))


@Fticket.route('/delete_ticket', methods=['GET', 'POST'])
def delete_ticket():
    if session['loggedin'] == True :
        ticket_id_args = request.args.get("tickettodelete")
        print(ticket_id_args)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM `ticket` WHERE `id` = %s', [ticket_id_args])
        mysql.connection.commit()

        flash("Le ticket a été supprimé avec succès !", "success")
        return redirect(url_for('Fticket.tickets'))

    return redirect(url_for('Fauth.login'))  

@Fticket.route("/notif_ticket")
def notif_ticket():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM ticket WHERE status = "En attente"')
    all_tickets1 = cursor.fetchall()
    all_tickets = all_tickets1[::-1]
    
    
    return render_template("includes/notification.html", all_tickets=all_tickets)

@Fticket.route("/change_status", methods=['GET', 'POST'])
def change_status():
    ticket_id = request.values.get("ticketidtochange")
    status = request.values.get("status")
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    print(status)
    if status == "encours":
        cursor.execute('UPDATE ticket SET status = "En cours" WHERE ID = %s', [ticket_id])
        cursor.execute('UPDATE ticket SET encharge = %s WHERE ID = %s', [session['username'], ticket_id])
        mysql.connection.commit()
    elif status == "effectue":
        cursor.execute('UPDATE ticket SET status = "Fini" WHERE ID = %s', [ticket_id])
        cursor.execute('UPDATE ticket SET encharge = %s WHERE ID = %s', [session['username'], ticket_id])
        mysql.connection.commit()

    return redirect(url_for('Fticket.ticket', ticket_id=ticket_id))