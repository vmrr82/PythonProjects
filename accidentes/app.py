from flask import Flask, request, jsonify, render_template
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import logging

app = Flask(__name__)

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de la conexión a PostgreSQL usando variables de entorno
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'FlaskServer')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASS = os.environ.get('DB_PASS', 'hsK0107hdV')

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            options="-c client_encoding=UTF8"
        )
        return conn
    except psycopg2.DatabaseError as e:
        logger.error(f"Error connecting to the database: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/accidentes', methods=['POST'])
def agregar_accidente():
    data = request.json

    if not all(key in data for key in ['fecha', 'hora', 'ubicacion', 'gravedad', 'tipo_vehiculos', 'victimas', 'coordenadas']):
        return jsonify({'status': 'error', 'message': 'Datos incompletos'}), 400

    try:
        lat, lng = map(float, data['coordenadas'].split(', '))
    except ValueError:
        return jsonify({'status': 'error', 'message': 'Coordenadas inválidas'}), 400

    with get_db_connection() as conn:
        if conn:
            try:
                with conn.cursor() as cur:
                    cur.execute('''
                        INSERT INTO public.calvia (fecha, hora, ubicacion, gravedad, tipo_vehiculos, victimas, lat, lng)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING id
                    ''', (data['fecha'], data['hora'], data['ubicacion'], data['gravedad'], data['tipo_vehiculos'], data['victimas'], lat, lng))
                    conn.commit()
                    accidente_id = cur.fetchone()[0]
                    return jsonify({
                        'status': 'success',
                        'id': accidente_id,
                        'fecha': data['fecha'],
                        'hora': data['hora'],
                        'ubicacion': data['ubicacion'],
                        'gravedad': data['gravedad'],
                        'tipo_vehiculos': data['tipo_vehiculos'],
                        'victimas': data['victimas'],
                        'lat': lat,
                        'lng': lng,
                        'coordenadas': [lat, lng]
                    }), 201
            except psycopg2.DatabaseError as e:
                logger.error(f"Error inserting data: {e}")
                return jsonify({'status': 'error', 'message': 'Error al insertar datos en la base de datos'}), 500
        else:
            logger.error("Database connection failed")
            return jsonify({'status': 'error', 'message': 'Database connection failed'}), 500

@app.route('/api/accidentes', methods=['GET'])
def obtener_accidentes():
    with get_db_connection() as conn:
        if conn:
            try:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute('SELECT * FROM public.calvia')
                    accidentes = cur.fetchall()
                    for accidente in accidentes:
                        accidente['hora'] = accidente['hora'].strftime('%H:%M:%S')
                        accidente['coordenadas'] = [accidente['lat'], accidente['lng']]
                    return jsonify(accidentes)
            except psycopg2.DatabaseError as e:
                logger.error(f"Error fetching data: {e}")
                return jsonify({'status': 'error', 'message': 'Error al obtener datos de la base de datos'}), 500
        else:
            logger.error("Database connection failed")
            return jsonify({'status': 'error', 'message': 'Database connection failed'}), 500

if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True, port=5000)
