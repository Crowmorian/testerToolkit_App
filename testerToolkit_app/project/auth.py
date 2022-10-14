# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 14:17:00 2022

@author: Crowmorian
"""
#Setting up of authentication routes

# Importing of necessary libraries
#************************************
from flask import Blueprint

#Declaring routes and variables
auth = Blueprint("auth", __name__)

@auth.route("/login")
def login():
    return "Login"

@auth.route("/logout")
def logout():
    return "Logout"
