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
    return render_template('index.html')

@main.route("cs/")
def CSindex():
    return render_template('cs/index.html')

@main.route("/createClient")
def createClient():    
    if selectedLanguage == "ENG":
        return render_template('createClient.html')
    elif selectedLanguage == "CS":
        return render_template('cs/createClient.html')

@main.route("/createIndividual")
def createIndividual():
    if selectedLanguage == "ENG":
        return render_template('createIndividual.html')
    elif selectedLanguage == "CS":
        return render_template('cs/createIndividual.html')

@main.route("/createLegalEntity")
def createLegalEntity():
    if selectedLanguage == "ENG":
        return render_template('createLegalEntity.html')
    elif selectedLanguage == "CS":
        return render_template('cs/createLegalEntity.html')

@main.route("/createMinor")
def createMinor():
    if selectedLanguage == "ENG":
        return render_template('createMinor.html')
    elif selectedLanguage == "CS":
        return render_template('cs/createMinor.html')
    
@main.route("/setEng")
def setEng ():
    return render_template('index.html')


@main.route("/setCs")
def setCs ():
    return render_template('cs/index.html')
