from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime
import serial, time
import emociones as em
import mysql.connector

app = Flask(__name__)

# Configuración de la conexión a la base de datos
db_config = {
    'user': 'admin',
    'password': 'admin',
    'host': 'localhost',
    'database': 'aula_inteligente'
}

# Configuración del puerto serial
serial_port = 'COM6'  # Cambiar al puerto serial correcto


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        if request.form.get('Iniciar'):
            codigo_maestro = request.form.get('codigo')
            materia = request.form.get('materia')
            dia, mes, anio, hora = formated_date()
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(buffered=True)
            query = "INSERT INTO clase (codigo_maestro, materia, dia, mes, anio, hora) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (codigo_maestro, materia, dia, mes, anio, hora)
            cursor.execute(query, values)
            conn.commit()
            query = "SELECT id FROM clase WHERE codigo_maestro = %s AND materia = %s AND dia = %s AND mes = %s " \
                    "AND anio = %s AND hora = %s"
            cursor.execute(query, (codigo_maestro, materia, dia, mes, anio, hora))
            result = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            redirected = redirect(url_for('clase'))
            redirected.set_cookie('id', str(result))
            return redirected
    elif request.method == 'GET':
        return render_template('inicio.html')


@app.route('/clase', methods=['POST', 'GET'])
def clase():
    id_uso = request.cookies.get('id', 1)
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(buffered=True)
    query = "SELECT * FROM lecturas WHERE clase_id = %s"
    cursor.execute(query, (id_uso,))
    lecturas = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("clase.html", lecturas=lecturas)


def formated_date():
    now = datetime.now()
    dia = now.strftime("%d")
    mes = now.strftime("%m")
    anio = now.strftime("%Y")
    hora = now.strftime("%H:%M")
    return dia, mes, anio, hora

def read_temperature():
    # Inicializar la conexión con el puerto serial
    ser = serial.Serial(serial_port, 9600)
    # Leer la temperatura desde el puerto serial
    pretemp = ser.read(5)
    temperature = str(pretemp, 'utf-8')
    ser.close()
    return temperature

if __name__ == '__main__':
    app.run()
