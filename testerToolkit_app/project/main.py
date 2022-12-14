# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 14:27:02 2022

@author: Crowmorian
"""

#Setting up of non-authentication routes

# Importing of necessary libraries
#************************************
from flask import Blueprint, render_template, request, session, flash
from flask_login import login_required
from random import randint, seed, choices
import sqlite3
import random
from datetime import date, timedelta, datetime
import schwifty
from dateutil.relativedelta import relativedelta

#Declaring routes and variables
main = Blueprint("main", __name__)

#Connecting database for generated and required data
con = sqlite3.connect("genData.sqlite")
cur = con.cursor()

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
    if session["individualSaved"] == "notSaved":
        session["individualUseFunky"] = None
        session["individualGender"] = "male"
        session["individualIsMinor"] = None
        session["individualNationality"] = "cz"
    
    return render_template('createIndividual.html',
        individualUseFunky = session["individualUseFunky"],
        individualGender = session["individualGender"],
        individualIsMinor = session["individualIsMinor"],
        individualNationality = session["individualNationality"])

@main.route("/cs/createIndividual")
@login_required
def CScreateIndividual():
    if session["individualSaved"] == "notSaved":
        session["individualUseFunky"] = None
        session["individualGender"] = "male"
        session["individualIsMinor"] = None
        session["individualNationality"] = "cz"
    
    return render_template('cs/createIndividual.html',
        individualUseFunky = session["individualUseFunky"],
        individualGender = session["individualGender"],
        individualIsMinor = session["individualIsMinor"],
        individualNationality = session["individualNationality"])


@main.route('/createIndividual', methods=['POST'])
@login_required
def createIndividual_post():
    session["individualSaved"] = "saved" 
    session["individualUseFunky"] = request.form.get("individualUseFunky")
    session["individualIsMinor"] = request.form.get("individualIsMinor")
    session["individualNationality"] = request.form.get("individualNationality")
    session["individualGender"] = request.form.get("individualGender")
    
    individualCreated = []
    foreigner = None
    
    if session["individualNationality"] == "cz":
        foreigner = None
    else:
        foreigner = "on"
    
    individualName = generateName(session["individualGender"], session["individualUseFunky"], foreigner)
    individualCreated.append(individualName)
    
    individualAddress = generateAddress(session["individualNationality"])
    individualCreated.append(individualAddress[0])
    
    if session["individualNationality"] == "cz":
        individualPhone = phoneNumberCS()
    elif session["individualNationality"] == "gb":
        individualPhone = phoneNumberUK()
    elif session["individualNationality"] == "us":
        individualPhone = phoneNumberUS()
    elif session["individualNationality"] == "eu":
        individualPhone = phoneNumberEU(individualAddress[1])
    individualCreated.append(individualPhone)
    
    individualPassport = passportNumber()
    individualCreated.append(individualPassport)
    
    individualDateOfBirth = dateOfBirth(session["individualIsMinor"])
    individualCreated.append(individualDateOfBirth)
    
    individualPID = idNumberCS(session["individualGender"],individualDateOfBirth)
    individualCreated.append(individualPID)
    individualCreated.append(individualAddress[1])
    
    return render_template('createIndividual.html',
        individualUseFunky = session["individualUseFunky"],
        individualGender = session["individualGender"],
        individualIsMinor = session["individualIsMinor"],
        individualNationality = session["individualNationality"],
        individualCreated = individualCreated)

@main.route('/cs/createIndividual', methods=['POST'])
@login_required
def CScreateIndividual_post():
    session["individualSaved"] = "saved" 
    session["individualUseFunky"] = request.form.get("individualUseFunky")
    session["individualIsMinor"] = request.form.get("individualIsMinor")
    session["individualNationality"] = request.form.get("individualNationality")
    session["individualGender"] = request.form.get("individualGender")
    
    individualCreated = []
    foreigner = None
    
    if session["individualNationality"] == "cz":
        foreigner = None
    else:
        foreigner = "on"
    
    individualName = generateName(session["individualGender"], session["individualUseFunky"], foreigner)
    individualCreated.append(individualName)
    
    individualAddress = generateAddress(session["individualNationality"])
    individualCreated.append(individualAddress[0])
    
    if session["individualNationality"] == "cz":
        individualPhone = phoneNumberCS()
    elif session["individualNationality"] == "gb":
        individualPhone = phoneNumberUK()
    elif session["individualNationality"] == "us":
        individualPhone = phoneNumberUS()
    elif session["individualNationality"] == "eu":
        individualPhone = phoneNumberEU(individualAddress[1])
    individualCreated.append(individualPhone)
    
    individualPassport = passportNumber()
    individualCreated.append(individualPassport)
    
    individualDateOfBirth = dateOfBirth(session["individualIsMinor"])
    individualCreated.append(individualDateOfBirth)
    
    individualPID = idNumberCS(session["individualGender"],individualDateOfBirth)
    individualCreated.append(individualPID)
    individualCreated.append(individualAddress[1])
    
    return render_template('cs/createIndividual.html',
        individualUseFunky = session["individualUseFunky"],
        individualGender = session["individualGender"],
        individualIsMinor = session["individualIsMinor"],
        individualNationality = session["individualNationality"],
        individualCreated = individualCreated)
    
@main.route("/createLegalEntity")
@login_required
def createLegalEntity():
    if session["legalSaved"] == "notSaved":
        session["legalUseFunky"] = None
        session["legalGender"] = "male"
        session["legalNationality"] = "cz"
        session["legalIco"] = "real"
        
    return render_template('createLegalEntity.html',
        legalUseFunky = session["legalUseFunky"],
        legalGender = session["legalGender"],
        legalNationality = session["legalNationality"],
        legalIco = session["legalIco"])

@main.route("/cs/createLegalEntity")
@login_required
def CScreateLegalEntity():
    return render_template('cs/createLegalEntity.html')

@main.route("/createLegalEntity", methods=['POST'])
@login_required
def createLegalEntity_post():
    session["legalSaved"] = "saved" 
    session["legalUseFunky"] = request.form.get("legalUseFunky")
    session["legalNationality"] = request.form.get("legalNationality")
    session["legalGender"] = request.form.get("legalGender")
    session["legalIco"] = request.form.get("legalIco")
    
    legalCreated = []
    legalforeigner = None
    
    if session["legalNationality"] == "cz":
        legalforeigner = None
    else:
        legalforeigner = "on"
    
    legalName = generateName(session["legalGender"], session["legalUseFunky"], legalforeigner)
    legalCreated.append(legalName)
    
    legalAddress = generateAddress(session["legalNationality"])
    legalCreated.append(legalAddress[0])
    
    if session["legalNationality"] == "cz":
        legalPhone = phoneNumberCS()
    elif session["legalNationality"] == "gb":
        legalPhone = phoneNumberUK()
    elif session["legalNationality"] == "us":
        legalPhone = phoneNumberUS()
    elif session["legalNationality"] == "eu":
        legalPhone = phoneNumberEU(legalAddress[1])
    legalCreated.append(legalPhone)
    
    legalPassport = passportNumber()
    legalCreated.append(legalPassport)
    
    legalDateOfBirth = dateOfBirth(None)
    legalCreated.append(legalDateOfBirth)
    
    legalPID = idNumberCS(session["legalGender"],legalDateOfBirth)
    legalCreated.append(legalPID)
    legalCreated.append(legalAddress[1])
    
    legalCIN = generateIco(session["legalIco"])
    legalCreated.append(legalCIN)
    
    legalComp = generateCompanyName()
    legalCreated.append(legalComp)
    
    today = date.today()
    cd1 = today
    creationStart = cd1.strftime("%Y-%m-%d")
    cd2 = today - relativedelta(months=3)
    creationEnd = cd2.strftime("%Y-%m-%d")
    
    legalCreationDate = legalDates(creationStart, creationEnd)
    legalCreated.append(legalCreationDate)
    
    dd1 = today - relativedelta(months=3)
    docStart = dd1.strftime("%Y-%m-%d")
    dd2 = today
    docEnd = dd2.strftime("%Y-%m-%d")
    
    legalDocDate = legalDates(docStart, docEnd)
    legalCreated.append(legalDocDate)
    
    legStart = legalCreationDate
    legEnd = legalDocDate
    
    legalLegalDate = legalDates(legStart, legEnd)
    legalCreated.append(legalLegalDate)
    
    legalDocUrl = generateURL()
    legalCreated.append(legalDocUrl)
    
    return render_template('createLegalEntity.html',
        legalUseFunky = session["legalUseFunky"],
        legalGender = session["legalGender"],
        legalNationality = session["legalNationality"],
        legalCreated = legalCreated)

@main.route("/createBussiness")
@login_required
def createBussiness():
    if session["bussinessSaved"] == "notSaved":
        session["bussinessUseFunky"] = None
        session["bussinessGender"] = "male"
        session["bussinessNationality"] = "cz"
        session["bussinessIco"] = "real"
        
    return render_template('createBussiness.html',
        bussinessUseFunky = session["bussinessUseFunky"],
        bussinessGender = session["bussinessGender"],
        bussinessNationality = session["bussinessNationality"],
        bussinessIco = session["bussinessIco"])

@main.route("/cs/createBussiness")
@login_required
def CScreateBussiness():
    if session["bussinessSaved"] == "notSaved":
        session["bussinessUseFunky"] = None
        session["bussinessGender"] = "male"
        session["bussinessNationality"] = "cz"
        session["bussinessIco"] = "real"
        
    return render_template('cs/createBussiness.html',
        bussinessUseFunky = session["bussinessUseFunky"],
        bussinessGender = session["bussinessGender"],
        bussinessNationality = session["bussinessNationality"],
        bussinessIco = session["bussinessIco"])

@main.route("/createBussiness", methods=['POST'])
@login_required
def createBussiness_post():
    session["bussinessSaved"] = "saved" 
    session["bussinessUseFunky"] = request.form.get("bussinessUseFunky")
    session["bussinessNationality"] = request.form.get("bussinessNationality")
    session["bussinessGender"] = request.form.get("bussinessGender")
    session["bussinessIco"] = request.form.get("bussinessIco")
    
    print(session["bussinessIco"])
    
    bussinessCreated = []
    bussinessforeigner = None
    
    if session["bussinessNationality"] == "cz":
        bussinessforeigner = None
    else:
        bussinessforeigner = "on"
    
    bussinessName = generateName(session["bussinessGender"], session["bussinessUseFunky"], bussinessforeigner)
    bussinessCreated.append(bussinessName)
    
    bussinessAddress = generateAddress(session["bussinessNationality"])
    bussinessCreated.append(bussinessAddress[0])
    
    if session["bussinessNationality"] == "cz":
        bussinessPhone = phoneNumberCS()
    elif session["bussinessNationality"] == "gb":
        bussinessPhone = phoneNumberUK()
    elif session["bussinessNationality"] == "us":
        bussinessPhone = phoneNumberUS()
    elif session["bussinessNationality"] == "eu":
        bussinessPhone = phoneNumberEU(bussinessAddress[1])
    bussinessCreated.append(bussinessPhone)
    
    bussinessPassport = passportNumber()
    bussinessCreated.append(bussinessPassport)
    
    bussinessDateOfBirth = dateOfBirth(None)
    bussinessCreated.append(bussinessDateOfBirth)
    
    bussinessPID = idNumberCS(session["bussinessGender"],bussinessDateOfBirth)
    bussinessCreated.append(bussinessPID)
    bussinessCreated.append(bussinessAddress[1])
    
    bussinessCIN = generateIco(session["bussinessIco"])
    bussinessCreated.append(bussinessCIN)
    
    bussinessCDN = generateConcessionNumber()
    bussinessCreated.append(bussinessCDN)
    
    return render_template('createBussiness.html',
        bussinessUseFunky = session["bussinessUseFunky"],
        bussinessGender = session["bussinessGender"],
        bussinessNationality = session["bussinessNationality"],
        bussinessCreated = bussinessCreated)

@main.route("/cs/createBussiness", methods=['POST'])
@login_required
def CScreateBussiness_post():
    session["bussinessSaved"] = "saved" 
    session["bussinessUseFunky"] = request.form.get("bussinessUseFunky")
    session["bussinessNationality"] = request.form.get("bussinessNationality")
    session["bussinessGender"] = request.form.get("bussinessGender")
    session["bussinessIco"] = request.form.get("bussinessIco")
    
    print(session["bussinessIco"])
    
    bussinessCreated = []
    bussinessforeigner = None
    
    if session["bussinessNationality"] == "cz":
        bussinessforeigner = None
    else:
        bussinessforeigner = "on"
    
    bussinessName = generateName(session["bussinessGender"], session["bussinessUseFunky"], bussinessforeigner)
    bussinessCreated.append(bussinessName)
    
    bussinessAddress = generateAddress(session["bussinessNationality"])
    bussinessCreated.append(bussinessAddress[0])
    
    if session["bussinessNationality"] == "cz":
        bussinessPhone = phoneNumberCS()
    elif session["bussinessNationality"] == "gb":
        bussinessPhone = phoneNumberUK()
    elif session["bussinessNationality"] == "us":
        bussinessPhone = phoneNumberUS()
    elif session["bussinessNationality"] == "eu":
        bussinessPhone = phoneNumberEU(bussinessAddress[1])
    bussinessCreated.append(bussinessPhone)
    
    bussinessPassport = passportNumber()
    bussinessCreated.append(bussinessPassport)
    
    bussinessDateOfBirth = dateOfBirth(None)
    bussinessCreated.append(bussinessDateOfBirth)
    
    bussinessPID = idNumberCS(session["bussinessGender"],bussinessDateOfBirth)
    bussinessCreated.append(bussinessPID)
    bussinessCreated.append(bussinessAddress[1])
    
    bussinessCIN = generateIco(session["bussinessIco"])
    bussinessCreated.append(bussinessCIN)
    
    bussinessCDN = generateConcessionNumber()
    bussinessCreated.append(bussinessCDN)
    
    return render_template('cs/createBussiness.html',
        bussinessUseFunky = session["bussinessUseFunky"],
        bussinessGender = session["bussinessGender"],
        bussinessNationality = session["bussinessNationality"],
        bussinessCreated = bussinessCreated)
    
@main.route("/setEng")
def setEng ():
    session["lang"] = "eng"
    return render_template('index.html')


@main.route("/setCs")
def setCs ():
    session["lang"] = "cs"
    return render_template('cs/index.html')

@main.route("/generators")
@login_required
def generators():
    return render_template('generators.html')
    
@main.route("/cs/generators")
@login_required
def CSgenerators():
    return render_template('cs/generators.html')

@main.route("/validateIBAN")
@login_required
def validateIBAN():
    if session["ibanValSaved"] == "notSaved":
        session["ibanValNumber"] = ""
        
    return render_template('validateIBAN.html',
        idanValNumber = session["ibanValNumber"])

    
@main.route("/cs/validateIBAN")
@login_required
def CSvalidateIBAN():
    if session["ibanValSaved"] == "notSaved":
        session["ibanValNumber"] = ""
        
    return render_template('cs/validateIBAN.html',
        idanValNumber = session["ibanValNumber"])

@main.route("/validateIBAN", methods=['POST'])
@login_required
def validateIBAN_post():
    session["ibanValSaved"] = "saved"
    session["ibanValNumber"] = request.form.get("ibanValNumber")
    
    results = []
    
    try:
        iban = schwifty.IBAN(session["ibanValNumber"])
        results.append(iban.formatted)
        results.append(iban.country_code)
        results.append(iban.bank_code)
        results.append(iban.account_code)
        results.append(iban.length)
        results.append(iban.bic)
        results.append(iban.country.official_name)
        flash("IBAN is valid", "valid")
    except:
       flash("IBAN not valid","notification")
        
    return render_template('validateIBAN.html',
        ibanValNumber = session["ibanValNumber"],
        results = results)

@main.route("/cs/validateIBAN", methods=['POST'])
@login_required
def CSvalidateIBAN_post():
    session["ibanValSaved"] = "saved"
    session["ibanValNumber"] = request.form.get("ibanValNumber")
    
    results = []
    
    try:
        iban = schwifty.IBAN(session["ibanValNumber"])
        results.append(iban.formatted)
        results.append(iban.country_code)
        results.append(iban.bank_code)
        results.append(iban.account_code)
        results.append(iban.length)
        results.append(iban.bic)
        results.append(iban.country.official_name)
        flash("IBAN is valid", "valid")
    except:
       flash("IBAN not valid","notification")
        
    return render_template('cs/validateIBAN.html',
        ibanValNumber = session["ibanValNumber"],
        results = results)
    
@main.route("/generateIBAN")
@login_required
def generateIBAN():
    if session["ibanGenSaved"] == "notSaved":
        session["ibanGenCountry"] = "CZ"
        session["ibanGenBankCode"] = ""
        session["ibanGenAccountID"] = ""
        session["ibanGenAccountNum"] = ""
    
    return render_template('generateIBAN.html',
        ibanGenCountry = session["ibanGenCountry"],
        ibanGenBankCode = session["ibanGenBankCode"],
        ibanGenAccountID = session["ibanGenAccountID"],
        ibanGenAccountNum = session["ibanGenAccountNum"])
    
@main.route("/cs/generateIBAN")
@login_required
def CSgenerateIBAN():
    if session["ibanGenSaved"] == "notSaved":
        session["ibanGenCountry"] = "CZ"
        session["ibanGenBankCode"] = ""
        session["ibanGenAccountID"] = ""
        session["ibanGenAccountNum"] = ""
    
    return render_template('cs/generateIBAN.html',
        ibanGenCountry = session["ibanGenCountry"],
        ibanGenBankCode = session["ibanGenBankCode"],
        ibanGenAccountID = session["ibanGenAccountID"],
        ibanGenAccountNum = session["ibanGenAccountNum"])
    return render_template('cs/generateIBAN.html')

@main.route("/generateIBAN", methods=['POST'])
@login_required
def generateIBAN_post():
    session["ibanGenSaved"] = "saved"
    session["ibanGenCountry"] = request.form.get("ibanGenCountry")
    session["ibanGenBankCode"] = request.form.get("ibanGenBankCode")
    session["ibanGenAccountID"] = request.form.get("ibanGenAccountID")
    session["ibanGenAccountNum"] = request.form.get("ibanGenAccountNum")
    
    results = []
    account = session["ibanGenAccountID"]+session["ibanGenAccountNum"]

    try:
        iban = ibanGen(session["ibanGenCountry"], session["ibanGenBankCode"], account)
        results.append(iban)
    except:
       print ("IBAN not valid")
       flash("IBAN Could not be generated from the given numbers. Please check the numbers and try again.")
    
    return render_template('generateIBAN.html',
        ibanGenCountry = session["ibanGenCountry"],
        ibanGenBankCode = session["ibanGenBankCode"],
        ibanGenAccountID = session["ibanGenAccountID"],
        ibanGenAccountNum = session["ibanGenAccountNum"],
        results = results)

@main.route("/cs/generateIBAN", methods=['POST'])
@login_required
def CSgenerateIBAN_post():
    session["ibanGenSaved"] = "saved"
    session["ibanGenCountry"] = request.form.get("ibanGenCountry")
    session["ibanGenBankCode"] = request.form.get("ibanGenBankCode")
    session["ibanGenAccountID"] = request.form.get("ibanGenAccountID")
    session["ibanGenAccountNum"] = request.form.get("ibanGenAccountNum")
    
    results = []
    account = session["ibanGenAccountID"]+session["ibanGenAccountNum"]

    try:
        iban = ibanGen(session["ibanGenCountry"], session["ibanGenBankCode"], account)
        results.append(iban)
    except:
       print ("IBAN not valid")
       flash("IBAN nemohl být ze zadaných čísel vygenerován. Zkontrolujte prosím údaje a zkuste to znovu.")
    
    return render_template('cs/generateIBAN.html',
        ibanGenCountry = session["ibanGenCountry"],
        ibanGenBankCode = session["ibanGenBankCode"],
        ibanGenAccountID = session["ibanGenAccountID"],
        ibanGenAccountNum = session["ibanGenAccountNum"],
        results = results)

@main.route("/generateSIPO")
@login_required
def generateSIPO():
    if session["sipoSaved"] == "notSaved":
        session["first"] = 1
        session["second"] = 2
        session["third"] = 3
        session["fourth"] = 4
        session["fifth"] = 5
        session["sixth"] = 6
        session["seventh"] = 7
        session["eighth"] = 8
        session["nineth"] = 9
        
    return render_template('generateSIPO.html',
        first = session["first"],
        second = session["second"],
        third = session["third"],
        fourth = session["fourth"],
        fifth = session["fifth"],
        sixth = session["sixth"],
        seventh = session["seventh"],
        eighth = session["eighth"],
        nineth = session["nineth"])
    
@main.route("/cs/generateSIPO")
@login_required
def CSgenerateSIPO():
    if session["sipoSaved"] == "notSaved":
            session["first"] = 1
            session["second"] = 2
            session["third"] = 3
            session["fourth"] = 4
            session["fifth"] = 5
            session["sixth"] = 6
            session["seventh"] = 7
            session["eighth"] = 8
            session["nineth"] = 9
            
    return render_template('cs/generateSIPO.html',
        first = session["first"],
        second = session["second"],
        third = session["third"],
        fourth = session["fourth"],
        fifth = session["fifth"],
        sixth = session["sixth"],
        seventh = session["seventh"],
        eighth = session["eighth"],
        nineth = session["nineth"])

@main.route("/generateSIPO", methods=['POST'])
@login_required
def generateSIPO_post():
    session["sipoSaved"] = "saved"
    session["first"] = request.form.get("first")
    session["second"] = request.form.get("second")
    session["third"] = request.form.get("third")
    session["fourth"] = request.form.get("fourth")
    session["fifth"] = request.form.get("fifth")
    session["sixth"] = request.form.get("sixth")
    session["seventh"] = request.form.get("seventh")
    session["eighth"] = request.form.get("eighth")
    session["nineth"] = request.form.get("nineth")
    
    results = []
    importedNumbers = [int(session["first"]),
                       int(session["second"]),
                       int(session["third"]),
                       int(session["fourth"]),
                       int(session["fifth"]),
                       int(session["sixth"]),
                       int(session["seventh"]),
                       int(session["eighth"]),
                       int(session["nineth"])
                       ]
    
    sipo = generateSIPONum(importedNumbers)
    
    results.append(sipo)
        
    return render_template('generateSIPO.html',
        first = session["first"],
        second = session["second"],
        third = session["third"],
        fourth = session["fourth"],
        fifth = session["fifth"],
        sixth = session["sixth"],
        seventh = session["seventh"],
        eighth = session["eighth"],
        nineth = session["nineth"],
        results = results)

@main.route("/cs/generateSIPO", methods=['POST'])
@login_required
def CSgenerateSIPO_post():
    session["sipoSaved"] = "saved"
    session["first"] = request.form.get("first")
    session["second"] = request.form.get("second")
    session["third"] = request.form.get("third")
    session["fourth"] = request.form.get("fourth")
    session["fifth"] = request.form.get("fifth")
    session["sixth"] = request.form.get("sixth")
    session["seventh"] = request.form.get("seventh")
    session["eighth"] = request.form.get("eighth")
    session["nineth"] = request.form.get("nineth")
    
    results = []
    importedNumbers = [int(session["first"]),
                       int(session["second"]),
                       int(session["third"]),
                       int(session["fourth"]),
                       int(session["fifth"]),
                       int(session["sixth"]),
                       int(session["seventh"]),
                       int(session["eighth"]),
                       int(session["nineth"])
                       ]
    
    sipo = generateSIPONum(importedNumbers)
    
    results.append(sipo)
        
    return render_template('cs/generateSIPO.html',
        first = session["first"],
        second = session["second"],
        third = session["third"],
        fourth = session["fourth"],
        fifth = session["fifth"],
        sixth = session["sixth"],
        seventh = session["seventh"],
        eighth = session["eighth"],
        nineth = session["nineth"],
        results = results)
    
@main.route("/generateCIN")
@login_required
def generateCIN():
    if session["cinGenSaved"] == "notSaved":
        session["howManyCINs"] = 10
        session["cinGenMode"] = "existing"
    
    return render_template('generateCIN.html',
        howManyCINs = session["howManyCINs"],
        cinGenMode = session["cinGenMode"])
    
@main.route("/cs/generateCIN")
@login_required
def CSgenerateCIN():
    if session["cinGenSaved"] == "notSaved":
        session["howManyCINs"] = 10
        session["cinGenMode"] = "existing"
    
    return render_template('cs/generateCIN.html',
        howManyCINs = session["howManyCINs"],
        cinGenMode = session["cinGenMode"])

@main.route("/generateCIN", methods=['POST'])
@login_required
def generateCIN_post():
    session["cinGenSaved"] = "saved"
    session["howManyCINs"] = request.form.get("howManyCINs")
    session["cinGenMode"] = request.form.get("cinGenMode")
    
    icos = []
    
    for i in range(0, int(request.form.get("howManyCINs"))):
        singleEntry = generateIco(session["cinGenMode"])
        icos.append(singleEntry)
    
    return render_template('generateCIN.html',
        howManyCINs = session["howManyCINs"],
        cinGenMode = session["cinGenMode"],
        results = icos)

@main.route("/cs/generateCIN", methods=['POST'])
@login_required
def CSgenerateCIN_post():
    session["cinGenSaved"] = "saved"
    session["howManyCINs"] = request.form.get("howManyCINs")
    session["cinGenMode"] = request.form.get("cinGenMode")
    
    icos = []
    
    for i in range(0, int(request.form.get("howManyCINs"))):
        singleEntry = generateIco(session["cinGenMode"])
        icos.append(singleEntry)
    
    return render_template('cs/generateCIN.html',
        howManyCINs = session["howManyCINs"],
        cinGenMode = session["cinGenMode"],
        results = icos)

@main.route("/generateDate")
@login_required
def generateDate():
    if session["dateSaved"] == "notSaved":
        today = date.today()
        d1 = today.strftime("%Y-%m-%d")
        session["howManyDates"] = 10
        session["dateStart"] = d1
        session["dateEnd"] = d1        
        
    return render_template('generateDate.html',
        howManyDates = session["howManyDates"],
        dateStart = session["dateStart"],
        dateEnd = session["dateEnd"])
    
@main.route("/cs/generateDate")
@login_required
def CSgenerateDate():
    if session["dateSaved"] == "notSaved":
        today = date.today()
        d1 = today.strftime("%Y-%m-%d")
        session["howManyDates"] = 10
        session["dateStart"] = d1
        session["dateEnd"] = d1        
        
    return render_template('cs/generateDate.html',
        howManyDates = session["howManyDates"],
        dateStart = session["dateStart"],
        dateEnd = session["dateEnd"])

@main.route("/generateDate", methods=['POST'])
@login_required
def generateDate_post():
    session["dateSaved"] = "saved"
    session["howManyDates"] = request.form.get("howManyDates")
    session["dateStart"] = request.form.get("dateStart")
    session["dateEnd"] = request.form.get("dateEnd")

    dates = []
    d1 = datetime.strptime(session["dateStart"], "%Y-%m-%d")
    d2 = datetime.strptime(session["dateEnd"], "%Y-%m-%d")
    
    delta = d2 - d1
    
    if delta.days <= 0:
        flash('Starting date need to be lower than ending date.')
    else:
        for i in range(0, int(session["howManyDates"])):
            randomDays = random.randrange(0, delta.days)
            subtraction = d2- timedelta(days=randomDays)
            randomDate = subtraction.strftime('%d.%m. %Y')
            
            dates.append(randomDate)
    
    return render_template('generateDate.html',
        howManyDates = session["howManyDates"],
        dateStart = session["dateStart"],
        dateEnd = session["dateEnd"],
        results = dates) 

@main.route("/cs/generateDate", methods=['POST'])
@login_required
def CSgenerateDate_post():
    session["dateSaved"] = "saved"
    session["howManyDates"] = request.form.get("howManyDates")
    session["dateStart"] = request.form.get("dateStart")
    session["dateEnd"] = request.form.get("dateEnd")

    dates = []
    d1 = datetime.strptime(session["dateStart"], "%Y-%m-%d")
    d2 = datetime.strptime(session["dateEnd"], "%Y-%m-%d")
    
    delta = d2 - d1
    
    if delta.days <= 0:
        flash('Konečné datum musí být vyšší než začínající datum')
    else:
        for i in range(0, int(session["howManyDates"])):
            randomDays = random.randrange(0, delta.days)
            subtraction = d2- timedelta(days=randomDays)
            randomDate = subtraction.strftime('%d.%m. %Y')
            
            dates.append(randomDate)
    
    return render_template('cs/generateDate.html',
        howManyDates = session["howManyDates"],
        dateStart = session["dateStart"],
        dateEnd = session["dateEnd"],
        results = dates) 
    
@main.route("/generateMail")
@login_required
def generateMail():
    if session["mailGenSaved"] == "notSaved":
        session["howManyEMails"] = 10
        session["eMailGenGender"] = "male"
        session["eMailNamePart"] = "fullName"
        session["eMailProvPart"] = "random"
    
    return render_template('generateMail.html',
        howManyEMails = session["howManyEMails"],
        eMailGenGender = session["eMailGenGender"],
        eMailNamePart = session["eMailNamePart"],
        eMailProvPart = session["eMailProvPart"])

@main.route("/cs/generateMail")
@login_required
def CSgenerateMail():
    if session["mailGenSaved"] == "notSaved":
        session["howManyEMails"] = 10
        session["eMailGenGender"] = "male"
        session["eMailNamePart"] = "fullName"
        session["eMailProvPart"] = "random"
    
    return render_template('cs/generateMail.html',
        howManyEMails = session["howManyEMails"],
        eMailGenGender = session["eMailGenGender"],
        eMailNamePart = session["eMailNamePart"],
        eMailProvPart = session["eMailProvPart"])

@main.route("/generateMail", methods=['POST'])
@login_required
def generateMail_post():
    session["mailGenSaved"] = "saved"
    session["eMailGenGender"] = request.form.get("eMailGenGender")
    session["howManyEMails"] = request.form.get("howManyEMails")
    session["eMailNamePart"] = request.form.get("eMailNamePart")
    session["eMailProvPart"] = request.form.get("eMailProvPart")
    
    results = generateCustomEMail(session["howManyEMails"], session["eMailGenGender"], session["eMailNamePart"], session["eMailProvPart"])
        
    return render_template('generateMail.html',
        howManyEMails = session["howManyEMails"],
        eMailGenGender = session["eMailGenGender"],
        eMailNamePart = session["eMailNamePart"],
        eMailProvPart = session["eMailProvPart"],
        results = results)

@main.route("/cs/generateMail", methods=['POST'])
@login_required
def CSgenerateMail_post():
    session["mailGenSaved"] = "saved"
    session["eMailGenGender"] = request.form.get("eMailGenGender")
    session["howManyEMails"] = request.form.get("howManyEMails")
    session["eMailNamePart"] = request.form.get("eMailNamePart")
    session["eMailProvPart"] = request.form.get("eMailProvPart")
    
    results = generateCustomEMail(session["howManyEMails"], session["eMailGenGender"], session["eMailNamePart"], session["eMailProvPart"])
        
    return render_template('cs/generateMail.html',
        howManyEMails = session["howManyEMails"],
        eMailGenGender = session["eMailGenGender"],
        eMailNamePart = session["eMailNamePart"],
        eMailProvPart = session["eMailProvPart"],
        results = results)

@main.route("/generateNumber")
@login_required
def generateNumber():
    if session["numGenSaved"] == "notSaved":
        session["howManyPNumbers"] = 10
        session["numGenNationality"] = "cz"
    
    return render_template('generateNumber.html',
        howManyPNumbers = session["howManyPNumbers"],
        numGenNationality = session["numGenNationality"])
    
@main.route("/cs/generateNumber")
@login_required
def CSgenerateNumber():
    if session["numGenSaved"] == "notSaved":
        session["howManyPNumbers"] = 10
        session["numGenNationality"] = "cz"
    
    return render_template('cs/generateNumber.html',
        howManyPNumbers = session["howManyPNumbers"],
        numGenNationality = session["numGenNationality"])

@main.route("/generateNumber", methods=['POST'])
@login_required
def generateNumber_post():
    session["numGenSaved"] = "saved"
    session["howManyPNumbers"] = request.form.get("howManyPNumbers")
    session["numGenNationality"] = request.form.get("numGenNationality")
    
    results = []
    
    for i in range(0, int(session["howManyPNumbers"])):
        if session["numGenNationality"] == "cz":
            number = phoneNumberCS()
            results.append(number)
        elif session["numGenNationality"] == "it":
            number = phoneNumberEU("Italy",0)
            results.append(number)
        elif session["numGenNationality"] == "de":
            number = phoneNumberEU("Germany",0)
            results.append(number)
        elif session["numGenNationality"] == "fr":
            number = phoneNumberEU("France",0)
            results.append(number)
        elif session["numGenNationality"] == "es":
            number = phoneNumberEU("Spain",0)
            results.append(number)
        elif session["numGenNationality"] == "se":
            number = phoneNumberEU("Sweden",0)
            results.append(number)
        elif session["numGenNationality"] == "gb":
            number = phoneNumberUK()
            results.append(number)
        elif session["numGenNationality"] == "us":
            number = phoneNumberUS()
            results.append(number)
    
    return render_template('generateNumber.html',
        howManyPNumbers = session["howManyPNumbers"],
        numGenNationality = session["numGenNationality"],
        results = results)

@main.route("/cs/generateNumber", methods=['POST'])
@login_required
def CSgenerateNumber_post():
    session["numGenSaved"] = "saved"
    session["howManyPNumbers"] = request.form.get("howManyPNumbers")
    session["numGenNationality"] = request.form.get("numGenNationality")
    
    results = []
    
    for i in range(0, int(session["howManyPNumbers"])):
        if session["numGenNationality"] == "cz":
            number = phoneNumberCS()
            results.append(number)
        elif session["numGenNationality"] == "it":
            number = phoneNumberEU("Italy",0)
            results.append(number)
        elif session["numGenNationality"] == "de":
            number = phoneNumberEU("Germany",0)
            results.append(number)
        elif session["numGenNationality"] == "fr":
            number = phoneNumberEU("France",0)
            results.append(number)
        elif session["numGenNationality"] == "es":
            number = phoneNumberEU("Spain",0)
            results.append(number)
        elif session["numGenNationality"] == "se":
            number = phoneNumberEU("Sweden",0)
            results.append(number)
        elif session["numGenNationality"] == "gb":
            number = phoneNumberUK()
            results.append(number)
        elif session["numGenNationality"] == "us":
            number = phoneNumberUS()
            results.append(number)
    
    return render_template('cs/generateNumber.html',
        howManyPNumbers = session["howManyPNumbers"],
        numGenNationality = session["numGenNationality"],
        results = results)

@main.route("/generateName")
@login_required
def generateRandomName():
    if session["nameGenSaved"] == "notSaved":
        session["howManyNames"] = 10
        session["nameGenNationality"] = "cz"
        session["nameGenGender"] = "male"
    
    return render_template('generateName.html',
        howManyNames = session["howManyNames"],
        nameGenNationality = session["nameGenNationality"],
        nameGenGender = session["nameGenGender"])

@main.route("/cs/generateName")
@login_required
def CSgenerateName():
    if session["nameGenSaved"] == "notSaved":
        session["howManyNames"] = 10
        session["nameGenNationality"] = "cz"
        session["nameGenGender"] = "male"
    
    return render_template('cs/generateName.html',
        howManyNames = session["howManyNames"],
        nameGenNationality = session["nameGenNationality"],
        nameGenGender = session["nameGenGender"])

@main.route("/generateName", methods=['POST'])
@login_required
def generateRandomName_post():
    session["nameGenSaved"] = "saved"
    session["howManyNames"] = request.form.get("howManyNames")
    session["nameGenNationality"] = request.form.get("nameGenNationality")
    session["nameGenGender"] = request.form.get("nameGenGender")
    
    results = []
    foreigner = None
    
    if session["nameGenNationality"] == "cz":
        foreigner = None
    else:
        foreigner = "on"
    
    for i in range(0,int(session["howManyNames"])):
        name = generateName(session["nameGenGender"], None, foreigner)
        name = name[0] + " " + name[1] + ", "
        results.append(name)

    return render_template('generateName.html',
        howManyNames = session["howManyNames"],
        nameGenNationality = session["nameGenNationality"],
        nameGenGender = session["nameGenGender"],
        results = results)

@main.route("/cs/generateName", methods=['POST'])
@login_required
def CSgenerateRandomName_post():
    session["nameGenSaved"] = "saved"
    session["howManyNames"] = request.form.get("howManyNames")
    session["nameGenNationality"] = request.form.get("nameGenNationality")
    session["nameGenGender"] = request.form.get("nameGenGender")
    
    results = []
    foreigner = None
    
    if session["nameGenNationality"] == "cz":
        foreigner = None
    else:
        foreigner = "on"
    
    for i in range(0,int(session["howManyNames"])):
        name = generateName(session["nameGenGender"], None, foreigner)
        name = name[0] + " " + name[1] + ", "
        results.append(name)

    return render_template('cs/generateName.html',
        howManyNames = session["howManyNames"],
        nameGenNationality = session["nameGenNationality"],
        nameGenGender = session["nameGenGender"],
        results = results)
    
@main.route("/generateRandom")
@login_required
def generateRandom():
    if session["randomSaved"] == "notSaved":
        session["howManyDigits"] = 10
        session["howManyNumbers"] = 1
        session["canStartZero"] = "None"
        session["zero"] = "on"
        session["one"] = "on"
        session["two"] = "on"
        session["three"] = "on"
        session["four"] = "on"
        session["five"] = "on"
        session["six"] = "on"
        session["seven"] = "on"
        session["eight"] = "on"
        session["nine"] = "on"
    
    return render_template('generateRandom.html',
        howManyDigits = session["howManyDigits"],
        howManyNumbers = session["howManyNumbers"],
        canStartZero = session["canStartZero"],
        zero = session["zero"],
        one = session["one"],
        two = session["two"],
        three = session["three"],
        four = session["four"],
        five = session["five"],
        six = session["six"],
        seven = session["seven"],
        eight = session["eight"],
        nine = session["nine"])

@main.route("/cs/generateRandom")
@login_required
def CSgenerateRandom():
    if session["randomSaved"] == "notSaved":
        session["howManyDigits"] = 10
        session["howManyNumbers"] = 1
        session["canStartZero"] = "None"
        session["zero"] = "on"
        session["one"] = "on"
        session["two"] = "on"
        session["three"] = "on"
        session["four"] = "on"
        session["five"] = "on"
        session["six"] = "on"
        session["seven"] = "on"
        session["eight"] = "on"
        session["nine"] = "on"
        
    return render_template('cs/generateRandom.html',
        howManyDigits = session["howManyDigits"],
        howManyNumbers = session["howManyNumbers"],
        canStartZero = session["canStartZero"],
        zero = session["zero"],
        one = session["one"],
        two = session["two"],
        three = session["three"],
        four = session["four"],
        five = session["five"],
        six = session["six"],
        seven = session["seven"],
        eight = session["eight"],
        nine = session["nine"])

@main.route('/generateRandom', methods=['POST'])
@login_required
def generateRandom_post():
    session["randomSaved"] = "saved"
    session["howManyDigits"] = request.form.get("howManyDigits")
    session["howManyNumbers"] = request.form.get("howManyNumbers")
    session["canStartZero"] = request.form.get("canStartZero")
    session["zero"] = request.form.get('zero')
    session["one"] = request.form.get('one')
    session["two"] = request.form.get('two')
    session["three"] = request.form.get('three')
    session["four"] = request.form.get('four')
    session["five"] = request.form.get('five')
    session["six"] = request.form.get('six')
    session["seven"] = request.form.get('seven')
    session["eight"] = request.form.get('eight')
    session["nine"] = request.form.get('nine')
    
    howManyDigits = int(request.form.get("howManyDigits"))
    howManyNumbers = int(request.form.get("howManyNumbers"))
    whichNums = []
    canStartZero = request.form.get("canStartZero")
    results = []
    
    if request.form.get('zero') == "on":
        whichNums.append(0)
    if request.form.get('one') == "on":
        whichNums.append(1)
    if request.form.get('two') == "on":
        whichNums.append(2)
    if request.form.get('three') == "on":
        whichNums.append(3)
    if request.form.get('four') == "on":
        whichNums.append(4)
    if request.form.get('five') == "on":
        whichNums.append(5)
    if request.form.get('six') == "on":
        whichNums.append(6)
    if request.form.get('seven') == "on":
        whichNums.append(7)
    if request.form.get('eight') == "on":
        whichNums.append(8)
    if request.form.get('nine') == "on":
        whichNums.append(9)
        
    if len(whichNums) == 0:
        flash('At least one number needs to be selected.')
    elif howManyDigits == 0:
        flash('Generated number needs to have at least 1 digit.')
    elif howManyNumbers == 0:
        flash('Need at least 1 number to generate.')
    elif canStartZero == None and len(whichNums) == 1 and whichNums[0] == 0:
        flash('If 0 is the only selected number, cannot generate numbers where 0 is not the first digit.')
    else:
        # generate some integers
        seed(randint(10000,99999))
        
        for i in range(0,howManyNumbers):    
            randomSequence = (choices(whichNums, k = howManyDigits))
        
            while randomSequence[0] == 0 and canStartZero == None:
                randomSequence = (choices(whichNums, k = howManyDigits))
            else:
                listToStr = ''.join([str(elem) for elem in randomSequence])
                results.append(listToStr)
        print(results, flush=True)

    return render_template('generateRandom.html',
        howManyDigits = session["howManyDigits"],
        howManyNumbers = session["howManyNumbers"],
        canStartZero = session["canStartZero"],
        zero = session["zero"],
        one = session["one"],
        two = session["two"],
        three = session["three"],
        four = session["four"],
        five = session["five"],
        six = session["six"],
        seven = session["seven"],
        eight = session["eight"],
        nine = session["nine"],
        results = results)

@main.route('/cs/generateRandom', methods=['POST'])
@login_required
def CSgenerateRandom_post():
    session["randomSaved"] = "saved"
    session["howManyDigits"] = request.form.get("howManyDigits")
    session["howManyNumbers"] = request.form.get("howManyNumbers")
    session["canStartZero"] = request.form.get("canStartZero")
    session["zero"] = request.form.get('zero')
    session["one"] = request.form.get('one')
    session["two"] = request.form.get('two')
    session["three"] = request.form.get('three')
    session["four"] = request.form.get('four')
    session["five"] = request.form.get('five')
    session["six"] = request.form.get('six')
    session["seven"] = request.form.get('seven')
    session["eight"] = request.form.get('eight')
    session["nine"] = request.form.get('nine')
    
    howManyDigits = int(request.form.get("howManyDigits"))
    howManyNumbers = int(request.form.get("howManyNumbers"))
    whichNums = []
    canStartZero = request.form.get("canStartZero")
    results = []
    
    if request.form.get('zero') == "on":
        whichNums.append(0)
    if request.form.get('one') == "on":
        whichNums.append(1)
    if request.form.get('two') == "on":
        whichNums.append(2)
    if request.form.get('three') == "on":
        whichNums.append(3)
    if request.form.get('four') == "on":
        whichNums.append(4)
    if request.form.get('five') == "on":
        whichNums.append(5)
    if request.form.get('six') == "on":
        whichNums.append(6)
    if request.form.get('seven') == "on":
        whichNums.append(7)
    if request.form.get('eight') == "on":
        whichNums.append(8)
    if request.form.get('nine') == "on":
        whichNums.append(9)
        
    if len(whichNums) == 0:
        flash('Musí být vybráno alespoň jedno číslo.')
    elif howManyDigits == 0:
        flash('Vygenerované číslo musí obsahovat alespoň jednu číslici.')
    elif howManyNumbers == 0:
        flash('Musí být vygenerováno alespoň jedno číslo.')
    elif canStartZero == None and len(whichNums) == 1 and whichNums[0] == 0:
        flash('Pokud seznam obsahuje pouze nulu, nelze generovat čísla bez nuly na prvním místě.')
    else:
        # generate some integers
        seed(randint(10000,99999))
        
        for i in range(0,howManyNumbers):    
            randomSequence = (choices(whichNums, k = howManyDigits))
        
            while randomSequence[0] == 0 and canStartZero == None:
                randomSequence = (choices(whichNums, k = howManyDigits))
            else:
                listToStr = ''.join([str(elem) for elem in randomSequence])
                results.append(listToStr)
        print(results, flush=True)

    return render_template('cs/generateRandom.html',
        howManyDigits = session["howManyDigits"],
        howManyNumbers = session["howManyNumbers"],
        canStartZero = session["canStartZero"],
        zero = session["zero"],
        one = session["one"],
        two = session["two"],
        three = session["three"],
        four = session["four"],
        five = session["five"],
        six = session["six"],
        seven = session["seven"],
        eight = session["eight"],
        nine = session["nine"],
        results = results)

#******************************************************************
#Client generation functions
#******************************************************************

#UK Phone Number
def phoneNumberUK():    
    finalNumber = ""
    genNumber = []
    code = "+44 "
    initNum = "7"
    
    for num in range(0,9):
        number = randint(0,9)
        genNumber.append(number)
    
    numToStr = ''.join([str(elem) for elem in genNumber])
    numToStrSpaced = numToStr[:2] + " " + numToStr[2:5] + " " +numToStr[5:]
    
    finalNumber = code + initNum + numToStrSpaced
    
    return(finalNumber)

#US Phone Number
def phoneNumberUS():
    finalNumber = ""
    genNumber1 = []
    genNumber2 = []
    genNumber3 = []
    code = "+1 "
    initNum1 = str(randint(2,9))
    initNum2 = str(randint(2,9))
    
    for num in range(0,2):
        number = randint(0,9)
        genNumber1.append(number)
    
    numToStr1 = ''.join([str(elem) for elem in genNumber1])
    
    for num in range(0,2):
        number = randint(0,9)
        genNumber2.append(number)
    
    numToStr2 = ''.join([str(elem) for elem in genNumber2])
    
    for num in range(0,4):
        number = randint(0,9)
        genNumber3.append(number)
    
    numToStr3 = ''.join([str(elem) for elem in genNumber3])
    
    finalNumber = code + initNum1 + numToStr1 + "-" + initNum2 + numToStr2 + "-" + numToStr3
    
    return(finalNumber)

#CS Phone Number
def phoneNumberCS():
    randNumber = []
    code = "+420 "
    
    con = sqlite3.connect("mysite/testerToolkit_app/project/genData.db")
    cur = con.cursor()
    
    cur.execute("SELECT * FROM phoneCS")
    
    phoneNumbers = cur.fetchall()
    firstIndex = randint(1,(len(phoneNumbers)-1))
    first = phoneNumbers[firstIndex]
    firstFinal = str(first[1])
    
    for num in range(0,6):
        number = randint(0,9)
        randNumber.append(number)
        
    numToStr = ''.join([str(elem) for elem in randNumber])
    numToStrSpaced = numToStr[:3] + " " + numToStr[3:]
    
    finalNumber = code + firstFinal + " " + numToStrSpaced
    
    cur.close() 
    return(finalNumber)

#EU Phone Number
def phoneNumberEU(country, crop=1):
    if crop == 1:
        country = country[1:]
        
    if country == "Italy":
        finalNumber = ""
        genNumber1 = []
        genNumber2 = []
        code = "+39 066 "
        
        for num in range(0,3):
            number = randint(1,9)
            genNumber1.append(number)
        
        numToStr1 = ''.join([str(elem) for elem in genNumber1])
        
        for num in range(0,4):
            number = randint(0,9)
            genNumber2.append(number)
        
        numToStr2 = ''.join([str(elem) for elem in genNumber2])
        
        finalNumber = code + numToStr1 + " " + numToStr2
        
        return(finalNumber)
    
    elif country == "Germany":
        finalNumber = ""
        genNumber1 = []
        code = "+49 30 "
        
        for num in range(0,6):
            number = randint(0,9)
            genNumber1.append(number)
        
        numToStr1 = ''.join([str(elem) for elem in genNumber1])
        
        finalNumber = code + numToStr1
        
        return(finalNumber)
    
    elif country == "France":
        finalNumber = ""
        genNumber1 = []
        genNumber2 = []
        genNumber3 = []
        genNumber4 = []
        code = "+33 06 "
        
        for num in range(0,2):
            number = randint(1,9)
            genNumber1.append(number)
        
        numToStr1 = ''.join([str(elem) for elem in genNumber1])
        
        for num in range(0,2):
            number = randint(1,9)
            genNumber2.append(number)
        
        numToStr2 = ''.join([str(elem) for elem in genNumber2])
        
        for num in range(0,2):
            number = randint(1,9)
            genNumber3.append(number)
        
        numToStr3 = ''.join([str(elem) for elem in genNumber3])
        
        for num in range(0,2):
            number = randint(1,9)
            genNumber4.append(number)
        
        numToStr4 = ''.join([str(elem) for elem in genNumber4])
        
        finalNumber = code + numToStr1 + " " + numToStr2 + " " + numToStr3 + " " + numToStr4
        
        return(finalNumber)
    
    elif country == "Spain":
        finalNumber = ""
        genNumber1 = []
        genNumber2 = []
        genNumber3 = []
        code = "+34 9"
        
        for num in range(0,2):
            number = randint(1,9)
            genNumber1.append(number)
        
        numToStr1 = ''.join([str(elem) for elem in genNumber1])
        
        for num in range(0,3):
            number = randint(1,9)
            genNumber2.append(number)
        
        numToStr2 = ''.join([str(elem) for elem in genNumber2])
        
        for num in range(0,3):
            number = randint(1,9)
            genNumber3.append(number)
        
        numToStr3 = ''.join([str(elem) for elem in genNumber3])
        
        finalNumber = code + numToStr1 + " " + numToStr2 + " " + numToStr3
        
        return(finalNumber)
    
    elif country == "Sweden":
        finalNumber = ""
        genNumber1 = []
        genNumber2 = []
        code = "+45 11 "
        
        for num in range(0,4):
            number = randint(1,9)
            genNumber1.append(number)
        
        numToStr1 = ''.join([str(elem) for elem in genNumber1])
        
        for num in range(0,4):
            number = randint(0,9)
            genNumber2.append(number)
        
        numToStr2 = ''.join([str(elem) for elem in genNumber2])
        
        finalNumber = code + numToStr1 + " " + numToStr2
        
        return(finalNumber)
    else:
        error = "Unknown country"
        return(error)

#Generate date of birth based on the state of "minor" variable
def dateOfBirth(minor):
    if minor == None:
        randomDays = random.randrange(6600, 26352)
        subtraction = date.today()- timedelta(days=randomDays)
        birthDate = subtraction.strftime('%d.%m. %Y')
    elif minor == "on":
        randomDays = random.randrange(500, 6600)
        subtraction = date.today()- timedelta(days=randomDays)
        birthDate = subtraction.strftime('%d.%m. %Y')
        
    return(birthDate)

#Generate ID number (rodné číslo) for CS clients
def idNumberCS(gender, birthDate):
    DOB = birthDate
    year = DOB[-2:]
    monthMale = DOB[3:5]
    monthFemale = int(monthMale) + 50
    day = DOB[0:2]
    identifier = "{:04d}".format(random.randrange(1, 9999))
    idListCS = []
    idNumCS = ""
    
    
    
    if gender == "male":
        idListCS.append(year)
        idListCS.append(monthMale)
        idListCS.append(day)
        idListCS.append("/")
        idListCS.append(identifier)
        idNumCS = ''.join([str(elem) for elem in idListCS])
        
    elif gender == "female":
        idListCS.append(year)
        idListCS.append(monthFemale)
        idListCS.append(day)
        idListCS.append("/")
        idListCS.append(identifier)
        idNumCS = ''.join([str(elem) for elem in idListCS])
            
    return(idNumCS)

#Generate Passport/ID Number
def passportNumber():
    numList = []
    
    for index in range(0,9):
        if index == 0:
            passNumberStep = random.randrange(1,9)
        else:
            passNumberStep = random.randrange(0,9)
            
        numList.append(passNumberStep)
        
    passNumber = ''.join([str(elem) for elem in numList])
    return(passNumber)

#Pull name data from the database based on the nationality and gender
def generateName(gender, funky, foreigner):    
    specialsFrom = 'ÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜÝßàáâãäåçèéêëìíîïñòóôõöùúûüýÿĀāĂăĄąĆćĈĉĊċČčĎďĐđĒēĔĕĖėĘęĚěĜĝĞğĠġĢģĤĥĦħĨĩĪīĬĭĮįİıĶķĸĹĺĻļĽľĿŀŁłŃńŅņŇňŉŊŋŌōŎŏŐőŔŕŖŗŘřŚśŜŝŞşŠšŢţŤťŦŧŨũŪūŬŭŮůŰűŲųŴŵŶŷŸŹźŻżŽžſ'
    specialsTo =   'AAAAAACEEEEIIIINOOOOOUUUUYsaaaaaaceeeeiiiinooooouuuuyyAaAaAaCcCcCcCcDdDdEeEeEeEeEeGgGgGgGgHhHhIiIiIiIiIiKkkLlLlLlLlLlNnNnNnNnNOoOoOoRrRrRrSsSsSsSsTtTtTtUuUuUuUuUuUuWwYyYZzZzZzs'

    con = sqlite3.connect("mysite/testerToolkit_app/project/genData.db")
    cur = con.cursor()
    
    print(gender, funky, foreigner)
    
    nameList = []
    
    if funky == "on":
        cur.execute("SELECT * FROM funkyNamesFirst")
        firstNameAll = cur.fetchall()
        cur.execute("SELECT * FROM funkyNamesLast")
        lastNameAll = cur.fetchall()
    elif funky == None and foreigner == "on" and gender == "male":
        cur.execute("SELECT * FROM maleENGfirst")
        firstNameAll = cur.fetchall()
        cur.execute("SELECT * FROM malefemaleEngLast")
        lastNameAll = cur.fetchall()
    elif funky == None and foreigner == "on" and gender == "female":
        cur.execute("SELECT * FROM femaleENGfirst")
        firstNameAll = cur.fetchall()
        cur.execute("SELECT * FROM malefemaleEngLast")
        lastNameAll = cur.fetchall()
    elif funky == None and foreigner == None and gender == "male":
        cur.execute("SELECT * FROM maleCSfirst")
        firstNameAll = cur.fetchall()
        cur.execute("SELECT * FROM maleCSLast")
        lastNameAll = cur.fetchall()
    elif funky == None and foreigner == None and gender == "female":
        cur.execute("SELECT * FROM femaleCSfirst")
        firstNameAll = cur.fetchall()
        cur.execute("SELECT * FROM femaleCSLast")
        lastNameAll = cur.fetchall()
    else:
        print("Cannot retrieve names from DB")
    
    firstNameIndex = random.randint(1,(len(firstNameAll)-1))
    lastNameIndex = random.randint(1,(len(lastNameAll)-1))
    
    firstNameLine = firstNameAll[firstNameIndex]
    firstNameFull = firstNameLine[1]
    firstName = firstNameFull.replace("\n","")
    nameList.append(firstName)
    lastNameLine = lastNameAll[lastNameIndex]
    lastNameFull = lastNameLine[1]
    lastName = lastNameFull.replace("\n","")
    nameList.append(lastName)
    
    usernameCut = firstName[0:3] + lastName[0:3]
    username = usernameCut.lower()
    
    for i in range(0,len(username)):
        for x in range(0,len(specialsFrom)):
            foundIndex = username.find(specialsFrom[x])
            if foundIndex > -1:
                newUsername = username.replace(specialsFrom[x], specialsTo[x])
                username = newUsername
                break
    
    nameList.append(username)
    
    mailAdress = username.lower() + "@mailinator.com"
    nameList.append(mailAdress)
    
    cur.close() 
    
    return(nameList)

#Generate random adress pulled from DB based on the nationality
def generateAddress(country):    
    con = sqlite3.connect("mysite/testerToolkit_app/project/genData.db")
    cur = con.cursor()

    addresses = []

    if country == "us":
        cur.execute("SELECT * FROM addressUSA")
        address = cur.fetchall()    
    elif country == "gb":
        cur.execute("SELECT * FROM addressUK")
        address = cur.fetchall()    
    elif country == "cz":
        cur.execute("SELECT * FROM addressCS")
        address = cur.fetchall()
    elif country == "eu":
        cur.execute("SELECT * FROM addressEU")
        address = cur.fetchall() 
    else:
        print("What the hell happened?", flush=True)
        
    addressIndex = random.randint(1,(len(address)-1))
    addressLine = address[addressIndex]
    addressCut = list(addressLine)
    del addressCut[0]
    
    if country == "cz":
        addressPart1 = str(addressCut[3]) + " " + str(addressCut[4]) + "/" + str(addressCut[5])
        if str(addressCut[1]) == str(addressCut[2]):
            addressPart2 = str(addressCut[1]) + ", " + str(addressCut[0])
        else:
            addressPart2 = str(addressCut[1]) + " " + str(addressCut[2]) + ", " + str(addressCut[0])
        addressPart3 = str(addressCut[6])
        addressFinal = addressPart1 + ", " + addressPart2 + ", " + addressPart3
    else:
        addressPart1 = str(addressCut[2]) + " " + str(addressCut[3])
        if str(addressCut[1]) == str(addressCut[5]):
            addressPart2 = str(addressCut[0])
        else:
            addressPart2 = str(addressCut[0]) + " " + str(addressCut[1])
        addressPart3 = str(addressCut[4]) + " " + str(addressCut[5])
        addressFinal = addressPart1 + ", " + addressPart2 + ", " + addressPart3
    
    addresses.append(addressFinal)
    
    
    
    if country == "eu" or country == "gb" or country == "us":
        birthCity = addressCut[0]
        country = addressCut[5]
    else:
        cityIndex = random.randint(1,len(address))
        cityLine = address[cityIndex]
        cityCut = list(cityLine)
        birthCity = cityCut[1]
        country = "Česká Republika"
    
    addresses.append(birthCity)
    
    cur.close()
    
    return(addresses, country)

#Generate ICO number from a random template, or Get a random existing ICO from DB
def generateIco(icotype):
    
    if icotype == "random":
        baseIco = []
        stringIco = []
        
        A1 = random.randint(1,9)
        baseIco.append(A1)
        B1 = random.randint(1,9)
        baseIco.append(B1)
        C1 = random.randint(1,9)
        baseIco.append(C1)
        D1 = random.randint(1,9)
        baseIco.append(D1)
        E1 = random.randint(1,9)
        baseIco.append(E1)
        F1 = random.randint(1,9)
        baseIco.append(F1)
        G1 = random.randint(1,9)
        baseIco.append(G1)
        
        A2 = 8
        B2 = 7
        C2 = 6
        D2 = 5
        E2 = 4
        F2 = 3
        G2 = 2
        
        A3 = A1 * A2
        B3 = B1 * B2
        C3 = C1 * C2
        D3 = D1 * D2
        E3 = E1 * E2
        F3 = F1 * F2
        G3 = G1 * G2
        
        A4 = A3 + B3 + C3 + D3 + E3 + F3 + G3
        B4 = A4 % 11
        C4 = 11 - B4
        D4 = C4 % 10
        baseIco.append(D4)
        
        for i in baseIco:
            x = str(i)
            stringIco.append(x)
        
        ico = "".join(stringIco)
    elif icotype == "real":
        con = sqlite3.connect("mysite/testerToolkit_app/project/genData.db")
        cur = con.cursor()
        
        cur.execute("SELECT * FROM ico")
        icoTable = cur.fetchall()    
        
        icoIndex = random.randint(1,len(icoTable))
        icoLine = icoTable[icoIndex]
        icoCut = list(icoLine)
        ico = str(icoCut[1])
        
    return(ico)

#Genereta Concession Document Number
def generateConcessionNumber():
    startCN = str(random.randint(100, 999))
    middleCN = str(random.randint(10, 99))
    lastCN = str(random.randint(100, 999))
    
    concessionNumber = startCN + " " + middleCN + " " + lastCN
    
    return(concessionNumber)

#Generate Custom Email address
def generateCustomEMail(number, gender, namePart, provPart):
    specialsFrom = 'ÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜÝßàáâãäåçèéêëìíîïñòóôõöùúûüýÿĀāĂăĄąĆćĈĉĊċČčĎďĐđĒēĔĕĖėĘęĚěĜĝĞğĠġĢģĤĥĦħĨĩĪīĬĭĮįİıĶķĸĹĺĻļĽľĿŀŁłŃńŅņŇňŉŊŋŌōŎŏŐőŔŕŖŗŘřŚśŜŝŞşŠšŢţŤťŦŧŨũŪūŬŭŮůŰűŲųŴŵŶŷŸŹźŻżŽžſ'
    specialsTo =   'AAAAAACEEEEIIIINOOOOOUUUUYsaaaaaaceeeeiiiinooooouuuuyyAaAaAaCcCcCcCcDdDdEeEeEeEeEeGgGgGgGgHhHhIiIiIiIiIiKkkLlLlLlLlLlNnNnNnNnNOoOoOoRrRrRrSsSsSsSsTtTtTtUuUuUuUuUuUuWwYyYZzZzZzs'

    emailList = []
    mailForeigner = ""
    mailGender = gender
    mailFunky = None
    provList = ["mailinator.com", "yahoo.com", "gmail.com", "hotmail.com", "quigley.net", "quick.net", "volny.cz", "seznam.cz"]
    
    for i in range(0, int(number)):
        foriegnerIdent = random.random()
        
        if foriegnerIdent < 0.5:
            mailForeigner = None
        else:
            mailForeigner = "on"
        
        nameGen = generateName(mailGender, mailFunky, mailForeigner)
        
        if namePart == "fullNameShort":
            name = nameGen[2]
        elif namePart == "fullName":
            name = nameGen[0] + nameGen[1]
        elif namePart == "fullNameDot":
            name = nameGen[0] + "." + nameGen[1]
        elif namePart == "firstNameNumber":
            name = nameGen[0] + str(random. randint(1, 999))
        elif namePart == "lastNameNumber":
            name = nameGen[1] + str(random. randint(1, 999))
        else:
            print("Unknown First Name Part")
        
        username = name
        
        for i in range(0,len(username)):
            for x in range(0,len(specialsFrom)):
                foundIndex = username.find(specialsFrom[x])
                if foundIndex > -1:
                    newUsername = username.replace(specialsFrom[x], specialsTo[x])
                    username = newUsername
                    break
                    
        
        finalNamePart = username.lower()
        
        if provPart == "random":
            newProvider = random.choice(provList)
        else:
            newProvider = provPart
            
        customEmail = finalNamePart + "@" + newProvider
        
        emailList.append(customEmail)
        
    return(emailList)
        
#Generate Sipo Numbers
def generateSIPONum(importNumbers):
    sipo = ""
    key = [3,7,3,1,7,3,1,7,3]
    multiplications = []
    lastNumberBase = 0
    lastNumber = 0
    lastNumberDefiniteve = 0
    importNumbersStr = []
    
    for i in range(0, len(importNumbers)):
        x = importNumbers[i] * key[i]
        multiplications.append(x)
        
    for y in range(0, len(multiplications)):
        lastNumberBase = lastNumberBase + multiplications[y]
    
    lastNumber = 10 - (lastNumberBase % 10)
    lastNumberDefiniteve = str(lastNumber % 10)
    
    for z in range(0, len(importNumbers)):
        w = str(importNumbers[z])
        importNumbersStr.append(w)
    
    sipo = "".join(importNumbersStr) + lastNumberDefiniteve
        
    return(sipo)

#Generate IBAN
def ibanGen(country, bank, account):
    iban = schwifty.IBAN.generate(country, bank, account)
    return iban

#Generate Company Name
def generateCompanyName():
    con = sqlite3.connect("mysite/testerToolkit_app/project/genData.db")
    cur = con.cursor()
    
    cur.execute("SELECT * FROM companyName")
    compTable = cur.fetchall()    
    
    compIndex = random.randint(1,(len(compTable)-1))
    compLine = compTable[compIndex]
    compCut = list(compLine)
    companyName = str(compCut[1])
    
    return(companyName)

#Generate random url
def generateURL():
    con = sqlite3.connect("mysite/testerToolkit_app/project/genData.db")
    cur = con.cursor()
    
    cur.execute("SELECT * FROM urls")
    urlTable = cur.fetchall()    
    
    urlIndex = random.randint(1,(len(urlTable)-1))
    urlLine = urlTable[urlIndex]
    urlCut = list(urlLine)
    url = str(urlCut[1])
    
    return(url)

#↨Generate dates for legal entity Creation
def legalDates(start, end):  
    d1 = datetime.strptime(start, "%Y-%m-%d")
    d2 = datetime.strptime(end, "%Y-%m-%d")
    
    delta = d1 - d2
    
    randomDays = random.randrange(0, delta.days)
    
    subtraction = d2 - timedelta(days=randomDays)
    randomDate = subtraction.strftime("%Y-%m-%d")        
        
    return(randomDate)













