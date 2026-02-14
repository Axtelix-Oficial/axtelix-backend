from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime # Para saber la hora exacta

app = Flask(__name__)
CORS(app)

cupones = {
    "1010": 300,
    "DUNK-OFFER": 100 # Por si vendes los tenis de 790
}

@app.route('/validar-cupon', methods=['POST'])
def validar():
    datos = request.json
    codigo = datos.get("codigo", "").upper()
    nombre_cliente = datos.get("nombre", "Desconocido")
    producto = datos.get("producto", "No especificado")

    if codigo in cupones:
        descuento = cupones[codigo]
        
        # --- EL DETECTIVE: Guardar en un archivo ---
        with open("usos_cupones.txt", "a") as f:
            fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{fecha}] {nombre_cliente} usó {codigo} para {producto} - Desc: ${descuento}\n")
        
        return jsonify({"valido": True, "descuento": descuento})
    else:
        return jsonify({"valido": False, "mensaje": "Cupón inválido"})