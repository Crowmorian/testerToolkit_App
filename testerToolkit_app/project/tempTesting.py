# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 14:28:44 2022

@author: Crowmorian
"""
#Generate random numbers in range
"""
# generate random integer values
from random import randint, seed, choices


# seed random number generator


howManyDigits = 5
howManyNumbers = 6
whichNums = [0,1,2,3,4,5,6,7,8,9]
canStartZero = True
results = []
listToStr = ""


# generate some integers
def randomNumber(howManyDigits, whichNums, canStartZero, howManyNumbers):
    seed(randint(10000,99999))
    
    for i in range(0,howManyNumbers):    
        randomSequence = (choices(whichNums, k = howManyDigits))
    
        while randomSequence[0] == 0 and canStartZero == False:
            randomSequence = (choices(whichNums, k = howManyDigits))
        else:
            listToStr = ''.join([str(elem) for elem in randomSequence])
            results.append(listToStr)
            
    print(results)
        
randomNumber(howManyDigits, whichNums, canStartZero, howManyNumbers)
"""
#Insert data into database
"""
import sqlite3
#Connecting database for generated and required data
con = sqlite3.connect("genData.db")
cur = con.cursor()

rowId = 1

file1 = open('funkyNamesLast3.txt', 'r')
Lines = file1.readlines()
  
for line in Lines:
    line = str(line)
    cur.execute("INSERT INTO funkyNamesLast (ID, Name) VALUES (?,?)", (rowId, line))
    rowId = rowId + 1


con.commit()
cur.close()
"""
#Importing adresses to database
"""
import sqlite3
import csv
#Connecting database for generated and required data
con = sqlite3.connect("genData.db")
cur = con.cursor()

rowId = 1

with open('addressUK.txt', encoding="utf-8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        cur.execute("INSERT INTO addressUK (ID, City, State, Street, Number, ZIP, Country) VALUES (?,?,?,?,?,?,?)", (rowId, row[2], row[3], row[1], row[0], row[4], row[5]))
        line_count += 1
        rowId = rowId + 1

con.commit()
cur.close()
"""
"""
import sqlite3
#Connecting database for generated and required data
con = sqlite3.connect("genData.db")
cur = con.cursor()
file = open('malefemaleENGlast.txt', encoding="utf-8")

rowId = 0

for line in file:
    cur.execute("INSERT INTO malefemaleENGlast (ID, name) VALUES (?,?)", (rowId, line))
    rowId = rowId + 1

con.commit()
cur.close()    
file.close()
"""
#














