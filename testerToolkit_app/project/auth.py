# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 14:17:00 2022

@author: Crowmorian
"""
#Setting up of authentication routes

# Importing of necessary libraries
#************************************
from flask import Blueprint, render_template, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from . import db

#Declaring routes and variables
auth = Blueprint("auth", __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route("/logout")
def logout():
    return "Logout"

@auth.route("/createUser")
def createUser():
    return render_template('createUser.html')

@auth.route('/createUser', methods=['POST'])
def signup_post():
    username = request.form.get('username')
    name = request.form.get('name')
    password = request.form.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if user: # if a user is found, we want to redirect back to signup page so user can try again
        return redirect(url_for('auth.createUser'))
    
    new_user = User(username=username, name=name, password=generate_password_hash(password, method='sha256'))
    
    db.session.add(new_user)
    db.session.commit()
    
    return redirect(url_for('main.index'))