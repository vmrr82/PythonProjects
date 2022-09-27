def aceleUno():  
    print("Los parámetros necesarios son Tiempo(s), Velocidad Inicial(m/s) y Velocidad Final(m/s).")
    tiempo = int(input("Por favor, introduce el tiempo en segundos: "))
    vInicial = int(input("Por favor, introduce la velocidad inicial en m/s: "))
    vFinal = int(input("Por favor, introduce la velocidad final en m/s: "))
    calculo = (vFinal - vInicial)/tiempo
    print (f"La aceleración es de {calculo:.2f}.".format(calculo))

def aceleDos():
    print("Los parámetros necesarios son Tiempo(s), Velocidad Inicial(m/s) y Distancia(m).")
    tiempo = int(input("Por favor, introduce el tiempo en segundos: "))
    vInicial = int(input("Por favor, introduce la velocidad inicial en m/s: "))
    distancia = int(input("Por favor, introduce la distancia: "))
    calculo = (2*distancia-2*vInicial)*tiempo/tiempo**2
    print (f"La aceleración es de {calculo:.2f}.".format(calculo))

def aceleTres():
    print("Los parámetros necesarios son Velocidad Inicial(m/s), Velocidad Final(m/s) y Distancia(m).")
    vInicial = int(input("Por favor, introduce la velocidad inicial en m/s: "))
    vFinal = int(input("Por favor, introduce la velocidad final en m/s: "))
    distancia = int(input("Por favor, introduce la distancia: "))
    calculo = (vFinal**2-vInicial**2)/2*distancia
    print (f"La aceleración es de {calculo:.2f}.".format(calculo))
