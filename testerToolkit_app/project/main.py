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

@main.route("/cs")
def CSindex():
    return render_template('cs/index.html')

@main.route("/createClient")
def createClient():    
    return render_template('createClient.html')

@main.route("/cs/createClient")
def CScreateClient():    
    return render_template('cs/createClient.html')

@main.route("/createIndividual")
def createIndividual():
    return render_template('createIndividual.html')

@main.route("/cs/createIndividual")
def CScreateIndividual():
    return render_template('cs/createIndividual.html')

@main.route("/createLegalEntity")
def createLegalEntity():
    return render_template('createLegalEntity.html')

@main.route("/cs/createLegalEntity")
def CScreateLegalEntity():
    return render_template('cs/createLegalEntity.html')

@main.route("/createMinor")
def createMinor():
    return render_template('createMinor.html')

@main.route("/cs/createMinor")
def CScreateMinor():
        return render_template('cs/createMinor.html')
    
@main.route("/setEng")
def setEng ():
    return render_template('index.html')


@main.route("/setCs")
def setCs ():
    return render_template('cs/index.html')

@main.route("/generators")
def generators():
        return render_template('generators.html')
    
@main.route("/cs/generators")
def CSgenerators():
        return render_template('cs/generators.html')
