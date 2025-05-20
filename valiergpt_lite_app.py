from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

# Initialiser le client OpenAI avec la nouvelle API (>= 1.0.0)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/analyse', methods=['POST'])
def analyse():
    data = request.json

    # Récupération des données du formulaire
    nom = data.get("nom", "Client inconnu")
    statut = data.get("statut", "Non précisé")
    activite = data.get("activite", "Non précisée")
    ca = data.get("ca", "Non précisé")
    salaries = data.get("salaries", "Non précisé")
    vehicules = data.get("vehicules", "Non précisé")
    local = data.get("local", "Non précisé")
    contrats = data.get("contrats", "Non précisé")
    commentaires = data.get("commentaires", "")

    # Prompt enrichi avec contexte Valier Assurance
    prompt = f"""
Tu es un assistant du cabinet de courtage VALIER, spécialisé en assurance IARD pour les TPE/PME du BTP, du commerce, de l’artisanat et des services.

Analyse les données suivantes et propose une synthèse claire des besoins assurantiels du client :

- Raison sociale : {nom}
- Statut juridique : {statut}
- Activité principale : {activite}
- Chiffre d'affaires : {ca}
- Nombre de salariés : {salaries}
- Véhicules / engins : {vehicules}
- Local professionnel : {local}
- Contrats existants : {contrats}
- Commentaires : {commentaires}

Objectifs :
1. Déterminer les risques à couvrir.
2. Proposer les contrats nécessaires ou à optimiser (RC pro, décennale, flotte, MRP, santé, PJ...).
3. Détecter les carences.
4. Suggérer un plan synthétique d’action, clair, en moins de 250 mots.

Utilise un ton professionnel, concis, orienté courtier. Ne fais pas de généralités vagues.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un expert en assurance professionnelle."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=600
        )

        message = response.choices[0].message.content
        return jsonify({"diagnostic": message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
