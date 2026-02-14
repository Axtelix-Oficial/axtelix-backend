from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Tu URL de Google Apps Script (la que termina en /exec)
URL_GOOGLE_SHEETS = "https://script.google.com/macros/s/AKfycbx82t1U0vkdx0trDnApRIPAMSg6H05mDefLsRD2xaQnE5c0fPwZ_vLyT_GjGuSQvSBI/exec"

@app.route('/validar-cupon', methods=['POST'])
def validar():
    try:
        datos = request.json
        # Limpiamos el código y lo pasamos a mayúsculas para evitar errores
        codigo = datos.get("codigo", "").strip().upper()
        productos = datos.get("productos", "Consulta de precio")

        # Enviamos solo lo que Google Sheets sabe procesar
        payload = {
            "codigo": codigo,
            "productos": productos
        }
        
        # 1. Llamada a Google Sheets
        respuesta = requests.post(URL_GOOGLE_SHEETS, json=payload)
        resultado = respuesta.json()

        # 2. Respuesta según lo que encuentre en tu Excel
        if resultado.get("status") == "success":
            return jsonify({
                "valido": True, 
                "descuento": resultado.get("descuento"),
                "mensaje": "¡Cupón aplicado con éxito!"
            })
        else:
            return jsonify({
                "valido": False, 
                "mensaje": resultado.get("mensaje", "Cupón inválido o agotado.")
            })

    except Exception as e:
        print(f"Error de conexión: {e}")
        return jsonify({"valido": False, "mensaje": "Error técnico: Revisa la conexión con Google."})

if __name__ == '__main__':
    # Configuración para Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)