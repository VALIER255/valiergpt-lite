from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Chargement du corpus métier Maat depuis un fichier JSON (à adapter si tu veux le faire dynamiquement)
with open("maat_corpus.json", "r", encoding="utf-8") as f:
    MAAT_RULES = json.load(f)

def validate_request(data):
    results = []
    for bloc in MAAT_RULES:
        bloc_id = bloc["bloc"]
        if "conditions" in bloc:
            bloc_result = {
                "bloc": bloc_id,
                "valid": True,
                "errors": []
            }
            for cond in bloc["conditions"]:
                key = cond["field"]
                expected = cond["value"]
                if key not in data or data[key] != expected:
                    bloc_result["valid"] = False
                    bloc_result["errors"].append(f"Champ '{key}' attendu: '{expected}', reçu: '{data.get(key)}'")
            results.append(bloc_result)
    return results

@app.route("/validate", methods=["POST"])
def validate():
    try:
        data = request.get_json()
        result = validate_request(data)
        return jsonify({"status": "ok", "validation": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/")
def home():
    return "Maat Validation API is running."

if __name__ == "__main__":
    app.run(debug=True)
