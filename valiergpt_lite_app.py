
from flask import Flask, request, jsonify
from flask_cors import CORS
from maat_engine import analyser as analyser_maat
from utils_normalize import normalize_activite

app = Flask(__name__)
CORS(app)

@app.route('/analyse', methods=['POST'])
def analyse():
    try:
        donnees_client = {
            "raison_sociale": request.form.get("raison_sociale", ""),
            "statut_juridique": request.form.get("statut_juridique", "").lower(),
            "activite_principale": request.form.get("activite_principale", "").lower(),
            "chiffre_affaires": float(request.form.get("chiffre_affaires", 0))
        }

        resultat = analyser_maat(donnees_client)
        return jsonify(resultat)

    except Exception as e:
        return jsonify({"erreur": f"Erreur de traitement : {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=10000)
