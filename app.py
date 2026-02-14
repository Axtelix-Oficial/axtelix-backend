from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# La URL de tu Google Apps Script (Sigue siendo la misma)
URL_GOOGLE_SHEETS = "https://script.google.com/macros/s/AKfycbx82t1U0vkdx0trDnApRIPAMSg6H05mDefLsRD2xaQnE5c0fPwZ_vLyT_GjGuSQvSBI/exec"

@app.route('/validar-cupon', methods=['POST'])
def validar():
    datos = request.json
    codigo = datos.get("codigo", "").strip().upper()
    productos = datos.get("productos", "Consulta de precio")

    # Ya no usamos la lista 'cupones' de aquí. 
    # Le mandamos el código directamente a Google Sheets para que él decida.
    payload = {
        "accion": "validar_y_registrar", # Le decimos qué queremos hacer
        "codigo": codigo,
        "productos": productos
    }
    
    try:
        # 1. Le preguntamos a Google Sheets
        respuesta = requests.post(URL_GOOGLE_SHEETS, json=payload)
        resultado = respuesta.json()

        # 2. Analizamos lo que dice tu Excel
        if resultado.get("status") == "success":
            # Si Google Sheets lo encontró y tenía usos disponibles
            return jsonify({
                "valido": True, 
                "descuento": resultado.get("descuento"),
                "mensaje": "¡Cupón aplicado con éxito!"
            })
        else:
            # Si no existe, o si ya se agotaron los usos (Límite vs UsosActuales)
            return jsonify({
                "valido": False, 
                "mensaje": resultado.get("mensaje", "Cupón inválido o agotado.")
            })

    except Exception as e:
        print(f"Error de conexión: {e}")
        return jsonify({"valido": False, "mensaje": "Error de conexión con el servidor."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)