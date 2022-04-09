from xml.dom.pulldom import CHARACTERS


def aceleracion():
    datos = input("De que datos dispones (TI,VI,VF,DI), introducelos con separación de ,: ")
    opciones = []
    eleccion = "".join(c for c in datos if c.isalpha())
    for xy in eleccion:
        opciones.append(xy)
    print(opciones)

aceleracion()
    
