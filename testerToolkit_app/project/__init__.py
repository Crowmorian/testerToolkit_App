# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 14:17:00 2022

@author: Crowmorian
"""
#Main initialization script:
    #Setting up app.route
    #Adding functions as they are developed

# Importing of necessary libraries
#************************************

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#Defining access to the SQLAlchemy
db = SQLAlchemy()

#Definition of the main functions
app = Flask(__name__)

app.config["SECRET_KEY"] = "secret-key-added-later"
app.config["SQALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

db.init_app(app)

#Registering blueprint for athentication routes
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

#Registering blueprint for non-authentication routes
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)