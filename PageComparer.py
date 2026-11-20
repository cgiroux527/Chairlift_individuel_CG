from tkinter import filedialog, messagebox, IntVar, Frame

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import customtkinter as ctk
import pandas as pd

from Chairlift import Chairlift

from math import pi

NOMBRE_LIFTS = 2

TEMPS_EMBARQUEMENTS_CSV = {2: 3.0, 3: 3.2, 4: 3.6, 5:4.0, 6: 4.0, 7:4.2, 8: 4.5, 9:5.0, 10: 5.0} #Calcul approximatif basé sur moyennes pour pouvoir utiliser la classe Chairlift (Temps d'embarquement). source : https://www.strmtg.developpement-durable.gouv.fr/en/chairlift-continuous-movement-unidirectional-a131.html?lang=en
DIST_ENTRE_CHAISES_CSV = 20

#TODO 216

class SelectionLift(ctk.CTkFrame) :

    def __init__(self, parent, df) :

        super().__init__(parent)

        self.chairlift = Chairlift()

        self.radio_var = IntVar(value=0)
        self.df = df

        self.choix_pays, self.choix_region = "", ""
        self.option_lift_perso, self.option_lift_csv, self.option_pays, self.option_region = None, None, None, None

        self.est_choisi = False

        self.creer_widgets()


    def creer_widgets(self) :
        
        self.radio_button_csv = ctk.CTkRadioButton(self, text="Depuis le CSV importé", command=self.quand_choix_csv, variable=self.radio_var, value=1, state="disabled")
        self.radio_button_csv.grid(row=0, column=0)
        
        radio_choix_perso = ctk.CTkRadioButton(self, text="Chairlift personnalisé", command=self.quand_choix_perso, variable=self.radio_var, value=2)
        radio_choix_perso.grid(row=1, column=0)


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
            self.option_region.configure(values=self.df.loc[self.df["countries"] == self.choix_pays, "regions"].unique().tolist())

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
            self.option_lift_csv.configure(values=self.df.loc[self.df["regions"] == self.choix_region, "name"].unique().tolist())

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

        self.option_pays = ctk.CTkOptionMenu(self, command=self.quand_pays, values=self.df["countries"].unique().tolist())
        self.option_pays.grid(row=2, column=0)
        self.option_pays.set("Pays")

        self.option_region = ctk.CTkOptionMenu(self, command=self.quand_region, values=["Choisir un pays"])
        self.option_region.grid(row=3, column=0)
        self.option_region.set("Region")

        self.option_lift_csv = ctk.CTkOptionMenu(self, command=self.quand_lift_csv, values=["Choisir une region"])
        self.option_lift_csv.grid(row=4, column=0)
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
        self.option_lift_perso = ctk.CTkOptionMenu(self, command=self.quand_lift_perso, values=["Aucune remontee cree"] if not self.chairlifts_cree else noms_chairlifts_cree)
        self.option_lift_perso.grid(row=2, column=0)
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

    def __init__(self, parent, chairlift) :
        super().__init__(parent)

        self.chairlift = chairlift

        self.creer_widgets()

    def creer_widgets(self) :
        self.label_nom = ctk.CTkLabel(self, text=self.chairlift.nom, font=("Arial", 20, "bold"), text_color="#4a7ff7",)
        self.label_nom.grid(row=0, column=0)

        self.label_vitesse = ctk.CTkLabel(self, text=f"\u00B7 Vitesse : {self.chairlift.obtenirVitesse()} m/s", text_color="#c8d1d9")
        self.label_vitesse.grid(row=1, column=0)

        self.label_personne_chaise = ctk.CTkLabel(self, text=f"\u00B7 {self.chairlift.obtenirNombreDePersonnesParChaise()} personnes par chaise", text_color="#c8d1d9")
        self.label_personne_chaise.grid(row=2, column=0)

        self.label_longueur = ctk.CTkLabel(self, text=f"\u00B7 Longueur du câble : {self.chairlift.obtenirLongueurDuTrajet()} m", text_color="#c8d1d9",)
        self.label_longueur.grid(row=3, column=0)

        self.label_temps = ctk.CTkLabel(self, text=f"\u00B7 Temps du trajet : {round(self.chairlift.calculerTempsTrajet(), 1)} s", text_color="#c8d1d9",)
        self.label_temps.grid(row=4, column=0)

    def get_capacite(self) :
        return self.chairlift.calculerNombreDePersonnesParHeure()

    def get_list_donnee(self) :
        #TODO verifications???
        return [self.chairlift.obtenirVitesse(), self.chairlift.obtenirNombreDePersonnesParChaise(), self.chairlift.obtenirLongueurDuTrajet(), self.chairlift.calculerTempsTrajet(), self.get_capacite()]

class GraphEtoile(Frame) :
    def __init__(self, parent, df) :
        super().__init__(parent)
        self.df_donnee = df

        self.categories = list(self.df_donnee)[1:]
        self.N = len(self.categories)

        self.angles = [n / float(self.N) * 2 * pi for n in range(self.N)]
        self.angles += self.angles[:1]

        self.figure = Figure(figsize=(6, 3.5))
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        self.axe = self.figure.add_subplot(111, polar=True)
        self.axe.set_theta_offset(pi / 2)
        self.axe.set_theta_direction(-1)

        self.axe.xticks(self.angles[:-1], self.categories)
        self.axe.set_rlabel_position(0)
        self.axe.yticks([10,20,30], ["10","20","30"], color="grey", size=7)
        self.axe.ylim(0,40)

    
        for i in range(NOMBRE_LIFTS) :
            valeurs = self.df_donnee.loc[i].drop('group').values.flatten().tolist()
            valeurs += valeurs[:1]
            self.axe.plot(self.angles, valeurs, linewidth=1, linestyle='solid', label="NOM")
            self.axe.fill(self.angles, valeurs, 'COULEUR', alpha=0.1)
            #TODO CHANGER POUR BIEN UTILISER LE DF...

        self.axe.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))


COLONNES = ["Vitesse", "Personnes par chaise", "Longueur câble", "Temps trajet", "Capacité"]

class PageComparer(ctk.CTkFrame) :

    def __init__(self, parent) :

        super().__init__(parent)

        self.df_csv = pd.DataFrame()

        self.choix = []
        self.affichage_choix = []
        for i in range(NOMBRE_LIFTS) :
            self.choix.append(SelectionLift(self, self.df_csv))
            self.choix[i].grid(row=2*(i+1), column=0)

        self.est_donnee_importee = False

        self.creer_widgets()

    
    def creer_widgets(self) :
        #Bouton importer 
        self.bouton_donnee = ctk.CTkButton(self, text="Choisir base donnée", command=self.quand_importer)
        self.bouton_donnee.grid(row=0, column=0)

        for i in range(NOMBRE_LIFTS) :
            label_lift = ctk.CTkLabel(self, text= f"Choix #{i+1}", font=("Arial", 15, "bold"))
            label_lift.grid(row=(2*i)+1, column=0)

        self.bouton_comparer = ctk.CTkButton(self, text="Comparer", command=self.quand_comparer)
        self.bouton_comparer.grid(row=2*NOMBRE_LIFTS+1, column=0)

    def quand_comparer(self) :
        
        if self.pret_a_comparer() :

            self.detruire_affichages()

            for i in range(NOMBRE_LIFTS) :
                self.affichage_choix.append(AfficherSelection(self, self.choix[i].chairlift))
                self.affichage_choix[i].grid(row=2*i+2, column=1)

                #TODO afficher la capacité, couleur spéciale pour juste celui le plus grand!!!

            self.graph = GraphEtoile(self, self.creer_df_donnee())
        else : 
            messagebox.showerror("Erreur ", "Choisir au moins 2 remontées pour les comparer")

    def creer_df_donnee(self) :
        
        resultat = pd.DataFrame() #TODO remplir le dataframe avec COLONNES et affichages_choix.get_list_donnee()

        return resultat

    
    def quand_importer(self) :
        self.chemin = filedialog.askopenfilename(defaultextension=".csv",
        filetypes=[("Fichiers CSV", "*.csv")])
        if self.chemin:
            try :
                self.importer()
                if self.est_donnee_importee :
                    for choix in self.choix:
                        choix.radio_button_csv.configure(state="normal")
                        choix.df = self.df_csv

            except (OSError, ValueError, KeyError) as erreur:
                messagebox.showerror("Erreur dans l'import", erreur)
                print("Chargement impossible ", erreur)


    def importer(self) :
        
        try :
            self.df_csv = pd.read_csv(self.chemin)
            
            self.df_csv = self.df_csv.drop_duplicates()

            self.df_csv = self.df_csv.loc[:,["name", "countries", "regions", "ski_area_names", "duration_sec", "capacity", "speed_m_per_s","occupancy","lift_type", "inclined_length_m", "vertical_m"]]

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

            self.est_donnee_importee = True

        except Exception as erreur :  
            messagebox.showerror("Erreur dans le fichier choisi ", f"Assurez vous d'avoir les bonnes colonnes de OpenSkiData : {erreur}")

        self.df_csv = self.df_csv.reset_index(drop=True)

    def pret_a_comparer(self) :
        for i in range(NOMBRE_LIFTS):
            if not self.choix[i].est_choisi:
                return False

        return True

    def detruire_affichages(self) :
        if len(self.affichage_choix) > 0 :
            for i in range(NOMBRE_LIFTS) :
                if self.affichage_choix[i] :
                    self.affichage_choix[i].destroy()
                else :
                    continue
            self.affichage_choix = []




#TODO frayeur de trop de vals dans le csv que je peux pas tester