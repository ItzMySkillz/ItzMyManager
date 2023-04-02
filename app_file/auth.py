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

# Création d'un blueprint pour la partie connexion
Fauth = Blueprint('Fauth', __name__)

# Route pour la page de connexion
@Fauth.route('/empl/connexion', methods=['GET', 'POST'])
def login_empl():

    # Si l'utilisateur a soumis un formulaire de connexion
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:

         # Récupération des informations de connexion de l'utilisateur
        username = request.form['username']
        password = request.form['password']

        # Cryptage du mot de passe de l'utilisateur
        hashpass = hashlib.md5(password.encode('utf8')).hexdigest()

            
        # Vérification des informations de connexion de l'utilisateur avec les données de la base de données
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM employee WHERE username = %s AND password = %s', (username, hashpass))
        account = cursor.fetchone()

        # Si les informations sont correctes
        if account:
            if account['register'] == "False":

                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                session['firstname'] = account['firstname']
                session['lastname'] = account['lastname']
                session['email'] = account['email']
                #Redirection ver la page afin de créer des tickets
                return redirect(url_for('Fauth.enregistrement_empl'))
            else:
                # Stockage des informations de l'utilisateur dans une session
                session['loggedin'] = True
                session['istech'] = False
                session['id'] = account['id']
                session['username'] = account['username']
                session['firstname'] = account['firstname']
                session['lastname'] = account['lastname']
                session['password'] = account['password']
                session['email'] = account['email']
                session['adresse'] = account['adresse']
                session['city'] = account['city']
                session['country'] = account['country']

                print("connecter")

                #Redirection ver la page afin de créer des tickets
                return redirect(url_for('Fticket.create_ticket'))

        # Si les informations sont incorrectes
        else:
            flash("Incorrect username/password!", "danger")

    elif request.method == 'POST':
        flash("Remplissez le formulaire !", "danger")

    # Affichage la template de la page de connexion avec les donnéer dessus
    return render_template('mobile/login.html',title="Connexion")

# Route pour la page de connexion
@Fauth.route('/connexion', methods=['GET', 'POST'])
def login():

    # Si l'utilisateur a soumis un formulaire de connexion
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:

        #Récupération des informations de connexion de l'utilisateur
        username = request.form['username']
        password = request.form['password']

        # Cryptage du mot de passe de l'utilisateur
        hashpass = hashlib.md5(password.encode('utf8')).hexdigest()

        # Vérification des informations de connexion de l'utilisateur avec les données de la base de données
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, hashpass))
        account = cursor.fetchone()

        # Si les informations sont correctes
        if account:
                
            # Stockage des informations de l'utilisateur dans une session
            total_accounts = cursor.execute('SELECT * FROM `accounts`')
            session['total_accounts'] = total_accounts
            session['loggedin'] = True
            session['istech'] = True
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

            # Redirection ver la page afin de créer des tickets
            return redirect(url_for('Fhome.home'))
                
        # Si les informations sont incorrectes
        else:
            flash("Incorrect username/password!", "danger")

    elif request.method == 'POST':
        flash("Remplissez le formulaire !", "danger")
        
    # Affichage la template de la page de connexion avec les donnéer dessus 
    return render_template('auth/login.html',title="Connexion")

# Route pour la page d'enregistrement
@Fauth.route('/enregistrement', methods=['GET', 'POST'])
def register():

    # Vérifie si la requête est de type POST et que tous les champs requis sont présents dans la requête
    if request.method == 'POST' and 'file' and 'username' in request.form and 'firstname' in request.form and 'lastname' in request.form and 'password' in request.form and 'password_repeat' in request.form and 'email' in request.form and 'adresse' in request.form and 'city' in request.form and 'country' in request.form:

        # Récupère les données du formulaire
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

        # Vérifie si un utilisateur ou un email existe déjà avec les informations fournies
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute( "SELECT * FROM accounts WHERE username LIKE %s OR email LIKE %s", (username, email))
        account = cursor.fetchone()

        # Vérifie si un compte existe déjà avec les informations fournies
        if account:
            flash("L'utilisateur ou l'email existe déjà!", "danger")

        # Vérifie si l'adresse email est valide
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash("Adresse e-mail invalide!", "danger")

        # Vérifie si le nom d'utilisateur ne contient que des caractères
        elif not re.match(r'[A-Za-z]+', username):
            flash("Le nom d'utilisateur ne doit contenir que des caractères!", "danger")
            
        # Vérifie si tous les champs ont été remplis
        elif not username or not password or not email or not adresse or not city or not country or not firstname or not lastname:
            flash("Veuillez remplir tout le champs !", "danger")

        # Vérifie si les mots de passe ne sont pas identiques
        elif password != password_repeat:
            flash("Les mots de passe ne sont pas identiques!", "danger")
        else:
            cursor.execute( "SELECT * FROM keycreate WHERE `key` LIKE %s", [keygen] )
            keyregf = cursor.fetchone()
            if keyregf:

                # Si aucune photo n'est fournie, utilise une image par défaut
                if not photo:
                    fullprofilepic_url = "static/uploads/pp/0e59a2d2-8545-11ed-a345-38c9861edab2.png"
                else:

                    # Récupère la photo uploadée et la renomme avec un UUID
                    photo = request.files['file']
                    profilepic_name = str(uuid.uuid1())+'.png'
                    profilepic_url = 'static/uploads/pp/'+profilepic_name
                    fullprofilepic_url = profilepic_url
                # Supprime l'ancienne image si elle existe
                if os.path.isfile(fullprofilepic_url) == True:
                    os.remove(fullprofilepic_url)

                # Enregistre la photo
                photo.save(os.path.join("static/uploads/pp/", profilepic_name))

                # Hash le mot de passe
                password_hash = hashlib.md5(password.encode('utf8')).hexdigest()
                # Supprime la clé de création utilisée pour créer le compte de la base de données
                cursor.execute('DELETE FROM keycreate WHERE `key` LIKE %s', [keygen])
                # Ajoute les informations de l'utilisateur à la base de données
                cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (username, email, password_hash, firstname, lastname, adresse, city, country, fullprofilepic_url))
                mysql.connection.commit()

                # Affiche un message de succès
                flash("Votre compte a été créé avec succès, la clé à été supprimé du registre !", "success")
                # Envoie un email de confirmation
                mail_account_register(email, firstname, lastname)

                
            else:
                # Affiche un message si la clé de création n'existe pas
                flash("La clé de création n'existe pas !", "success")
    elif request.method == 'POST':
        # Affiche un message si le formulaire est incomplet
        flash("Remplissez le formulaire !", "danger")

    # Affichage la template de la page d'enregistrement avec les donnéer dessus 
    return render_template('auth/register.html',title="Enregistrement")

# Route pour la page pour generer un clé
@Fauth.route('/empl/enregistrement', methods=['GET', 'POST'])
def enregistrement_empl():
    if session['loggedin'] == True:
        # Vérifie si un utilisateur ou un email existe déjà avec les informations fournies
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute( "SELECT * FROM employee WHERE id = %s", [session['id']])
        empl = cursor.fetchone()

        if request.method == 'POST':
            # Créer des variables pour un accès facile
            adresse = request.form['adresse']
            city = request.form['city']
            country = request.form['country']
            password = request.form['password']
            password_repeat = request.form['password_repeat']

            if password != password_repeat:
                flash("Les mots de passe ne sont pas identiques!", "danger")

            else:
                password_hash = hashlib.md5(password.encode('utf8')).hexdigest()

                cursor.execute('UPDATE employee SET adresse = %s, city = %s, country = %s, password = %s, register = %s WHERE ID = %s', (adresse, city, country, password_hash, "True", session['id']))
                mysql.connection.commit()

                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute( "SELECT * FROM employee WHERE id = %s", [session['id']])
                emplnew = cursor.fetchone()

                session['loggedin'] = True
                session['istech'] = False
                session['id'] = emplnew['id']
                session['username'] = emplnew['username']
                session['firstname'] = emplnew['firstname']
                session['lastname'] = emplnew['lastname']
                session['password'] = emplnew['password']
                session['email'] = emplnew['email']
                session['adresse'] = emplnew['adresse']
                session['city'] = emplnew['city']
                session['country'] = emplnew['country']
                return redirect(url_for('Fticket.create_ticket'))
            
        elif request.method == 'POST':
            # Affiche un message si le formulaire est incomplet
            flash("Remplissez le formulaire !", "danger")

    else: 
        return url_for('Fauth.login_empl')

    return render_template('auth/register_employe.html', title="Utilisateur")
    

    

# Route pour la page de mot de passe oublié
@Fauth.route('/mdp_oublie', methods=['GET', 'POST'])
def forgot_password():

    # Si la méthode est POST et que le champ 'email' est rempli
    if request.method == 'POST' and 'email' in request.form:
        
        # Génération d'un nouveau mot de passe aléatoire
        characters = "01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ&*(){}[]|/\?!@#$%^abcdefghijklmnopqrstuvwxyz"
        new_password = "".join(random.sample(characters, 15))

        # Récupération de l'email et hachage du mot de passe
        email = request.form['email']
        password_hash = hashlib.md5(new_password.encode('utf8')).hexdigest()
            
        # Mise à jour du mot de passe dans la base de données
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE accounts SET password = %s WHERE email = %s', (password_hash, email))
        mysql.connection.commit()

        # Envoi d'un email au utilisateur avec le nouveau mot de passe
        flash("L'email à été envoyer avec succès !", "success")
        user_forgot_password(email, new_password)

        # Redirection vers la page de mot de passe oublié
        return redirect(url_for('Fauth.forgot_password'))

    # Si le formulaire n'est pas rempli correctement
    elif request.method == 'POST':
        flash("Veuillez remplir tout les champs !", "danger")

    # Affichage de la page de mot de passe oublié
    return render_template('auth/forgot_password.html',title="Login")


# Route pour la page de mot de passe oublié
@Fauth.route('/empl/mdp_oublie', methods=['GET', 'POST'])
def forgot_password_empl():

    # Si la méthode est POST et que le champ 'email' est rempli
    if request.method == 'POST' and 'email' in request.form:
        
        # Génération d'un nouveau mot de passe aléatoire
        characters = "01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ&*(){}[]|/\?!@#$%^abcdefghijklmnopqrstuvwxyz"
        new_password = "".join(random.sample(characters, 15))

        # Récupération de l'email et hachage du mot de passe
        email = request.form['email']
        password_hash = hashlib.md5(new_password.encode('utf8')).hexdigest()
            
        # Mise à jour du mot de passe dans la base de données
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE accounts SET password = %s WHERE email = %s', (password_hash, email))
        mysql.connection.commit()

        # Envoi d'un email au utilisateur avec le nouveau mot de passe
        flash("L'email à été envoyer avec succès !", "success")
        user_forgot_password(email, new_password)

        # Redirection vers la page de mot de passe oublié
        return redirect(url_for('Fauth.forgot_password'))

    # Si le formulaire n'est pas rempli correctement
    elif request.method == 'POST':
        flash("Veuillez remplir tout les champs !", "danger")

    # Affichage de la page de mot de passe oublié
    return render_template('mobile/forgot_password.html',title="Login")


# Route pour la page de deconnexion
@Fauth.route('/deconnexion')
def logout():

    # Effacer les données de session
    session.clear()

    # Mettre à jour l'état de connexion à déconnecté
    session['loggedin'] = False

    # Afficher l'état de connexion pour vérification
    print(session['loggedin'])

    # Rediriger l'utilisateur vers la page de connexion
    return redirect(url_for('Fauth.login'))


# Route pour la page de deconnexion
@Fauth.route('/empl/deconnexion')
def logout_empl():

    # Effacer les données de session
    session.clear()

    # Mettre à jour l'état de connexion à déconnecté
    session['loggedin'] = False

    # Afficher l'état de connexion pour vérification
    print(session['loggedin'])

    # Rediriger l'utilisateur vers la page de connexion
    return redirect(url_for('Fauth.login_empl'))