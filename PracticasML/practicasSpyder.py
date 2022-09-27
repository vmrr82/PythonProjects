# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

iris_conj = load_iris(as_frame=(True))

#print(format(iris_conj.keys())) #claves conjunto
#print(format(iris_conj['data])) #longitud y anchura pétalos
#print(format(iris_conj['data'].shape)) #150 samples 4 features
#print(format(iris_conj['data'][:5]))# Cinco primeras filas
#print(format(iris_conj['target']))#Identificación de especies
#print(format(iris_conj['target_names']))#Nombre de especies
#print(format(iris_conj['filename']))

#-------------------------------------------------------------------
"""
iris_data = iris_conj['frame']
fig,ax = plt.subplots()

ax.plot(iris_data)

iris_nuevo = load_dataset('iris')
lmplot('petal_width','petal_length',
       data=iris_nuevo, #Correlación entre longitud y anchura de pétalos
       fit_reg=(False),
       hue='species',
       palette=('Set2'), #Colores
       scatter_kws={"s":100}) #Tamaño

plt.title('Diagrama de correlación anchura y longitud de pétalos', color='blue')
plt.grid()
"""
"""
iris_sepalos = load_dataset('iris')
plt.style.use('dark_background')
lmplot('sepal_width','sepal_length',
       data = iris_sepalos,
       fit_reg=False,
       hue='species',
       palette=('Set2'),
       scatter_kws={"s":100})
estilos_plt = plt.style.available
plt.grid()
plt.title('Diagrama de correlación anchura y longitud de sépalos', color='blue')
"""

"""iris_nuevo = sns.load_dataset('iris')
sns.pairplot(iris_nuevo,hue='species') #Función pairplot"""


X_train,X_test,y_train,y_test=train_test_split(iris_conj['data'],iris_conj['target'],random_state=0)


dcorr=pd.plotting.scatter_matrix(X_train,
                                 c=y_train,
                                 figsize=(15,15),
                                 hist_kwds={'bins':20},
                                 s=60,
                                 alpha=0.8)
knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(X_train,y_train)








 