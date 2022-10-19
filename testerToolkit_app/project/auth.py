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
from models import Users
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
def createUser_post():
    database_uri = 'sqlite:///userDB.sqlite'
    Session = sessionmaker()

    engine = create_engine(database_uri)
    session = Session(bind=engine)
    
    username = request.form.get('username')
    name = request.form.get('name')
    password = request.form.get('password')
    
    user = Users.query.filter_by(login=username).first()
    
    if user: 
        return redirect(url_for('auth.createUser'))
    
    new_user = Users(username=username, name=name, password=generate_password_hash(password, method='sha256'))
    
    session.session.add(new_user)
    session.session.commit()
    
    return redirect(url_for('main.index'))