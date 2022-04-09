def conversormskm():
        conversormskm =  int(input("Introduce la velocidad en m/s: "))
        tokmh = conversormskm*3.6
        print(str(conversormskm) +  'm/s son ' + str(tokmh) + ' km/h' )

def conversorkmms():
        conversorkmms = int(input("Introduce la velocidad en km/h: "))
        toms = conversorkmms/3
        print(str(conversorkmms) + ' km/h son ' + str(round(toms,2)) + ' m/s')