import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import json
from app import app, es_par

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_status_code(client):
    response = client.get('/')
    assert response.status_code == 200

def test_home_response_json(client):
    response = client.get('/')
    data = response.get_json()
    assert isinstance(data, dict)
    assert 'message' in data
    assert data['message'] == '¡Hola DevOps con Roxs!'
    assert 'timestamp' in data
    assert 'status' in data
    assert data['status'] == 'success'

def test_health_status_code(client):
    response = client.get('/health')
    assert response.status_code == 200

def test_health_response_json(client):
    response = client.get('/health')
    data = response.get_json()
    assert isinstance(data, dict)
    assert data['status'] == 'healthy'
    assert 'uptime_seconds' in data
    assert isinstance(data['uptime_seconds'], float)
    assert data['uptime_seconds'] >= 0
    assert 'memory_usage' in data
    assert data['memory_usage'].endswith('%')
    percent = float(data['memory_usage'].replace('%', ''))
    assert 0 <= percent <= 100
    assert 'timestamp' in data

def test_es_par_true():
    assert es_par(2) is True
    assert es_par(0) is True
    assert es_par(-4) is True

def test_es_par_false():
    assert es_par(1) is False
    assert es_par(-3) is False
    assert es_par(99) is False

def test_saludo_ok(client):
    response = client.get('/saludo/Roxs')
    assert response.status_code == 200
    data = response.get_json()
    assert 'saludo' in data
    assert data['saludo'] == '¡Hola Roxs!'
    assert data['mensaje'] == 'Bienvenido a mi aplicación'
    assert 'timestamp' in data

def test_saludo_nombre_vacio(client):
    response = client.get('/saludo/')
    # Flask will return 404 for missing parameter, not 400
    assert response.status_code == 404

def test_saludo_nombre_espacios(client):
    response = client.get('/saludo/   ')
    data = response.get_json()
    assert response.status_code == 400
    assert 'error' in data
    assert data['error'] == 'El nombre no puede estar vacío'

def test_saludo_nombre_largo(client):
    nombre_largo = 'a' * 100
    response = client.get(f'/saludo/{nombre_largo}')
    assert response.status_code == 200
    data = response.get_json()
    # Nombre debe estar truncado a 50 caracteres
    assert data['saludo'] == f'¡Hola {"a"*50}!'

def test_suma_ok(client):
    response = client.get('/suma/3/5')
    assert response.status_code == 200
    data = response.get_json()
    assert data['operacion'] == 'suma'
    assert data['numeros'] == [3, 5]
    assert data['resultado'] == 8
    assert 'timestamp' in data
   
def test_multiplicacion_ok(client):
    response = client.get('/multiplicacion/4/5')
    assert response.status_code == 200
    data = response.get_json()
    assert data['operacion'] == 'multiplicacion'
    assert data['numeros'] == [4, 5]
    assert data['resultado'] == 20
    assert 'timestamp' in data
    
def test_calculadora_suma(client):
    response = client.post('/calculadora', json={'operacion': 'suma', 'a': 10, 'b': 5})
    assert response.status_code == 200
    data = response.get_json()
    assert data['operacion'] == 'suma'
    assert data['numeros'] == [10, 5]
    assert data['resultado'] == 15
    assert 'timestamp' in data
    
def test_info_status_code(client):
    response = client.get('/info')
    assert response.status_code == 200

def test_info_response_json(client):
    response = client.get('/info')
    data = response.get_json()
    assert isinstance(data, dict)
    assert data['app'] == 'Mi App Python DevOps'
    assert data['version'] == '1.0.0'
    assert 'python_version' in data
    assert isinstance(data['endpoints'], list)
    assert '/ - Página principal' in data['endpoints']

def test_suma_numero_grande(client):
    response = client.get('/suma/1000001/1')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Números demasiado grandes'

def test_multiplicacion_numero_grande(client):
    response = client.get('/multiplicacion/1000001/2')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Números demasiado grandes'

def test_calculadora_resta(client):
    response = client.post('/calculadora', json={'operacion': 'resta', 'a': 10, 'b': 3})
    assert response.status_code == 200
    data = response.get_json()
    assert data['operacion'] == 'resta'
    assert data['numeros'] == [10, 3]
    assert data['resultado'] == 7

def test_calculadora_multiplicacion(client):
    resp = client.post('/calculadora', json={'operacion': 'multiplicacion', 'a': 2, 'b': 3})
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['resultado'] == 6

def test_calculadora_division(client):
    response = client.post('/calculadora', json={'operacion': 'division', 'a': 10, 'b': 2})
    assert response.status_code == 200
    data = response.get_json()
    assert data['operacion'] == 'division'
    assert data['numeros'] == [10, 2]
    assert data['resultado'] == 5

def test_calculadora_division_por_cero(client):
    response = client.post('/calculadora', json={'operacion': 'division', 'a': 10, 'b': 0})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'División por cero no permitida'

def test_calculadora_operacion_invalida(client):
    response = client.post('/calculadora', json={'operacion': 'potencia', 'a': 2, 'b': 3})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Operación no válida'

def test_calculadora_numeros_no_numericos(client):
    response = client.post('/calculadora', json={'operacion': 'suma', 'a': 'x', 'b': 3})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Los números deben ser numéricos'

def test_404_error(client):
    response = client.get('/noexiste')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Endpoint no encontrado'
    assert data['status'] == 404

