from tkinter import filedialog, messagebox, IntVar

import customtkinter as ctk
import pandas as pd

from Chairlift import Chairlift


NOMBRE_ROWS_PAR_LIFT = 6
NOMBRE_COMPARER = 2


class Compare(ctk.CTkFrame) :

    def __init__(self, parent) :

        super().__init__(parent)

        self.chairlift_1 = Chairlift()
        self.chairlift_2 = Chairlift()

        self.est_donnee_importee = False
        self.radio_vars = [IntVar(value=0), IntVar(value=0)]

        self.radio_buttons_csv = []
        self.frames_lift = []

        self.creer_widgets()


    def creer_widgets(self) :

        self.creer_choix_lift(1) 
        self.creer_choix_lift(2)

        #Bouton importer 
        self.bouton_donnee = ctk.CTkButton(self, text="Choisir base donnée", command=self.quand_importer)
        self.bouton_donnee.grid(row=0, column=0)
        

    def creer_choix_lift(self, numero) :
        #Creer une frame pour chacun
        self.frames_lift.append(ctk.CTkFrame(self))
        self.frames_lift[numero-1].grid(row=numero, column=0)

        #Mettre les widgets dans la frame
        label_lift = ctk.CTkLabel(self.frames_lift[numero-1], text= f"Chairlift #{numero}", font=("Arial", 20, "bold"))
        label_lift.grid(row=0, column=0)

        self.radio_buttons_csv.append(ctk.CTkRadioButton(self.frames_lift[numero-1], text="Depuis le CSV importé", command=lambda :self.quand_choix_csv(numero), variable=self.radio_vars[numero-1], value=numero, state="disabled"))
        self.radio_buttons_csv[numero-1].grid(row=1, column=0)

        radio_choix_perso = ctk.CTkRadioButton(self.frames_lift[numero-1], text="Chairlift personnalisé", command=lambda :self.quand_choix_perso(numero), variable=self.radio_vars[numero-1], value=numero+1)
        radio_choix_perso.grid(row=2, column=0)

        

        
    def changer_etat_csv(self) :
        for i in range(NOMBRE_COMPARER) :
            self.radio_buttons_csv[i].configure(state="normal" if self.est_donnee_importee else "disabled")

    def quand_pays(self, choice) :
        if choice != "Pays" :
            self.choix_pays = choice
            print("pays choisi : ", choice)

    def quand_region(self, choice) :
        if choice != "Region" :
            self.choix_region = choice
            print("region choisi : ", choice)

    def quand_choix_csv(self, numero) :
        print("options menu csv")

        option_pays = ctk.CTkOptionMenu(self.frames_lift[numero-1], command=self.quand_pays, values=self.df_import["countries"].unique().tolist())
        option_pays.grid(row=3, column=0)
        option_pays.set("Pays")

        option_region = ctk.CTkOptionMenu(self.frames_lift[numero-1], command=self.quand_region, values=self.df_import.loc[self.df_import["countries"] == self.choix_pays, "regions"].unique().tolist())
        option_region.grid(row=4, column=0)
        option_region.set("Region")
        #TODO utiliser radio var pour savoir lequel doit etre disabled
        #les options menu du csv avec pandas
            #choix pays
                #choix region 
                    #choix lift
    
    def quand_choix_perso(self, numero) :
        print("options menu personnalisee")
        #Les options menu avec chairlift personnalisee
            #choix lift 

    def quand_importer(self) :
        self.chemin = filedialog.askopenfilename(defaultextension=".csv",
        filetypes=[("Fichiers CSV", "*.csv")])
        if self.chemin:
            try :
                self.importer()
                self.est_donnee_importee = True
                self.changer_etat_csv()

            except (OSError, ValueError, KeyError) as erreur:
                messagebox.showerror("Erreur dans l'import : ", erreur)
                print("Chargement impossible ", erreur)


    def importer(self) :
        self.df_import = pd.read_csv(self.chemin)

        self.df_import = self.df_import.drop_duplicates()
        try :
            self.df_import = self.df_import.loc[:,["name", "countries", "regions", "ski_area_names", "duration_sec", "capacity", "speed_m_per_s","occupancy","lift_type", "inclined_length_m", "vertical_m"]]

            self.df_import = self.df_import.dropna()

            condition_vitesse = (self.df_import["speed_m_per_s"] >= 1.0) & (self.df_import["speed_m_per_s"] <= 10.0)
            self.df_import = self.df_import[condition_vitesse]

        except Exception as erreur :  
            messagebox.showerror("Erreur dans le fichier choisi ", f"Assurez vous d'avoir les bonnes colonnes de OpenSkiData : {erreur}")

        self.df_import = self.df_import.reset_index(drop=True)

        