
from maat_logique_decennale_allianz import analyse_allianz_decennale

def analyser_donnees_client(donnees):
    activite = donnees.get("activite_principale", "").lower().strip()
    if activite:
        return analyse_allianz_decennale(donnees)
    return {
        "alertes": ["Aucune activité principale définie."],
        "produits_recommandes": []
    }
