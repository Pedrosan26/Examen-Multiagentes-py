from flask import Flask, jsonify, send_file
import json
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilitar CORS para solicitudes desde Unity

@app.route("/")
def index():
    return "Endpoint de datos en /agente"

@app.route("/agente")
def get_agent_data():
    file_path = os.path.join(os.path.dirname(__file__), "simulation_data.json")
    
    if not os.path.exists(file_path):
        return jsonify({"error": "Datos no disponibles"}), 404
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=10000)