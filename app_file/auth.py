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

# Importer le module Fauth
@Fauth.route('/empl/connexion', methods=['GET', 'POST'])
def login_empl():
    
    # Si la méthode de la requête est POST et que les champs username et password sont présents dans le formulaire
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
         
        # Récupérer les valeurs des champs username et password
        username = request.form['username']
        password = request.form['password']
        
        # Hacher le mot de passe avec l'algorithme MD5
        hashpass = hashlib.md5(password.encode('utf8')).hexdigest()
            
        
        # Créer un curseur pour exécuter des requêtes SQL sur la base de données MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Exécuter une requête pour sélectionner l'employé qui correspond au username et au mot de passe haché
        cursor.execute('SELECT * FROM employee WHERE username = %s AND password = %s', (username, hashpass))
        # Récupérer le résultat de la requête sous forme de dictionnaire
        account = cursor.fetchone()
        
        # Si le compte existe
        if account:

            # Si le compte n'est pas encore enregistré
            if account['register'] == "False":
                # Créer une session avec les informations du compte
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                session['firstname'] = account['firstname']
                session['lastname'] = account['lastname']
                session['email'] = account['email']
                
                # Rediriger vers la page d'enregistrement de l'employé
                return redirect(url_for('Fauth.enregistrement_empl'))
            
            # Sinon, si le compte est déjà enregistré
            else:
                # Créer une session avec les informations du compte
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
                
                # Rediriger vers la page de création de ticket
                return redirect(url_for('Fticket.create_ticket'))

        # Sinon, si le compte n'existe pas
        else:
            # Afficher un message d'erreur indiquant que le nom d'utilisateur ou le mot de passe est incorrect
            flash("Utilisateur ou mot de passe incorrect!", "danger")

    # Sinon, si la méthode de la requête est POST mais que les champs username et password ne sont pas présents dans le formulaire
    elif request.method == 'POST':
        
        # Afficher un message d'erreur indiquant qu'il faut remplir le formulaire
        flash("Remplissez le formulaire!", "danger")
    
    # Renvoyer le template HTML de la page de connexion
    return render_template('mobile/login.html',title="Connexion")

    
# Importer le module Fauth
@Fauth.route('/connexion', methods=['GET', 'POST'])
def login():
    
    # Si la méthode de la requête est POST et que les champs username et password sont présents dans le formulaire
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        
        # Récupérer les valeurs des champs username et password
        username = request.form['username']
        password = request.form['password']
        
        # Hacher le mot de passe avec l'algorithme MD5
        hashpass = hashlib.md5(password.encode('utf8')).hexdigest()
        
        # Créer un curseur pour exécuter des requêtes SQL sur la base de données MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Exécuter une requête pour sélectionner le compte qui correspond au username et au mot de passe haché
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, hashpass))
        # Récupérer le résultat de la requête sous forme de dictionnaire
        account = cursor.fetchone()
        
        # Si le compte existe
        if account:
                
            # Exécuter une requête pour compter le nombre total de comptes dans la base de données
            total_accounts = cursor.execute('SELECT * FROM `accounts`')
            # Créer une session avec les informations du compte et le nombre total de comptes
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
            session['telephone'] = account['telephone']
            
            # Rediriger vers la page d'accueil
            return redirect(url_for('Fhome.home'))
                
        # Sinon, si le compte n'existe pas
        else:
            # Afficher un message d'erreur indiquant que le nom d'utilisateur ou le mot de passe est incorrect
            flash("Utilisateur ou mot de passe incorrect!", "danger")
    elif request.method == 'POST':
        # Sinon, si la méthode de la requête est POST mais que les champs username et password ne sont pas présents dans le formulaire
        
        # Afficher un message d'erreur indiquant qu'il faut remplir le formulaire
        flash("Remplissez le formulaire!", "danger")
    
    # Renvoyer le template HTML de la page de connexion, en changeant le chemin du fichier par rapport au code précédent
    return render_template('auth/login.html',title="Connexion")


# Importer le module Fauth
@Fauth.route('/enregistrement', methods=['GET', 'POST'])
def register():
    
    # Si la méthode de la requête est POST et que tous les champs du formulaire sont présents
    if request.method == 'POST' and 'file' and 'username' in request.form and 'firstname' in request.form and 'lastname' in request.form and 'password' in request.form and 'password_repeat' in request.form and 'email' in request.form and 'adresse' in request.form and 'city' in request.form and 'country' in request.form:
        
        # Récupérer les valeurs des champs du formulaire
        username = request.form['username']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        password = request.form['password']
        password_repeat = request.form['password_repeat']
        email = request.form['email']
        telephone = request.form['telephone']
        adresse = request.form['adresse']
        city = request.form['city']
        country = request.form['country']
        photo = request.files['file']
        keygen = request.form['keygen']
        
        # Créer un curseur pour exécuter des requêtes SQL sur la base de données MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Exécuter une requête pour vérifier si le username ou l'email existe déjà dans la table accounts
        cursor.execute( "SELECT * FROM accounts WHERE username LIKE %s OR email LIKE %s", (username, email))
        # Récupérer le résultat de la requête sous forme de dictionnaire
        account = cursor.fetchone()
        
        # Si le compte existe déjà
        if account:
            # Afficher un message d'erreur indiquant que l'utilisateur ou l'email existe déjà
            flash("L'utilisateur ou l'email existe déjà!", "danger")
        
        # Sinon, si l'email n'est pas valide selon une expression régulière
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            # Afficher un message d'erreur indiquant que l'adresse email est invalide
            flash("Adresse e-mail invalide!", "danger")
        
        # Sinon, si le username ne contient pas que des caractères selon une expression régulière
        elif not re.match(r'[A-Za-z]+', username):
            # Afficher un message d'erreur indiquant que le nom d'utilisateur ne doit contenir que des caractères
            flash("Le nom d'utilisateur ne doit contenir que des caractères!", "danger")
            
        
        # Sinon, si un des champs du formulaire est vide
        elif not username or not password or not email or not adresse or not city or not country or not firstname or not lastname or not telephone:
            # Afficher un message d'erreur indiquant qu'il faut remplir tout le champs
            flash("Veuillez remplir tout le champs!", "danger")
        
        # Sinon, si le mot de passe et sa confirmation ne sont pas identiques
        elif password != password_repeat:
            # Afficher un message d'erreur indiquant que les mots de passe ne sont pas identiques
            flash("Les mots de passe ne sont pas identiques!", "danger")
        
        # Sinon, si tous les champs sont valides
        else:
            # Exécuter une requête pour vérifier si la clé de création existe dans la table keycreate
            cursor.execute( "SELECT * FROM keycreate WHERE `key` LIKE %s", [keygen] )
            # Récupérer le résultat de la requête sous forme de dictionnaire
            keyregf = cursor.fetchone()
            
            # Si la clé existe
            if keyregf:
                
                # Si aucune photo n'est fournie
                if not photo:
                    # Définir l'url par défaut de la photo de profil
                    fullprofilepic_url = "static/uploads/pp/0e59a2d2-8545-11ed-a345-38c9861edab2.png"
                else:
                    # Sinon, si une photo est fournie
                    
                    # Récupérer le fichier photo
                    photo = request.files['file']
                    # Générer un nom unique pour la photo avec l'extension .png
                    profilepic_name = str(uuid.uuid1())+'.png'
                    # Définir l'url de la photo en fonction du nom généré et du dossier où elle sera enregistrée
                    profilepic_url = 'static/uploads/pp/'+profilepic_name
                    fullprofilepic_url = profilepic_url
                
                # Si le fichier à l'url de la photo existe déjà
                if os.path.isfile(fullprofilepic_url) == True:
                    # Supprimer le fichier existant
                    os.remove(fullprofilepic_url)
                
                # Enregistrer le fichier photo dans le dossier spécifié
                photo.save(os.path.join("static/uploads/pp/", profilepic_name))
                
                # Hacher le mot de passe avec l'algorithme MD5
                password_hash = hashlib.md5(password.encode('utf8')).hexdigest()
                
                # Supprimer la clé de création de la table keycreate
                cursor.execute('DELETE FROM keycreate WHERE `key` LIKE %s', [keygen])
                
                # Insérer les informations du compte dans la table accounts
                cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (username, email, password_hash, firstname, lastname, adresse, city, country, fullprofilepic_url, telephone))
                # Valider les changements dans la base de données
                mysql.connection.commit()
                
                # Afficher un message de succès indiquant que le compte a été créé et que la clé a été supprimée
                flash("Votre compte a été créé avec succès, la clé a été supprimée du registre!", "success")
                
                # Envoyer un mail de confirmation au compte créé
                mail_account_register(email, firstname, lastname)
                
            else:
                
                # Sinon, si la clé n'existe pas
                
                # Afficher un message d'erreur indiquant que la clé de création n'existe pas
                flash("La clé de création n'existe pas!", "success")
    elif request.method == 'POST':
        
        # Sinon, si la méthode de la requête est POST mais que tous les champs du formulaire ne sont pas présents
        
        # Afficher un message d'erreur indiquant qu'il faut remplir le formulaire
        flash("Remplissez le formulaire!", "danger")
    
    # Renvoyer le template HTML de la page d'enregistrement
    return render_template('auth/register.html',title="Enregistrement")

# Importer le module Fauth
@Fauth.route('/empl/enregistrement', methods=['GET', 'POST'])
def enregistrement_empl():
    # Si la session est active
    if session['loggedin'] == True:
        
        # Créer un curseur pour exécuter des requêtes SQL sur la base de données MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Exécuter une requête pour sélectionner l'employé qui correspond à l'id de la session
        cursor.execute( "SELECT * FROM employee WHERE id = %s", [session['id']])
        # Récupérer le résultat de la requête sous forme de dictionnaire
        empl = cursor.fetchone()
        
        # Si la méthode de la requête est POST
        if request.method == 'POST':
            
            # Récupérer les valeurs des champs du formulaire
            adresse = request.form['adresse']
            city = request.form['city']
            country = request.form['country']
            password = request.form['password']
            password_repeat = request.form['password_repeat']
            
            # Si le mot de passe et sa confirmation ne sont pas identiques
            if password != password_repeat:
                # Afficher un message d'erreur indiquant que les mots de passe ne sont pas identiques
                flash("Les mots de passe ne sont pas identiques!", "danger")
            
            # Sinon, si les mots de passe sont identiques
            else:
                
                # Hacher le mot de passe avec l'algorithme MD5
                password_hash = hashlib.md5(password.encode('utf8')).hexdigest()
                
                # Exécuter une requête pour mettre à jour les informations de l'employé dans la table employee, en indiquant que le compte est enregistré
                cursor.execute('UPDATE employee SET adresse = %s, city = %s, country = %s, password = %s, register = %s WHERE ID = %s', (adresse, city, country, password_hash, "True", session['id']))
                # Valider les changements dans la base de données
                mysql.connection.commit()
                
                # Créer un nouveau curseur pour exécuter des requêtes SQL sur la base de données MySQL
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                # Exécuter une requête pour sélectionner l'employé qui correspond à l'id de la session
                cursor.execute( "SELECT * FROM employee WHERE id = %s", [session['id']])
                # Récupérer le résultat de la requête sous forme de dictionnaire
                emplnew = cursor.fetchone()
                
                # Créer une session avec les informations du compte mis à jour
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
                
                # Rediriger vers la page de création de ticket
                return redirect(url_for('Fticket.create_ticket'))
        
        # Sinon, si la méthode de la requête est POST mais que tous les champs du formulaire ne sont pas présents
        elif request.method == 'POST':
            # Afficher un message d'erreur indiquant qu'il faut remplir le formulaire
            flash("Remplissez le formulaire!", "danger")
    else: 
        # Sinon, si la session n'est pas active
        
        # Rediriger vers la page de connexion de l'employé
        return url_for('Fauth.login_empl')
    
    # Renvoyer le template HTML de la page d'enregistrement de l'employé
    return render_template('auth/register_employe.html', title="Enregistrement")

    
    
# Importer le module Fauth
@Fauth.route('/mdp_oublie', methods=['GET', 'POST'])
def forgot_password():
    
    # Si la méthode de la requête est POST et que le champ email est présent dans le formulaire
    if request.method == 'POST' and 'email' in request.form:
        
        
        # Définir une chaîne de caractères possibles pour générer un nouveau mot de passe
        characters = "01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ&*(){}[]|/\?!@#"
        # Générer un nouveau mot de passe aléatoire de 15 caractères à partir de la chaîne
        new_password = "".join(random.sample(characters, 15))
        
        # Récupérer la valeur du champ email
        email = request.form['email']
        
        # Si l'email est vide
        if email == "":
            # Afficher un message d'erreur indiquant qu'il faut remplir l'email
            flash("Veuillez remplir votre email!", "danger")
        
        # Sinon, si l'email est valide
        else:
            
            
            # Hacher le nouveau mot de passe avec l'algorithme MD5
            password_hash = hashlib.md5(new_password.encode('utf8')).hexdigest()
                
            
            # Créer un curseur pour exécuter des requêtes SQL sur la base de données MySQL
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # Exécuter une requête pour mettre à jour le mot de passe du compte qui correspond à l'email
            cursor.execute('UPDATE accounts SET password = %s WHERE email = %s', (password_hash, email))
            # Valider les changements dans la base de données
            mysql.connection.commit()
            
            # Afficher un message de succès indiquant que l'email a été envoyé avec le nouveau mot de passe
            flash("L'email a été envoyé avec succès!", "success")
            
            # Envoyer un mail au compte avec le nouveau mot de passe
            user_forgot_password(email, new_password)
        
        # Rediriger vers la page de mot de passe oublié
        return redirect(url_for('Fauth.forgot_password'))
    
    # Sinon, si la méthode de la requête est POST mais que le champ email n'est pas présent dans le formulaire
    elif request.method == 'POST':
        
        # Afficher un message d'erreur indiquant qu'il faut remplir tous les champs
        flash("Veuillez remplir tout les champs!", "danger")
    
    # Renvoyer le template HTML de la page de mot de passe oublié
    return render_template('auth/forgot_password.html',title="Mot de passe oublié")

# Importer le module Fauth
@Fauth.route('/empl/mdp_oublie', methods=['GET', 'POST'])
def forgot_password_empl():
    
    # Si la méthode de la requête est POST et que le champ email est présent dans le formulaire
    if request.method == 'POST' and 'email' in request.form:
        
        
        # Définir une chaîne de caractères possibles pour générer un nouveau mot de passe
        characters = "01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ&*(){}[]|/\?!@#"
        # Générer un nouveau mot de passe aléatoire de 15 caractères à partir de la chaîne
        new_password = "".join(random.sample(characters, 15))
        
        # Récupérer la valeur du champ email
        email = request.form['email']
        
        # Si l'email est vide
        if email == "":
            # Afficher un message d'erreur indiquant qu'il faut remplir l'email
            flash("Veuillez remplir votre email!", "danger")
        
        # Sinon, si l'email est valide
        else:
           
            # Hacher le nouveau mot de passe avec l'algorithme MD5
            password_hash = hashlib.md5(new_password.encode('utf8')).hexdigest()
                
            
            # Créer un curseur pour exécuter des requêtes SQL sur la base de données MySQL
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # Exécuter une requête pour mettre à jour le mot de passe de l'employé qui correspond à l'email
            cursor.execute('UPDATE employee SET password = %s WHERE email = %s', (password_hash, email))
            # Valider les changements dans la base de données
            mysql.connection.commit()
            
            # Afficher un message de succès indiquant que l'email a été envoyé avec le nouveau mot de passe
            flash("L'email a été envoyé avec succès!", "success")
            
            # Envoyer un mail à l'employé avec le nouveau mot de passe
            user_forgot_password(email, new_password)
            
            # Rediriger vers la page de mot de passe oublié de l'employé
            return redirect(url_for('Fauth.forgot_password_empl'))
    
    elif request.method == 'POST':
        # Sinon, si la méthode de la requête est POST mais que le champ email n'est pas présent dans le formulaire
        
        # Afficher un message d'erreur indiquant qu'il faut remplir tous les champs
        flash("Veuillez remplir tout les champs!", "danger")
    
    # Renvoyer le template HTML de la page de mot de passe oublié de l'employé
    return render_template('auth/forgot_password.html',title="Mot de passe oublié")

# Importer le module Fauth
@Fauth.route('/deconnexion')
def logout():
    
    # Effacer les données de la session
    session.clear()
    
    # Indiquer que la session n'est plus active
    session['loggedin'] = False
    
    # Rediriger vers la page de connexion
    return redirect(url_for('Fauth.login'))

# Importer le module Fauth
@Fauth.route('/empl/deconnexion')
def logout_empl():
    
    # Effacer les données de la session
    session.clear()
    
    # Indiquer que la session n'est plus active
    session['loggedin'] = False
    
    # Rediriger vers la page de connexion de l'employé
    return redirect(url_for('Fauth.login_empl'))
