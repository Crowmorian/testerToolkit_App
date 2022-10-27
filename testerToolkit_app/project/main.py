# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 14:27:02 2022

@author: Crowmorian
"""

#Setting up of non-authentication routes

# Importing of necessary libraries
#************************************
from flask import Blueprint, render_template, request, session
from flask_login import login_required

#Declaring routes and variables
main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template('index.html')

@main.route("/cs")
def CSindex():
    return render_template('cs/index.html')

@main.route("/createClient")
@login_required
def createClient():    
    return render_template('createClient.html')

@main.route("/cs/createClient")
@login_required
def CScreateClient():    
    return render_template('cs/createClient.html')

@main.route("/createIndividual")
@login_required
def createIndividual():
    return render_template('createIndividual.html')

@main.route("/cs/createIndividual")
@login_required
def CScreateIndividual():
    return render_template('cs/createIndividual.html')

@main.route("/createLegalEntity")
@login_required
def createLegalEntity():
    return render_template('createLegalEntity.html')

@main.route("/cs/createLegalEntity")
@login_required
def CScreateLegalEntity():
    return render_template('cs/createLegalEntity.html')

@main.route("/createMinor")
@login_required
def createMinor():
    return render_template('createMinor.html')

@main.route("/cs/createMinor")
@login_required
def CScreateMinor():
        return render_template('cs/createMinor.html')
    
@main.route("/setEng")
def setEng ():
    return render_template('index.html')


@main.route("/setCs")
def setCs ():
    return render_template('cs/index.html')

@main.route("/generators")
@login_required
def generators():
        return render_template('generators.html')
    
@main.route("/cs/generators")
@login_required
def CSgenerators():
        return render_template('cs/generators.html')
    
@main.route("/generateIBAN")
@login_required
def generateIBAN():
        return render_template('generateIBAN.html')
    
@main.route("/cs/generateIBAN")
@login_required
def CSgenerateIBAN():
        return render_template('cs/generateIBAN.html')

@main.route("/generateSIPO")
@login_required
def generateSIPO():
        return render_template('generateSIPO.html')
    
@main.route("/cs/generateSIPO")
@login_required
def CSgenerateSIPO():
        return render_template('cs/generateSIPO.html')
    
@main.route("/generateCIN")
@login_required
def generateCIN():
        return render_template('generateCIN.html')
    
@main.route("/cs/generateCIN")
@login_required
def CSgenerateCIN():
        return render_template('cs/generateCIN.html')
    
@main.route("/generateDate")
@login_required
def generateDate():
        return render_template('generateDate.html')
    
@main.route("/cs/generateDate")
@login_required
def CSgenerateDate():
        return render_template('cs/generateDate.html')
    
@main.route("/generateMailNumber")
@login_required
def generateMailNumber():
        return render_template('generateMailNumber.html')
    
@main.route("/cs/generateMailNumber")
@login_required
def CSgenerateMailNumber():
        return render_template('cs/generateMailNumber.html')
    
@main.route("/generateRandom")
@login_required
def generateRandom():
        return render_template('generateRandom.html')
    
@main.route("/cs/generateRandom")
@login_required
def CSgenerateRandom():
        return render_template('cs/generateRandom.html')
    
#test session variable memory
@main.route('/generateRandom', methods=['POST'])
def generateRandom_post():
    session["zero"] = request.form.get('zero')
    print(session["zero"], flush=True)
    print(session["number"], flush=True)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    