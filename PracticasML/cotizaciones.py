import csv
import matplotlib.pyplot as plt
from datetime import datetime

nomb_fich='cotiz_GRIF.csv'
#Cargamos las fechas y los datos de las cotizaciones máximas y mínimas
with open(nomb_fich) as f:
    lectura=csv.reader(f,delimiter=';')
    encabezados=next(lectura)
    fechas, maximos, minimos=[],[],[]
    for fila in lectura:
        fecha=datetime.strptime(fila[0],'%d/%m/%Y')
        maximo=float(fila[6])
        minimo=float(fila[7])
        fechas.append(fecha)
        maximos.append(maximo)
        minimos.append(minimo)

#Trazamos la gráfica con las fechas y las cotizaciones máximas y mínimas en dichos días
plt.style.use('classic') 
fig,ax=plt.subplots()
ax.plot(fechas,maximos,c="red")
ax.plot(fechas,minimos,c='blue')
 
#Damos formato a la gráfica
plt.title("Cotización máxima y mínima de acciones de GRIFOL, 3er trimestre 2021", fontsize=14)
plt.xlabel("Meses julio a septiembre",fontsize=14)
fig.autofmt_xdate()
plt.ylabel("Cotizaciones",fontsize=14)

    


