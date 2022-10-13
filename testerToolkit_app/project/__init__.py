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

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Tester Toolkit'

