
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def analyser_client(data):
    produits = []
    alertes = []

    activite = data.get("activite_principale", "").lower().strip()
    ca = data.get("chiffre_affaires", 0)
    statut = data.get("statut_juridique", "").lower().strip()

    activites_eligibles = ["maçonnerie", "maçon", "charpentier", "charpente", "gros œuvre"]

    if activite in activites_eligibles:
        if statut == "sci":
            alertes.append("❗️ SCI non éligible à la RC Décennale Allianz.")
        elif 35000 <= ca <= 5000000:
            produits.append("RC Décennale Allianz – ASBTP")
        elif ca > 5000000:
            alertes.append("CA trop élevé pour ce produit (max 5 M€).")
        else:
            alertes.append("CA trop faible pour Allianz (minimum 35 000 €).")
    else:
        alertes.append(f"Activité « {activite} » non éligible à ASBTP Allianz.")

    if not produits:
        alertes.append("Aucun produit recommandé avec les données actuelles.")

    return {
        "produits_recommandes": produits,
        "alertes": alertes
    }

@app.route("/analyse", methods=["POST"])
def diagnostic():
    data = request.get_json()
    resultat = analyser_client(data)
    return jsonify(resultat)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
