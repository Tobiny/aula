from flask import Flask, request, render_template
from datetime import datetime
import serial, time
import mysql.connector

app = Flask(__name__)

# Configuración de la conexión a la base de datos
db_config = {
    'user': 'usuario',
    'password': 'contraseña',
    'host': 'localhost',
    'database': 'nombre_base_datos'
}

# Configuración del puerto serial
serial_port = 'COM6'  # Cambiar al puerto serial correcto


# Ruta para recibir la petición POST del sistema de reconocimiento facial
@app.route('/emotions', methods=['POST'])
def process_emotions():
    # Leer los datos de emociones enviados por el sistema de reconocimiento facial
    data = request.get_json()
    emotion = data['emotion']

    # Leer la temperatura desde el puerto serial
    temperature = read_temperature()

    # Guardar los datos en la base de datos
    save_data(emotion, temperature)

    return 'Datos guardados correctamente'


def read_temperature():
    # Inicializar la conexión con el puerto serial
    ser = serial.Serial(serial_port, 9600)
    # Leer la temperatura desde el puerto serial
    pretemp = ser.read(5)
    temperature = str(pretemp, 'utf-8')
    ser.close()
    return temperature


def save_data(emotion, temperature):
    # Establecer la conexión con la base de datos
    # conn = mysql.connector.connect(**db_config)
    # cursor = conn.cursor()

    # Insertar los datos en la tabla correspondiente
    # query = "INSERT INTO datos_emociones (emocion, temperatura) VALUES (%s, %s)"
    # values = (emotion, temperature)
    # cursor.execute(query, values)

    # Confirmar y cerrar la conexión con la base de datos
    # conn.commit()
    # cursor.close()
    # conn.close()
    print("Recibí", emotion, temperature)


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        if request.form.get('Iniciar'):
            print('Inicio de clase a las ', datetime.now())
        if request.form.get('Terminar'):
            print('Fin de la clase a las ', datetime.now())
    elif request.method == 'GET':
        return render_template('inicio.html')

if __name__ == '__main__':
    app.run()
