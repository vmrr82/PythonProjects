from lzma import FILTER_LZMA1
import pandas as pd

file = pd.read_csv('MLAccidentes.csv',encoding='UTF-8',sep=';').sort_values(by=['fecha'])

vehiculos = file[['turismo','furgon','camion','autobus','motociclet','ciclomotor','bicicleta','vmp','peaton','animal']]

columnas = file.groupby('nucleo')['turismo','furgon','camion','autobus','motociclet','ciclomotor','bicicleta','vmp','peaton','animal'].apply(lambda x: (x=='VERDADERO').sum())

print(columnas)

