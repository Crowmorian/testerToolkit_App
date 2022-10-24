# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 14:17:00 2022

@author: Crowmorian
"""
#Setting up of authentication routes

# Importing of necessary libraries
#************************************
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import Users
from __init__ import db
from flask_login import login_user, login_required, logout_user
from configFile import selectedLanguage

#Declaring routes and variables
auth = Blueprint("auth", __name__)

@auth.route('/login')
def login():    
    if selectedLanguage == "ENG":
        return render_template('login.html')
    elif selectedLanguage == "CS":
        return render_template('cs/login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    user = Users.query.filter_by(login=username).first()
    
    if not user or not check_password_hash(user.password, password):
        flash('Incorrect username or password, please try again.')
        return redirect(url_for('auth.login'))
    
    login_user(user)
    
    return redirect(url_for('main.index'))

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route("/createUser")
@login_required
def createUser():    
    
    if selectedLanguage == "ENG":
        return render_template('createUser.html')
    elif selectedLanguage == "CS":
        return render_template('/cscreateUser.html')

@auth.route('/createUser', methods=['POST'])
def createUser_post():
    username = request.form.get('username')
    name = request.form.get('name')
    password = request.form.get('password')
    admin = request.form.get('admin')
    
    if admin == "on":
        admin = 1
    else:
        admin = 0
    
    print(admin, flush=True)
    
    user = Users.query.filter_by(login=username).first()
    
    if user: 
        flash("Username already exists.")
        return redirect(url_for('auth.createUser'))
    
    new_user = Users(login=username, name=name, password=generate_password_hash(password, method='sha256'), admin=admin)
    
    db.session.add(new_user)
    db.session.commit()
    
    return redirect(url_for('main.index'))