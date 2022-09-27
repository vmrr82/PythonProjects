import geopy
import pandas as pd
import folium

api = geopy.geocoders.MapBox(api_key='pk.eyJ1Ijoidm1ydWl6IiwiYSI6ImNrdHlweG85eDBicmEybnBjdzl3ZHo5d3EifQ.c4_40DScJjA-URnf1n3zdw')

file = pd.read_csv('GeoCode\MLAccidentes.csv',encoding='UTF-8',sep=';')
file.dropna(subset=['n'],how='all',inplace=True)
file['n'] = file['n'].astype('int').astype('str')
file['direccion_completa'] = file.ubicacion + ", " + file.n + ", " + file.nucleo
file['gcode'] = file.direccion_completa.apply(api.geocode)

file['lat'] = [g.latitude for g in file.gcode]
file['long'] = [g.longitude for g in file.gcode]

direcciones = pd.concat([file['direccion_completa'],file['lat'],file['long']],axis=1)
print(direcciones.head(10))




"""mapa = folium.Map(location=(39.528454368023205, 2.5078566859760225), zoom_start=5)
for index, row in file.iterrows():
    folium.Marker(location=(row['lat'],row['long']),tooltip=row['ubicacion'] + ", " +  row['n'] + ", " +row['nucleo']).add_to(mapa)
mapa.save('index.html')"""