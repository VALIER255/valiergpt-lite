
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def analyse_assurance(client_data):
    produits = []
    alertes = []

    # Extraction des données
    activite = client_data.get("activite", "").lower()
    ca = client_data.get("ca", 0)
    statut = client_data.get("statut_juridique", "").lower()

    # --- Logique Allianz RC Décennale ---
    if activite == "maçonnerie":
        if statut == "sci":
            alertes.append("❗️ SCI non acceptée chez Allianz pour la RC Décennale.")
        elif 35000 <= ca <= 200000:
            produits.append("✅ Allianz RC Décennale : produit forfaitaire possible.")
        elif ca > 200000:
            produits.append("✅ Allianz RC Décennale : contrat révisable au-delà de 200 K€ de CA.")
            alertes.append("⚠️ Le contrat devient révisable sur CA réel déclaré N-1.")
        else:
            alertes.append("❌ CA trop faible pour Allianz (minimum 35 000 €).")

    # --- Rappel général ---
    if not produits:
        alertes.append("Aucun produit recommandé avec les données actuelles.")

    return {
        "produits_recommandes": produits,
        "alertes": alertes
    }

@app.route('/analyse', methods=['POST'])
def analyse():
    client_data = request.get_json()
    resultat = analyse_assurance(client_data)
    return jsonify(resultat)

@app.route('/')
def index():
    return "ValierGPT Lite App est en ligne."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
