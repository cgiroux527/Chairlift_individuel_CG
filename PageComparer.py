from tkinter import filedialog, messagebox, IntVar

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import customtkinter as ctk
import pandas as pd

from Chairlift import Chairlift
from Accueil import Accueil

from math import pi

from PIL import Image

#Différentes constantes pour combler un manque dans le CSV de OpenSkiData
TEMPS_EMBARQUEMENTS_CSV = {2: 3.0, 3: 3.2, 4: 3.6, 5:4.0, 6: 4.0, 7:4.2, 8: 4.5, 9:5.0, 10: 5.0} #Calcul approximatif basé sur moyennes pour pouvoir utiliser la classe Chairlift (Temps d'embarquement). source : https://www.strmtg.developpement-durable.gouv.fr/en/chairlift-continuous-movement-unidirectional-a131.html?lang=en
DIST_ENTRE_CHAISES_CSV = 20

"""Classe qui gère la sélection d'une seule remontée"""
class SelectionLift(ctk.CTkFrame) :

    def __init__(self, parent, df) :

        super().__init__(parent, fg_color="transparent")

        #Initialisation de l'instance de Chairlift utilisée pour les calculs
        self.chairlift = Chairlift()

        #Initialisation des attributs aux valeurs de bases
        self.radio_var = IntVar(value=0)
        self.df = df

        self.choix_pays, self.choix_region = "", ""
        self.option_lift_perso, self.option_lift_csv, self.option_pays, self.option_region = None, None, None, None

        self.est_choisi = False

        #Appeler la création des widgets qui sont là dès le début
        self.creer_widgets()


    def creer_widgets(self) :
        #Création des radiobuttons pour décider où prendre la remontée à comparer
        self.radio_button_csv = ctk.CTkRadioButton(self, text="Depuis le CSV importé", command=self.quand_choix_csv, variable=self.radio_var, value=1, state="disabled", radiobutton_height=15, radiobutton_width=15)
        self.radio_button_csv.grid(row=0, column=0, padx=10, pady=3, sticky="nsew")
        
        radio_choix_perso = ctk.CTkRadioButton(self, text="Chairlift personnalisé", command=self.quand_choix_perso, variable=self.radio_var, value=2, radiobutton_height=15, radiobutton_width=15)
        radio_choix_perso.grid(row=1, column=0, padx=10, pady=3, sticky="nsew")


    def quand_choix_csv(self) :
        #Si il y avait des OptionMenu provenant du créateur, les détruire
        if self.option_lift_perso :
            self.option_lift_perso.destroy()
            self.option_lift_perso = None

        #Création des 3 OptionMenu, initialiser les pays et en mettre aucun dans les 2 autres. 
        self.option_pays = ctk.CTkOptionMenu(self, command=self.quand_pays, values=self.df["countries"].sort_values().unique().tolist())
        self.option_pays.grid(row=2, column=0, padx=10, pady=(2,3), sticky="nsew")
        self.option_pays.set("Pays")

        self.option_region = ctk.CTkOptionMenu(self, command=self.quand_region, values=["Choisir un pays"])
        self.option_region.grid(row=3, column=0, padx=10, pady=3, sticky="nsew")
        self.option_region.set("Region")

        self.option_lift_csv = ctk.CTkOptionMenu(self, command=self.quand_lift_csv, values=["Choisir une region"])
        self.option_lift_csv.grid(row=4, column=0, padx=10, pady=3, sticky="nsew")
        self.option_lift_csv.set("Remontee")
        

    def quand_pays(self, choix) :
        #Si le choix n'est pas la valeur de base du OptionMenu
        if choix != "Pays" :
            #Initialiser l'attribut du choix du pays pour filtrer la suite
            self.choix_pays = choix
            print("pays choisi : ", choix)

            #Ramener les autres optionMenu à leur base, car nous revenons au choix du pays, alors les autres ne sont pas choisis 
            self.choix_region = ""
            self.choix_lift_csv = ""
            self.option_region.configure(values=["Choisir un pays"])
            self.option_region.set("Region")
            self.option_lift_csv.configure(values=["Choisir une region"])
            self.option_lift_csv.set("Remontee")
            #Filtrer et ajouter les bonnes valeurs
            self.option_region.configure(values=self.df.loc[self.df["countries"] == self.choix_pays, "regions"].sort_values().unique().tolist())

            #S'assurer que le booléen est bien Faux pour ne pas comparer encore
            self.est_choisi = False


    def quand_region(self, choix) :
        #S'assurer que le choix est bien valide
        if choix != "Region" and choix != "Choisir un pays" :
            #La suite suit la même logique que "self.quand_pays"
            self.choix_region = choix
            print("region choisi : ", choix)

            self.choix_lift_csv = ""
            self.option_lift_csv.configure(values=["Choisir une region"])
            self.option_lift_csv.set("Remontee")

            self.option_lift_csv.configure(values=self.df.loc[self.df["regions"] == self.choix_region, "name"].sort_values().unique().tolist())

            self.est_choisi = False

            
    def quand_lift_csv(self, choix) :
        if choix != "Remontee" and choix != "Choisir une region":
            self.choix_lift_csv = choix
            print("lift du csv choisi : ", choix)

            #Retrouver avec Pandas le lift choisi dans l'importation
            condition_nom_lift = (self.df["name"] == self.choix_lift_csv) & (self.df["countries"] == self.choix_pays) & (self.df["regions"] == self.choix_region)
            self.df_lift_choisi = self.df[condition_nom_lift]
            print("lift du csv choisi : ", self.df_lift_choisi)

            #Modifier le nom de l'instance Chairlift
            self.chairlift.nom = self.choix_lift_csv

            #Trouver la longueur du câble et le nomnre de personnes par chaise 
            longueur = int(self.df_lift_choisi.loc[:,"inclined_length_m"].item())
            personnes_par_chaise = int(self.df_lift_choisi.loc[:,"occupancy"].item())

            #Définir le reste des paramètres de l'instance du Chairlift avec ceux dans le CSV
            self.chairlift.definirVitesse(float(self.df_lift_choisi.loc[:,"speed_m_per_s"].item()))
            self.chairlift.definirNombreDePersonnesParChaise(personnes_par_chaise)
            self.chairlift.definirLongueurDuTrajet(longueur)


            
            #Définir les paramètres à partir de constantes moyennes, car ce sont des paramètres non fournis dans le CSV de OpenSkiData
            self.chairlift.definirTempsDebarquement(TEMPS_EMBARQUEMENTS_CSV[personnes_par_chaise])
            self.chairlift.definirTempsEmbarquement(TEMPS_EMBARQUEMENTS_CSV[personnes_par_chaise])
            
            self.chairlift.definirNombreDeChaise(longueur/DIST_ENTRE_CHAISES_CSV)

            #La remontée est maintenant bien choisi, alors nous pouvons comparer
            self.est_choisi = True

    
    def quand_choix_perso(self) :
        print("options menu personnalisee")
        #Réinitialiser et détruire les anciennes instances pour les options provenant du CSV
        if self.option_region and self.option_pays and self.option_lift_csv :
            self.option_pays.destroy()
            self.option_region.destroy()
            self.option_lift_csv.destroy()
            self.option_lift_csv, self.option_pays, self.option_region = None, None, None

        #Récupérer à l'extérieur des plusieurs frames Parentes (j'usqu'à MainApp) la liste des remontées créées
        self.chairlifts_cree = self.master.master.master.get_chairlifts()
        noms_chairlifts_cree = [lift.nom for lift in self.chairlifts_cree]
        noms_chairlifts_cree.sort()

        #Créer et initialiser l'option Menu des remontées créées avec le créateur 
        self.option_lift_perso = ctk.CTkOptionMenu(self, command=self.quand_lift_perso, values=["Aucune remontee cree"] if not self.chairlifts_cree else noms_chairlifts_cree)
        self.option_lift_perso.grid(row=2, column=0, padx=10, pady=3, sticky="nsew")
        self.option_lift_perso.set("Remontee cree") 

    def quand_lift_perso(self, choix) :
        #Vérifier le choix provenant du créateur 
        if choix != "Remontee Perso" and choix != "Aucune remontee cree" :
            self.choix_lift_cree = choix
            print("lift cree choisi : ", self.choix_lift_cree)
            #Appeler la méthode qui trouve la bonne remontée dans la liste de celles créées
            self.chairlift = self.trouver_lift_cree()
            #La remontée est maintenant choisie
            self.est_choisi = True
            

    def trouver_lift_cree(self) :
        for lift in self.chairlifts_cree :
            #Retourner l'instance de Chairlift lorsque leurs noms correspondent
            if lift.nom == self.choix_lift_cree :
                print("Lift trouvee : ", lift.nom)
                return lift
            else : 
                continue

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
        resultat = pd.DataFrame()
        #Pour toutes les données du df de base, on ajoute les series normalisées à un nouveau DataFrame (resultat)
        for colonne in self.df_donnee.columns :
            series_x = self.df_donnee.loc[:, colonne]
            resultat[colonne] = normaliser_x(series_x, BORNES[colonne][0], BORNES[colonne][1])
        return resultat

#Fonction hors de la classe qui permet de normaliser une serie (x) avec le minimum et le maximum voulu
def normaliser_x(x, min, max) :
    #Formule : (x-xmin)/(xmax-xmin) *10 -> c'est donc sur un total de 10
        return ((x-min)/(max-min)*10).clip(lower=0, upper=10)

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


