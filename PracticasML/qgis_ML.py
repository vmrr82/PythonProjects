# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 11:52:24 2022

@author: vmrru
"""

import pandas as pd
from matplotlib import pyplot as plt

archivo =pd.read_csv('qgis.csv')
dia_semana = archivo[['ALCOHOLEMIA','DIA_SEMANA']].replace(['Negativa','Positivo'],(0,1))
fig,ax = plt.subplots(1)
ax.bar(dia_semana,len(dia_semana))


