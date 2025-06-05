
from flask import Flask, request, jsonify
from flask_cors import CORS
from maat_engine import analyser as analyser_maat
from utils_normalize import normalize_activite

app = Flask(__name__)
CORS(app)

@app.route('/analyse', methods=['POST'])
def analyse():
    data = request.get_json(force=True)
    raison_sociale = data.get("raison_sociale", "")
    statut = data.get("statut_juridique", "").lower()
    activite = data.get("activite_principale", "").lower()
try:
    chiffre_affaires = float(data.get("chiffre_affaires", 0))
except ValueError:
    chiffre_affaires = 0
    
try:
        donnees_client = {
            "raison_sociale": raison_sociale,
            "statut_juridique": statut ,
            "activite_principale": activite,
            "chiffre_affaires": chiffre_affaires
        }
        
        resultat = analyser_maat(donnees_client)
        return jsonify(resultat)

except Exception as e:
        return jsonify({"erreur": f"Erreur de traitement : {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=10000)
