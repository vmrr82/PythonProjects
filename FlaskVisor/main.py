from flask import Flask
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, MetaData, Table, Select

DATABASE_URL = "postgresql://postgres:hsK0107hdV@localhost:5432/FlaskServer"

engine = create_engine(url=DATABASE_URL, echo=True, future=True)
connection = engine.connect()

meta = MetaData(schema='public') #Cambiar schema
mlAccidentes = Table('Calvia',meta,autoload_with=engine) #Cambiar Tabla

columnas = mlAccidentes.columns.keys()
query = Select(mlAccidentes)
resultSet = connection.execute(query).fetchall()

#postgres to pandas dataframe

file = pd.DataFrame(resultSet, columns=mlAccidentes.columns.keys()).fillna(np.nan)

#mapboxClave = open('E:\Programacion\compartida2\.mapbox_token').read()
layer = "open-street-map"

#Visualización con plotly

hover_columnas = {'Fecha':True, 'Mes':True,'Ubicacion':True,'Gravedad':True,'Alcoholemia':True, 'coord_x':False, 'coord_y':False}
dict_colors = {'POSITIVO':'red','NEGATIVO':'#A1F34E',
               'SIN HERIDOS':'#165806','HERIDO_HOSP-24':'#F4800D','HERIDO_HOSP+24':'#F41E0D','FALLECIDO':'black',
               'DIURNO':'#F4CD0D','NOCTURNO':'#4E2E1F',
               'VERDADERO':'#1E90FF','FALSO':'#FFD700'}

visor = px.scatter_mapbox(data_frame=file, lat=file['coord_y'], lon=file['coord_x'], 
                          mapbox_style='open-street-map',
                          zoom=12,
                          width=1200,
                          height=500,
                          hover_data=hover_columnas,
                          color=file['Gravedad'],
                          color_discrete_map=dict_colors)


#Se crea app
server = Flask(__name__)
app = Dash(server=server,
           meta_tags=[{'lang':'es','name':"viewport","content": "width=device-width, initial-scale=1"}])

app.layout = html.Div(children=[
    html.Meta(httpEquiv="refresh",content="60",lang="es"),
    html.H1(children='VISOR DE ACCIDENTES', id='titulo'),

    html.Div(children='''Dash: A web application framework for your data.''', id='subtitulo'),

    dcc.Graph(id='mapa', figure=visor)
    ]
)


if __name__ == '__main__':
    app.run_server(host="127.0.0.1",debug=True, port=80, use_reloader=True)