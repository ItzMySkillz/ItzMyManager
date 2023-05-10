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
import csv
from ldap3 import *
from ldap3.core.exceptions import LDAPBindError, LDAPSocketOpenError, LDAPInvalidCredentialsResult

# Création d'un blueprint pour la partie profile
Fprofile = Blueprint('Fprofile', __name__)

# Route pour la page de tout les profiles technicien
@Fprofile.route('/profiles/tech', methods=['GET', 'POST'])
def profiles_tech():
    
    # Vérifie si l'utilisateur est connecté en vérifiant la valeur de la clé 'loggedin' dans le dictionnaire de session
    if session['loggedin'] == True and session['istech'] == True:

        # Crée un curseur pour une connexion MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Exécute une requête pour sélectionner toutes les entrées de la table 'accounts'
        cursor.execute('SELECT * FROM accounts')

        # Récupère les résultats de la requête
        all_account = cursor.fetchall()

        # Rend la template "all_profile.html" avec les arguments appropriés
        return render_template('home/all_profile.html', username=session['username'], title="Utilisateurs", all_account = all_account, technicien=True)

    # Si l'utilisateur n'est pas connecté, redirige vers la page de connexion
    return redirect(url_for('Fauth.login')) 


# Route pour la page de tout les profiles employers
@Fprofile.route('/profiles/empl')
def profiles_empl():

    # Vérifie si l'utilisateur est connecté en vérifiant la valeur de la clé 'loggedin' dans le dictionnaire de session
    if session['loggedin'] == True and session['istech'] == True:

        # Crée un curseur pour une connexion MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Exécute une requête pour sélectionner toutes les entrées de la table 'employee'
        cursor.execute('SELECT * FROM employee')

        # Récupère les résultats de la requête
        all_account = cursor.fetchall()

        # Rend la template "all_profile.html" avec les arguments appropriés
        return render_template('home/all_profile.html', username=session['username'], title="Utilisateurs", all_account = all_account, technicien=False)

    # Si l'utilisateur n'est pas connecté, redirige vers la page de connexion
    return redirect(url_for('Fauth.login'))


# Route pour la page de tout profile de l'utilisateur
@Fprofile.route('/profile')
def profile():

    # Vérifie si l'utilisateur est connecté en vérifiant la valeur de la clé 'loggedin' dans le dictionnaire de session
    if session['loggedin'] == True and session['istech'] == True:

        # Vérifie si l'utilisateur est un utilisateur normal ou un administrateur
        if session['id'] == 1:
            print("User")

            # Si l'utilisateur est un utilisateur normal, rend la template avec l'argument isKey=True
            return render_template('auth/profile.html', username=session['username'], title="Profile", isKey=True)
        else:
            print("Admin")

            # Si l'utilisateur est un administrateur, rend la template avec l'argument isKey=False
            return render_template('auth/profile.html', username=session['username'], title="Profile", isKey=False)

    # Si l'utilisateur n'est pas connecté, redirige vers la page de connexion
    return redirect(url_for('Fauth.login')) 


# Route pour la page de tout profile de l'utilisateur
@Fprofile.route('/empl/profile')
def profile_me():

    # Vérifie si l'utilisateur est connecté en vérifiant la valeur de la clé 'loggedin' dans le dictionnaire de session
    if session['loggedin'] == True:

        # Rend la template pour les mobiles
        return render_template('mobile/profile.html', username=session['username'], title="Profile")

    # Si l'utilisateur n'est pas connecté, redirige vers la page de connexion
    return redirect(url_for('Fauth.login_empl')) 


# Route pour la page de tout profile de l'employer
@Fprofile.route('/profiles/empl/empl', methods=['GET', 'POST'])
def profile_empl():

    # Vérifie si l'utilisateur est connecté en vérifiant la valeur de la clé 'loggedin' dans le dictionnaire de session
    if session['loggedin'] == True and session['istech'] == True:

        # Récupère l'ID de l'utilisateur à partir de la requête
        user_id = request.values.get("user_id")
        user_id_args = request.args.get("user_id")
        print(user_id_args)

        # Crée un curseur pour une connexion MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Exécute une requête pour sélectionner l'entrée de la table 'employee' correspondant à l'ID de l'utilisateur
        cursor.execute('SELECT * FROM employee  WHERE ID = %s', [user_id_args])

        # Récupère les résultats de la requête
        other_account = cursor.fetchone()
        
        # Rend la template "other_profile.html" avec les arguments appropriés
        return render_template('auth/other_profile.html', username=session['username'], title="Utilisateur", other_account=other_account, technicien = False) 

    # Si l'utilisateur n'est pas connecté, redirige vers la page de connexion
    return redirect(url_for('Fauth.login'))


# Route pour la page de tout profile du technicien
@Fprofile.route('/profile/tech/tech', methods=['GET', 'POST'])
def profile_tech():

    # Vérifie si l'utilisateur est connecté en vérifiant la valeur de la clé 'loggedin' dans le dictionnaire de session
    if session['loggedin'] == True and session['istech'] == True:

        # Récupère l'ID de l'utilisateur à partir de la requête
        user_id = request.values.get("user_id")
        user_id_args = request.args.get("user_id")
        print(user_id_args)

        # Crée un curseur pour une connexion MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Exécute une requête pour sélectionner l'entrée de la table 'accounts' correspondant à l'ID de l'utilisateur
        cursor.execute('SELECT * FROM accounts WHERE ID = %s', [user_id])

        # Récupère les résultats de la requête
        other_account = cursor.fetchone()

        # Vérifie si l'utilisateur actuel est un administrateur ou un utilisateur normal et si l'utilisateur affiché est l'administrateur
        if session['id'] == 1:
            if int(user_id) == 1:
                print("AdminAdmin")

                # Si l'utilisateur actuel est un administrateur et l'utilisateur affiché est l'administrateur, rend la template avec l'argument delete=False
                return render_template('auth/other_profile.html', username=session['username'], title="Utilisateur", other_account=other_account, delete = False, technicien = True) 
            else:
                print("Admin")

                # Si l'utilisateur actuel est un administrateur et l'utilisateur affiché n'est pas l'administrateur, rend la template avec l'argument delete=True
                return render_template('auth/other_profile.html', username=session['username'], title="Utilisateur", other_account=other_account, delete= True, technicien = True) 
        else:
            print("User")

            # Si l'utilisateur actuel n'est pas un administrateur, rend la template avec l'argument delete=False
            return render_template('auth/other_profile.html', username=session['username'], title="Utilisateur", other_account=other_account, delete = False, technicien = True) 

    # Si l'utilisateur n'est pas connecté, redirige vers la page de connexion
    return redirect(url_for('Fauth.login'))

# Route pour la page de creation de compte
@Fprofile.route('/profile/creation/tech', methods=['GET', 'POST'])
def create_account_tech():

    # Vérifie si l'utilisateur est connecté en vérifiant la valeur de la clé 'loggedin' dans le dictionnaire de session
    if session['loggedin'] == True and session['istech'] == True:

         # Si l'utilisateur a soumis un formulaire
        if request.method == 'POST' and 'username' in request.form and 'firstname' in request.form and 'lastname' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'telephone' in request.form:
            
            # Créer des variables pour un accès facile
            username = request.form['username']
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            email = request.form['email']
            adresse = request.form['address']
            city = request.form['city']
            country = request.form['country']
            telephone = request.form['telephone']
            
            # Crée un curseur pour une connexion MySQL
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            
            # Verifiera dans technicien si le compte existe
            cursor.execute( "SELECT * FROM accounts WHERE username LIKE %s OR email LIKE %s", (username, email))
            account = cursor.fetchone()
                
            # Si le compte existe, afficher une erreur et des vérifications de validation
            if account:
                flash("L'utilisateur ou l'email existe déjà!", "danger")
            
             # Vérifie si l'adresse email est valide
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash("Adresse e-mail invalide!", "danger")
            
            # Vérifie si le nom d'utilisateur ne contient que des caractères
            elif not re.match(r'[A-Za-z]+', username):
                flash("Le nom d'utilisateur ne doit contenir que des caractères!", "danger")
            
            # Vérifie si tous les champs ont été remplis
            elif not username or not email or not adresse or not city or not country or not firstname or not lastname or not telephone:
                flash("Veuillez remplir tout le champs !", "danger")
            else:

                # Choix de un photo de profile predefinie
                fullprofilepic_url = "uploads/pp/0e59a2d2-8545-11ed-a345-38c9861edab2.png"

                # Genere un mot de passe chiffrer en hash md5
                characters = "01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ&*(){}[]|/\?!@#$%^abcdefghijklmnopqrstuvwxyz"
                password = "".join(random.sample(characters, 15))
                password_hash = hashlib.md5(password.encode('utf8')).hexdigest()

                # Ajoute les informations de l'utilisateur à la base de données
                cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (username, email, password_hash, firstname, lastname, adresse, city, country, fullprofilepic_url, telephone))
                mysql.connection.commit()
            
                # Affiche un message de succès
                flash("Votre compte a été créé avec succès", "success")

                # Envoie un email à l'utilisateur avec ces données
                user_password = password
                create_account_mail(email, firstname, lastname, username, adresse, city, country, user_password)

        elif request.method == 'POST':
            # Affiche un message si le formulaire est incomplet
            flash("Remplissez le formulaire !", "danger")
        
        # Affichage la template de la page creation de profile
        return render_template('home/create_profile_tech.html', username=session['username'], title="Utilisateur") 

    # Si l'utilisateur n'est pas connecté, redirige vers la page de connexion
    return redirect(url_for('Fauth.login'))

# Route pour la page de creation de compte
@Fprofile.route('/profile/creation/empl', methods=['GET', 'POST'])
def create_account_empl():

    # Vérifie si l'utilisateur est connecté en vérifiant la valeur de la clé 'loggedin' dans le dictionnaire de session
    if session['loggedin'] == True and session['istech'] == True:

         # Si l'utilisateur a soumis un formulaire
        if request.method == 'POST' and 'username' in request.form and 'firstname' in request.form and 'lastname' in request.form and 'email' in request.form:
            
            
            # Créer des variables pour un accès facile
            username = request.form['username']
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            email = request.form['email']
            
            # Crée un curseur pour une connexion MySQL
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            # Verifiera dans employer si le compte existe
            cursor.execute( "SELECT * FROM employee WHERE username LIKE %s OR email LIKE %s", (username, email))
            account = cursor.fetchone()
            
            # Si le compte existe, afficher une erreur et des vérifications de validation
            if account:
                flash("L'utilisateur ou l'email existe déjà!", "danger")
            
             # Vérifie si l'adresse email est valide
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash("Adresse e-mail invalide!", "danger")
            
            # Vérifie si le nom d'utilisateur ne contient que des caractères
            elif not re.match(r'[A-Za-z]+', username):
                flash("Le nom d'utilisateur ne doit contenir que des caractères!", "danger")
            
            # Vérifie si tous les champs ont été remplis
            elif not username or not email or not firstname or not lastname:
                flash("Veuillez remplir tout le champs !", "danger")

            else:

                # Genere un mot de passe chiffrer en hash md5
                characters = "01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ&*(){}[]|/?!@#$%^abcdefghijklmnopqrstuvwxyz"
                password = "".join(random.sample(characters, 15))
                password_hash = hashlib.md5(password.encode('utf8')).hexdigest()

                # Ajoute les informations de l'utilisateur à la base de données
                cursor.execute('INSERT INTO employee VALUES (NULL, %s, %s, %s, %s, %s, "", "", "", %s)', (username, email, firstname, lastname, password_hash, "False"))
                mysql.connection.commit()
                    
                # Affiche un message de succès
                flash("Votre compte a été créé avec succès", "success")

                # Envoie un email à l'utilisateur avec ces données
                user_password = password
                create_empl_mail(email, firstname, lastname, username, user_password)


        elif request.method == 'POST':
            # Affiche un message si le formulaire est incomplet
            flash("Remplissez le formulaire !", "danger")
        
        # Affichage la template de la page creation de profile
        return render_template('home/create_profile.html', username=session['username'], title="Utilisateur") 

    # Si l'utilisateur n'est pas connecté, redirige vers la page de connexion
    return redirect(url_for('Fauth.login'))


# Route pour la page de suppression de compte technicien
@Fprofile.route('/profile/tech/suppresion', methods=['GET', 'POST'])
def delete_account():

    # Vérifie si l'utilisateur est connecté
    if session['loggedin'] == True and session['istech'] == True:

        # Récupère l'ID de l'utilisateur à supprimer à partir de la requête GET
        user_id_args = request.args.get("usertodelete")
        print(user_id_args)

        # Crée un curseur pour exécuter des requêtes MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Supprime l'utilisateur correspondant à l'ID récupéré de la table 'accounts'
        cursor.execute('DELETE FROM `accounts` WHERE `id` = %s', [user_id_args])
        mysql.connection.commit()

        # Met à jour le nombre total de comptes dans l'objet session
        total_accounts1 = cursor.execute('SELECT * FROM `employee`')
        total_accounts2 = cursor.execute('SELECT * FROM `accounts`')
        session['total_accounts'] = total_accounts1 + total_accounts2

        # Envoie un message de succès et redirige vers la page 'profiles_tech'
        flash("Le compte a été supprimé avec succès !", "success")
        return redirect(url_for('Fprofile.profiles_tech'))

    # Si l'utilisateur n'est pas connecté, redirige vers la page de connexion
    return redirect(url_for('Fauth.login'))


# Route pour la page de suppression de compte employer
@Fprofile.route('/profile/empl/suppression', methods=['GET', 'POST'])
def delete_empl():
    
    # Vérifie si l'utilisateur est connecté
    if session['loggedin'] == True and session['istech'] == True:

        # Récupère l'ID de l'utilisateur à supprimer à partir de la requête GET
        user_id_args = request.args.get("usertodelete")
        print(user_id_args)

        # Crée un curseur pour exécuter des requêtes MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Supprime l'utilisateur correspondant à l'ID récupéré de la table 'employee'
        cursor.execute('DELETE FROM `employee` WHERE `id` = %s', [user_id_args])
        mysql.connection.commit()

        # Met à jour le nombre total de comptes dans l'objet session
        total_accounts1 = cursor.execute('SELECT * FROM `employee`')
        total_accounts2 = cursor.execute('SELECT * FROM `accounts`')
        session['total_accounts'] = total_accounts1 + total_accounts2

        # Envoie un message de succès et redirige vers la page 'profiles_empl'
        flash("Le compte a été supprimé avec succès !", "success")
        return redirect(url_for('Fprofile.profiles_empl'))

    # Si l'utilisateur n'est pas connecté, redirige vers la page de connexion
    return redirect(url_for('Fauth.login'))


# Route pour la page pour changer de photo de profile
@Fprofile.route('/profile/update/photo', methods=['GET', 'POST'])
def change_photo():

    # Vérifie si la méthode de la requête est POST et s'il y a un "file_change" dans la requête
    if request.method == 'POST' and 'file_change':

        # Récupère la nouvelle photo de profil de la requête
        photo_ch = request.files['file_change']

        # Vérifie si la photo de profil est valide
        if not photo_ch:
            flash("Veuillez ajouter votre photo de profile !", "danger")
        else:

            # Donne un nom unique à l'image
            profilepic_name_ch = str(uuid.uuid1())+'.png'
            profilepic_url_ch = 'uploads/pp/'+profilepic_name_ch
            fullprofilepic_url_ch = profilepic_url_ch

            # Enregistre l'image dans le répertoire "static/uploads/pp/"
            photo_ch.save(os.path.join("static/uploads/pp/", profilepic_name_ch))
            
            # Crée un curseur pour exécuter des requêtes MySQL
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            # Met à jour la colonne 'profilepic' de l'utilisateur avec la nouvelle photo de profil dans la table 'accounts'
            cursor.execute('UPDATE accounts SET profilepic = %s WHERE ID = %s', (fullprofilepic_url_ch, session['id']))
            mysql.connection.commit()

            # Met à jour l'objet session avec la nouvelle photo de profil
            session['profilepic'] = fullprofilepic_url_ch

            # Envoie un message de succès et redirige vers la page de profil
            flash("Votre photo de profil à été changer avec succès !", "success")
            return redirect(url_for('Fprofile.profile'))
            
    # Si la requête est de type POST mais il n'y a pas de "file_change"
    elif request.method == 'POST':
        flash("Veuillez ajouter votre photo de profile !", "danger")

    # Redirige vers la page de profil
    return redirect(url_for('Fprofile.profile'))


# Route pour la page pour changer de mot de passe
@Fprofile.route('/profile/update/password', methods=['GET', 'POST'])
def change_pswd():

    # Vérifie si la méthode de la requête est POST et si les champs 'newpswd' et 'newpswd_confirm' sont présents dans la requête
    if request.method == 'POST' and 'newpswd' in request.form and 'newpswd_confirm' in request.form:

        # Récupère les nouveaux mots de passe de la requête
        newpswd = request.form['newpswd']
        newpswd_confirm = request.form['newpswd_confirm']

        # Vérifie si les mots de passe saisis sont identiques
        if newpswd != newpswd_confirm:
            flash("Les mots de passe ne sont pas identiques!", "danger")

        # Vérifie si les champs sont vide
        elif not newpswd or not newpswd_confirm:
            flash("Veuillez remplir tout les champs !", "danger")
        else:

            # Hash le mot de passe
            password_hash = hashlib.md5(newpswd.encode('utf8')).hexdigest()

            # Vérifie si l'utilisateur est mobile ou non
            if session['istech'] == False:

                # Connexion a la base de donnee et mise a jour du mot de passe
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('UPDATE employee SET password = %s WHERE ID = %s', (password_hash, session['id']))
                mysql.connection.commit()

                account = cursor.fetchone()
            elif session['istech'] == True:

                # Connexion a la base de donnee et mise a jour du mot de passe
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('UPDATE accounts SET password = %s WHERE ID = %s', (password_hash, session['id']))
                mysql.connection.commit()

                account = cursor.fetchone()

            # Affichage message de succès
            flash("Votre mot de passe à été changer avec succès !", "success")

            # Ajout des variables pour l'email et envoie de l'email
            lastname = session['lastname']
            firstname = session['firstname']
            email = session['email']
            user_account_password(email, firstname, lastname)

            if session['istech'] == True:
                # Redirection vers la page de base
                return redirect(url_for('Fprofile.profile'))
            elif session['istech'] == False:
                # Redirection vers la page de base
                return redirect(url_for('Fprofile.profile_me'))

    # Si la requête est de type POST mais il n'y a pas les champs 'newpswd' et 'newpswd_confirm'
    elif request.method == 'POST':
        flash("Veuillez remplir tout les champs !", "danger")

    if session['istech'] == True:
        # Redirection vers la page de base
        return redirect(url_for('Fprofile.profile'))
    elif session['istech'] == False:
        # Redirection vers la page de base
        return redirect(url_for('Fprofile.profile_me'))


# Route pour la page pour changer le donnee adresse
@Fprofile.route('/profile/update/info', methods=['GET', 'POST'])
def change_info():

    # Vérifie si la méthode de la requête est POST
    if request.method == 'POST':
        
        # Récupère les nouvelles valeurs de l'adresse de la requête
        new_username = request.form['new_username']
        new_email = request.form['new_email']
        new_firstname = request.form['new_firstname']
        new_lastname = request.form['new_lastname']

        # Récupère les anciennes valeurs de l'adresse de la session
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
                    if session['istech'] == False:
                        cursor.execute('UPDATE employee SET username = %s WHERE ID = %s', (new_username, session['id']))
                        mysql.connection.commit()
                    elif session['istech'] == True: 
                        cursor.execute('UPDATE accounts SET username = %s WHERE ID = %s', (new_username, session['id']))
                        mysql.connection.commit()

                    session['username'] = new_username


            if not new_email:
                print("pass email")
                new_email = old_email
            else:
                if session['istech'] == False:
                    cursor.execute('UPDATE employee SET email = %s WHERE ID = %s', (new_email, session['id']))
                    mysql.connection.commit()  
                elif session['istech'] == True: 
                    cursor.execute('UPDATE accounts SET email = %s WHERE ID = %s', (new_email, session['id']))
                    mysql.connection.commit()
                
                session['email'] = new_email


            if not new_firstname:
                print("pass first name")
                new_firstname = old_firstname
            else:
                if session['istech'] == False:
                    cursor.execute('UPDATE employee SET firstname = %s WHERE ID = %s', (new_firstname, session['id']))
                    mysql.connection.commit()
                elif session['istech'] == True: 
                    cursor.execute('UPDATE accounts SET firstname = %s WHERE ID = %s', (new_firstname, session['id']))
                    mysql.connection.commit()

                session['firstname'] = new_firstname

            if not new_lastname:
                print("pass last name")
                new_lastname = old_lastname
            else:
                if session['istech'] == False:
                    cursor.execute('UPDATE employee SET lastname = %s WHERE ID = %s', (new_lastname, session['id']))
                    mysql.connection.commit()
                elif session['istech'] == True: 
                    cursor.execute('UPDATE accounts SET lastname = %s WHERE ID = %s', (new_lastname, session['id']))
                    mysql.connection.commit()

                session['lastname'] = new_lastname

            account = cursor.fetchone()
            flash("Modification apporté avec succès !", "success")
            user_account_information(new_username, new_email, new_firstname, new_lastname)

            if session['istech'] == True:
                # Redirection vers la page de base
                return redirect(url_for('Fprofile.profile'))
            elif session['istech'] == False:
                # Redirection vers la page de base
                return redirect(url_for('Fprofile.profile_me'))
            
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash("Veuillez remplir minimum un champ !", "danger")

    if session['istech'] == True:
        # Redirection vers la page de base
        return redirect(url_for('Fprofile.profile'))
    elif session['istech'] == False:
        # Redirection vers la page de base
        return redirect(url_for('Fprofile.profile_me'))


# Route pour la page pour changer le donnee adresse
@Fprofile.route('/profile/update/adresse', methods=['GET', 'POST'])
def change_adresse():

    # Vérifie si la méthode de la requête est POST
    if request.method == 'POST':

        # Récupère les nouvelles valeurs de l'adresse de la requête
        new_address = request.form['new_address']
        new_city = request.form['new_city']
        new_country = request.form['new_country']

        # Récupère les anciennes valeurs de l'adresse de la session
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
                if session['istech'] == False:
                    cursor.execute('UPDATE employee SET adresse = %s WHERE ID = %s', (new_address, session['id']))
                    mysql.connection.commit()
                elif session['istech'] == True: 
                    cursor.execute('UPDATE accounts SET adresse = %s WHERE ID = %s', (new_address, session['id']))
                    mysql.connection.commit()


                session['adresse'] = new_address


            if not new_city:
                print("pass city")
                new_city = old_city
            else:
                if session['istech'] == False:
                    cursor.execute('UPDATE employee SET city = %s WHERE ID = %s', (new_city, session['id']))
                    mysql.connection.commit()
                elif session['istech'] == True: 
                    cursor.execute('UPDATE accounts SET city = %s WHERE ID = %s', (new_city, session['id']))
                    mysql.connection.commit()


                session['city'] = new_city


            if not new_country:
                print("pass country")
                new_country = old_country
            else:
                if session['istech'] == False:
                    cursor.execute('UPDATE employee SET country = %s WHERE ID = %s', (new_country, session['id']))
                    mysql.connection.commit()
                elif session['istech'] == True: 
                    cursor.execute('UPDATE accounts SET country = %s WHERE ID = %s', (new_country, session['id']))
                    mysql.connection.commit()


                session['country'] = new_country

            account = cursor.fetchone()
            flash("Modification apporté avec succès !", "success")
            lastname = session['lastname']
            firstname = session['firstname']
            email = session['email']
            user_account_address(new_address, new_city, new_country, lastname, firstname, email)

            if session['istech'] == True:
                # Redirection vers la page de base
                return redirect(url_for('Fprofile.profile'))
            elif session['istech'] == False:
                # Redirection vers la page de base
                return redirect(url_for('Fprofile.profile_me'))
            
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash("Veuillez remplir minimum un champ !", "danger")

    if session['istech'] == True:
        # Redirection vers la page de base
        return redirect(url_for('Fprofile.profile'))
    elif session['istech'] == False:
        # Redirection vers la page de base
        return redirect(url_for('Fprofile.profile_me'))

# Route pour la page pour generer un clé
@Fprofile.route('/profile/keygen', methods=['GET', 'POST'])
def generatekey():

    # Vérifie si la méthode de la requête est POST
    if request.method == 'POST':

        # Crée un curseur pour exécuter des requêtes MySQL
        cursorkey = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Génère une clé aléatoire
        key = str(uuid.uuid1())+str(uuid.uuid1())
        key_tot = 'key.'+key
        print(key_tot)

        # Enregistre la clé générée dans la session
        session['keygenerate'] = key_tot

        # Insère la clé générée dans la table 'keycreate'
        cursorkey.execute('INSERT INTO keycreate VALUES (NULL, %s)', [key_tot])
        mysql.connection.commit()

        # Affichage message de succes
        flash("Clé généré avec succès, après l'utilisation de celle-ci elle sera supprimé!", "success")
        
        # Redirection vers la page de base
        return redirect(url_for('Fprofile.profile'))

    # Si la méthode de la requête n'est pas POST
    elif request.method == 'POST':

        flash("Erreur !", "danger")

    # Redirige vers la page de profil
    return redirect(url_for('Fprofile.profile'))

# Route pour la page pour generer un clé
@Fprofile.route('/importation/csv')
def importation():
    
    return render_template('home/importation.html', username=session['username'], title="Importation via CSV")

# Route pour la page pour generer un clé
@Fprofile.route('/importation/ad')
def importation_ad():
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute( "SELECT * FROM local_import")
    local_import = cursor.fetchall()

    return render_template('home/importation_ad.html', username=session['username'], local_import=local_import, title="Importation via AD")

# Route pour la page pour generer un clé
@Fprofile.route('/import_ad', methods=['GET', 'POST'])
def import_ad():
    # Vérifie si la méthode de la requête est POST
    if request.method == 'POST':
        ip = request.form['ip']
        utilisateur = request.form['utilisateur']
        passwordg = request.form['password']
        domain = request.form['domain']
        ext = request.form['ext']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('TRUNCATE TABLE local_import')
        if ip == "" or utilisateur == "" or passwordg == "" or domain == "" or ext == "":
            flash("Veuillez complèter le formulaire !", "danger")
            return redirect(url_for('Fprofile.importation_ad'))
        else:
            try:
                # Connexion au serveur Active Directory
                server = Server(ip, port=389, get_info=ALL)
                username = utilisateur
                password = passwordg
                ad = Connection(server, user=username, password=password, auto_bind=True)
            
                # Recherche de tous les utilisateurs
                ad.search(search_base=f'DC={domain},DC={ext}', search_filter='(objectClass=user)', attributes=['sAMAccountName', 'givenName', 'sn', 'mail'])

                # Récupération de la liste des utilisateurs
                users = []
                for entry in ad.entries:
                    user = {
                        'username': entry.sAMAccountName,
                        'firstname': entry.givenName,
                        'lastname': entry.sn,
                        'email': entry.mail
                    }
                    users.append(user)

                # Fermeture de la connexion
                ad.unbind()

                # Affichage de la liste des utilisateurs
                for user in users:
                    if not user['lastname'] and not user['firstname'] and not user['email']:
                        pass
                    else:
                            
                        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                        cursor.execute('INSERT INTO local_import(username, lastname, firstname, email, imported) VALUES(%s, %s, %s, %s, %s)', (user['username'], user['lastname'], user['firstname'], user['email'], "False"))
                        mysql.connection.commit()


            except LDAPInvalidCredentialsResult:
                flash("Nom d'utilisateur ou mot de passe incorrect !", "danger")
                return redirect(url_for('Fprofile.importation_ad'))

            except LDAPSocketOpenError:
                flash("Impossible de trouvé le serveur Active Directory !", "danger")
                return redirect(url_for('Fprofile.importation_ad'))

            except LDAPBindError:
                flash("Nom d'utilisateur ou mot de passe incorrect !", "danger")
                return redirect(url_for('Fprofile.importation_ad'))
            
            except:
                flash("Nom d'utilisateur ou mot de passe incorrect ou serveur AD incorrect !", "danger")
                return redirect(url_for('Fprofile.importation_ad'))

            # Redirige vers la page de profil
            return redirect(url_for('Fprofile.importation_ad'))

    # Si la méthode de la requête n'est pas POST
    elif request.method == 'POST':
        flash("Veuillez complèter le formulaire !", "danger")
        return redirect(url_for('Fprofile.importation_ad'))

    # Redirige vers la page de profil
    return redirect(url_for('Fprofile.importation_ad'))

# Route pour la page pour generer un clé
@Fprofile.route('/import_user', methods=['GET', 'POST'])
def import_user():

    # Récupère l'ID de l'utilisateur à supprimer à partir de la requête GET
    user_id_args = request.args.get("user_id")

    # Vérifie si un utilisateur ou un email existe déjà avec les informations fournies
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute( "SELECT * FROM local_import WHERE id = %s", [user_id_args])
    local_account = cursor.fetchone()

    # Vérifie si un utilisateur ou un email existe déjà avec les informations fournies
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute( "SELECT * FROM employee WHERE username LIKE %s OR email LIKE %s", (local_account['username'], local_account['email']))
    account = cursor.fetchone()
                    

    # Vérifie si un compte existe déjà avec les informations fournies
    if account:
        flash("L'utilisateur existe déjà !", "danger")
        return redirect(url_for('Fprofile.importation_ad'))
    else:

        # Génération d'un nouveau mot de passe aléatoire
        characters = "01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ&*(){}[]|/\?!@#$%^abcdefghijklmnopqrstuvwxyz"
        password = "".join(random.sample(characters, 15))
        hashpass = hashlib.md5(password.encode('utf8')).hexdigest()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE local_import SET imported = %s WHERE ID = %s', ("True", local_account['id']))
        mysql.connection.commit()

        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO employee(firstname, lastname, username, password, email, register) VALUES(%s, %s, %s, %s, %s, "False")', (local_account['firstname'], local_account['lastname'], local_account['username'], hashpass, local_account['email']))
        mysql.connection.commit()
        
        flash("Utilisateur importé avec succès !", "success")

        create_empl_mail(local_account['email'], local_account['firstname'], local_account['lastname'], local_account['username'], password)

        return redirect(url_for('Fprofile.importation_ad'))

# Route pour la page pour generer un clé
@Fprofile.route('/import_file', methods=['GET', 'POST'])
def import_file():
    # Vérifie si la méthode de la requête est POST
    if request.method == 'POST':
        csvv = request.files['csv']
        csvname = csvv.filename
        if csvname.endswith(".csv") == True:

            # Donne un nom unique à l'image
            csv_name_ch = 'employe' + '.csv'
            csv_url_ch = 'static/uploads/csv/'+csv_name_ch
            fullcsv_url_ch = csv_url_ch

            # Enregistre l'image dans le répertoire "static/uploads/pp/"
            csvv.save(os.path.join("static/uploads/csv/", csv_name_ch))
            cursorimp = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            csv_data = csv.reader(open('static/uploads/csv/employe.csv'), delimiter=';')
            try:
                for row in csv_data:
                    # Vérifie si un utilisateur ou un email existe déjà avec les informations fournies
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute( "SELECT * FROM employee WHERE username LIKE %s OR email LIKE %s", (row[2], row[4]))
                    account = cursor.fetchone()
                    

                    # Vérifie si un compte existe déjà avec les informations fournies
                    if account:
                        pass
                    else:
                        print(row[3])
                        hashpass = hashlib.md5(row[3].encode('utf8')).hexdigest()
                        cursorimp.execute('INSERT INTO employee(firstname, lastname, username, password, email, register) VALUES(%s, %s, %s, %s, %s, "False")', (row[0], row[1], row[2], hashpass, row[4]))
                        mysql.connection.commit()
                    
            except:
                flash("Il y a une erreur dans votre fichier CSV, veuilliez le vérifier !", "danger")

            flash("Utilisateur importé avec succès !", "success")
            return redirect(url_for('Fprofile.importation'))
        else:
            flash("Veuillez importé un fichier CSV !", "danger")
            return redirect(url_for('Fprofile.importation'))

    # Si la méthode de la requête n'est pas POST
    elif request.method == 'POST':

        flash("Veuillez téléverser votre fichier CSV !", "danger")

    # Redirige vers la page de profil
    return redirect(url_for('Fprofile.importation'))