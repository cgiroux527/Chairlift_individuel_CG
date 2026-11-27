from tkinter import filedialog, messagebox

import customtkinter as ctk
import pandas as pd

from Accueil import Accueil
from SelectionLift import SelectionLift
from AfficherSelection import AfficherSelection
from GraphCompare import GraphCompare

from math import pi

from PIL import Image

COULEURS = ["red", "blue", "green", "yellow"]
COLONNES = ["Vitesse", "Taille chaise", "Longueur câble", "Temps trajet", "Capacité"]

"""Classe qui gère la page au complet, alors l'appel des instances des autres classes"""
class PageComparer(ctk.CTkFrame) :

    def __init__(self, parent) :

        super().__init__(parent, fg_color="transparent")

        #Initialiser le df vide pour l'importation
        self.df_csv = pd.DataFrame()

        #Aller chercher le nombre de remontées observées choisis dans l'accueil
        self.nb_observer = self.master.nb_lift

        self.choix = []
        self.affichage_choix = []

        self.est_donnee_importee = False

        self.creer_widgets()

        #Configurer la taille que peut prendre les lignes et colonnes
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=3)

        for i in range(self.nb_observer) :
            self.grid_rowconfigure(i, weight=1)
        self.grid_rowconfigure(self.nb_observer+1, weight=0)

    
    def creer_widgets(self) :
        #Une frame dans laquelle on place tous les éléments de la première colonnes, rend le expand=True plus facile à gérer, plus prévisible
        self.frame_choix = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_choix.grid(row=0, column=0, rowspan=self.nb_observer, padx=20, pady=10, sticky="nsew")

        #Une frame pour mettre la "maison" et le bouton d'importation ensemble 
        frame_coin_gauche = ctk.CTkFrame(self.frame_choix, fg_color="transparent")
        frame_coin_gauche.grid(row=0, column= 0, sticky="nsew")

        #Bouton pour revenir à l'accueil, celui-ci est transparent et contient une image de maison 
        image_accueil = ctk.CTkImage(light_image=Image.open("maison.png"), size=(17,17))
        self.bouton_accueil = ctk.CTkButton(frame_coin_gauche, image=image_accueil, text="", fg_color="transparent", hover=False, command=self.quand_accueil, width=30, height=30,)
        self.bouton_accueil.grid(row=0, column=0, sticky="w", pady=5, padx=(10,5))

        #Bouton d'importation
        self.bouton_donnee = ctk.CTkButton(frame_coin_gauche, text="Choisir base donnée", command=self.quand_importer)
        self.bouton_donnee.grid(row=0, column=1, sticky="ew", pady=5, padx=(5,10))

        #Ajouter le bon nombre d'instances de SelectionLift dans la liste de ceux-ci 
        for i in range(self.nb_observer) :
            self.choix.append(SelectionLift(self.frame_choix, self.df_csv))
            self.choix[i].grid(row=2*(i+1), column=0, sticky="nsew")

        #Ajouter le texte "Choix" pour chaque instance de SelectionLift
        for i in range(self.nb_observer) :
            label_lift = ctk.CTkLabel(self.frame_choix, text= f"Choix #{i+1}", font=("Arial", 15, "bold"), text_color=COULEURS[i])
            label_lift.grid(row=(2*i)+1, column=0, sticky="nsew")

        #Bouton qui recommence la comparaison
        self.bouton_comparer = ctk.CTkButton(self.frame_choix, text="Comparer", command=self.quand_comparer)
        self.bouton_comparer.grid(row=2*self.nb_observer+1, column=0, sticky="ns", pady=(15,3), padx=10)

    #Méthode appelée pour revenir à l'accueil
    def quand_accueil(self) :
        self.master.changer_page(Accueil)

    def quand_comparer(self) :
        #S'assurer que les remontées sont toutes choisies
        if self.pret_a_comparer() :
            #Appeler la destruction de ce qui était présent avant
            self.detruire_affichages()

            noms = []
            #Afficher la sélection de chacun des choix
            for i in range(self.nb_observer) :
                self.affichage_choix.append(AfficherSelection(self, self.choix[i].chairlift, i))
                self.affichage_choix[i].grid(row=i, column=1, sticky="nsew", padx=20, pady=10)
                #Ajouter les noms à une liste des noms, pour les graphiques
                noms.append(self.affichage_choix[i].chairlift.nom)

            #Afficher les graphiques
            self.graph = GraphCompare(self, self.creer_df_donnee(), noms)
            self.graph.grid(row=0, column=2, rowspan=self.nb_observer, sticky="nsew")

            #Bouton d'exportation
            self.bouton_exporter = ctk.CTkButton(self, text="Exporter le DataFrame", command=self.quand_exporter)
            self.bouton_exporter.grid(row=self.nb_observer+1, column=0, sticky="ns", pady=(10,15), padx=10)
      
        else : 
            messagebox.showerror("Erreur ", f"Choisir au moins {self.nb_observer} remontées pour les comparer")

    def pret_a_comparer(self) :
        #S'assurer que pour le nombre choisi chacun des choix a est_choisi = True
        for i in range(self.nb_observer):
            if not self.choix[i].est_choisi:
                return False

        return True

    def detruire_affichages(self) :
        #Si il y avait des affichages, les détruire et réinitialiser la liste
        if len(self.affichage_choix) > 0 :
            for i in range(self.nb_observer) :
                if self.affichage_choix[i] :
                    self.affichage_choix[i].destroy()
                else :
                    continue
            self.affichage_choix = []


    def creer_df_donnee(self) :
        listes = []
        #Créer un dataframe avec ce qui est affiché, utile pour l'exportation
        for i in range(self.nb_observer) :
            listes.append(self.affichage_choix[i].get_list_donnee())

        return pd.DataFrame(listes, columns=COLONNES)

    def quand_exporter(self) :
        #Demander où mettre le fichier exporté
        chemin_exporter = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Fichiers CSV", "*.csv")])
        
        try :
            #À l'aide de Pandas, mettre tout le DataFrame dans le CSV 
            df_exporter = self.creer_df_donnee()
            print(df_exporter)
            df_exporter.to_csv(chemin_exporter, index=False)
            messagebox.showinfo(title="Reussite", message=f"Fichier a été exporté à : {chemin_exporter}")
        except Exception as erreur:
            messagebox.showerror("Erreur d'exportation", f"Erreur inattendue : {erreur}")

    def quand_importer(self) :
        #Choisir le fichier à importer
        self.chemin_importer = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("Fichiers CSV", "*.csv")])
        if self.chemin_importer:
            try :
                #Appeler l'importation
                self.importer()
                if self.est_donnee_importee :
                    messagebox.showinfo(title="Réussite", message=f"Le fichier suivant a bien été importé :\n {self.chemin_importer} \nCertaines données peuvent avoir été supprimées pour le bon fonctionnement du comparateur")
                    for choix in self.choix:
                        #Rendre les radiobuttons de csv fonctionnels si l'importation est réussie
                        choix.radio_button_csv.configure(state="normal")
                        choix.df = self.df_csv

            except (OSError, ValueError, KeyError) as erreur:
                messagebox.showerror("Erreur dans l'import", erreur)
                print("Chargement impossible ", erreur)


    def importer(self) :   
        try :
            #Mettre dans un df le csv choisi
            self.df_csv = pd.read_csv(self.chemin_importer)
            #Enlever s'il y a des copies
            self.df_csv = self.df_csv.drop_duplicates()
            #Seulement garder ceux qui contiennent toutes ces colonnes, ce sont celles importantes pour la comparaison
            self.df_csv = self.df_csv.loc[:,["name", "countries", "regions", "duration_sec", "capacity", "speed_m_per_s","occupancy", "inclined_length_m"]]
            #Enlever les lignes qui contiennent des NAN ou simplement rien
            self.df_csv = self.df_csv.dropna()

            #Retirer les lifts qui ont le même nom aux mêmes endroits 
            self.df_csv = self.df_csv.drop_duplicates(subset=["countries", "regions", "name"])

            #Trier pour que les vitesse aient du sens
            condition_vitesse = (self.df_csv["speed_m_per_s"] >= 1.0) & (self.df_csv["speed_m_per_s"] <= 10.0)
            self.df_csv = self.df_csv[condition_vitesse]

            #Trier pour que la longueur du cable ait du sens
            condition_longueur = (self.df_csv["inclined_length_m"] >= 1.0) & (self.df_csv["inclined_length_m"] <= 10000.0)
            self.df_csv = self.df_csv[condition_longueur]

            #Enlever les instances de deux pays differents et pareil pour region et names (ex : Alberta; Manitoba. pour la même remontée)
            condition_2_pays = self.df_csv["countries"].str.contains(";") | self.df_csv["countries"].str.contains(",")
            self.df_csv = self.df_csv[~condition_2_pays]

            condition_2_regions = self.df_csv["regions"].str.contains(";") | self.df_csv["regions"].str.contains(",")
            self.df_csv = self.df_csv[~condition_2_regions]

            condition_2_noms = self.df_csv["name"].str.contains(";") | self.df_csv["name"].str.contains(",")
            self.df_csv = self.df_csv[~condition_2_noms]

            #Enlever les faux noms de chairlifts (trop courts pour avoir du sens)
            condition_nom_court = self.df_csv["name"].str.len() > 3
            self.df_csv = self.df_csv[condition_nom_court]

            #S'assurer que le nombre de personnes par chaise est correct.
            condition_occupancy = (self.df_csv["occupancy"] >= 2) & (self.df_csv["occupancy"] <= 10)
            self.df_csv = self.df_csv[condition_occupancy]

            #Réinitialiser les index importés
            self.df_csv = self.df_csv.reset_index(drop=True)

            #La variable permet maintenant de confirmer que l'importation est réussie
            self.est_donnee_importee = True

        #Envoyer une erreur si l'importation avec toutes ces conditions échoue
        except Exception as erreur :  
            messagebox.showerror("Erreur dans le fichier choisi ", f"Assurez vous d'avoir les bonnes colonnes de OpenSkiData : {erreur}")


