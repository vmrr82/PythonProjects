import math
import cmath
from fractions import Fraction
import random

numero = 6.7
to_floor = math.floor(numero)
#print(to_floor)

rSquare = -25
to_square = cmath.sqrt(rSquare)
#print(to_square,type(to_square))

toFraction = Fraction(0.75)
#print(toFraction)



bonoloto = [random.randint(1,49)]
contador = 1
while contador <6:
    numero = random.randint(1,49)
    if numero not in bonoloto:
        bonoloto.append(numero)
        contador+=1
#print(sorted(bonoloto))