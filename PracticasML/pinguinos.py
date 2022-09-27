# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 16:50:49 2022

@author: vmrru
"""


import pandas as pd
import matplotlib.pyplot as plt
import seaborn

with open('penguins_mod.csv') as file:
    lectura_pandas = pd.read_csv(file) 
    print(lectura_pandas.head())

fig,ax = plt.subplots()
seaborn.lmplot('bill_length_mm','bill_depth_mm',
       data=lectura_pandas,
       fit_reg=False,
       hue='species')
plt.grid()
seaborn.pairplot(lectura_pandas,hue='species')

                   
    
   
        