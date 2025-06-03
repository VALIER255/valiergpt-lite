# maat_engine.py

import unicodedata

def normaliser_texte(texte):
    """Supprime les accents et met en minuscules pour standardiser les comparaisons."""
    if not isinstance(texte, str):
        return ""
    texte = unicodedata.normalize('NFKD', texte).encode('ASCII', 'ignore').decode('utf-8')
    return texte.lower().strip()

def analyse_decennale_allianz(data):
    produits = []
    alertes = []

    activite = normaliser_texte(data.get("activite_principale", ""))
    ca = data.get("chiffre_affaires", 0)
    statut = normaliser_texte(data.get("statut_juridique", ""))
    dom = data.get("siege_dom", False)
    sci = "sci" in statut

    # Bloc 1 à 6 Allianz décennale (logique consolidée)
    if sci:
        alertes.append("Les SCI ne sont pas assurables en RC Décennale Allianz.")
        return {"produits_recommandes": [], "alertes": alertes}

    if "maçon" in activite and ca <= 500000 and not dom:
        produits.append("RC Décennale Allianz – ASBTP")
    elif "charpent" in activite and ca <= 400000:
        produits.append("RC Décennale Allianz – ASBTP")
    elif "couverture" in activite and ca <= 350000:
        produits.append("RC Décennale Allianz – ASBTP")
    elif "bet" in activite or "architecte" in activite:
        alertes.append("Les professions intellectuelles du bâtiment ne sont pas assurables chez Allianz sauf cas très spécifiques d'exécution directe.")
    else:
        alertes.append("Aucun produit recommandé avec les données actuelles.")

    return {
        "produits_recommandes": produits,
        "alertes": alertes
    }
