from tkinter import messagebox

import customtkinter as ctk

from Chairlift import Chairlift
from GraphControl import GraphControl
from Accueil import Accueil
from Sliders import Sliders

class PageCreation(ctk.CTkFrame) :
    def __init__(self, parent) :
        # Initialiser la fenêtre principale
        super().__init__(parent)
    
        # Initialiser, en privé, le Chairlift courant
        self.__chairlift = Chairlift()
    
        # Initialiser la frame des sliders et autres boutons
        self.grid_rowconfigure(0, weight=1)
        self.sliders = Sliders(self, self.__chairlift, self.mettre_a_jour)
        self.sliders.grid(row=0, column=0, rowspan=3, sticky="nsew", padx=12, pady=12)
    
        # Initialiser la frame du Graphique
        self.graph = GraphControl(self, self.__chairlift)
        self.graph.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=12, pady=12)
    
        # Affichage du label du nombre de personnes par heure avec les paramètres courants.
        self.label_nb_personne = ctk.CTkLabel(self, bg_color="white", text="Nombre de personnes par heure : " + str(self.__chairlift.calculerNombreDePersonnesParHeure()), text_color="black")
        self.label_nb_personne.grid(row=1, column=1, columnspan=2, sticky="nsew", padx=10, pady=(0,12))
        # Bouton de rafraichissement
        self.bouton_rafraichissement = ctk.CTkButton(self, text="Recalculer", command=self._rafraichissement)
        self.bouton_rafraichissement.grid(row=2, column=1, sticky="nsew", padx=12, pady=(3,12))
        #Bouton creer
        self.bouton_creer = ctk.CTkButton(self, text="Créer et revenir à l'accueil", command=self._creer_lift)
        self.bouton_creer.grid(row=2, column=2, sticky="nsew", padx=12, pady=(3,12))
    
        # Modifier le poids des différentes colonnes
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        #Configurer les rows du grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
    
        # Appeler mettre à jour qui met à jour l'image/le graph
        self.mettre_a_jour()
    
    # Mettre à jour le graphique 
    def mettre_a_jour(self):
        self.graph.mise_a_jour_image()
    
        self.label_nb_personne.configure(text="Nombre de personnes par heure : " + str(self.__chairlift.calculerNombreDePersonnesParHeure()))
    
    # Commande du bouton de rafraichissement qui recalcule et déselectionne
    def _rafraichissement(self) :
        self.sliders.reset_radio_var()
    
        self.label_nb_personne.configure(text="Nombre de personnes par heure : " + str(self.__chairlift.calculerNombreDePersonnesParHeure()))

    def get_chairlift_courant(self) :
        return self.__chairlift

    def _creer_lift(self) :
        nom = self.sliders.get_entry_nom()

        if len(nom) > 0 and self.existe_pas(nom) :          
            self.master.ajouter_chairlift(self.__chairlift)
            self.__chairlift.definirNom(nom)
            self.master.changer_page(Accueil)
        elif len(nom) == 0 :
            messagebox.showwarning(title="Erreur", message="Veuillez entrer un nom pour la remontée créée")
        else :
            messagebox.showerror(title="Erreur", message="Veuillez choisir un nouveau nom" )

    def existe_pas(self, nom) :
        for lift in self.master.get_chairlifts() :
            if nom == lift.nom :
                return False
            else : 
                continue