# sauvegarde.py

import pandas as pd

def sauvegarder_sauts(df, fichier="carnet_sauts.csv"):
    """Sauvegarde le DataFrame des sauts dans un fichier CSV."""
    df.to_csv(fichier, index=False)
    print("Données sauvegardées dans", fichier)

def charger_sauts(fichier="carnet_sauts.csv"):
    """Charge les sauts depuis un fichier CSV dans un DataFrame pandas."""
    try:
        df = pd.read_csv(fichier)
        print("Données chargées depuis", fichier)
        return df
    except FileNotFoundError:
        print("Aucun fichier trouvé, création d'un nouveau DataFrame.")
        columns = ["date", "lieu", "avion", "hauteur", "voile", "type_saut"]
        return pd.DataFrame(columns=columns)