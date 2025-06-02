
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/analyse', methods=['POST'])
def analyse():
    data = request.get_json()
    # Traitement fictif (remplacer par ton moteur Maat plus tard)
    return jsonify({
        "diagnostic": f"Merci, nous avons reçu les données de {data.get('raison_sociale', 'entreprise inconnue')}."
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Par défaut : 5000 en local
    app.run(host='0.0.0.0', port=port)
