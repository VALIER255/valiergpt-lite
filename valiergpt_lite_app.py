
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def analyser_client(data):
    produits = []
    alertes = []

    activite = data.get("activite_principale", "").lower()
    ca = data.get("chiffre_affaires", 0)
    nb_salaries = data.get("nombre_salaries", 0)
    dom = data.get("siege_dom", False)

    # Exemple simple de logique conditionnelle métier
    if "maçonnerie" in activite and ca <= 500000 and not dom:
        produits.append("RC Décennale Allianz – ASBTP")

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
