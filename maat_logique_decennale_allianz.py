
# fichier : maat_logique_decennale_allianz.py

def normalize_activite(activite: str) -> str:
    """
    Normalise l'intitulé d'activité pour simplifier les comparaisons.
    """
    return activite.strip().lower()


def verifier_eligibilite_allianz_decennale(statut: str, activite: str, chiffre_affaires: float) -> dict:
    raisons = []
    produits_recommandes = []
    eligibilite = True

    statut = statut.lower().strip()
    activite = activite.lower().strip()

    # Bloc 1 – Exclusions catégoriques
    if statut in ["sci", "association", "auto-construction"]:
        raisons.append("Les SCI, associations et structures d'auto-construction ne sont pas assurables en RC Décennale Allianz.")
        eligibilite = False

    # Bloc 2 – Activités interdites
    activites_interdites = [
        "désamiantage", "nucléaire", "offshore", "fondations spéciales", "ouvrages maritimes", "ouvrages fluviaux"
    ]
    if any(interdite in activite for interdite in activites_interdites):
        raisons.append(f"L'activité '{activite}' fait partie des exclusions Allianz (ex : {', '.join(activites_interdites)}).")
        eligibilite = False

    # Bloc 3 – Seuil minimum de chiffre d'affaires
    if chiffre_affaires < 35000:
        raisons.append("Le chiffre d'affaires est insuffisant pour l'acceptation Allianz (minimum 35 000 €).")
        eligibilite = False

    # Bloc 4 – Activités éligibles avec forfait
    activites_forfaitaires = [
        "maçonnerie", "charpente", "plomberie", "électricité", "peinture", "carrelage"
    ]
    if activite in activites_forfaitaires and 35000 <= chiffre_affaires <= 200000:
        produits_recommandes.append("RC Décennale Allianz – ASBTP Forfaitaire")
        eligibilite = True

    # Bloc 5 – Activités révisables au-delà de 200 000 €
    if activite in activites_forfaitaires and chiffre_affaires > 200000:
        produits_recommandes.append("RC Décennale Allianz – ASBTP Révisable")
        eligibilite = True

    # Bloc 6 – Cas ambigus ou spéciaux
    if activite not in activites_forfaitaires + activites_interdites:
        raisons.append("Activité inhabituelle ou nécessitant un visa technique Allianz. Étude manuelle requise.")
        eligibilite = False

    return {
        "eligibilite": eligibilite,
        "raisons": raisons,
        "produits_recommandes": produits_recommandes
    }
