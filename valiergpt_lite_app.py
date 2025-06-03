# valiergpt_lite_app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from maat_engine import analyse_decennale_allianz

app = Flask(__name__)
CORS(app)

@app.route("/diagnostic", methods=["POST"])
def diagnostic():
    data = request.get_json()
    resultat = analyse_decennale_allianz(data)
    return jsonify(resultat)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)

