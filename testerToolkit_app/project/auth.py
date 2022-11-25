# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 14:17:00 2022

@author: Crowmorian
"""
#Setting up of authentication routes

# Importing of necessary libraries
#************************************
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import Users
from __init__ import db
from flask_login import login_user, login_required, logout_user
from uuid import uuid4

#Declaring routes and variables
auth = Blueprint("auth", __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/cs/login')
def CSlogin():    
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
    session['number'] = str(uuid4())
    session["randomSaved"] = "notSaved"
    session["individualSaved"] = "notSaved"
    session["bussinessSaved"] = "notSaved"
    session["nameGenSaved"] = "notSaved"
    session["numGenSaved"] = "notSaved"
    
    return redirect(url_for('main.index'))

@auth.route('/cs/login', methods=['POST'])
def CSlogin_post():
    username = request.form.get('username')
    password = request.form.get('password')

    user = Users.query.filter_by(login=username).first()
    
    if not user or not check_password_hash(user.password, password):
        flash('Nesprávné jméno nebo heslo, zkuste to prosím znovu')
        return redirect(url_for('auth.CSlogin'))
    
    login_user(user)
    session['number'] = str(uuid4())
    session["randomSaved"] = "noteSaved"
    
    return redirect(url_for('main.CSindex'))

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route("/cs/logout")
@login_required
def CSlogout():
    logout_user()
    return redirect(url_for('main.CSindex'))

@auth.route("/createUser")
@login_required
def createUser():        
    return render_template('createUser.html')

@auth.route("/cs/createUser")
@login_required
def CScreateUser(): 
    return render_template('cs/createUser.html')

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

@auth.route('/cs/createUser', methods=['POST'])
def CScreateUser_post():
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
        flash("Uživatel s tímto jménem již existuje")
        return redirect(url_for('auth.CScreateUser'))
    
    new_user = Users(login=username, name=name, password=generate_password_hash(password, method='sha256'), admin=admin)
    
    db.session.add(new_user)
    db.session.commit()
    
    return redirect(url_for('main.CSindex'))