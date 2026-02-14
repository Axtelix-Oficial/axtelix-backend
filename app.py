from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app) 

# Esta es tu lista de cupones única
cupones = {
    "AXT-VIP-100": 100,
    "PROMO-500": 500,
    "PRUEBA": 300,
    "PRUEBA-2": 200
}

@app.route('/validar-cupon', methods=['POST'])
def validar():
    datos = request.json
    codigo = datos.get("codigo", "").upper()
    
    if codigo in cupones:
        descuento = cupones[codigo]
        # Aquí es donde se borra: una vez entregado, desaparece de la lista
        del cupones[codigo] 
        return jsonify({"valido": True, "descuento": descuento})
    else:
        return jsonify({"valido": False, "mensaje": "Cupón inválido o ya usado"})

if __name__ == '__main__':
    # Este ajuste permite que el servidor de internet le asigne un puerto automáticamente
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)