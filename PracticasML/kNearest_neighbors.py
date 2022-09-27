# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 17:43:41 2022

@author: vmrru
"""
from sklearn.datasets import load_iris
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

iris_conj = load_iris(as_frame=(True))

X_train,X_test,y_train,y_test=train_test_split(iris_conj['data'],iris_conj['target'],random_state=0)

dimensiones = [5.5,4.1,0.8,0.5]
X_a_dimensiones = np.array([dimensiones])

knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(X_train,y_train)

prediccion = knn.predict(X_a_dimensiones)

print("El número correspondiente a la especie que predice el algoritmo es:",format(prediccion))

print("El nombre de la especie correspondiente a ese número es:", format(iris_conj['target_names'][prediccion]))

prediccion_test= knn.predict(X_test)
print("Predicciones realizadas:\n",prediccion_test)

print("La exactitud del modelo es:","{0:.2f}".format(np.mean((prediccion_test==y_test)))) #nivel de exactitud con numpy
print("La exactitud del modelo es: {0:.2f}".format(knn.score(X_test,y_test))) #nivel de exactitud con sklearn
