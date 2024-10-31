from saut import Saut
from sauvegarde import sauvegarder_sauts, charger_sauts
import pandas as pd
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
from datetime import datetime

# Charger le DataFrame des sauts depuis le fichier
df_sauts = charger_sauts()

# Dictionnaire des types de saut autorisés avec leurs abréviations
TYPES_AUTORISES = {
    "Freefly": "FF",
    "Vol Relatif": "VR",
    "Wingsuit": "WS",
    "PAC": "PAC",
    "Solo": "SO",
    "Tandem": "TA",
    "Video Tandem": "VDO",
    "BPJEPS PAC": "BPJEPS",
    "Init B2": "Init B2",
    "Init B4": "Init B4",
    "Init Bi4": "Init B4",
    "Anim Freefly": "Anim FF",
    "Anim Vol Relatif": "Anim VR",
    "Hop & Pop": "H&P",
    "2way Tibo": "2way Tibo",
}

def valider_date(date_str):
    """Vérifie si la date est au format JJ/MM/AAAA et est valide."""
    try:
        datetime.strptime(date_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def sauvegarder_donnees():
    """Sauvegarde les données du DataFrame dans un fichier."""
    sauvegarder_sauts(df_sauts)
    messagebox.showinfo("Sauvegarde", "Les données ont été sauvegardées avec succès.")

def ajouter_saut():
    """Ajouter des sauts au carnet à partir des informations saisies dans l'interface."""
    try:
        nb_sauts = int(entry_nb_sauts.get())
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer un nombre valide.")
        return

    # Demander les informations communes pour tous les sauts
    date = entry_date.get()
    
    # Vérification du format de la date
    if not valider_date(date):
        messagebox.showerror("Erreur", "Veuillez entrer une date valide au format JJ/MM/AAAA.")
        return

    lieu = entry_lieu.get()
    avion = entry_avion.get()
    hauteur = entry_hauteur.get()
    voile = entry_voile.get()

    # Vérifier que le total des sauts correspond au nombre total
    total_sauts = 0
    types_sauts = {}

    for key in TYPES_AUTORISES.keys():
        try:
            count = int(entry_counts[key].get())
            if count < 0:
                raise ValueError("Le nombre de sauts ne peut pas être négatif.")
            types_sauts[key] = count
            total_sauts += count
        except ValueError:
            continue  # Ignorer les entrées non valides

    if total_sauts != nb_sauts:
        messagebox.showerror("Erreur", f"Le nombre total de sauts ({total_sauts}) doit correspondre au nombre de sauts saisi ({nb_sauts}).")
        return

    global df_sauts
    nouveaux_sauts = []

    # Créer un saut pour chaque type spécifié
    for type_saut, count in types_sauts.items():
        for _ in range(count):
            saut = Saut(date, lieu, avion, hauteur, voile, type_saut)
            nouveaux_sauts.append(saut.to_dict())

    # Ajouter les nouveaux sauts au DataFrame
    df_sauts = pd.concat([df_sauts, pd.DataFrame(nouveaux_sauts)], ignore_index=True)
    messagebox.showinfo("Succès", f"{nb_sauts} saut(s) ajouté(s) avec succès !")

    # Sauvegarde automatique des données
    sauvegarder_donnees()

    # Réinitialiser les champs d'entrée
    clear_entries()

def clear_entries():
    """Réinitialiser les champs d'entrée."""
    entry_nb_sauts.delete(0, tk.END)
    entry_date.delete(0, tk.END)
    entry_lieu.delete(0, tk.END)
    entry_avion.delete(0, tk.END)
    entry_hauteur.delete(0, tk.END)
    entry_voile.delete(0, tk.END)

    # Réinitialiser les entrées de compte
    for key in TYPES_AUTORISES.keys():
        entry_counts[key].delete(0, tk.END)

def afficher_sauts():
    """Afficher les sauts dans une nouvelle fenêtre."""
    global df_sauts  # Déclarez df_sauts comme une variable globale
    if df_sauts.empty:
        messagebox.showinfo("Info", "Aucun saut enregistré.")
        return

    # Créer une nouvelle fenêtre
    window = tk.Toplevel(root)
    window.title("Sauts enregistrés")

    # Créer une colonne date en datetime
    df_sauts['date'] = pd.to_datetime(df_sauts['date'], errors='coerce', format='mixed')  # Conversion
    df_sauts['date'] = df_sauts['date'].dt.strftime('%d/%m/%Y')  # Formater la date

    # Triez le DataFrame par date
    df_sauts = df_sauts.sort_values(by='date')  # Trier par date

    # Créer un style pour le Treeview
    style = ttk.Style()
    style.configure("Treeview", justify="center")  # Centrer les données dans le Treeview

    # Créer un tableau avec ttk.Treeview
    tree = ttk.Treeview(window, columns=("Date", "Lieu", "Avion", "Hauteur", "Voile", "Type"), show='headings')
    tree.heading("Date", text="Date")
    tree.heading("Lieu", text="Lieu")
    tree.heading("Avion", text="Avion")
    tree.heading("Hauteur", text="Hauteur (m)")
    tree.heading("Voile", text="Voile")
    tree.heading("Type", text="Type")
    
    # Centrer le texte des colonnes
    for col in tree["columns"]:
        tree.column(col, anchor="center")

    # Insérer les données
    for _, row in df_sauts.iterrows():
        tree.insert("", tk.END, values=(row['date'], row['lieu'], row['avion'], row['hauteur'], row['voile'], row['type_saut']))  # Modifié ici

    # Afficher le tableau
    tree.pack(expand=True, fill=tk.BOTH)

    # Afficher le nombre total de sauts
    total_sauts = len(df_sauts)
    label_total = tk.Label(window, text=f"Nombre total de sauts : {total_sauts}")
    label_total.pack()

    # Graphiques
    afficher_graphiques()

def afficher_graphiques():
    """Afficher des graphiques pour les sauts."""
    global df_sauts  # Déclarez df_sauts comme une variable globale
    if df_sauts.empty:
        return

    # Créer une copie du DataFrame pour le traitement des mois
    df_sauts_month = df_sauts.copy()

    # Convertir la colonne 'date' en datetime et créer une colonne 'mois'
    df_sauts_month['mois'] = pd.to_datetime(df_sauts_month['date'], format="%d/%m/%Y").dt.to_period('M')

    # Filtrer pour garder uniquement les sauts de l'année en cours
    current_year = pd.to_datetime('today').year
    df_sauts_month = df_sauts_month[df_sauts_month['mois'].dt.year == current_year]

    # Créer une plage de tous les mois de l'année en cours
    all_months = pd.date_range(start=f"{current_year}-01-01", end=pd.to_datetime('today').normalize(), freq='MS').to_period('M')

    # Compter le nombre de sauts par mois
    sauts_par_mois = df_sauts_month['mois'].value_counts().reindex(all_months, fill_value=0)

    # Graphique du nombre de sauts par mois
    fig1 = plt.figure(figsize=(12, 6))
    sauts_par_mois.plot(kind='bar', color='skyblue')
    plt.title("Nombre de sauts par mois")
    plt.xlabel("Mois")
    plt.ylabel("Nombre de sauts")

    # Formater les mois au format "MM/AAAA"
    tick_labels = [f"{m.month:02d}/{m.year}" for m in sauts_par_mois.index]
    plt.xticks(ticks=range(len(sauts_par_mois.index)), labels=tick_labels, rotation=45)

    plt.tight_layout()
    plt.show(block=False)  # Affiche le graphique

    # Graphique du nombre de sauts par type avec le DataFrame d'origine
    sauts_par_type = df_sauts['type_saut'].value_counts()
    
    fig2, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        sauts_par_type,
        autopct=lambda pct: f"{pct:.1f}%\n({int(pct/100*sum(sauts_par_type))})",
        startangle=90,
        textprops={'color':"black", 'fontsize': 10}
    )

# Ajouter la légende sur le côté droit du camembert
    ax.legend(wedges, sauts_par_type.index, title="Types de saut", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    # Afficher le titre et le total de sauts sous le camembert
    plt.title("Répartition des sauts par type")
    plt.ylabel("")  # Masquer le label de l'axe des y
    total_sauts = sauts_par_type.sum()
    plt.figtext(0.5, 0.02, f"Nombre total de sauts : {total_sauts}", ha="center", fontsize=12)

    plt.show(block=False)  # Affiche le graphique

    # Renommer les fenêtres après qu'elles aient été affichées
    fig1.canvas.manager.window.title("Nombre de sauts par mois")
    fig2.canvas.manager.window.title("Type de sauts effectués")

# Créer la fenêtre principale
root = tk.Tk()
root.title("Carnet de Saut")

# Cadre pour ajouter des sauts
add_saut_frame = tk.Frame(root)
add_saut_frame.pack(padx=10, pady=10)

# Créer les champs d'entrée
label_nb_sauts = tk.Label(add_saut_frame, text="Combien de sauts avez-vous fait aujourd'hui ?")
label_nb_sauts.grid(row=0, column=0, sticky=tk.W)
entry_nb_sauts = tk.Entry(add_saut_frame)
entry_nb_sauts.grid(row=0, column=1)

label_date = tk.Label(add_saut_frame, text="Date (JJ/MM/AAAA) :")
label_date.grid(row=1, column=0, sticky=tk.W)
entry_date = tk.Entry(add_saut_frame)
entry_date.grid(row=1, column=1)

label_lieu = tk.Label(add_saut_frame, text="Lieu :")
label_lieu.grid(row=2, column=0, sticky=tk.W)
entry_lieu = tk.Entry(add_saut_frame)
entry_lieu.grid(row=2, column=1)

label_avion = tk.Label(add_saut_frame, text="Avion :")
label_avion.grid(row=3, column=0, sticky=tk.W)
entry_avion = tk.Entry(add_saut_frame)
entry_avion.grid(row=3, column=1)

label_hauteur = tk.Label(add_saut_frame, text="Hauteur (en mètres) :")
label_hauteur.grid(row=4, column=0, sticky=tk.W)
entry_hauteur = tk.Entry(add_saut_frame)
entry_hauteur.grid(row=4, column=1)

label_voile = tk.Label(add_saut_frame, text="Voile utilisée :")
label_voile.grid(row=5, column=0, sticky=tk.W)
entry_voile = tk.Entry(add_saut_frame)
entry_voile.grid(row=5, column=1)

# Créer des entrées pour le nombre de sauts de chaque type
entry_counts = {}
label_type = tk.Label(add_saut_frame, text="Nombre de sauts par type :")
label_type.grid(row=6, column=0, sticky=tk.W, columnspan=2)

for i, key in enumerate(TYPES_AUTORISES.keys()):
    label = tk.Label(add_saut_frame, text=f"{key} :")
    label.grid(row=7 + i, column=0, sticky=tk.W)
    entry = tk.Entry(add_saut_frame)
    entry.grid(row=7 + i, column=1)
    entry_counts[key] = entry

# Bouton pour ajouter le saut
button_ajouter = tk.Button(add_saut_frame, text="Ajouter Saut", command=ajouter_saut)
button_ajouter.grid(row=7 + len(TYPES_AUTORISES), column=0, columnspan=2)

# Bouton pour afficher les sauts
button_afficher = tk.Button(root, text="Afficher Sauts", command=afficher_sauts)
button_afficher.pack(pady=10)

# Lancer la boucle principale
root.mainloop()
