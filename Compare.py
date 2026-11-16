from tkinter import filedialog, messagebox, IntVar

import customtkinter as ctk
import pandas as pd

from Chairlift import Chairlift

NOMBRE_LIFTS = 2

class Compare(ctk.CTkFrame) :

    def __init__(self, parent, df) :

        super().__init__(parent)

        self.chairlift = Chairlift()

        self.radio_var = IntVar(value=0)
        self.df = df

        self.choix_pays, self.choix_region = "", ""
        self.option_lift_perso, self.option_lift_csv, self.option_pays, self.option_region = None, None, None, None

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

            

    def quand_lift_csv(self, choix) :
        if choix != "Remontee" and choix != "Choisir une region":
            self.choix_lift_csv = choix
            print("lift du csv choisi : ", choix)

            #TODO ajouter que c'est le chairlift choisi! pour cette instance de COMPARE

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

        chairlifts_cree = self.master.master.get_chairlifts()
        noms_chairlifts_cree = [lift.nom for lift in chairlifts_cree]
        self.option_lift_perso = ctk.CTkOptionMenu(self, command=self.quand_lift_perso, values=["Aucune remontee cree"] if not chairlifts_cree else noms_chairlifts_cree)
        self.option_lift_perso.grid(row=2, column=0)
        self.option_lift_perso.set("Remontee cree") 

    def quand_lift_perso(self, choix) :
        if choix != "Remontee Perso" and choix != "Aucune remontee cree" :
            self.choix_lift_csv = choix
            print("lift du createur choisi : ", choix)
        
            #TODO ajouter que c'est le chairlift choisi! pour cette instance de COMPARE


        
class CompareWindow(ctk.CTkFrame) :

    def __init__(self, parent) :

        super().__init__(parent)

        self.df_csv = pd.DataFrame()

        self.choix = []
        for i in range(NOMBRE_LIFTS) :
            self.choix.append(Compare(self, self.df_csv))
            self.choix[i].grid(row=2*(i+1), column=0)

        self.est_donnee_importee = False

        self.creer_widgets()

    
    def creer_widgets(self) :
        #Bouton importer 
        self.bouton_donnee = ctk.CTkButton(self, text="Choisir base donnée", command=self.quand_importer)
        self.bouton_donnee.grid(row=0, column=0)

        for i in range(NOMBRE_LIFTS) :
            label_lift = ctk.CTkLabel(self, text= f"Chairlift #{i+1}", font=("Arial", 20, "bold"))
            label_lift.grid(row=2*i+1, column=0)

    
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
                messagebox.showerror("Erreur dans l'import : ", erreur)
                print("Chargement impossible ", erreur)


    def importer(self) :
        self.df_csv = pd.read_csv(self.chemin)

        self.df_csv = self.df_csv.drop_duplicates()
        try :
            self.df_csv = self.df_csv.loc[:,["name", "countries", "regions", "ski_area_names", "duration_sec", "capacity", "speed_m_per_s","occupancy","lift_type", "inclined_length_m", "vertical_m"]]

            self.df_csv = self.df_csv.dropna()

            condition_vitesse = (self.df_csv["speed_m_per_s"] >= 1.0) & (self.df_csv["speed_m_per_s"] <= 10.0)
            self.df_csv = self.df_csv[condition_vitesse]

            #Enlever les instances de deux pays differents et pareil pour region et names (ex : Alberta; Manitoba. pour le meme lift)
            condition_2_pays = self.df_csv["countries"].str.contains(";") | self.df_csv["countries"].str.contains(",")
            self.df_csv = self.df_csv[~condition_2_pays]

            condition_2_regions = self.df_csv["regions"].str.contains(";") | self.df_csv["regions"].str.contains(",")
            self.df_csv = self.df_csv[~condition_2_regions]

            condition_2_noms = self.df_csv["name"].str.contains(";") | self.df_csv["name"].str.contains(",")
            self.df_csv = self.df_csv[~condition_2_noms]

            self.est_donnee_importee = True

        except Exception as erreur :  
            messagebox.showerror("Erreur dans le fichier choisi ", f"Assurez vous d'avoir les bonnes colonnes de OpenSkiData : {erreur}")

        self.df_csv = self.df_csv.reset_index(drop=True)
