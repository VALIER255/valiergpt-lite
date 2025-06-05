
from flask import Flask, request, jsonify
from flask_cors import CORS
from maat_engine import analyser
from utils_normalize import normalize_activite

app = Flask(__name__)
CORS(app)

@app.route('/analyse', methods=['POST'])
def analyse():
    try:
        donnees_client = request.get_json(force=True)

        # Extraction avec fallback et traitement
        raison_sociale = donnees_client.get("raison_sociale", "")
        statut = donnees_client.get("statut_juridique", "").lower()
        activite = donnees_client.get("activite_principale", "").lower()
        try:
            chiffre_affaires = float(donnees_client.get("chiffre_affaires", 0))
        except ValueError:
            chiffre_affaires = 0

        resultat = analyser({
            "raison_sociale": raison_sociale,
            "statut_juridique": statut,
            "activite_principale": activite,
            "chiffre_affaires": chiffre_affaires
        })

        return jsonify(resultat)
    except Exception as e:
        return jsonify({"erreur": f"Erreur de traitement : {str(e)}"})

@app.route("/")
def accueil():
    return "Bienvenue sur ValierGPT Lite – API d’analyse assurantielle."

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=10000)

