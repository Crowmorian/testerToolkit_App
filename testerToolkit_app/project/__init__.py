# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 14:17:00 2022

@author: Crowmorian
"""
#Main initialization script:
    #Setting up app.route
    #Inicializing the app
    #Mapping blueprints of authentication and main paths

# Importing of necessary libraries
#************************************

from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from datetime import timedelta


#Definition of the main functions
selectedLanguage = "ENG"
app = Flask(__name__, template_folder = './templates', static_folder = './templates/static')

app.config['SECRET_KEY'] = "secretKey" #os.urandom(12).hex()
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///userDB.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
session["lang"] = "eng"

from models import Users

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(hours=1)

#Registering blueprint for athentication routes
from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

#Registering blueprint for non-authentication routes
from main import main as main_blueprint
app.register_blueprint(main_blueprint)

