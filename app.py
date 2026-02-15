from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
# Esto permite que tu HTML (frontend) hable con este Python (backend) sin bloqueos
CORS(app)

# 1. TU URL DE GOOGLE APPS SCRIPT
# Mantenemos tu URL actual que ya termina en /exec
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxRLZ1aoJGdfA5s3ItUfXd2wCyI-ulxjcAhdVCkH1ztQm_VLcauKcTd96qFk-7iKORW/exec"

@app.route('/')
def home():
    return "Bot de Axtelix: ¡Estoy vivo y trabajando!"

@app.route('/obtener-inventario', methods=['GET'])
def obtener_inventario():
    try:
        # Pedimos los datos a Google Sheets
        respuesta = requests.get(GOOGLE_SCRIPT_URL, timeout=10)
        datos = respuesta.json()
        
        # Si Google nos manda la lista dentro de una llave llamada "productos", la extraemos
        # Si nos manda la lista directamente, usamos esa.
        if isinstance(datos, dict) and "productos" in datos:
            return jsonify(datos["productos"])
        return jsonify(datos)
        
    except Exception as e:
        print(f"Error: {e}")
        # Si falla, mandamos una lista vacía para que el HTML use su 'RESPALDO'
        return jsonify([])

@app.route('/validar-cupon', methods=['POST'])
def validar_cupon():
    try:
        datos_cliente = request.json
        # Le enviamos el código del cupón a Google para que lo cheque
        respuesta = requests.post(GOOGLE_SCRIPT_URL, json=datos_cliente, timeout=10)
        return jsonify(respuesta.json())
        
    except Exception as e:
        print(f"Error en cupones: {e}")
        return jsonify({"valido": False, "mensaje": "Servidor ocupado, intenta en 30 segundos"})

if __name__ == '__main__':
    # Render usa el puerto que él quiera, por eso usamos os.environ.get
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=puerto)