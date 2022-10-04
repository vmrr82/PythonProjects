import random
import os,time


contador = 0
while contador <5:
    numerosTablas = [2,3,4,5,6]
    numeros = [2,3,4,5,6,7,8,9,10]
    
    num1 = random.choice(numerosTablas)
    num2 = random.choice(numeros)

    operacion = num1 * num2
    
    print('Puntuación: ' + str(contador))
    resultado = int(input('Cuanto es ' + str(num1) + ' x ' + str(num2) + ': '))
    
                                             
    if resultado == operacion:
        print('muy bien Mario, acertaste')
        contador +=1
        time.sleep(2)
        print(os.system('cls'))
    else:
        print('lo siento Mario, no es correcto, el resultado es ' + str(operacion))    
        contador -=1
        time.sleep(2)
        print(os.system('cls'))
        
else:
    print('Muy bien Mario, acabaste el ejercicio')
