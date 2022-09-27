# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 06:43:41 2022

@author: vmrru
"""

import pandas as pd
import matplotlib.pyplot as plt
import datetime

with open('Basilea_clima.csv') as file:
    lectura = pd.read_csv(file, delimiter=',')
    print(lectura.info()) #número de columnas y encabezados
    print(str(len(lectura['Basilea_Temperature'])) + " mediciones.")
fg,ax = plt.subplots()
plt.style.use('seaborn')
ax.plot(lectura['Basilea_Temperature'], c='red')
fechas = []
for fila in lectura['timestamp']:
    pd.Timestamp(fechas.append(fila))

for x in lectura['timestamp']:
    if x[3] in fechas:
        print("fecha" + str(x[3]))
        