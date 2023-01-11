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

Ferreur = Blueprint('Ferreur', __name__)

@Ferreur.errorhandler(404)
def page_not_found(e):
    return render_template('other/404lin.html', title="Erreur 404"), 404