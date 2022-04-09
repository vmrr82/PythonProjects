from operaciones.mru import *
from operaciones.conversiones import *

class formulas:

    def __init__(self):
        self.opcion
         
    def opcion(self):
        operaciones = {1:"- Conversor m/s -> km/h.",
                       2:"- Conversor km/h -> m/s.",
                       3:"- Cálculo MRU de velocidad.",
                       4:"- Cálculo MRU de distancia.",
                       5:"- Cálculo MRU de tiempo."}
        for x,y in operaciones.items():
            print(x,y)
        opcion = int(input("Elige una de las operaciones descritas: "))
        if opcion == 1:
            conversormskm()
        elif opcion == 2:
            conversorkmms()   
        elif opcion == 3:
            mruvelocidad()
        elif opcion == 4:
            mrudistancia()
        elif opcion == 5:
            mrutiempo()
            
iniciar = formulas()
iniciar.opcion()


    