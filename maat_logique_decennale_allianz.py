# fichier : maat_logique_decennale_allianz.py

def normalize_activite(activite: str) -> str:
    return activite.strip().lower()


def verifier_eligibilite_allianz_decennale(statut: str, activite: str, chiffre_affaires: float) -> dict:
    raisons = []
    produits_recommandes = []

    statut = statut.lower().strip()
    activite = activite.lower().strip()

    # Initialisation
    eligibilite = True

    # Bloc 1 – Exclusions catégoriques
    bloc1 = statut not in ["sci", "association", "auto-construction"]
    if not bloc1:
        raisons.append("Les SCI, associations et structures d'auto-construction ne sont pas assurables en RC Décennale Allianz.")
    eligibilite = eligibilite and bloc1

    # Bloc 2 – Activités interdites
    activites_interdites = [
        "désamiantage", "nucléaire", "offshore", "fondations spéciales", "ouvrages maritimes", "ouvrages fluviaux"
    ]
    bloc2 = not any(interdite in activite for interdite in activites_interdites)
    if not bloc2:
        raisons.append(f"L'activité '{activite}' fait partie des exclusions Allianz (ex : {', '.join(activites_interdites)}).")
    eligibilite = eligibilite and bloc2

    # Bloc 3 – Seuil minimum de chiffre d'affaires
    bloc3 = chiffre_affaires >= 35000
    if not bloc3:
        raisons.append("Le chiffre d'affaires est insuffisant pour l'acceptation Allianz (minimum 35 000 €).")
    eligibilite = eligibilite and bloc3

    # Bloc 4 et 5 – Produits forfaitaires ou révisables
    activites_forfaitaires = [
        "maçonnerie", "charpente", "plomberie", "électricité", "peinture", "carrelage"
    ]
    if eligibilite and activite in activites_forfaitaires:
        if chiffre_affaires <= 200000:
            produits_recommandes.append("RC Décennale Allianz – ASBTP Forfaitaire")
        else:
            produits_recommandes.append("RC Décennale Allianz – ASBTP Révisable")

    # Bloc 6 – Cas inhabituels (à la fin si tout le reste passe mais activité inconnue)
    bloc6 = activite in activites_forfaitaires or any(interdite in activite for interdite in activites_interdites)
    if eligibilite and not bloc6:
        raisons.append("Activité inhabituelle ou nécessitant un visa technique Allianz. Étude manuelle requise.")
        eligibilite = False

    return {
        "eligibilite": eligibilite,
        "raisons": raisons,
        "produits_recommandes": produits_recommandes
    }
