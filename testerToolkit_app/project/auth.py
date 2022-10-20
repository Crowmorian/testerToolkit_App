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
from flask_login import login_user

#Declaring routes and variables
auth = Blueprint("auth", __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    user = Users.query.filter_by(login=username).first()
    
    if not user or not check_password_hash(user.password, password):
        flash('Incorrect name or password, please try again.')
        return redirect(url_for('auth.login'))
    
    login_user(user)
    
    return redirect(url_for('main.index'))

@auth.route("/logout")
def logout():
    return "Logout"

@auth.route("/createUser")
def createUser():
    return render_template('createUser.html')

@auth.route('/createUser', methods=['POST'])
def createUser_post():
    username = request.form.get('username')
    name = request.form.get('name')
    password = request.form.get('password')
    
    user = Users.query.filter_by(login=username).first()
    
    if user: 
        flash("Username already exists.")
        return redirect(url_for('auth.createUser'))
    
    new_user = Users(login=username, name=name, password=generate_password_hash(password, method='sha256'))
    
    db.session.add(new_user)
    db.session.commit()
    
    return redirect(url_for('main.index'))