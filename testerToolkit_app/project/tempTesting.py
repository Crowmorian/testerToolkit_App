# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 14:28:44 2022

@author: Crowmorian
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