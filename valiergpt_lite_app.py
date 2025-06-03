
from flask import Flask, request, jsonify
from flask_cors import CORS
from maat_engine import analyser as analyser_maat
from utils_normalize import normalize_activite

app = Flask(__name__)
CORS(app)

@app.route('/analyse', methods=['POST'])
def analyse():
    try:
        data = request.json

        # Normalisation de l'activité si présente
        if "activite_principale" in data:
            data["activite_principale"] = normalize_activite(data["activite_principale"])

        resultats = analyser_maat(data)
        return jsonify(resultats)
    except Exception as e:
        return jsonify({"erreur": f"Erreur de traitement : {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=10000)
