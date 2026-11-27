from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import customtkinter as ctk

from math import pi
from pandas import DataFrame

#Données constantes utilisées pour la création des graphiques
COULEURS = ["red", "blue", "green", "yellow"]

COLONNES = ["Vitesse", "Taille chaise", "Longueur câble", "Temps trajet", "Capacité"]
BORNES = dict(zip(COLONNES, [[1,10], [1, 10], [1, 9000], [1, 1500], [1, 3500]])) #Trouvé avec les maximums du csv et en faisant des tests de création

"""Classe qui gère les différents graphiques affichés"""
class GraphCompare(ctk.CTkFrame) :
    def __init__(self, parent, df, noms) :
        super().__init__(parent, fg_color="transparent")

        #Initialiser les paramètres donnés
        self.df_donnee = df
        self.noms = noms

        #Créer deux attributs utiles
        self.categories = list(self.df_donnee)
        self.normalisee = self.normaliser_donnees()

        #Appeler la création de widgets
        self.creer_widgets()

    def creer_widgets(self) :
        #creer la tabview et placer les deux dedans 
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.tabs_graphs = ctk.CTkTabview(self)
        self.tabs_graphs.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.tabs_graphs.add("1 - Barres")
        self.tabs_graphs.add("2 - Radar")
        self.tabs_graphs.set("2 - Radar")

        #Création des graphiques avec leurs onglets respectifs
        self.creer_graphe_bar("1 - Barres")
        self.creer_graphe_etoile("2 - Radar")

    def creer_graphe_bar(self, tab) :
        #Initialiser la figure 
        figure = Figure(figsize=(7, 5), layout="constrained")

        #Ajouter un Canva dans la bonne tab, dans la figure
        canvas = FigureCanvasTkAgg(figure, master=self.tabs_graphs.tab(tab))
        #Afficher le canva
        canvas.get_tk_widget().pack(fill="both", expand=True)

        #Ajouter le graphique (plot) à la figure
        graph = figure.add_subplot(111)

        #Mettre le bon graph avec les valeurs normalisee dans celui-ci
        complet = graph.grouped_bar(self.normalisee, group_spacing=1, tick_labels=self.noms, labels=COLONNES)
        graph.legend()

        #Afficher les valeurs arrondies sur le dessus des barres
        for conteneur in complet.bar_containers:
            graph.bar_label(conteneur, padding=3, fmt="%.2f")
        #Mettre une limite, 10, car les valeurs sont normalisées sur 10
        graph.set_ylim(0, 10)


    def creer_graphe_etoile(self, tab) :

        #Nombre de catgégories
        N = len(self.categories)

        #Définir les angles de chacune des catégories
        angles = []
        for n in range(N) :
            angles.append(n/float(N) * 2*pi)

        #Ajouter le premier angle pour pouvoir fermer le cercle
        angles += angles[:1]

        #Encore une fois initialiser la figure, le canva et le graph
        figure = Figure(figsize=(7, 5), layout="constrained")
        
        canvas = FigureCanvasTkAgg(figure, master=self.tabs_graphs.tab(tab))
        canvas.get_tk_widget().pack(fill="both", expand=True)

        #Polar=True pour obtenir un plot de style Radar
        graph = figure.add_subplot(111, polar=True)

        #TODO
        graph.set_theta_offset(pi / 2)
        graph.set_theta_direction(-1)

        #Délimiter les valeurs possibles en x (en cercle, avec angles) et en y 
        graph.set_xticks(angles[:-1], self.categories)
        graph.set_rlabel_position(0)
        graph.set_yticks([2,4,6,8,10], ["2","4","6","8","10"], color="grey", size=7)
        graph.set_ylim(0,10)

        for i in range(len(self.df_donnee)) :
            valeurs = self.normalisee.iloc[i].values.flatten().tolist()
            #Fermer la ligne sur le graphique en ajoutant la valeur de départ
            valeurs += valeurs[:1]
            graph.plot(angles, valeurs, linewidth=1, linestyle='solid', color=COULEURS[i]) 
            graph.fill(angles, valeurs, COULEURS[i], alpha=0.1)


    def normaliser_donnees(self) :
        resultat = DataFrame()
        #Pour toutes les données du df de base, on ajoute les series normalisées à un nouveau DataFrame (resultat)
        for colonne in self.df_donnee.columns :
            series_x = self.df_donnee.loc[:, colonne]
            resultat[colonne] = normaliser_x(series_x, BORNES[colonne][0], BORNES[colonne][1])
        return resultat

#Fonction hors de la classe qui permet de normaliser une serie (x) avec le minimum et le maximum voulu
def normaliser_x(x, min, max) :
    #Formule : (x-xmin)/(xmax-xmin) *10 -> c'est donc sur un total de 10
        return ((x-min)/(max-min)*10).clip(lower=0, upper=10)
