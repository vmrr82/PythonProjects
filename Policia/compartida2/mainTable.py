import sqlalchemy
from sqlalchemy import create_engine, MetaData
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, dash_table,ctx, no_update
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output
from dash.exceptions import PreventUpdate
import numpy as np
import flask
#from waitress import serve

mapboxClave = open('compartida2\.mapbox_token').read()
# postgres connection
engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres',encoding='UTF-8', echo=True, future=True)
#engine = create_engine('postgresql://polgis:polcalvia@crates:5432/polgis',encoding='UTF-8', echo=True, future=True)

connection = engine.connect()
meta = MetaData()
mlAccidentes = sqlalchemy.Table('MLAccidentes',meta,autoload=True,autoload_with=engine)
columnas = mlAccidentes.columns.keys()
query = sqlalchemy.select([mlAccidentes])
resultsProxy = connection.execute(query)

resultSet = resultsProxy.fetchall()

#postgres to pandas dataframe

file = pd.DataFrame(resultSet).fillna(np.nan)

#Correcciones tabla
dia_semana = file['dia_semana'].replace({1:'LUNES',2:'MARTES',3:'MIÉRCOLES',4:'JUEVES',5:'VIERNES',6:'SÁBADO',7:'DOMINGO'},inplace=True)
tipo_veh = file.groupby(by=['turismo','furgon','camion','autobus','motociclet','ciclomotor','bicicleta','vmp','peaton','animal'],dropna=False).count()
file.columns = file.columns.str.replace('alcoholemi','alcoholemia')
file['n'] = file['n'].fillna('-')
file['mes'] = file['mes'].astype(str)
file['ubicacion_'] = file['ubicacion_'].fillna('-').astype(str)
file['ubicacion'] = file['ubicacion'].fillna('-').astype(str)
file['nucleo'] = file['nucleo'].astype(str)
file['alcoholemia'] = file['alcoholemia'].str.upper().astype(str)
file['aÑo'] = file.iloc[:,5].fillna(0).astype(str).str[:4]
file['dia_semana'] = file.iloc[:,7].astype(str).str.upper()
renamesSemana = file.rename(columns={'dia_semana':'dia semana'},inplace=True)
file['gravedad'] = file['gravedad'].str.upper().astype(str)
file['horario'] = np.where((file.hora > file.HORARIO_SOL_AMANECER) & (file.hora < file.HORARIO_SOL_OCASO),'DIURNO','NOCTURNO')
#------------------------------------------------------#


layer = "open-street-map"

server = flask.Flask(__name__)
app = Dash(__name__,server=server,meta_tags=[{'lang':'es','name':"viewport","content": "width=device-width, initial-scale=1"}])
app.title = "Visor de accidentes de tráfico de Calvià"



app.layout = html.Div(lang='es',style={'width':'1536px','height':'864px'},
    children =[html.Div([
        dbc.Row([html.Div([
            html.H1("VISOR DE ACCIDENTES",className='header',style={'color':'#fff','font-family':'monospace'}),
            html.Img(src=r"assets/Policia_Local_Derecha.png",width='400px',title='Ajuntament de Calvià - Policía Local',className="bloqIcon"),
            html.H2("POLICÍA LOCAL DE CALVIÀ",className='secondHeader',style={'color':'#fff','font-family':'monospace'})])],className='top'),

        dbc.Row([html.Div([
                    html.H3("TOTAL ACCIDENTES",className='tituloTotal'),
                    html.P(file['id'].count(),className='numTotal')],style={'width':'220px','height':'120px'},className='bloqTotal'),
                html.Div([
                    html.H3('PRIMERO REGISTRADO',className='tituloPrimero'),
                    html.P(pd.to_datetime(file['fecha']).min().strftime('%d-%m-%Y'),className='numFecha')],
                            style={'width':'260px','height':'120px'},className='bloqPrimero'),
                html.Div([
                    html.H3('ÚLTIMO REGISTRADO',className='tituloUltimo'),
                    html.P(pd.to_datetime(file['fecha']).max().strftime('%d-%m-%Y'),className='numFecha')],
                            style={'width':'240px','height':'120px'},className='bloqUltimo'),
                html.Div([
                    html.H3('MÁXIMO DIARIO',className='tituloMaxDiario'),
                    html.P(file['fecha'].value_counts().max(),className='numeroMaxDiario')],
                                style={'width':'210px','height':'120px'},className='bloqDiario'),
                html.Div([
                    html.H3('MÁXIMO IMPLICADOS',className='tituloMaxImplicados'),
                    html.P(file['n_vehÍc'].max(),className='numeroMaxImplicados')],
                        style={'width':'240px','height':'120px'},className='bloqImplicados'),
                html.Button(className='contact-button',title='atestados@calvia.com')],className='bloquesSup'),

        dbc.Row([html.Div([
            dbc.Col(
                html.Div([dcc.RadioItems(id="radioItem", options=["Puntos de colisión","Heatmap"],value="Puntos de colisión")],className='radioItem')),
            dbc.Col(
                html.Div([dcc.Graph(id='mapaCallback',responsive=True,config={'displaylogo':False,'displayModeBar':True,'showLink':False},
                            style={'width':'700px','height':'500px'})]),className='mapa')]),
            dbc.Col([
                html.Div([dash_table.DataTable(
                                    columns=[{  'name':'ID','id': 'id','type':'numeric','selectable':False,'hideable':True},{
                                                'name':'FECHA','id': 'fecha','type':'datetime','selectable':False,'hideable':True},{
                                                'name':'AÑO','id': 'aÑo','type':'text','selectable':True,'hideable':True},{
                                                'name':'MES','id':'mes','type':'text','selectable':True,'hideable':True},{
                                                'name':'DÍA SEMANA','id':'dia semana','type':'text','selectable':True,'hideable':True},{
                                                'name':'UBICACIÓN','id':'ubicacion','type':'text','selectable':False,'hideable':True},{
                                                'name':'NÚCLEO','id':'nucleo','type':'text','selectable':True,'hideable':True},{
                                                'name':'Nº VEHÍC.','id':'n_vehÍc','type':'text','selectable':True,'hideable':True},{
                                                'name':'GRAVEDAD','id':'gravedad','type':'text','selectable':True,'hideable':True},{
                                                'name':'ALCOHOLEMIA','id':'alcoholemia','type':'text','selectable':True,'hideable':True},{
                                                'name':'HORARIO','id':'horario','type':'text','selectable':True,'hideable':True}
                                                ],
                                    style_cell_conditional=[{'if':{'column_id':'id'},'width':'40px'},
                                                            {'if':{'column_id':'aÑo'},'width':'57px'},
                                                            {'if':{'column_id':'fecha'},'width':'80px'},
                                                            {'if':{'column_id':'mes'},'width':'80px'},
                                                            {'if':{'column_id':'ubicacion'},'width':'80px'},
                                                            {'if':{'column_id':'dia semana'},'width':'100px'},
                                                            {'if':{'column_id':'gravedad'},'width':'100px'},
                                                            {'if':{'column_id':'nucleo'},'width':'140px'},
                                                            {'if':{'column_id':'n_vehÍc'},'width':'100px'},
                                                            {'if':{'column_id':'alcoholemia'},'width':'110px'},
                                                            {'if':{'column_id':'horario'},'width':'80px'}],
                                    data=file.to_dict('records'),
                                    page_size=20,
                                    page_action='native',
                                    style_as_list_view=True,
                                    filter_options={'case':'insensitive'},
                                    filter_action='native',
                                    filter_query = '',
                                    column_selectable="single",
                                    sort_action='native',
                                    sort_mode='single',
                                    sort_by=[{'column_id':'fecha','direction':'desc'}],
                                    selected_columns=[],
                                    row_selectable='single',
                                    fixed_rows={'headers': True},
                                    style_table={'overflowY': 'auto',
                                                 'overflowX':'auto',
                                                 'height':'400px',
                                                 'width':'700px'},
                                    style_cell={'textAlign': 'left',
                                                'overflow': 'hidden',
                                                'textOverflow': 'ellipsis',
                                                'fontSize':10},
                                    style_data={'color': '#1a4775',
                                                'backgroundColor': 'white',
                                                'height':10},
                                    style_data_conditional=[{'if': {'row_index': 'odd'},'backgroundColor': 'white'},
                                                            {'if':{'filter_query':'{gravedad} = "FALLECIDO"','column_id':'gravedad'},'backgroundColor':'#918C8C'},
                                                            {'if':{'filter_query':'{gravedad} = "HERIDO_HOSP-24"','column_id':'gravedad'},'backgroundColor':'#F7C699'},
                                                            {'if':{'filter_query':'{gravedad} = "HERIDO_HOSP+24"','column_id':'gravedad'},'backgroundColor':'#F68978'},
                                                            {'if':{'filter_query':'{alcoholemia} = "POSITIVO"','column_id':'alcoholemia'},'backgroundColor':'#FA7D7D'},
                                                            {'if':{'filter_query':'{horario} = "NOCTURNO"','column_id':'horario'},'backgroundColor':'#C3BDBD'}],
                                    tooltip_header={col: "Selecciona una columna para observar los resultados en el mapa."
                                                    for col in file},
                                     style_header={'backgroundColor': 'white',
                                                    'color': '#1a4775',
                                                    'fontWeight': 'bold', 
                                                    'align':'center'},
                                    style_filter={'backgroundColor':'white',
                                                    'color':'white',
                                                    'width':'180px'},id='mainTable')]),
                            html.Div(id='totalFilter',className='totalFilter'),
                            html.Div([html.Button(id='clear_filter',children='Limpiar Formulario',n_clicks=0)],id='filterButton')])],className='rowOne'),

        dbc.Row([html.Div(dcc.Graph(figure={'layout':{'paper_bgcolor':'rgb(8, 34, 85)','plot_bgcolor':'rgb(8, 34, 85)','font':{'color':'white'}}},id='figraphs',responsive=True,
                        config={'displaylogo':False,'displayModeBar':False,'showLink':False},style={'width':'700px','height':'550px'}),className='figGraphs'),
                 html.Div(dcc.Graph(figure={'layout':{'paper_bgcolor':'rgb(8, 34, 85)','plot_bgcolor':'rgb(8, 34, 85)','font':{'color':'white'}}},id='secondFigGraphs',responsive=True,
                        config={'displaylogo':False,'displayModeBar':False,'showLink':False},style={'width':'700px','height':'550px'}),className='secondFigGraphs')],className='rowTwo')
       ])
    ])

#------------------------------------------------------------------------------------------------------------#     
           
file['cluster'] = np.random.randint(1,30,len(file['ubicacion']))
column_order = {'dia semana':['LUNES','MARTES','MIÉRCOLES','JUEVES','VIERNES','SÁBADO','DOMINGO'],
                'gravedad':['SIN HERIDOS','HERIDO_HOSP-24','HERIDO_HOSP+24','FALLECIDO'],
                'mes':['ENERO','FEBRERO','MARZO','ABRIL','MAYO','JUNIO','JULIO','AGOSTO','SEPTIEMBRE','OCTUBRE','NOVIEMBRE','DICIEMBRE'],
                'aÑo':['2020','2021','2022']}

dict_colors = {'POSITIVO':'red','NEGATIVO':'#A1F34E',
                    'SIN HERIDOS':'#165806','HERIDO_HOSP-24':'#F4800D','HERIDO_HOSP+24':'#F41E0D','FALLECIDO':'black',
                    'DIURNO':'#F4CD0D','NOCTURNO':'#4E2E1F'}


#Callbacks------------------------------------------------------------------------------------------------------#

@app.callback(Output('totalFilter','children'),Input('mainTable','derived_virtual_data'))
def countFilter(value):
    try:
        return 'Resultados filtro    ' + str(len(value))
    except TypeError:
        return no_update

@app.callback(Output('mapaCallback','figure'),
              [Input('mainTable','derived_virtual_data'),
              Input('mainTable','selected_columns'),Input('radioItem','value'),
              Input('mainTable','selected_row_ids')],prevent_initial_call=True)
def update_graphs(filter_table,selected_columns,radioItem,selected_row):

    if selected_columns is None:
        raise PreventUpdate
    
    if selected_row is None:
        selected_row = []
    pd.options.mode.chained_assignment = None #warning off
    
    dff = file if filter_table is None else pd.DataFrame(filter_table)
   
    templatesHover = """
    <b>ID: </b>%{customdata[8]}<br>
    <b>FECHA: </b>%{customdata[0]}<br>
    <b>HORA: </b>%{customdata[1]}<br>
    <b>UBICACIÓN: </b> %{customdata[2]}<br>
    <b>Nº: </b> %{customdata[3]}<br>
    <b>CRUCE: </b> %{customdata[4]}<br>
    <b>NÚCLEO: </b> %{customdata[5]}<br>
    <b>GRAVEDAD: </b> %{customdata[6]}<br>
    <b>ALCOHOLEMIA: </b> %{customdata[7]}<br>
    <b>Nº IMPLICADOS: </b> %{customdata[9]}<br>"""

    updateMenusMap = [dict(buttons=list([
                                        dict(args=['mapbox.style',"open-street-map"],
                                            label='Open-Street-Map',
                                            method='relayout'),
                                        dict(args=['mapbox.style', "satellite-streets"],
                                            label="Fotografía",
                                            method='relayout')]),
                                        type='dropdown',
                                        x=.3,
                                        borderwidth=1.5)]
    #Don't Touch 
    file['n_vehÍc'] = file['n_vehÍc'].astype(str)
    c = ctx.args_grouping

    if radioItem == 'Heatmap': #density mapbox
        
            figHeatmap = px.density_mapbox(file, lat=file['coord_y'],lon=file['coord_x'],
                            radius=4,
                            center=dict(lat=39.50599813464821, lon=2.501832035716808), 
                            zoom=11,
                            hover_name='nucleo',
                            mapbox_style= "open-street-map")
            figHeatmap.update_layout(margin={"r":5,"t":5,"l":5,"b":5},coloraxis_showscale=True,
                                    xaxis_tickangle=45, plot_bgcolor='rgb(8, 34, 85)', paper_bgcolor='rgb(8, 34, 85)',font=dict(color='#8a8d93'))
           
            return figHeatmap

    elif radioItem == 'Puntos de colisión': #Puntos de colisión

        fig1 = px.scatter_mapbox(file,lat=file['coord_y'],
                                 lon=file['coord_x'],
                                color=file['gravedad'],
                                zoom=12, 
                                height=550,width=700,
                                category_orders={'gravedad':['SIN HERIDOS','HERIDO_HOSP-24','HERIDO_HOSP+24','FALLECIDO']},
                                mapbox_style="open-street-map",
                                hover_data=['fecha','hora','ubicacion','n','ubicacion_','nucleo','gravedad','alcoholemia','id','n_vehÍc'],
                                color_discrete_map=dict_colors)
        fig1.update_traces(hovertemplate=templatesHover,hoverinfo="none",hoverlabel=dict(bgcolor='#F7F2F1',font_size=11))
        fig1.update_layout(legend_title_text='gravedad'.upper(),legend_borderwidth=2, legend_title_side='top',
                                legend_bordercolor='#fff',legend_font_color='#fff',plot_bgcolor='rgb(8, 34, 85)', 
                                paper_bgcolor='rgb(8, 34, 85)',font=dict(color='#8a8d93'),
                                margin={"r":150,"t":5,"l":5,"b":5},mapbox_accesstoken=mapboxClave,
                                        margin_autoexpand=True,
                                        autosize=True,
                                        updatemenus=updateMenusMap)
        

        if c[0].triggered: #filter datatble
            try:        
                fig1 = px.scatter_mapbox(dff,lat=dff['coord_y'],lon=dff['coord_x'],
                                    color='gravedad',
                                    zoom=12, 
                                    height=550,width=700,
                                    category_orders={'gravedad':['SIN HERIDOS','HERIDO_HOSP-24','HERIDO_HOSP+24','FALLECIDO']},
                                    mapbox_style="open-street-map",
                                    hover_data=['fecha','hora','ubicacion','n','ubicacion_','nucleo','gravedad','alcoholemia','id','n_vehÍc'],
                                    color_discrete_map={'POSITIVO':'red','NEGATIVO':'#A1F34E',
                                                        'SIN HERIDOS':'#A1F34E','HERIDO_HOSP-24':'#F4800D','HERIDO_HOSP+24':'#F41E0D','FALLECIDO':'black',
                                                        'DIURNO':'#F4CD0D','NOCTURNO':'#4E2E1F'})
                fig1.update_traces(hovertemplate=templatesHover,hoverinfo="none",hoverlabel=dict(bgcolor='#F7F2F1',font_size=11))
                fig1.update_layout(legend_title_text='gravedad'.upper(),legend_borderwidth=2, legend_title_side='top',
                                    legend_bordercolor='#fff',legend_font_color='#fff',plot_bgcolor='rgb(8, 34, 85)', 
                                    paper_bgcolor='rgb(8, 34, 85)',font=dict(color='#8a8d93'),
                                    margin={"r":150,"t":5,"l":5,"b":5},mapbox_accesstoken=mapboxClave,
                                        margin_autoexpand=True,
                                        autosize=True,
                                        updatemenus=updateMenusMap)
                return fig1
            except KeyError:
                return no_update   
    
        elif c[1].triggered: #select columns
            scatter_column = px.scatter_mapbox(file,lat=file['coord_y'],
                                                    lon=file['coord_x'],
                                    color=file[selected_columns[0]],
                                    zoom=12,
                                    category_orders=column_order,
                                    mapbox_style="open-street-map",
                                    color_discrete_map=dict_colors,
                                    hover_data=[file['fecha'],file['hora'],file['ubicacion'],file['n'],file['ubicacion_'],file['nucleo'],file['gravedad'],file['alcoholemia'],file['id'],file['n_vehÍc']])
            scatter_column.update_traces(hovertemplate=templatesHover,hoverinfo="none",hoverlabel=dict(bgcolor='#F7F2F1',font_size=11))
            scatter_column.update_layout(legend_font_color='#fff',legend_title_text=selected_columns[0].upper(),
                                        legend_traceorder='normal',xaxis_tickangle=45, plot_bgcolor='rgb(8, 34, 85)',paper_bgcolor='rgb(8, 34, 85)',
                                        font=dict(color='#8a8d93'),legend_borderwidth=2, legend_bordercolor='#fff',
                                        legend_title_side='top',mapbox_accesstoken=mapboxClave,
                                        margin={"r":150,"t":5,"l":5,"b":5},
                                        margin_autoexpand=True,
                                        autosize=True,
                                        updatemenus=updateMenusMap)
            
            return scatter_column
        
        elif c[3].triggered:#selected_row
            dfrow = file[file.id == selected_row[0]]
            fig1Row = px.scatter_mapbox(dfrow,
                                    lat=dfrow['coord_y'],
                                    lon=dfrow['coord_x'],
                                    color=selected_columns[0],
                                    zoom=14, 
                                    height=550,width=700,
                                    category_orders={'gravedad':['SIN HERIDOS','HERIDO_HOSP-24','HERIDO_HOSP+24','FALLECIDO']},
                                    mapbox_style="open-street-map",
                                    hover_data=['fecha','hora','ubicacion','n','ubicacion_','nucleo','gravedad','alcoholemia','id','n_vehÍc'],
                                    color_discrete_map=dict_colors)
            fig1Row.update_traces(hovertemplate=templatesHover,hoverinfo="none",hoverlabel=dict(bgcolor='#F7F2F1',font_size=11))
            fig1Row.update_layout(legend_title_text=selected_columns[0].upper(),legend_borderwidth=2, legend_title_side='top',
                                    legend_bordercolor='#fff',legend_font_color='#fff',plot_bgcolor='rgb(8, 34, 85)', 
                                    paper_bgcolor='rgb(8, 34, 85)',font=dict(color='#8a8d93'),
                                    margin={"r":150,"t":5,"l":5,"b":5},mapbox_accesstoken=mapboxClave,
                                    margin_autoexpand=True,
                                    autosize=True,
                                    updatemenus=updateMenusMap)
            
            return fig1Row          
        return fig1

#histogram from columns
@app.callback(Output('figraphs','figure'),
                Output('secondFigGraphs','figure'),
            Input('mainTable','selected_columns'),prevent_initial_call=True)

def rowsToGraph(selected_columns):

    if selected_columns[0] is None:
        raise PreventUpdate

#pie
    pie = px.pie(file,names=file[selected_columns[0]],
                color=file[selected_columns[0]],     
                color_discrete_map=dict_colors)
    
    pie.update_traces(showlegend=True)
    pie.update_layout(margin_autoexpand=False,margin=dict(r=190),legend_font_color='#fff',legend_itemclick=False,legend_title_text=selected_columns[0].upper())
    pie.update_layout(title_text=f'TOTALES {selected_columns[0]}'.upper(),title_font=dict(size=20, color='#fff', family="Lato, sans-serif"),xaxis_tickangle=0, plot_bgcolor='rgb(8, 34, 85)', paper_bgcolor='rgb(8, 34, 85)',font=dict(color='#8a8d93'))
    pie.update_traces(sort=False,pull=0.1, textinfo='label',textposition='inside',hoverinfo='label+percent+value',hovertemplate="%{label}<br>Total: %{value}<br>Porcentaje %{percent}<extra></extra>",)
    
#hist
    hist = px.histogram(file, x=file[selected_columns[0]], 
                                color="aÑo", barmode="group",
                                category_orders=column_order,
                                color_discrete_map=dict_colors)
    hist.update_xaxes(showticklabels=True,categoryorder='array',showline=True)
    hist.update_traces(hovertext=None, hovertemplate="Total: %{y},<br>%{x}")
    hist.update_layout(title_text=f'TOTAL {selected_columns[0]} POR AÑOS.'.upper(),showlegend=True,legend_title="")
    hist.update_layout(margin=dict(t=70, b=0, l=70, r=40),
                            xaxis_tickangle=45,
                            xaxis_title=' ', yaxis_title=" ",
                            plot_bgcolor='rgb(8, 34, 85)', paper_bgcolor='rgb(8, 34, 85)',
                            title_font=dict(size=20, color='#fff', family="Lato, sans-serif"),
                            font=dict(color='#8a8d93'),
                            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                            legend_itemclick="toggleothers")

    return pie,hist

    
#filter clean
  

@app.callback([Output('mainTable','filter_query'),Output('mainTable','selected_columns'),Output('mainTable','selected_row_ids')],
                    Input('clear_filter','n_clicks'))

def resetFilter(n_clicks): 
    if n_clicks is not None:
        return "",['gravedad'],[]
   

if __name__ == '__main__':
    app.run_server(host='0.0.0.0',debug=True,port=80)
    #serve(app.server, host='0.0.0.0',port=80)
    
    
