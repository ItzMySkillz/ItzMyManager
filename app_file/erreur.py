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

# Création d'un blueprint pour la partie erreur
Ferreur = Blueprint('Ferreur', __name__)

# Route pour la page d'erreur 404
@Ferreur.errorhandler(404)
def page_not_found(e):
    try:
        if session ['loggedin'] == True:
            if session['istech'] == True:
                # Affichage la template de la page d'erreur 404
                return render_template('other/404lin.html', title="Erreur 404"), 404
            else:
                # Affichage la template de la page d'erreur 404
                return render_template('other/404linmob.html', title="Erreur 404"), 404
        else:
            # Affichage la template de la page d'erreur 404
            return render_template('other/404lout.html', title="Erreur 404"), 404
    except:
        # Affichage la template de la page d'erreur 404
        return render_template('other/404lout.html', title="Erreur 404"), 404
    
    