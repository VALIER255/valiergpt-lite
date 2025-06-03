
# maat_logique_decennale_allianz.py

def normalize_activite(activite):
    """Normalise l’activité : minuscule + sans accent + stripping."""
    import unicodedata
    return ''.join(
        c for c in unicodedata.normalize('NFD', activite.lower())
        if unicodedata.category(c) != 'Mn'
    ).strip()


def analyser_donnees(donnees):
    alertes = []
    produits = []

    statut = donnees.get("statut_juridique", "").lower().strip()
    activite = normalize_activite(donnees.get("activite_principale", ""))
    ca = donnees.get("chiffre_affaires", 0)

    # Bloc 1 – Exclusion par statut juridique
    if "sci" in statut:
        alertes.append("Les SCI ne sont pas assurables en RC Décennale Allianz.")
        return {"alertes": alertes, "produits_recommandes": produits}

    # Bloc 2 – Seuil minimum de chiffre d’affaires
    if ca < 35000:
        alertes.append("Chiffre d'affaires trop faible pour Allianz Décennale (min. 35 000 €).")
        return {"alertes": alertes, "produits_recommandes": produits}

    # Bloc 3 – Activités expressément refusées
    activites_refusees = [
        "désamiantage", "fondations spéciales", "paratonnerre", "pieux", "pieux forés", "pieux battus"
    ]
    for act_refusee in activites_refusees:
        if act_refusee in activite:
            alertes.append(f"Activité refusée par Allianz : {act_refusee}")
            return {"alertes": alertes, "produits_recommandes": produits}

    # Bloc 4 – Activités soumises à visa interne
    activites_soumises_a_visa = [
        "pisciniste", "ouvrages maritimes", "ouvrages fluviaux", "ouvrages souterrains",
        "travaux de dépollution", "construction en zone sismique", "construction de bâtiments agricoles"
    ]
    for act_visa in activites_soumises_a_visa:
        if act_visa in activite:
            alertes.append(f"Activité soumise à visa interne Allianz : {act_visa}")
            # Pas de rejet mais signalement
            break

    # Bloc 5 – Seuils de CA par type d'activité (seuil d’alerte)
    seuils_ca_par_activite = {
        "maçon": 100000,
        "charpentier": 100000,
        "couvreur": 80000,
        "plaquiste": 70000
    }
    for clef, seuil in seuils_ca_par_activite.items():
        if clef in activite:
            if ca < seuil:
                alertes.append(f"Chiffre d'affaires jugé trop faible pour activité : {clef} (seuil : {seuil} €).")
            break

    # Bloc 6 – Acceptation par défaut
    produits.append("RC Décennale Allianz – ASBTP")

    return {
        "alertes": alertes,
        "produits_recommandes": produits
    }
