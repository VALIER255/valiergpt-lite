from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Exemple de fonction de validation simplifiée basée sur la logique Maat
def valider_client(data):
    diagnostic = []

    activite = data.get("activite", "").lower()
    ca = data.get("chiffre_affaires", 0)
    siege = data.get("siege_social", "").upper()

    # Bloc A : Siège social
    if not siege:
        diagnostic.append("Siège social non précisé.")
    elif not (siege.startswith("FR") or siege.startswith("GP") or siege.startswith("RE") or siege.startswith("MQ") or siege.startswith("GF") or siege.startswith("YT") or siege.startswith("MF")):
        diagnostic.append("Entreprise hors zone France / DOM non admissible pour ASBTP.")

    # Bloc B : Forme juridique - ignorée ici pour simplification

    # Bloc C : Activité
    activites_autorisees = [
        "maconnerie", "charpente", "couverture", "carrelage", "plomberie",
        "electricite", "peinture", "platrerie", "etancheite"
    ]
    if activite not in activites_autorisees:
        diagnostic.append("Activité non admissible pour ASBTP : {}".format(activite))

    # Bloc D : Chiffre d'affaires
    if ca < 35000:
        diagnostic.append("Chiffre d'affaires trop faible pour souscription (minimum 35 000 €).")
    elif ca > 5000000:
        diagnostic.append("Chiffre d'affaires trop élevé pour ce produit (max 5 M€).")

    # Bloc E : Autres critères ignorés pour simplification

    if not diagnostic:
        return "Client admissible pour souscription ASBTP."
    else:
        return "\n".join(diagnostic)

@app.route("/analyse", methods=["POST"])
def analyse():
    try:
        data = request.get_json()
        resultat = valider_client(data)
        return jsonify({"diagnostic": resultat})
    except Exception as e:
        return jsonify({"erreur": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
