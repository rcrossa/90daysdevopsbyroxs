from flask import Flask, jsonify, request
import datetime
import logging
import os
import time
import psutil  # pip install psutil
from werkzeug.exceptions import BadRequest

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuración desde variables de entorno
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
app.config['PORT'] = int(os.getenv('FLASK_PORT', 5000))

start_time = time.time()

@app.route('/')
def home():
    return jsonify({
        'message': '¡Hola DevOps con Roxs!',
        'timestamp': datetime.datetime.now().isoformat(),
        'status': 'success'
    })

@app.route('/health')
def health():
    uptime = time.time() - start_time
    return jsonify({
        'status': 'healthy',
        'uptime_seconds': round(uptime, 2),
        'memory_usage': f"{psutil.virtual_memory().percent}%",
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.route('/saludo/<nombre>')
def saludo(nombre):
    # Validación básica
    if not nombre or len(nombre.strip()) == 0:
        return jsonify({'error': 'El nombre no puede estar vacío'}), 400
    
    # Sanitización básica
    nombre_limpio = nombre.strip()[:50]  # Limitar longitud
    
    return jsonify({
        'saludo': f'¡Hola {nombre_limpio}!',
        'mensaje': 'Bienvenido a mi aplicación',
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.route('/suma/<int:a>/<int:b>')
def suma(a, b):
    # Validación de rangos
    if abs(a) > 1000000 or abs(b) > 1000000:
        return jsonify({'error': 'Números demasiado grandes'}), 400
    
    resultado = a + b
    logger.info(f'Suma realizada: {a} + {b} = {resultado}')
    return jsonify({
        'operacion': 'suma',
        'numeros': [a, b],
        'resultado': resultado,
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.route('/multiplicacion/<int:a>/<int:b>')
def multiplicacion(a, b):
    # Validación de rangos
    if abs(a) > 1000000 or abs(b) > 1000000:
        return jsonify({'error': 'Números demasiado grandes'}), 400

    resultado = a * b
    logger.info(f'Multiplicación realizada: {a} * {b} = {resultado}')
    return jsonify({
        'operacion': 'multiplicacion',
        'numeros': [a, b],
        'resultado': resultado,
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.route('/calculadora', methods=['POST'])
def calculadora():
    try:
        if not request.is_json:
            return jsonify({'error': 'Content-Type debe ser application/json'}), 415
        data = request.get_json()
        if not data:
            return jsonify({'error': 'JSON requerido'}), 400
            
        operacion = data.get('operacion')
        a = data.get('a')
        b = data.get('b')
        
        if operacion not in ['suma', 'resta', 'multiplicacion', 'division']:
            return jsonify({'error': 'Operación no válida'}), 400
            
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            return jsonify({'error': 'Los números deben ser numéricos'}), 400
        
        if operacion == 'suma':
            resultado = a + b
        elif operacion == 'resta':
            resultado = a - b
        elif operacion == 'multiplicacion':
            resultado = a * b
        elif operacion == 'division':
            if b == 0:
                return jsonify({'error': 'División por cero no permitida'}), 400
            resultado = a / b
            
        return jsonify({
            'operacion': operacion,
            'numeros': [a, b],
            'resultado': resultado,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f'Error en calculadora: {e}')
        return jsonify({'error': 'Error procesando la solicitud'}), 500

@app.route('/info')
def info():
    return jsonify({
        'app': 'Mi App Python DevOps',
        'version': '1.0.0',
        'python_version': os.sys.version,
        'endpoints': [
            '/ - Página principal',
            '/health - Estado de salud',
            '/suma/<a>/<b> - Sumar dos números',
            '/saludo/<nombre> - Saludar por nombre',
            '/calculadora (POST) - Calculadora completa',
            '/info - Información de la app'
        ]
    })

@app.route('/forzar_error')
def forzar_error():
    raise Exception("Error forzado para test")

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint no encontrado', 'status': 404}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f'Error interno: {error}')
    return jsonify({'error': 'Error interno del servidor', 'status': 500}), 500

@app.errorhandler(BadRequest)
def bad_request(error):
    return jsonify({'error': 'Solicitud incorrecta', 'status': 400}), 400

def es_par(n): return n % 2 == 0

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)