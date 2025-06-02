from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Chargement du corpus Maat au démarrage
with open("maat.json", encoding="utf-8") as f:
    maat_corpus = json.load(f)


def valider_blocs_maat(data_client):
    """
    Simule une validation bloc par bloc via les règles métier stockées dans maat_corpus.
    Retourne les blocs validés, une synthèse, et des recommandations simples.
    """
    activite = data_client.get("activite", "").lower()
    recommendations = []
    blocs_valides = []
    synthese = []

    # Vérification activité compatible avec Allianz ASBTP
    if any(mot in activite for mot in ["maçon", "charpentier", "construction", "gros oeuvre"]):
        for bloc in maat_corpus:
            nom = bloc.get("bloc")
            regle = bloc.get("regle")
            description = bloc.get("resume")
            if eval(regle, {}, data_client):  # on évalue la règle sur le JSON client
                blocs_valides.append(nom)
                synthese.append(f"✅ Bloc {nom} validé : {description}")
            else:
                synthese.append(f"❌ Bloc {nom} non validé : {description}")

        recommendations.append("Proposer la #fichedecennaleallianz si tous les blocs sont valides.")
        if "bloc H" not in blocs_valides:
            recommendations.append("Vérifier la présence d’une protection juridique.")

    else:
        synthese.append("Activité non compatible avec ASBTP Allianz (charpentier, maçon, etc. uniquement).")
        recommendations.append("Proposer autre contrat décennale si activité compatible.")

    return {
        "diagnostic": "\n".join(synthese),
        "blocs_valides": blocs_valides,
        "recommandations": recommendations,
        "source": "Elron (Maat)",
        "debug": True
    }


@app.route("/analyse", methods=["POST"])
def analyse():
    try:
        data = request.json
        mode = data.get("mode", "auto")

        if mode == "guidé":
            resultat = valider_blocs_maat(data)
            return jsonify(resultat)

        else:
            # Fallback : réponse générale CGT (pas de logique métier)
            return jsonify({
                "diagnostic": "Merci pour votre demande. Nous avons besoin de plus d’informations pour orienter votre assurance professionnelle. Veuillez préciser l’activité, le chiffre d’affaires, le statut juridique, les véhicules, les locaux et les contrats existants.",
                "source": "CGT (générique)",
                "debug": False
            })

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
