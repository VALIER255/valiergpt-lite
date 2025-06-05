
# fichier : maat_logique_decennale_allianz.py

def normalize_activite(activite: str) -> str:
    """
    Normalise l'intitulé d'activité pour simplifier les comparaisons.
    """
    return activite.strip().lower()

def verifier_eligibilite_allianz_decennale(statut: str, activite: str, ca: int) -> dict:
    """
    Applique les règles d'éligibilité Allianz pour la RC Décennale.
    Retourne un dictionnaire avec les alertes et la liste des produits recommandés.
    """
    alertes = []
    produits_recommandes = []

    statut_normalise = statut.strip().lower()
    activite_normalisee = normalize_activite(activite)

    # Bloc 1 — Statuts exclus
    if statut_normalise in ["sci", "sci construction vente", "association", "auto-construction"]:
        alertes.append("Les SCI, associations et structures d'auto-construction ne sont pas assurables en RC Décennale Allianz.")
        return {"alertes": alertes, "produits_recommandes": produits_recommandes}

    # Bloc 2 — Activités interdites
    activites_interdites = [
        "désamiantage", "forage pétrolier", "nucléaire", "maritime", "offshore", "conception d'ouvrages d'art",
        "maîtrise d'œuvre", "bureau d'étude", "architecte", "éolien", "photovoltaïque"
    ]
    for mot in activites_interdites:
        if mot in activite_normalisee:
            alertes.append(f"L'activité déclarée contient un terme interdit pour Allianz : {mot}")
            return {"alertes": alertes, "produits_recommandes": produits_recommandes}

    # Bloc 3 — CA minimum
    if ca < 35000:
        alertes.append("Le chiffre d'affaires est insuffisant pour l'acceptation Allianz (minimum 35 000 €).")
        return {"alertes": alertes, "produits_recommandes": produits_recommandes}

    # Bloc 4 — CA entre 35k et 200k
    if 35000 <= ca <= 200000:
        produits_recommandes.append("RC Décennale Allianz – ASBTP")
        return {"alertes": alertes, "produits_recommandes": produits_recommandes}

    # Bloc 5 — CA > 200k → contrat révisable
    if ca > 200000:
        produits_recommandes.append("RC Décennale Allianz – ASBTP (contrat révisable)")
        return {"alertes": alertes, "produits_recommandes": produits_recommandes}

    # Bloc 6 — Sécurité pour activité non reconnue (si aucune règle n’a matché)
    alertes.append("Aucun produit recommandé avec les données actuelles.")
    return {"alertes": alertes, "produits_recommandes": produits_recommandes}
