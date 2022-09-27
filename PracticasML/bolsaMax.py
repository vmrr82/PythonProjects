# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 13:36:36 2022

@author: vmrru
"""

import csv
import matplotlib.pyplot as plt
from datetime import datetime



with open ('cotiz_GRIF.csv') as f:
    lectura = csv.reader(f,delimiter=';')
    encabezados = next(lectura)
    maximos = []
    fechas = []
    for fila in lectura:
        maximos.append(float(fila[6]))
        fechas.append(datetime.strptime(fila[0], '%d/%m/%Y'))
#print(maximos)
#print(fechas)

plt.style.use('classic')
fig,ax = plt.subplots()
ax.plot(fechas,maximos,c='red')
plt.title("Cotización de acciones de GRIFOL, 3er trimestre 2021", fontsize=16)
plt.xlabel("Meses julio a septiembre",fontsize=14)
plt.ylabel("Valores")
fig.autofmt_xdate()
plt.grid()

