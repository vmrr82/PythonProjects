 
def mruvelocidad():
    distancia = int(input("Por favor, introduce la distancia en metros: "))
    tiempo = int(input("Por favor, introduce el tiempo en segundos: "))
    calculo = round(distancia/tiempo,2)
    print(f"La velocidad es de  {calculo:.2f}  m/s".format(calculo))
        
def mrudistancia():
    velocidad = int(input("Por favor, introduce la velocidad en m/s: "))
    tiempo = int(input("Por favor, introduce la velocidad en segundos: "))
    calculo = round(velocidad*tiempo,2)
    print(f"La distancia es de {calculo:.2f} metros".format(calculo))

def mrutiempo():
    distancia = int(input("Por favor, introduce la distancia en metros: "))
    velocidad = int(input("Por favor, introduce la velocidad en m/s: "))
    calculo = round(distancia/velocidad,2)
    print(f"El tiempo es de {calculo:.2f} segundos".format(calculo))