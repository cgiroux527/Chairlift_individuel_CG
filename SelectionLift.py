import customtkinter as ctk
from tkinter import IntVar

from Chairlift import Chairlift

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
