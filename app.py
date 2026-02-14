from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Tu lista de cupones activos
cupones = {
    "AXTE-LIX-NEW": 200,
    "5050": 200
}

# La URL de tu Google Apps Script
URL_GOOGLE_SHEETS = "https://script.google.com/macros/s/AKfycbzg45LFQW27Yswi-FYjoC7TzdQfJi1wBAzMGKUpgWK3YjIbAHJzU9AsQOA-Fgf_GiiC/exec"

@app.route('/validar-cupon', methods=['POST'])
def validar():
    datos = request.json
    codigo = datos.get("codigo", "").strip().upper()
    productos = datos.get("productos", "Venta desde la web")

    # 1. Verificar si el cupón existe en tu lista inicial
    if codigo in cupones:
        descuento = cupones[codigo]
        
        # 2. Intentar registrar en Google Sheets y ver si ya fue usado
        payload = {
            "codigo": codigo,
            "descuento": descuento,
            "productos": productos
        }
        
        try:
            # Hacemos la petición a Google y esperamos su respuesta
            respuesta = requests.post(URL_GOOGLE_SHEETS, json=payload)
            resultado_google = respuesta.json() # Esto recibe lo que el Apps Script responde

            # 3. Si Google dice que es un error (porque ya existe en la columna B)
            if resultado_google.get("status") == "error":
                return jsonify({
                    "valido": False, 
                    "mensaje": "Este cupón ya fue canjeado anteriormente."
                })

            # 4. Si Google dice "success", entonces sí aplicamos el descuento
            return jsonify({
                "valido": True, 
                "descuento": descuento,
                "mensaje": "¡Cupón aplicado con éxito!"
            })

        except Exception as e:
            print(f"Error de conexión con Google: {e}")
            # En caso de error de conexión, tú decides si dejar pasar el cupón o no.
            # Por seguridad, aquí lo dejamos pasar, pero avisamos en consola.
            return jsonify({"valido": True, "descuento": descuento})
            
    else:
        return jsonify({"valido": False, "mensaje": "Cupón inválido o expirado"})

if __name__ == '__main__':
    # Importante: Render usa el puerto 10000 por defecto
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)