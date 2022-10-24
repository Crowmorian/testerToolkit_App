# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 14:27:02 2022

@author: Crowmorian
"""

#Setting up of non-authentication routes

# Importing of necessary libraries
#************************************
from flask import Blueprint, render_template
from configFile import selectedLanguage

#Declaring routes and variables
main = Blueprint("main", __name__)

@main.route("/")
def index():
    if selectedLanguage == "ENG":
        return render_template('index.html')
    elif selectedLanguage == "CS":
        return render_template('CS/index.html')

@main.route("/createClient")
def createClient():
    return render_template('createClient.html')

@main.route("/createIndividual")
def createIndividual():
    return render_template('createIndividual.html')

@main.route("/createLegalEntity")
def createLegalEntity():
    return render_template('createLegalEntity.html')

@main.route("/createMinor")
def createMinor():
    return render_template('createMinor.html')