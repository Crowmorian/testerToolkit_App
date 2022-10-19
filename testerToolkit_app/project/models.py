# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 14:27:22 2022

@author: Crowmorian
"""

#Setting up of user models

# Importing of necessary libraries
#************************************
from __init__ import db

class User(db.model):
    id = db.Column(db.integer, primary_key=True) #User ID serving as a primary key for identification
    login = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))