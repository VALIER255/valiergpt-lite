from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyse_metier(data):
    activité = data.get("activite", "").lower()
    risques = []
    suggestions = []

    if any(mot in activité for mot in ["plâtrerie", "maçonnerie", "charpente", "gros œuvre", "construction"]):
        risques.append("Travaux structurels → décennale obligatoire")
        suggestions.append("Souscrire RC + RC décennale")
    if int(data.get("salaries", "0")) >= 1:
        suggestions.append("Prévoir prévoyance ou santé collective")
    if "local" in data.get("local", "").lower():
        suggestions.append("Vérifier la couverture MRP")
    if int(data.get("vehicules", "0").split()[0]) >= 2:
        suggestions.append("Étudier une formule flotte")

    retour = "\n".join(risques + suggestions)
    return retour if retour else "Aucune logique détectée automatiquement."

@app.route('/analyse', methods=['POST'])
def analyse():
    data = request.json

    nom = data.get("nom", "Client inconnu")
    statut = data.get("statut", "Non précisé")
    activite = data.get("activite", "Non précisée")
    ca = data.get("ca", "Non précisé")
    salaries = data.get("salaries", "Non précisé")
    vehicules = data.get("vehicules", "Non précisé")
    local = data.get("local", "Non précisé")
    contrats = data.get("contrats", "Non précisé")
    commentaires = data.get("commentaires", "")

    analyse_métier = analyse_metier(data)

    prompt = f"""
Tu es un assistant spécialisé en assurance professionnelle au sein du cabinet VALIER.

Voici les données du client :

- Raison sociale : {nom}
- Statut juridique : {statut}
- Activité principale : {activite}
- Chiffre d'affaires : {ca}
- Nombre de salariés : {salaries}
- Véhicules / engins : {vehicules}
- Local professionnel : {local}
- Contrats existants : {contrats}
- Commentaires : {commentaires}

Voici l'analyse préliminaire métier (interne) :
{analyse_métier}

Rédige une synthèse claire structurée en 4 blocs :
1. 📌 Profil du client (activité, statut, CA, effectif)
2. ⚠️ Risques identifiés (métiers, véhicules, salariés, locaux)
3. ✅ Contrats recommandés (obligatoires + optionnels)
4. 🧩 Actions immédiates Valier à mettre en place

Utilise un ton professionnel, concis et orienté courtier. Termine par une mention du #ProtocoleValier applicable.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un conseiller expert en assurance professionnelle."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=600
        )
        message = response.choices[0].message.content
        return jsonify({"diagnostic": message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
