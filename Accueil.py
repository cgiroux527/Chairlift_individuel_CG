import customtkinter as ctk

from PIL import Image

from tkinter import messagebox

#Constante du nombre de remontées, sera dans le OptionMenu correspondant, ici 4 et plus de rentre pas dans la taille de mon écran, modifier celle-ci pour avoir accès à plus. 2 doit être le minimum.
NOMBRES_LIFTS = ["2","3"]

"""Classe qui gère l'accueil et donc le choix entre le comparateur et le créateur"""
class Accueil(ctk.CTkFrame) :

    def __init__(self, parent) :
        super().__init__(parent, fg_color="transparent")

        #Bouton pour accéder au créateur
        ctk.CTkButton(self, text="Créateur de remontée",  font=("Arial", 21), command=parent.afficher_createur, height=40, width= 300).grid(column=0, row=2, padx=20, pady=20)

        #Titre de l'application en haut en gros
        ctk.CTkLabel(self, text="ELEVATE", font=("Arial", 60, "bold")).grid(row=0, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")

        #image centrale dans l'accueil, placée dans un label pour l'afficher
        img_lift = ctk.CTkImage(light_image=Image.open("skilift.png"), size=(400,400))
        label_img_lift = ctk.CTkLabel(self, image=img_lift, text="")
        label_img_lift.grid(row=1, column=0, padx=20, pady=20, columnspan=3, sticky="nsew")

        #Création d'une frame pour placer le option menu et le bouton de comparateur ensemble
        frame_comparer = ctk.CTkFrame(self, fg_color="transparent")
        frame_comparer.grid(row=2, column=2, padx=20, pady=20)
        #Bouton pour accéder au comparateur
        ctk.CTkButton(frame_comparer, text="Comparateur de remontées", font=("Arial", 21), command=parent.afficher_comparer, height=40, width= 300).grid(column=0, row=0, padx=(10,2))
        self.nb_est_choisi = False
        #Option menu pour choisir le nombre de remontées à comparer
        option_nb_lift = ctk.CTkOptionMenu(frame_comparer, values=NOMBRES_LIFTS, command=self.quand_option_nb, height=40, width=65)
        option_nb_lift.set("2")
        option_nb_lift.grid(row=0, column=1, padx=(2,10))
        #Initialiser de base à 2
        self.nb_lift = 2

        #Configurer l'espace pour les colonnes et lignes de la frame de l'Accueil
        for i in range(3) :
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)

    #Appelé pour valider le choix dans l'option menu du comparateur, Nombre de lift sera alors modifié
    def quand_option_nb(self, choix) :
        nb = int(choix)
        if nb >=2 and nb <= 4 :
            self.nb_lift = int(choix)
        else :
            messagebox.showerror(title="Erreur", message="Valeur invalide")

    def get_nb_lift(self) :
        #La constante est en string pour les mettre dans l'option menu, transformé en int pour utiliser ses valeurs
        nb_int = [int(n) for n in NOMBRES_LIFTS]
        #S'assurer que rien ne déborde le maximum ni le minimum et retourner le nombre de remontées
        if self.nb_lift >= min(nb_int) and self.nb_lift <= max(nb_int) :
            return self.nb_lift
        else : 
            return 2



