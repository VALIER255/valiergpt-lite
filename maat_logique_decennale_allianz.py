
def analyse_allianz_decennale(donnees_client):
    alertes = []
    produits_recommandes = []

    activite = donnees_client.get("activite_principale", "").lower().strip()
    statut = donnees_client.get("statut_juridique", "").lower().strip()
    chiffre_affaires = donnees_client.get("chiffre_affaires", 0)

    # Bloc 1 : Activités acceptées
    activites_acceptables = [
        "maçon", "maçonnerie", "charpentier", "charpente", "couvreur", "couverture",
        "menuisier", "menuiserie", "plâtrier", "plaquiste", "peintre", "electricien"
    ]

    if activite not in activites_acceptables:
        alertes.append("Activité non acceptée pour Allianz Décennale.")

    # Bloc 2 : Statuts refusés
    statuts_refuses = ["sci", "association", "auto entrepreneur"]
    if any(statut_refuse in statut for statut_refuse in statuts_refuses):
        alertes.append("Statut juridique refusé pour la souscription (ex. SCI, Association, Auto-entrepreneur).")

    # Bloc 3 : Seuil de chiffre d'affaires
    if chiffre_affaires < 35000:
        alertes.append("Chiffre d'affaires trop faible pour souscrire chez Allianz (min 35 000 €).")

    # Bloc 4 : Seuil de CA au-delà duquel le contrat devient révisable
    if chiffre_affaires > 200000:
        alertes.append("Contrat Allianz devient révisable au-delà de 200 000 € de CA annuel.")

    if not alertes:
        produits_recommandes.append("RC Décennale Allianz – ASBTP")

    return {
        "alertes": alertes,
        "produits_recommandes": produits_recommandes
    }
