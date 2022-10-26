# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 14:28:44 2022

@author: Crowmorian
"""
from flask import Blueprint, render_template

#Declaring global variables and settings
selectedLanguage = "ENG"
configFile = Blueprint("configFile", __name__)

@configFile.route("/switchEng")
def setEng ():
    selectedLanguage = "ENG"

@configFile.route("/switchCs")
def setCS ():
    selectedLanguage = "CS"