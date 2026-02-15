from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# 1. TU URL DE GOOGLE APPS SCRIPT (La que termina en /exec)
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwmlZ1tW9IUqtZINXBMiJYSk3mNeyth_ycgHLV_Y4YLkLeBddZfSECvnHHC_T2_IoOx/exec"

@app.route('/')
def home():
    return "Backend de Axtelix Funcionando Correctamente"

@app.route('/obtener-inventario', methods=['GET'])
def obtener_inventario():
    try:
        # Llamamos al doGet de tu Google Script
        respuesta = requests.get(GOOGLE_SCRIPT_URL)
        respuesta.raise_for_status()
        
        # El script ya devuelve el JSON con "productos"
        return jsonify(respuesta.json())
        
    except Exception as e:
        print(f"Error en inventario: {e}")
        return jsonify({
            "status": "error",
            "message": "Error al conectar con Google Script"
        }), 500

@app.route('/validar-cupon', methods=['POST'])
def validar_cupon():
    try:
        datos_cliente = request.json
        # Enviamos el cupón al doPost de tu Google Script
        respuesta = requests.post(GOOGLE_SCRIPT_URL, json=datos_cliente)
        respuesta.raise_for_status()
        
        return jsonify(respuesta.json())
        
    except Exception as e:
        print(f"Error en cupones: {e}")
        return jsonify({
            "status": "error",
            "mensaje": "Error al validar el cupón"
        }), 500

if __name__ == '__main__':
    # Puerto dinámico para Render
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=puerto)