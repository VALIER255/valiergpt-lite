from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyse_metier_avancee(data):
    activité = data.get("activite", "").lower()
    statut = data.get("statut", "").lower()
    ca_str = data.get("ca", "0").replace("€", "").replace(" ", "").replace("M", "00000")
    try:
        ca = int(float(ca_str))
    except:
        ca = 0
    salaries = int(data.get("salaries", "0"))
    contrats = data.get("contrats", "").lower()
    vehicules = data.get("vehicules", "")
    local = data.get("local", "").lower()

    risques = []
    fiches = []
    suggestions = []

    if any(mot in activité for mot in ["plâtrerie", "maçonnerie", "charpente", "gros œuvre", "construction", "btp", "rénovation"]):
        if "décennale" not in contrats:
            risques.append("⚠️ Décennale absente pour activité BTP")
            fiches.append("#fichedecennale")
        suggestions.append("Souscrire RC Pro + RC Décennale")

    if ca > 100000:
        suggestions.append("Revoir les seuils de garantie en fonction du CA")
    if ca > 250000:
        suggestions.append("Vérifier pertinence MRP et santé collective")
        fiches.append("#fichemrp")

    if "auto" in statut or "micro" in statut:
        risques.append("⚠️ Statut auto-entrepreneur : exclusions possibles en PJ / MRP")
        fiches.append("#fichepjamateur")

    if "sasu" in statut or "sas" in statut:
        if salaries >= 1:
            suggestions.append("Prévoir prévoyance ou santé dirigeant")
        fiches.append("#ficheprevoyance")

    try:
        veh_count = int(vehicules.split()[0])
        if veh_count >= 2:
            suggestions.append("Étudier contrat flotte")
            fiches.append("#ficheflotteaxa")
    except:
        pass

    if "oui" in local:
        suggestions.append("Vérifier présence ou besoin d’une MRP")
        fiches.append("#fichemrp")

    if "sci" in statut and "habitation" in activité:
        risques.append("⚠️ SCI non acceptée en habitation AXA")
        fiches.append("#fichepnoaxa")

    analyse = "\n".join(risques + suggestions)
    fiches_mention = ", ".join(set(fiches))
    return analyse, fiches_mention

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

    analyse_métier, fiches = analyse_metier_avancee(data)

    prompt = f"""
Tu es un assistant expert en assurance professionnelle chez VALIER.

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

Analyse interne métier (pré-règles appliquées) :
{analyse_métier}

Fiches EVA suggérées : {fiches}

Structure ta réponse comme suit :
1. 📌 Profil du client
2. ⚠️ Risques identifiés
3. ✅ Contrats recommandés
4. 🧩 Actions immédiates Valier

Mentionne en conclusion les fiches #EVA utiles et la pertinence du #ProtocoleValier.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un conseiller expert en assurance professionnelle."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=700
        )
        message = response.choices[0].message.content
        return jsonify({"diagnostic": message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
