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

Fauth = Blueprint('Fauth', __name__)

@Fauth.route('/', methods=['GET', 'POST'])
def login():
    if request.MOBILE == True:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            # Create variables for easy access
            username = request.form['username']
            password = request.form['password']

            hashpass = hashlib.md5(password.encode('utf8')).hexdigest()
                # Check if account exists using MySQL
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM employee WHERE username = %s OR email = %s AND password = %s', (username, username, hashpass))
            account = cursor.fetchone()
                # Fetch one record and return result
                    
                        # If account exists in accounts table in out database
            if account:
                    # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                session['firstname'] = account['firstname']
                session['lastname'] = account['lastname']
                session['password'] = account['password']
                session['email'] = account['email']
                session['adresse'] = account['adresse']
                session['city'] = account['city']
                session['country'] = account['country']

                # Redirect to home page
                print("connecter")
                return redirect(url_for('Fticket.create_ticket'))
            else:
                    # Account doesnt exist or username/password incorrect
                flash("Incorrect username/password!", "danger")

        elif request.method == 'POST':
            flash("Remplissez le formulaire !", "danger")

        return render_template('mobile/login.html',title="Connexion")
    elif request.MOBILE == False:
        # Output message if something goes wrong...
        # Check if "username" and "password" POST requests exist (user submitted form)
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            # Create variables for easy access
            username = request.form['username']
            password = request.form['password']

            hashpass = hashlib.md5(password.encode('utf8')).hexdigest()
            # Check if account exists using MySQL
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM accounts WHERE username = %s OR email = %s AND password = %s', (username, username, hashpass))
            account = cursor.fetchone()
            # Fetch one record and return result
                
           # If account exists in accounts table in out database
            if account:
                # Create session data, we can access this data in other routes
                total_accounts = cursor.execute('SELECT * FROM `accounts`')
                session['total_accounts'] = total_accounts
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                session['firstname'] = account['firstname']
                session['lastname'] = account['lastname']
                session['password'] = account['password']
                session['email'] = account['email']
                session['adresse'] = account['adresse']
                session['city'] = account['city']
                session['country'] = account['country']
                session['profilepic'] = account['profilepic']

                # Redirect to home page
                return redirect(url_for('Fhome.home'))
            else:
                    # Account doesnt exist or username/password incorrect
                flash("Incorrect username/password!", "danger")

        elif request.method == 'POST':
            flash("Remplissez le formulaire !", "danger")

        return render_template('auth/login.html',title="Connexion")



# http://localhost:5000/pythinlogin/register 
# This will be the registration page, we need to use both GET and POST requests
@Fauth.route('/register', methods=['GET', 'POST'])
def register():
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'file' and 'username' in request.form and 'firstname' in request.form and 'lastname' in request.form and 'password' in request.form and 'password_repeat' in request.form and 'email' in request.form and 'adresse' in request.form and 'city' in request.form and 'country' in request.form:
        # Create variables for easy access
        username = request.form['username']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        password = request.form['password']
        password_repeat = request.form['password_repeat']
        email = request.form['email']
        adresse = request.form['adresse']
        city = request.form['city']
        country = request.form['country']
        photo = request.files['file']
        keygen = request.form['keygen']
                # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute('SELECT * FROM accounts WHERE username = %s', (username))
        cursor.execute( "SELECT * FROM accounts WHERE username LIKE %s OR email LIKE %s", (username, email))
        account = cursor.fetchone()

        # If account exists show error and validation checks
        if account:
            flash("L'utilisateur ou l'email existe déjà!", "danger")
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash("Adresse e-mail invalide!", "danger")
        elif not re.match(r'[A-Za-z]+', username):
            flash("Le nom d'utilisateur ne doit contenir que des caractères!", "danger")
        elif not username or not password or not email or not adresse or not city or not country or not firstname or not lastname:
            flash("Veuillez remplir tout le champs !", "danger")
        elif password != password_repeat:
            flash("Les mots de passe ne sont pas identiques!", "danger")
        else:
            cursor.execute( "SELECT * FROM keycreate WHERE `key` LIKE %s", [keygen] )
            keyregf = cursor.fetchone()
            if keyregf:
                if not photo:
                    fullprofilepic_url = "static/uploads/pp/0e59a2d2-8545-11ed-a345-38c9861edab2.png" 
                else:
                    photo = request.files['file']
                    profilepic_name = str(uuid.uuid1())+'.png'
                    profilepic_url = 'static/uploads/pp/'+profilepic_name
                    fullprofilepic_url = profilepic_url

                    if os.path.isfile(fullprofilepic_url) == True:
                        os.remove(fullprofilepic_url)

                    photo.save(os.path.join("static/uploads/pp/", profilepic_name))

                password_hash = hashlib.md5(password.encode('utf8')).hexdigest()
                cursor.execute('DELETE FROM keycreate WHERE `key` LIKE %s', [keygen])
                cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (username, email, password_hash, firstname, lastname, adresse, city, country, fullprofilepic_url))
                mysql.connection.commit()
    
                flash("Votre compte a été créé avec succès, la clé à été supprimé du registre !", "success")
                mail_account_register(email, firstname, lastname)

                
            else:
                flash("La clé de création n'existe pas !", "success")
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash("Remplissez le formulaire !", "danger")
    # Show registration form with message (if any)
    return render_template('auth/register.html',title="Enregistrement")

@Fauth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST' and 'email' in request.form:
        characters = "01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ&*(){}[]|/\?!@#$%^abcdefghijklmnopqrstuvwxyz"
        new_password = "".join(random.sample(characters, 15))

        email = request.form['email']
        password_hash = hashlib.md5(new_password.encode('utf8')).hexdigest()
            
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE accounts SET password = %s WHERE email = %s', (password_hash, email))
        mysql.connection.commit()

        account = cursor.fetchone()

        flash("L'email à été envoyer avec succès !", "success")
        user_forgot_password(email, new_password)
        return redirect(url_for('forgot_password'))
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash("Veuillez remplir tout les champs !", "danger")

    return render_template('auth/forgot_password.html',title="Login")

@Fauth.route('/logout')
def logout():
    session.clear()
    session['loggedin'] = False
    print(session['loggedin'])
    return redirect(url_for('Fauth.login')) 
    