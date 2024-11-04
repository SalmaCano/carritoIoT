from flask import Flask, request, jsonify
import requests  # Asegúrate de instalar la biblioteca requests

app = Flask(_name_)

# Dirección IP y puerto del ESP32, ajústalo según tu configuración
ESP32_URL = "http://192.168.1.10/control"  # Reemplaza con la IP real de tu ESP32

@app.route('/')
def index():
    return open('index.html').read()

@app.route('/control', methods=['POST'])
def control():
    data = request.get_json()
    action = data.get('action')
    response_message = ""
    
    # Enviar acción al ESP32 según la acción recibida
    try:
        esp_response = requests.post(ESP32_URL, json={'action': action})
        if esp_response.status_code == 200:
            response_message = esp_response.json().get('message', 'Comando ejecutado en ESP32')
        else:
            response_message = "Error al comunicarse con ESP32"
    except Exception as e:
        response_message = f"Error: {str(e)}"

    # Respuestas locales para confirmar el envío de comandos
    if action == 'forward':
        response = "El carrito está avanzando y el LED correspondiente está encendido"
    elif action == 'backward':
        response = "El carrito está retrocediendo y el LED correspondiente está encendido"
    elif action == 'left':
        response = "El carrito gira a la izquierda y el LED correspondiente está encendido"
    elif action == 'right':
        response = "El carrito gira a la derecha y el LED correspondiente está encendido"
    elif action == 'stop':
        response = "El carrito se detiene y el LED correspondiente está encendido"
    elif action == 'rotate30':
        response = "El carrito gira 30 grados"
    elif action == 'rotate90':
        response = "El carrito gira 90 grados"
    elif action == 'rotate180':
        response = "El carrito gira 180 grados"
    else:
        response = "Acción desconocida"

    return jsonify({'status': 'OK', 'message': response_message or response})

if _name_ == '_main_':
    app.run(debug=True)