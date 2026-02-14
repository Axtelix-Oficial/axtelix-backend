from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app) 

# Tu lista de cupones
cupones = {
    "AXTELIX-PRUEBA": 300
}

@app.route('/validar-cupon', methods=['POST'])
def validar():
    datos = request.json
    codigo = datos.get("codigo", "").upper()
    
    if codigo in cupones:
        descuento = cupones[codigo]
        # Se borra de la memoria para que sea de un solo uso
        del cupones[codigo] 
        return jsonify({"valido": True, "descuento": descuento})
    else:
        return jsonify({"valido": False, "mensaje": "Cupón inválido o ya usado"})

@app.route('/')
def home():
    return "Servidor Axtelix Activo"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)