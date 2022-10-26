# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 14:28:44 2022

@author: Crowmorian
"""


# generate random integer values
import random
from random import randint
from random import seed

# seed random number generator
seed(randint(10000,99999))

howMany = 5
whichNums = [0,1,2,3,4,5,6,7,8,9]
canStartZero = False

# generate some integers
def randomNumber(howMany, whichNums, canStartZero):
    randomSequence = (random.choices(whichNums, k = howMany))

    if randomSequence[0] == 0:
        randomNumber(howMany, whichNums, canStartZero)
        print("Retrying")
    else:
        print(randomSequence)
        
randomNumber(howMany, whichNums, canStartZero)




