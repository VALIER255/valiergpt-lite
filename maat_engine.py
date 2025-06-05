
from maat_logique_decennale_allianz import verifier_eligibilite_allianz_decennale


def analyser(donnees_client: dict) -> dict:
    """
    Analyse les données client en fonction des règles Allianz Décennale.
    Retourne les produits recommandés et éventuelles alertes.
    """
    produits = []
    alertes = []

    statut = donnees_client.get("statut_juridique", "").lower()
    activite = donnees_client.get("activite_principale", "").lower()
    # chiffre_affaires = donnees_client.get("chiffre_affaires", 0)
    chiffre_affaires = 258236

    resultats = verifier_eligibilite_allianz_decennale(
        statut, activite, chiffre_affaires
    )
    print("DEBUG:", resultats)  # TEMPORAIRE pour test Render (à commenter après)
    if resultats.get("eligibilite"):
        produits.extend(resultats.get("produits_recommandes", []))
    else:
        alertes.extend(resultats.get("alertes", []))

    return {"produits_recommandes": produits, "alertes": alertes}

