import difflib

def normalize_activite(activite):
    """
    Normalise les intitulés d'activité pour matcher les valeurs attendues.
    Corrige la casse et les erreurs mineures (ex: maçon => Macon)
    """
    activite = activite.strip().lower()
    mapping = {
        "macon": "Macon",
        "maçon": "Macon",
        "maconnerie": "Macon",
        "charpente": "Charpentier",
        "charpentier": "Charpentier",
        "couvreur": "Couvreur",
        "electricien": "Electricien",
        "électricien": "Electricien",
        "plaquiste": "Plaquiste",
        "plombier": "Plombier",
        "carreleur": "Carreleur",
    }
    if activite in mapping:
        return mapping[activite]
    else:
        closest = difflib.get_close_matches(activite, mapping.keys(), n=1, cutoff=0.8)
        return mapping[closest[0]] if closest else activite.capitalize()

def verifier_admissibilite_allianz(data):
    alertes = []
    produits = []

    statut = data.get("statut_juridique", "").strip().upper()
    activite = normalize_activite(data.get("activite_principale", ""))
    ca = data.get("chiffre_affaires", 0)

    # Bloc 1 : SCI exclue
    if "SCI" in statut:
        alertes.append("Les SCI ne sont pas assurables en RC Décennale Allianz.")
        return alertes, produits

    # Bloc 2 : Seuil minimal de CA
    if ca < 35000:
        alertes.append("Le chiffre d'affaires est insuffisant pour une souscription Allianz (minimum 35 000 €).")
        return alertes, produits

    # Bloc 3 : Seuil maximal de CA pour la tarification forfaitaire
    if ca > 200000:
        alertes.append("Le chiffre d'affaires dépasse le seuil de tarification forfaitaire Allianz (200 000 €). Le risque doit être analysé individuellement.")

    # Bloc 4 : Activités autorisées (liste de base, simplifiée ici)
    activites_autorisees = ["Macon", "Charpentier", "Couvreur", "Electricien", "Plaquiste", "Plombier", "Carreleur"]
    if activite not in activites_autorisees:
        alertes.append(f"L'activité '{activite}' n'est pas assurée en décennale par Allianz dans le cadre standard.")
        return alertes, produits

    # Bloc 5 : Activité unique OK
    if "," in activite:
        alertes.append("Plusieurs activités détectées. Allianz exige une activité principale clairement définie pour la tarification forfaitaire.")

    # Bloc 6 : Conditions d’éligibilité additionnelles (aucune faute lourde connue ici)
    # On pourrait enrichir ici avec des règles sur sinistralité, antécédents, etc.

    # Si tout est bon
    if not alertes:
        produits.append("RC Décennale Allianz – ASBTP")

    return alertes, produits
