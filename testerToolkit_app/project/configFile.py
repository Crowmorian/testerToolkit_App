# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 14:28:44 2022

@author: Crowmorian
"""
from flask import Blueprint, render_template
from __init__ import reload_blueprints

#Declaring global variables and settings
global selectedLanguage
selectedLanguage = "ENG"
configFile = Blueprint("configFile", __name__)

@configFile.route("/setEng")
def setEng ():
    selectedLanguage = "ENG"
    print(selectedLanguage, flush=True)
    reload_blueprints()
    return render_template('index.html')


@configFile.route("/setCs")
def setCs ():
    selectedLanguage = "CS"
    print(selectedLanguage, flush=True)
    reload_blueprints()
    return render_template('cs/index.html')
