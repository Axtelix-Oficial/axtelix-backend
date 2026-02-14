from flask import Flask, request, jsonify
from flask_cors import CORS
import requests # Importante para hablar con Google

app = Flask(__name__)
CORS(app)

# Tu lista de cupones
cupones = {
    "2020": 300,
    "DUNK-OFFER": 100
}

# URL que copiaste de Google Apps Script
URL_GOOGLE_SHEETS = "https://script.google.com/macros/s/AKfycbxyTW2mDwxXeHvVHZi0JbiWxLqlgkwHuUrr3D7D9c4Ug9iHOIDGCqMqMyKlTOPBjuHA/exec"

@app.route('/validar-cupon', methods=['POST'])
def validar():
    datos = request.json
    codigo = datos.get("codigo", "").upper()
    # Si tu JS no manda productos aún, pondrá "Desconocido"
    productos = datos.get("productos", "Venta desde la web")

    if codigo in cupones:
        descuento = cupones[codigo]
        
        # --- ENVIAR A GOOGLE SHEETS ---
        payload = {
            "codigo": codigo,
            "descuento": descuento,
            "productos": productos
        }
        try:
            # Mandamos los datos a tu Excel en la nube
            requests.post(URL_GOOGLE_SHEETS, json=payload)
        except Exception as e:
            print(f"Error enviando a Google: {e}")
        
        return jsonify({"valido": True, "descuento": descuento})
    else:
        return jsonify({"valido": False, "mensaje": "Cupón inválido"})

if __name__ == '__main__':
    app.run(debug=True)