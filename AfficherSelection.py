import customtkinter as ctk


COULEURS = ["red", "blue", "green", "yellow"]

"""Classe qui gère l'affichage de l'instance sélectionnée"""
class AfficherSelection(ctk.CTkFrame) :

    def __init__(self, parent, chairlift, indice) :
        super().__init__(parent, fg_color="transparent")

        #Initialiser les paramètres donnés à l'appel de la classe
        self.chairlift = chairlift
        #Sera utilisé pour s'assurer d'avoir la bonne remontée dans la liste
        self.indice = indice

        #Créer les widgets avec la méthode correspondante
        self.creer_widgets()

    def creer_widgets(self) :
        #Un label par paramètre du chairlift donné en paramètre
        self.label_nom = ctk.CTkLabel(self, text=self.chairlift.nom, font=("Arial", 20, "bold"), text_color=COULEURS[self.indice])
        self.label_nom.grid(row=0, column=0, pady=(20,0))

        self.label_vitesse = ctk.CTkLabel(self, text=f"\u00B7 Vitesse : {self.chairlift.obtenirVitesse()} m/s")
        self.label_vitesse.grid(row=1, column=0)

        self.label_personne_chaise = ctk.CTkLabel(self, text=f"\u00B7 {self.chairlift.obtenirNombreDePersonnesParChaise()} personnes par chaise")
        self.label_personne_chaise.grid(row=2, column=0)

        self.label_longueur = ctk.CTkLabel(self, text=f"\u00B7 Longueur du câble : {self.chairlift.obtenirLongueurDuTrajet()} m")
        self.label_longueur.grid(row=3, column=0)

        self.label_temps = ctk.CTkLabel(self, text=f"\u00B7 Temps du trajet : {round(self.chairlift.calculerTempsTrajet(), 1)} s")
        self.label_temps.grid(row=4, column=0)

        #Appel de la méthode associé pour avoir la capacité
        self.label_capacite = ctk.CTkLabel(self, text=f"\u2192 Capacité : {self.get_capacite()} personnes par heure", text_color=COULEURS[self.indice], font=("Arial", 15))
        self.label_capacite.grid(row=5, column=0)

    def get_capacite(self) :
        #Calcul à l'aide de la classe associée à une instance de Chairlift
        return self.chairlift.calculerNombreDePersonnesParHeure()

    def get_list_donnee(self) :
        #Créer une liste des paramètres du Chairlift affiché, sera utilisé pour l'exportation
        return [self.chairlift.obtenirVitesse(), self.chairlift.obtenirNombreDePersonnesParChaise(), self.chairlift.obtenirLongueurDuTrajet(), self.chairlift.calculerTempsTrajet(), self.get_capacite()]

