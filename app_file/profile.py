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

Fprofile = Blueprint('Fprofile', __name__)

@Fprofile.route('/profiles_tech', methods=['GET', 'POST'])
def profiles_tech():
    # Check if user is loggedin
    if session['loggedin'] == True :
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts')
        all_account = cursor.fetchall()
                
        return render_template('home/all_profile.html', username=session['username'], title="Utilisateurs", all_account = all_account, technicien=True)

        # User is loggedin show them the home page
    # User is not loggedin redirect to login page
    return redirect(url_for('Fauth.login')) 

@Fprofile.route('/profiles_empl')
def profiles_empl():
    # Check if user is loggedin
    if session['loggedin'] == True :
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM employee')
        all_account = cursor.fetchall()

        return render_template('home/all_profile.html', username=session['username'], title="Utilisateurs", all_account = all_account, technicien=False)
        
    # User is not loggedin redirect to login page
    return redirect(url_for('Fauth.login'))

@Fprofile.route('/profile')
def profile():
    # Check if user is loggedin
    if session['loggedin'] == True :
        if request.MOBILE == True:
            return render_template('mobile/profile.html', username=session['username'], title="Profile")
        elif request.MOBILE == False:
            if session['id'] == 1:
                print("User")
                return render_template('auth/profile.html', username=session['username'], title="Profile", isKey=True)
            else:
                print("Admin")
                return render_template('auth/profile.html', username=session['username'], title="Profile", isKey=False)
        

    # User is not loggedin redirect to login page
    return redirect(url_for('Fauth.login')) 

@Fprofile.route('/profile_empl', methods=['GET', 'POST'])
def profile_empl():
    if session['loggedin'] == True :
        user_id = request.values.get("user_id")
        user_id_args = request.args.get("user_id")
        print(user_id_args)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM employee  WHERE ID = %s', [user_id_args])
        other_account = cursor.fetchone()

        return render_template('auth/other_profile.html', username=session['username'], title="Utilisateur", other_account=other_account, technicien = False) 

    return redirect(url_for('Fauth.login'))

@Fprofile.route('/profile_tech', methods=['GET', 'POST'])
def profile_tech():
    if session['loggedin'] == True :
        user_id = request.values.get("user_id")
        user_id_args = request.args.get("user_id")
        print(user_id_args)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE ID = %s', [user_id])
        other_account = cursor.fetchone()


        if session['id'] == 1:
            if int(user_id) == 1:
                print("AdminAdmin")
                return render_template('auth/other_profile.html', username=session['username'], title="Utilisateur", other_account=other_account, delete = False, technicien = True) 
            else:
                print("Admin")
                return render_template('auth/other_profile.html', username=session['username'], title="Utilisateur", other_account=other_account, delete= True, technicien = True) 
        else:
            print("User")
            return render_template('auth/other_profile.html', username=session['username'], title="Utilisateur", other_account=other_account, delete = False, technicien = True) 

    return redirect(url_for('Fauth.login'))

@Fprofile.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if session['loggedin'] == True :
        if request.method == 'POST' and 'username' in request.form and 'firstname' in request.form and 'lastname' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form:
            # Create variables for easy access
            username = request.form['username']
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            email = request.form['email']
            adresse = request.form['address']
            city = request.form['city']
            country = request.form['country']
                    # Check if account exists using MySQL
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # cursor.execute('SELECT * FROM accounts WHERE username = %s', (username))
            if request.form['type'] == "employer":
                cursor.execute( "SELECT * FROM employee WHERE username LIKE %s OR email LIKE %s", (username, email))
                account = cursor.fetchone()
            elif request.form['type'] == "technicien":
                cursor.execute( "SELECT * FROM accounts WHERE username LIKE %s OR email LIKE %s", (username, email))
                account = cursor.fetchone()
                
            # If account exists show error and validation checks
            if account:
                flash("L'utilisateur ou l'email existe déjà!", "danger")
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash("Adresse e-mail invalide!", "danger")
            elif not re.match(r'[A-Za-z]+', username):
                flash("Le nom d'utilisateur ne doit contenir que des caractères!", "danger")
            elif not username or not email or not adresse or not city or not country or not firstname or not lastname:
                flash("Veuillez remplir tout le champs !", "danger")
            else:
                print(request.form['type'])
                if request.form['type'] == "employer":
                    characters = "01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ&*(){}[]|/\?!@#$%^abcdefghijklmnopqrstuvwxyz"
                    password = "".join(random.sample(characters, 15))

                    password_hash = hashlib.md5(password.encode('utf8')).hexdigest()

                    cursor.execute('INSERT INTO employee VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s)', (username, email, firstname, lastname, password_hash, adresse, city, country))
                    mysql.connection.commit()
            
                    flash("Votre compte a été créé avec succès", "success")

                    user_password = password
                    create_account_mail(email, firstname, lastname, username, adresse, city, country, user_password)

                elif request.form['type'] == "technicien":
                    fullprofilepic_url = "static/uploads/pp/0e59a2d2-8545-11ed-a345-38c9861edab2.png"
                    characters = "01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ&*(){}[]|/\?!@#$%^abcdefghijklmnopqrstuvwxyz"
                    password = "".join(random.sample(characters, 15))

                    password_hash = hashlib.md5(password.encode('utf8')).hexdigest()

                    cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (username, email, password_hash, firstname, lastname, adresse, city, country, fullprofilepic_url))
                    mysql.connection.commit()
            
                    flash("Votre compte a été créé avec succès", "success")
                    user_password = password
                    create_account_mail(email, firstname, lastname, username, adresse, city, country, user_password)
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            flash("Remplissez le formulaire !", "danger")
        return render_template('home/create_profile.html', username=session['username'], title="Utilisateur") 

    return redirect(url_for('Fauth.login'))

@Fprofile.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    if session['loggedin'] == True :
        user_id_args = request.args.get("usertodelete")
        print(user_id_args)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM `accounts` WHERE `id` = %s', [user_id_args])
        mysql.connection.commit()

        total_accounts1 = cursor.execute('SELECT * FROM `employee`')
        total_accounts2 = cursor.execute('SELECT * FROM `accounts`')
        session['total_accounts'] = total_accounts1 + total_accounts2

        flash("Le compte a été supprimé avec succès !", "success")
        return redirect(url_for('Fprofile.profiles_tech'))

    return redirect(url_for('Fauth.login'))

@Fprofile.route('/delete_empl', methods=['GET', 'POST'])
def delete_empl():
    if session['loggedin'] == True :
        user_id_args = request.args.get("usertodelete")
        print(user_id_args)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM `employee` WHERE `id` = %s', [user_id_args])
        mysql.connection.commit()

        total_accounts1 = cursor.execute('SELECT * FROM `employee`')
        total_accounts2 = cursor.execute('SELECT * FROM `accounts`')
        session['total_accounts'] = total_accounts1 + total_accounts2

        flash("Le compte a été supprimé avec succès !", "success")
        return redirect(url_for('Fprofile.profiles_empl'))

    return redirect(url_for('Fauth.login'))  
    
@Fprofile.route('/change_photo', methods=['GET', 'POST'])
def change_photo():
    if request.method == 'POST' and 'file_change':

        photo_ch = request.files['file_change']

        if not photo_ch:
            flash("Veuillez ajouter votre photo de profile !", "danger")
        else:
            profilepic_name_ch = str(uuid.uuid1())+'.png'
            profilepic_url_ch = 'static/uploads/pp/'+profilepic_name_ch
            fullprofilepic_url_ch = profilepic_url_ch

            photo_ch.save(os.path.join("static/uploads/pp/", profilepic_name_ch))
            
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE accounts SET profilepic = %s WHERE ID = %s', (fullprofilepic_url_ch, session['id']))
            mysql.connection.commit()

            session['profilepic'] = fullprofilepic_url_ch

            flash("Votre photo de profil à été changer avec succès !", "success")
            return redirect(url_for('Fprofile.profile'))
            

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash("Veuillez ajouter votre photo de profile !", "danger")
    # Show registration form with message (if any)
    return redirect(url_for('Fprofile.profile'))


@Fprofile.route('/change_pswd', methods=['GET', 'POST'])
def change_pswd():
    if request.method == 'POST' and 'newpswd' in request.form and 'newpswd_confirm' in request.form:
        newpswd = request.form['newpswd']
        newpswd_confirm = request.form['newpswd_confirm']
        if newpswd != newpswd_confirm:
            flash("Les mots de passe ne sont pas identiques!", "danger")
        elif not newpswd or not newpswd_confirm:
            flash("Veuillez remplir tout les champs !", "danger")
        else:

            password_hash = hashlib.md5(newpswd.encode('utf8')).hexdigest()
            if request.MOBILE == True:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('UPDATE employee SET password = %s WHERE ID = %s', (password_hash, session['id']))
                mysql.connection.commit()

                account = cursor.fetchone()
            elif request.MOBILE == False:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('UPDATE accounts SET password = %s WHERE ID = %s', (password_hash, session['id']))
                mysql.connection.commit()

                account = cursor.fetchone()

            flash("Votre mot de passe à été changer avec succès !", "success")
            lastname = session['lastname']
            firstname = session['firstname']
            email = session['email']
            user_account_password(email, firstname, lastname)
            return redirect(url_for('Fprofile.profile'))
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash("Veuillez remplir tout les champs !", "danger")

    return redirect(url_for('Fprofile.profile'))

@Fprofile.route('/change_info', methods=['GET', 'POST'])
def change_info():
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_email = request.form['new_email']
        new_firstname = request.form['new_firstname']
        new_lastname = request.form['new_lastname']
        old_username = session['username']
        old_email = session['email']
        old_firstname = session['firstname']
        old_lastname = session['lastname']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        if not new_username and not new_email and not new_firstname and not new_lastname:
            flash("Veuillez remplir minimum un champ !", "danger")
        else:
            if not new_username:
                print("pass username")
                new_username = old_username
            else:
                if not re.match(r'[A-Za-z]+', new_username):
                    flash("Le nom d'utilisateur ne doit contenir que des caractères!", "danger")
                else:
                    if request.MOBILE == True:
                        cursor.execute('UPDATE employee SET username = %s WHERE ID = %s', (new_username, session['id']))
                        mysql.connection.commit()
                    elif request.MOBILE == False: 
                        cursor.execute('UPDATE accounts SET username = %s WHERE ID = %s', (new_username, session['id']))
                        mysql.connection.commit()

                    session['username'] = new_username


            if not new_email:
                print("pass email")
                new_email = old_email
            else:
                if request.MOBILE == True:
                    cursor.execute('UPDATE employee SET email = %s WHERE ID = %s', (new_email, session['id']))
                    mysql.connection.commit()  
                elif request.MOBILE == False: 
                    cursor.execute('UPDATE accounts SET email = %s WHERE ID = %s', (new_email, session['id']))
                    mysql.connection.commit()
                
                session['email'] = new_email


            if not new_firstname:
                print("pass first name")
                new_firstname = old_firstname
            else:
                if request.MOBILE == True:
                    cursor.execute('UPDATE employee SET firstname = %s WHERE ID = %s', (new_firstname, session['id']))
                    mysql.connection.commit()
                elif request.MOBILE == False: 
                    cursor.execute('UPDATE accounts SET firstname = %s WHERE ID = %s', (new_firstname, session['id']))
                    mysql.connection.commit()

                session['firstname'] = new_firstname

            if not new_lastname:
                print("pass last name")
                new_lastname = old_lastname
            else:
                if request.MOBILE == True:
                    cursor.execute('UPDATE employee SET lastname = %s WHERE ID = %s', (new_lastname, session['id']))
                    mysql.connection.commit()
                elif request.MOBILE == False: 
                    cursor.execute('UPDATE accounts SET lastname = %s WHERE ID = %s', (new_lastname, session['id']))
                    mysql.connection.commit()

                session['lastname'] = new_lastname

            account = cursor.fetchone()
            flash("Modification apporté avec succès !", "success")
            user_account_information(new_username, new_email, new_firstname, new_lastname)
            return redirect(url_for('profile'))
            
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash("Veuillez remplir minimum un champ !", "danger")

    return redirect(url_for('Fprofile.profile'))


@Fprofile.route('/change_adresse', methods=['GET', 'POST'])
def change_adresse():
    if request.method == 'POST':
        new_address = request.form['new_address']
        new_city = request.form['new_city']
        new_country = request.form['new_country']
        old_address = session['adresse']
        old_city = session['city']
        old_country = session['country']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        if not new_address and not new_city and not new_country:
            flash("Veuillez remplir minimum un champ !", "danger")
        else:
            if not new_address:
                print("pass address")
                new_address = old_address
            else:
                if request.MOBILE == True:
                    cursor.execute('UPDATE employee SET adresse = %s WHERE ID = %s', (new_address, session['id']))
                    mysql.connection.commit()
                elif request.MOBILE == False: 
                    cursor.execute('UPDATE accounts SET adresse = %s WHERE ID = %s', (new_address, session['id']))
                    mysql.connection.commit()


                session['adresse'] = new_address


            if not new_city:
                print("pass city")
                new_city = old_city
            else:
                if request.MOBILE == True:
                    cursor.execute('UPDATE employee SET city = %s WHERE ID = %s', (new_city, session['id']))
                    mysql.connection.commit()
                elif request.MOBILE == False: 
                    cursor.execute('UPDATE accounts SET city = %s WHERE ID = %s', (new_city, session['id']))
                    mysql.connection.commit()


                session['city'] = new_city


            if not new_country:
                print("pass country")
                new_country = old_country
            else:
                if request.MOBILE == True:
                    cursor.execute('UPDATE employee SET country = %s WHERE ID = %s', (new_country, session['id']))
                    mysql.connection.commit()
                elif request.MOBILE == False: 
                    cursor.execute('UPDATE accounts SET country = %s WHERE ID = %s', (new_country, session['id']))
                    mysql.connection.commit()


                session['country'] = new_country

            account = cursor.fetchone()
            flash("Modification apporté avec succès !", "success")
            lastname = session['lastname']
            firstname = session['firstname']
            email = session['email']
            user_account_address(new_address, new_city, new_country, lastname, firstname, email)
            return redirect(url_for('profile'))
            
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash("Veuillez remplir minimum un champ !", "danger")

    return redirect(url_for('Fprofile.profile'))

@Fprofile.route('/generatekey', methods=['GET', 'POST'])
def generatekey():
    if request.method == 'POST':
        cursorkey = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        key = str(uuid.uuid1())+str(uuid.uuid1())
        key_tot = 'key.'+key
        print(key_tot)

        session['keygenerate'] = key_tot

        cursorkey.execute('INSERT INTO keycreate VALUES (NULL, %s)', [key_tot])
        mysql.connection.commit()

        flash("Clé généré avec succès, après l'utilisation de celle-ci elle sera supprimé!", "success")
        return redirect(url_for('profile'))
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash("Erreur !", "danger")

    return redirect(url_for('Fprofile.profile'))