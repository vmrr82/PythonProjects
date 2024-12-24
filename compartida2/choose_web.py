from flask import Flask
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import sqlalchemy

# Initialize Flask server
server = Flask(__name__)

# Initialize Dash app with Flask server
app = Dash(
    __name__,
    server=server,
    meta_tags=[
        {'lang': 'es'},
        {'name': "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)

# Set the title of the Dash app
app.title = "Visor de accidentes de tráfico"

# Define the layout of the Dash app
app.layout = html.Div([
    dbc.Row([
        dcc.Dropdown(
            id='location-dropdown',
            options=[
                {'label': 'Andratx', 'value': 'Andratx'},
                {'label': 'Bunyola', 'value': 'Bunyola'},
                {'label': 'Calvià', 'value': 'Calvià'}
            ],
            style={'width': '280px'}
        )
    ])
])

# Global variables for schema and table
schema = "Andratx"
table = "Andratx"

# Function to update the schema and table
def update_schema_and_table(value):
    global schema, table
    schema = value
    table = value

# Define the callback to update the schema and table
@app.callback(
    Output('location-dropdown', 'value'),
    [Input('location-dropdown', 'value')])


def update_output(value):
    if value:
        update_schema_and_table(value)
    return value


# Run the server
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True, port=80)
