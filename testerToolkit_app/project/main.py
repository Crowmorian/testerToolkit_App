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
from datetime import date, timedelta
import subprocess
import pyperclip

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
    return render_template('cs/createIndividual.html')

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
    
@main.route("/createLegalEntity")
@login_required
def createLegalEntity():
    return render_template('createLegalEntity.html')

@main.route("/cs/createLegalEntity")
@login_required
def CScreateLegalEntity():
    return render_template('cs/createLegalEntity.html')

@main.route("/createBussiness")
@login_required
def createBussiness():
    return render_template('createBussiness.html')

@main.route("/cs/createBussiness")
@login_required
def CScreateBussiness():
    return render_template('cs/createBussiness.html')
    
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

#UK Number

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

#US Number

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

#CS Number

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

#EU Number

def phoneNumberEU(country):
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

#Variables taken from POST

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

#Passport ID Number
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

#Pull name data from the database

def generateName(gender, funky, foreigner):
    specialsFrom = 'ÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜÝßàáâãäåçèéêëìíîïñòóôõöùúûüýÿĀāĂăĄąĆćĈĉĊċČčĎďĐđĒēĔĕĖėĘęĚěĜĝĞğĠġĢģĤĥĦħĨĩĪīĬĭĮįİıĶķĸĹĺĻļĽľĿŀŁłŃńŅņŇňŉŊŋŌōŎŏŐőŔŕŖŗŘřŚśŜŝŞşŠšŢţŤťŦŧŨũŪūŬŭŮůŰűŲųŴŵŶŷŸŹźŻżŽžſ'
    specialsTo =   'AAAAAACEEEEIIIINOOOOOUUUUYsaaaaaaceeeeiiiinooooouuuuyyAaAaAaCcCcCcCcDdDdEeEeEeEeEeGgGgGgGgHhHhIiIiIiIiIiKkkLlLlLlLlLlNnNnNnNnNOoOoOoRrRrRrSsSsSsSsTtTtTtUuUuUuUuUuUuWwYyYZzZzZzs'

    con = sqlite3.connect("mysite/testerToolkit_app/project/genData.db")
    cur = con.cursor()
    
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

@main.route('/copyToClipboard',methods=["POST","GET"])
@login_required
def copyToClipboard():
    copyText = request.form.get("value")
    cmd='echo '+copyText.strip()+'|clip'
    subprocess.check_call(cmd, shell=True)
    return "nothing"





























