# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 14:27:02 2022

@author: Crowmorian
"""

#Setting up of non-authentication routes

# Importing of necessary libraries
#************************************
from flask import Blueprint

#Declaring routes and variables
main = Blueprint("main", __name__)

@main.route("/")
def index():
    return "Index"

@main.route("/profile")
def profile():
    return "Profile"