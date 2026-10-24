from flask import Flask, request, jsonify
import time
import os

app = Flask(__name__)

# Base de datos temporal en memoria
servidores_activos = {}

@app.route('/reportar', methods=['POST'])
def reportar_servidor():
    data = request.json or {}
    server_id = data.get("serverId")
    
    if not server_id:
        return jsonify({"status": "error", "message": "Falta serverId"}), 400
        
    servidores_activos[server_id] = {
        "placeId": data.get("placeId"),
        "maxHuevo": data.get("maxHuevo"),
        "jugadores": data.get("jugadores"),
        "maxJugadores": data.get("maxJugadores"),
        "timestamp": time.time()
    }
    return jsonify({"status": "success"}), 200

@app.route('/obtener_mejores', methods=['GET'])
def obtener_mejores():
    ahora = time.time()
    lista_limpia = []
    
    for s_id, info in list(servidores_activos.items()):
        if ahora - info["timestamp"] < 300:  
            info["serverId"] = s_id
            lista_limpia.append(info)
            
    lista_ordenada = sorted(lista_limpia, key=lambda x: x['maxHuevo'], reverse=True)
    return jsonify(lista_ordenada), 200

if __name__ == '__main__':
    # Render asigna el puerto automáticamente mediante variables de entorno
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
