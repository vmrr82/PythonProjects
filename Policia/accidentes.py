from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from natsort import index_natsorted


libro = pd.read_csv('accidentes.csv')

recuentoAnios = libro.groupby('AÑO').MES.count()
anio2020 = libro[libro.AÑO == 2020]
anio2021 = libro[libro.AÑO == 2021]

xmeses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
gravedad = ['Sin Heridos','Herido Leve','Herido Grave','Fallecido']

meses2020 = anio2020.groupby('MES').AÑO.count().reindex(xmeses,axis=0)
meses2021 = anio2021.groupby('MES').AÑO.count().reindex(xmeses,axis=0)

leve_2020 = anio2020.groupby('MES').HERIDOS_LE.sum().reindex(xmeses,axis=0)
grave_2020 = anio2020.groupby('MES').HERIDOS_GR.sum().reindex(xmeses,axis=0)
falle_2020 = anio2020.groupby('MES').FALLECIDOS.sum().reindex(xmeses,axis=0)

leve_2021 = anio2021.groupby('MES').HERIDOS_LE.sum().reindex(xmeses,axis=0)
grave_2021 = anio2021.groupby('MES').HERIDOS_GR.sum().reindex(xmeses,axis=0)
falle_2021 = anio2021.groupby('MES').FALLECIDOS.sum().reindex(xmeses,axis=0)

# GRÁFICA MESES 2020 Y 2021-------------------
x = np.arange(len(xmeses))+1
width = 0.35

fig,ax = plt.subplots()
a20 = ax.bar(x-width/2,meses2020,width,align='edge')
a21 = ax.bar(x+width/2,meses2021,width,align='edge')

ax.set_xticks(x)
ax.set_xticklabels(xmeses)
ax.grid(True,alpha=0.2)
ax.legend(['2020','2021'])

plt.title('Accidentes por meses')
plt.xlabel('Meses')
plt.ylabel('Total')
fig.tight_layout()
plt.show()

#---------------------------------------------
#GRÁFICA PLOT DOS NIVELES POR GRAVEDAD
plt.subplot(2,1,1)
plt.plot(leve_2020,color='orange',marker='o',label='Heridos Leves')
plt.plot(grave_2020,color='red',marker='o',label='Heridos Graves')
plt.plot(falle_2020,color='black',marker='o',label='Fallecidos')
plt.legend()
plt.grid(True,alpha=0.2)
plt.title('Gravedad Año 2020')

plt.subplot(2,1,2)
plt.plot(leve_2021,color='orange',marker='o',label='Heridos Leves')
plt.plot(grave_2021,color='red',marker='o',label='Heridos Graves')
plt.plot(falle_2021,color='black',marker='o',label='Fallecidos')
plt.legend()
plt.grid(True,alpha=0.2)
plt.title('Gravedad Año 2021')
#plt.plot(leve_2020,label='Heridos Leve',color='orange',linewidth=2,marker='o')
#plt.plot(grave_2020,label='Heridos Graves',color='blue',linewidth=2,marker='o')
#plt.plot(falle_2020,label='Fallecidos',color='black',linewidth=2,marker='o')

plt.legend()
plt.show()





