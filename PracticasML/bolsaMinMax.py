# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 13:36:36 2022

@author: vmrru
"""

import csv
import matplotlib.pyplot as plt
from datetime import datetime


with open('cotiz_GRIF.csv') as file:
    
    lectura = csv.reader(file,delimiter=';')
    encabezados = next(lectura)
    minimas = []
    fechas = []
    maximos = []
    for fila in lectura:
        minimas.append(float(fila[7]))
        fechas.append(datetime.strptime(fila[0],'%d/%m/%Y'))
        maximos.append(float(fila[6]))
    fig,ax = plt.subplots()
    minima, = ax.plot(fechas,minimas, alpha=0.5)
    maxima, = ax.plot(fechas,maximos, c='red', alpha=0.5)
    ax.legend(['Mínimas','Máximas'])
    plt.fill_between(fechas,maximos,minimas,facecolor='grey',alpha=0.5)
    plt.title('Cotización máxima y mínima de acciones GRIFOL, 3er trimestre 2021')
    plt.xlabel('Meses julio a septiembre')
    fig.autofmt_xdate()