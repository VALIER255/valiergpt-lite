# utils_normalize.py

import difflib

# Dictionnaire d'activités normalisées (simplifié ici, à enrichir selon besoin)
ACTIVITES_NORMALISEES = {
    "maçon": "Maçonnerie",
    "macon": "Maçonnerie",
    "maçonnerie": "Maçonnerie",
    "charpentier": "Charpente",
    "charpente": "Charpente",
    "couvreur": "Couverture",
    "electricien": "Électricité",
    "électricien": "Électricité",
    "plombier": "Plomberie",
    "peintre": "Peinture",
    "menuisier": "Menuiserie",
}

def normalize_activite(activite: str) -> str:
    if not activite:
        return ""

    activite = activite.lower().strip()
    activite_clean = activite.replace("é", "e").replace("è", "e").replace("ê", "e").replace("ç", "c")

    # Tentative de correspondance exacte
    if activite_clean in ACTIVITES_NORMALISEES:
        return ACTIVITES_NORMALISEES[activite_clean]

    # Sinon, tentative d'approximation
    correspondances = difflib.get_close_matches(activite_clean, ACTIVITES_NORMALISEES.keys(), n=1, cutoff=0.7)
    if correspondances:
        return ACTIVITES_NORMALISEES[correspondances[0]]

    # Si aucune correspondance : retour brut mais propre
    return activite.title()
