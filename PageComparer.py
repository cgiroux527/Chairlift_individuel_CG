from tkinter import filedialog, messagebox, IntVar, Frame

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import customtkinter as ctk
import pandas as pd

from Chairlift import Chairlift
from Accueil import Accueil

from math import pi

import csv

from PIL import Image

TEMPS_EMBARQUEMENTS_CSV = {2: 3.0, 3: 3.2, 4: 3.6, 5:4.0, 6: 4.0, 7:4.2, 8: 4.5, 9:5.0, 10: 5.0} #Calcul approximatif basé sur moyennes pour pouvoir utiliser la classe Chairlift (Temps d'embarquement). source : https://www.strmtg.developpement-durable.gouv.fr/en/chairlift-continuous-movement-unidirectional-a131.html?lang=en
DIST_ENTRE_CHAISES_CSV = 20

class SelectionLift(ctk.CTkFrame) :

    def __init__(self, parent, df) :

        super().__init__(parent, fg_color="transparent")

        self.chairlift = Chairlift()

        self.radio_var = IntVar(value=0)
        self.df = df

        self.choix_pays, self.choix_region = "", ""
        self.option_lift_perso, self.option_lift_csv, self.option_pays, self.option_region = None, None, None, None

        self.est_choisi = False

        self.creer_widgets()


    def creer_widgets(self) :
        
        self.radio_button_csv = ctk.CTkRadioButton(self, text="Depuis le CSV importé", command=self.quand_choix_csv, variable=self.radio_var, value=1, state="disabled", radiobutton_height=15, radiobutton_width=15)
        self.radio_button_csv.grid(row=0, column=0, padx=10, pady=3, sticky="nsew")
        
        radio_choix_perso = ctk.CTkRadioButton(self, text="Chairlift personnalisé", command=self.quand_choix_perso, variable=self.radio_var, value=2, radiobutton_height=15, radiobutton_width=15)
        radio_choix_perso.grid(row=1, column=0, padx=10, pady=3, sticky="nsew")


    def quand_pays(self, choix) :
        if choix != "Pays" :
            self.choix_pays = choix
            print("pays choisi : ", choix)

            #Ramener les autres à la base 
            self.choix_region = ""
            self.choix_lift_csv = ""
            self.option_region.configure(values=["Choisir un pays"])
            self.option_region.set("Region")
            self.option_lift_csv.configure(values=["Choisir une region"])
            self.option_lift_csv.set("Remontee")
            #Filtrer
            self.option_region.configure(values=self.df.loc[self.df["countries"] == self.choix_pays, "regions"].sort_values().unique().tolist())

            self.est_choisi = False


    def quand_region(self, choix) :
        if choix != "Region" and choix != "Choisir un pays" :
            self.choix_region = choix
            print("region choisi : ", choix)

            #Ramener lift csv à la base
            self.choix_lift_csv = ""
            self.option_lift_csv.configure(values=["Choisir une region"])
            self.option_lift_csv.set("Remontee")
            #Filtrer
            self.option_lift_csv.configure(values=self.df.loc[self.df["regions"] == self.choix_region, "name"].sort_values().unique().tolist())

            self.est_choisi = False

            

    def quand_lift_csv(self, choix) :
        if choix != "Remontee" and choix != "Choisir une region":
            self.choix_lift_csv = choix
            print("lift du csv choisi : ", choix)

            condition_nom_lift = (self.df["name"] == self.choix_lift_csv) & (self.df["countries"] == self.choix_pays) & (self.df["regions"] == self.choix_region)
            self.df_lift_choisi = self.df[condition_nom_lift]
            print("lift du csv choisi : ", self.df_lift_choisi)

            self.chairlift.nom = self.choix_lift_csv

            self.chairlift.definirVitesse(float(self.df_lift_choisi.loc[:,"speed_m_per_s"].item()))
            self.chairlift.definirNombreDePersonnesParChaise(int(self.df_lift_choisi.loc[:,"occupancy"].item()))
            self.chairlift.definirLongueurDuTrajet(int(self.df_lift_choisi.loc[:,"inclined_length_m"].item()))

            cle = int(self.df_lift_choisi.loc[:,"occupancy"].item())
            
            longueur = int(self.df_lift_choisi.loc[:,"inclined_length_m"].item())

            self.chairlift.definirTempsDebarquement(TEMPS_EMBARQUEMENTS_CSV[cle])
            self.chairlift.definirTempsEmbarquement(TEMPS_EMBARQUEMENTS_CSV[cle])
            
            self.chairlift.definirNombreDeChaise(longueur/DIST_ENTRE_CHAISES_CSV)


            self.est_choisi = True

    def quand_choix_csv(self) :
        if self.option_lift_perso :
            self.option_lift_perso.destroy()
            self.option_lift_perso = None

        self.option_pays = ctk.CTkOptionMenu(self, command=self.quand_pays, values=self.df["countries"].sort_values().unique().tolist())
        self.option_pays.grid(row=2, column=0, padx=10, pady=(2,3), sticky="nsew")
        self.option_pays.set("Pays")

        self.option_region = ctk.CTkOptionMenu(self, command=self.quand_region, values=["Choisir un pays"])
        self.option_region.grid(row=3, column=0, padx=10, pady=3, sticky="nsew")
        self.option_region.set("Region")

        self.option_lift_csv = ctk.CTkOptionMenu(self, command=self.quand_lift_csv, values=["Choisir une region"])
        self.option_lift_csv.grid(row=4, column=0, padx=10, pady=3, sticky="nsew")
        self.option_lift_csv.set("Remontee")
    
    def quand_choix_perso(self) :
        print("options menu personnalisee")
        if self.option_region and self.option_pays and self.option_lift_csv :
            self.option_pays.destroy()
            self.option_region.destroy()
            self.option_lift_csv.destroy()
            self.option_lift_csv, self.option_pays, self.option_region = None, None, None

        self.chairlifts_cree = self.master.master.get_chairlifts()
        noms_chairlifts_cree = [lift.nom for lift in self.chairlifts_cree]
        noms_chairlifts_cree.sort()
        self.option_lift_perso = ctk.CTkOptionMenu(self, command=self.quand_lift_perso, values=["Aucune remontee cree"] if not self.chairlifts_cree else noms_chairlifts_cree)
        self.option_lift_perso.grid(row=2, column=0, padx=10, pady=3, sticky="nsew")
        self.option_lift_perso.set("Remontee cree") 

    def quand_lift_perso(self, choix) :
        if choix != "Remontee Perso" and choix != "Aucune remontee cree" :
            self.choix_lift_cree = choix
            print("lift cree choisi : ", self.choix_lift_cree)
            self.chairlift = self.trouver_lift_cree()
            self.est_choisi = True
            

    def trouver_lift_cree(self) :
        for lift in self.chairlifts_cree :
            if lift.nom == self.choix_lift_cree :
                print("Lift trouvee : ", lift.nom)
                return lift
            else : 
                continue


class AfficherSelection(ctk.CTkFrame) :

    def __init__(self, parent, chairlift, indice) :
        super().__init__(parent, fg_color="transparent")

        self.chairlift = chairlift
        self.indice = indice

        self.creer_widgets()

    def creer_widgets(self) :
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

        self.label_capacite = ctk.CTkLabel(self, text=f"\u2192 Capacité : {self.get_capacite()} personnes par heure", text_color=COULEURS[self.indice], font=("Arial", 15))
        self.label_capacite.grid(row=5, column=0)

    def get_capacite(self) :
        return self.chairlift.calculerNombreDePersonnesParHeure()

    def get_list_donnee(self) :
        return [self.chairlift.obtenirVitesse(), self.chairlift.obtenirNombreDePersonnesParChaise(), self.chairlift.obtenirLongueurDuTrajet(), self.chairlift.calculerTempsTrajet(), self.get_capacite()]


COULEURS = ["red", "blue", "green", "yellow"]

COLONNES = ["Vitesse", "Taille chaise", "Longueur câble", "Temps trajet", "Capacité"]
BORNES = dict(zip(COLONNES, [[1,10], [1, 10], [1, 9000], [1, 1500], [1, 3500]])) #Trouvé avec les maximums du csv et en faisant des tests de création

class GraphCompare(ctk.CTkFrame) :
    def __init__(self, parent, df, noms) :
        super().__init__(parent, fg_color="transparent")
        self.df_donnee = df
        self.noms = noms

        self.categories = list(self.df_donnee)
        self.normalisee = self.normaliser_donnees()

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

        self.creer_graphe_bar()
        self.creer_graphe_etoile()

    def creer_graphe_bar(self) :
        figure = Figure(figsize=(7, 5), layout="constrained")
        
        canvas = FigureCanvasTkAgg(figure, master=self.tabs_graphs.tab("1 - Barres"))
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        graph = figure.add_subplot(111)

        complet = graph.grouped_bar(self.normalisee, group_spacing=1, tick_labels=self.noms, labels=COLONNES)
        graph.legend()
        for conteneur in complet.bar_containers:
            graph.bar_label(conteneur, padding=3, fmt="%.2f")
        
        graph.set_ylim(0, 10)


    def creer_graphe_etoile(self) :

        N = len(self.categories)

        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]

        figure = Figure(figsize=(7, 5), layout="constrained")
        
        canvas = FigureCanvasTkAgg(figure, master=self.tabs_graphs.tab("2 - Radar"))
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        graph = figure.add_subplot(111, polar=True)
        graph.set_theta_offset(pi / 2)
        graph.set_theta_direction(-1)

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
        resultat = pd.DataFrame()
        for colonne in self.df_donnee.columns :
            series_x = self.df_donnee.loc[:, colonne]
            resultat[colonne] = normaliser_x(series_x, BORNES[colonne][0], BORNES[colonne][1])
        return resultat


def normaliser_x(x, min, max) :
    #Formule : (x-xmin)/(xmax-xmin) *10 -> c'est donc sur un total de 10
        return ((x-min)/(max-min)*10).clip(lower=0, upper=10)


class PageComparer(ctk.CTkFrame) :

    def __init__(self, parent) :

        super().__init__(parent, fg_color="transparent")

        self.df_csv = pd.DataFrame()

        self.nb_observer = self.master.nb_lift

        self.choix = []
        self.affichage_choix = []

        self.est_donnee_importee = False

        self.creer_widgets()

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=3)

        for i in range(self.nb_observer) :
            self.grid_rowconfigure(i, weight=1)
        self.grid_rowconfigure(self.nb_observer+1, weight=0)

    
    def creer_widgets(self) :
        self.frame_choix = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_choix.grid(row=0, column=0, rowspan=self.nb_observer, padx=20, pady=10, sticky="nsew")
        #Bouton importer 
        frame_coin_gauche = ctk.CTkFrame(self.frame_choix, fg_color="transparent")
        frame_coin_gauche.grid(row=0, column= 0, sticky="nsew")

        image_accueil = ctk.CTkImage(light_image=Image.open("maison.png"), size=(17,17))
        self.bouton_accueil = ctk.CTkButton(frame_coin_gauche, image=image_accueil, text="", fg_color="transparent", hover=False, command=self.quand_accueil, width=30, height=30,)
        self.bouton_accueil.grid(row=0, column=0, sticky="w", pady=5, padx=(10,5))

        self.bouton_donnee = ctk.CTkButton(frame_coin_gauche, text="Choisir base donnée", command=self.quand_importer)
        self.bouton_donnee.grid(row=0, column=1, sticky="ew", pady=5, padx=(5,10))

        for i in range(self.nb_observer) :
            self.choix.append(SelectionLift(self.frame_choix, self.df_csv))
            self.choix[i].grid(row=2*(i+1), column=0, sticky="nsew")

        for i in range(self.nb_observer) :
            label_lift = ctk.CTkLabel(self.frame_choix, text= f"Choix #{i+1}", font=("Arial", 15, "bold"), text_color=COULEURS[i])
            label_lift.grid(row=(2*i)+1, column=0, sticky="nsew")

        self.bouton_comparer = ctk.CTkButton(self.frame_choix, text="Comparer", command=self.quand_comparer)
        self.bouton_comparer.grid(row=2*self.nb_observer+1, column=0, sticky="ns", pady=(15,3), padx=10)

    def quand_accueil(self) :
        self.master.changer_page(Accueil)

    def quand_comparer(self) :
        
        if self.pret_a_comparer() :

            self.detruire_affichages()

            noms = []
            for i in range(self.nb_observer) :
                self.affichage_choix.append(AfficherSelection(self, self.choix[i].chairlift, i))
                self.affichage_choix[i].grid(row=i, column=1, sticky="nsew", padx=20, pady=10)
                noms.append(self.affichage_choix[i].chairlift.nom)

            self.graph = GraphCompare(self, self.creer_df_donnee(), noms)
            self.graph.grid(row=0, column=2, rowspan=self.nb_observer, sticky="nsew")

            self.bouton_exporter = ctk.CTkButton(self, text="Exporter le DataFrame", command=self.quand_exporter)
            self.bouton_exporter.grid(row=self.nb_observer+1, column=0, sticky="ns", pady=(10,15), padx=10)
      
        else : 
            messagebox.showerror("Erreur ", f"Choisir au moins {self.nb_observer} remontées pour les comparer")

    def creer_df_donnee(self) :
        listes = []
        for i in range(self.nb_observer) :
            listes.append(self.affichage_choix[i].get_list_donnee())

        return pd.DataFrame(listes, columns=COLONNES)

    def quand_exporter(self) :
        chemin_exporter = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Fichiers CSV", "*.csv")])
        
        try :
            df_exporter = self.creer_df_donnee()
            print(df_exporter)
            df_exporter.to_csv(chemin_exporter, index=False)
            messagebox.showinfo(title="Reussite", message=f"Fichier a été exporté à : {chemin_exporter}")
        except Exception as erreur:
            messagebox.showerror("Erreur d'exportation", f"Erreur inattendue : {erreur}")

    def quand_importer(self) :
        self.chemin_importer = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("Fichiers CSV", "*.csv")])
        if self.chemin_importer:
            try :
                self.importer()
                if self.est_donnee_importee :
                    messagebox.showinfo(title="Réussite", message=f"Le fichier suivant a bien été importé :\n {self.chemin_importer} \nCertaines données peuvent avoir été supprimées pour le bon fonctionnement du comparateur")
                    for choix in self.choix:
                        choix.radio_button_csv.configure(state="normal")
                        choix.df = self.df_csv

            except (OSError, ValueError, KeyError) as erreur:
                messagebox.showerror("Erreur dans l'import", erreur)
                print("Chargement impossible ", erreur)


    def importer(self) :
        
        try :
            self.df_csv = pd.read_csv(self.chemin_importer)
            
            self.df_csv = self.df_csv.drop_duplicates()

            self.df_csv = self.df_csv.loc[:,["name", "countries", "regions", "duration_sec", "capacity", "speed_m_per_s","occupancy", "inclined_length_m"]]

            self.df_csv = self.df_csv.dropna()

            #Retirer les lifts qui ont le même nom aux mêmes endroits 
            self.df_csv = self.df_csv.drop_duplicates(subset=["countries", "regions", "name"])

            #Trier pour que les vitesse aient du sens
            condition_vitesse = (self.df_csv["speed_m_per_s"] >= 1.0) & (self.df_csv["speed_m_per_s"] <= 10.0)
            self.df_csv = self.df_csv[condition_vitesse]

            #Trier pour que la longueur du cable ait du sens
            condition_longueur = (self.df_csv["inclined_length_m"] >= 1.0) & (self.df_csv["inclined_length_m"] <= 10000.0)
            self.df_csv = self.df_csv[condition_longueur]

            #Enlever les instances de deux pays differents et pareil pour region et names (ex : Alberta; Manitoba. pour le meme lift)
            condition_2_pays = self.df_csv["countries"].str.contains(";") | self.df_csv["countries"].str.contains(",")
            self.df_csv = self.df_csv[~condition_2_pays]

            condition_2_regions = self.df_csv["regions"].str.contains(";") | self.df_csv["regions"].str.contains(",")
            self.df_csv = self.df_csv[~condition_2_regions]

            condition_2_noms = self.df_csv["name"].str.contains(";") | self.df_csv["name"].str.contains(",")
            self.df_csv = self.df_csv[~condition_2_noms]

            #Enlever les faux noms de chairlifts 
            condition_nom_court = self.df_csv["name"].str.len() > 3
            self.df_csv = self.df_csv[condition_nom_court]

            condition_occupancy = (self.df_csv["occupancy"] >= 2) & (self.df_csv["occupancy"] <= 10)
            self.df_csv = self.df_csv[condition_occupancy]

            self.est_donnee_importee = True

        except Exception as erreur :  
            messagebox.showerror("Erreur dans le fichier choisi ", f"Assurez vous d'avoir les bonnes colonnes de OpenSkiData : {erreur}")

        self.df_csv = self.df_csv.reset_index(drop=True)

    def pret_a_comparer(self) :
        for i in range(self.nb_observer):
            if not self.choix[i].est_choisi:
                return False

        return True

    def detruire_affichages(self) :
        if len(self.affichage_choix) > 0 :
            for i in range(self.nb_observer) :
                if self.affichage_choix[i] :
                    self.affichage_choix[i].destroy()
                else :
                    continue
            self.affichage_choix = []

#TODO virgule au debut du truc d'export