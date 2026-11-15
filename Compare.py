from tkinter import filedialog, messagebox, IntVar

import customtkinter as ctk
import pandas as pd

from Chairlift import Chairlift


NOMBRE_ROWS_PAR_LIFT = 5
NOMBRE_COMPARER = 2


class Compare(ctk.CTkFrame) :

    def __init__(self, parent) :

        super().__init__(parent)

        self.chairlift_1 = Chairlift()
        self.chairlift_2 = Chairlift()

        self.est_donnee_importee = False
        self.radio_vars = [IntVar(value=0), IntVar(value=0)]
        self.radio_buttons_csv = []

        self.creer_widgets()


    def creer_widgets(self) :

        self.creer_choix_lift(1) 
        self.creer_choix_lift(2)

        #Bouton importer 
        self.bouton_donnee = ctk.CTkButton(self, text="Choisir base donnée", command=self.quand_importer)
        self.bouton_donnee.grid(row=0, column=0)

    """nombre_lifts = 1
        while nombre_lifts < 3 :
            

            #RADIO BUTTON choix entre csv et personnalisé
            if self.est_donnee_importee :
                self.bouton_donnee.destroy()
                self.radio_choix_csv = ctk.CTkRadioButton(self, text="Depuis le CSV importé", command=self.quand_choix_csv, variable=self.radio_var, value=1)
                self.radio_choix_csv.grid(row=1, column=0)
            else : 
                #Bouton importer 
                self.bouton_donnee = ctk.CTkButton(self, text="Choisir base donnée", command=self.quand_importer)
                self.bouton_donnee.grid(row=1, column=0)

            self.radio_choix_perso = ctk.CTkRadioButton(self, text="Chairlift personnalisé", command=self.quand_choix_perso, variable=self.radio_var, value=2)
            self.radio_choix_perso.grid(row=2, column=0)
            
            nombre_lifts += 1"""
        

    def creer_choix_lift(self, numero) :
        #Creer une frame pour chacun
        frame_lift = ctk.CTkFrame(self)
        frame_lift.grid(row=numero, column=0)

        #Mettre les widgets dans la frame
        label_lift = ctk.CTkLabel(frame_lift, text= f"Chairlift #{numero}", font=("Arial", 20, "bold"))
        label_lift.grid(row=0, column=0)


        self.radio_buttons_csv.append(ctk.CTkRadioButton(frame_lift, text="Depuis le CSV importé", command=self.quand_choix_csv, variable=self.radio_vars[numero-1], value=numero, state="disabled"))
        self.radio_buttons_csv[numero-1].grid(row=1, column=0)
        
    def changer_etat_csv(self) :
        for i in range(NOMBRE_COMPARER) :
            self.radio_buttons_csv[i].configure(state="normal" if self.est_donnee_importee else "disabled")

    def quand_choix_csv(self) :
        print("options menu csv")
        #les options menu du csv avec pandas
            #choix pays
                #choix region 
                    #choix lift
    
    def quand_choix_perso(self) :
        print("options menu personnalisee")
        #Les options menu avec chairlift personnalisee
            #choix lift 

    def quand_importer(self) :
        self.chemin = filedialog.askopenfilename(defaultextension=".csv",
        filetypes=[("Fichiers CSV", "*.csv")])
        if self.chemin:
            try :
                df_lecture = pd.read_csv(self.chemin)
                self.importer(df_lecture)
                self.est_donnee_importee = True
                self.changer_etat_csv()

            except (OSError, ValueError, KeyError) as erreur:
                messagebox.showerror("Erreur dans l'import : ", erreur)
                print("Chargement impossible ", erreur)


    def importer(self, df) :
        df = pd.read_csv(self.chemin)

        df = df.drop_duplicates()
        try :
            df = df.loc[:,["name", "countries", "regions", "ski_area_names", "duration_sec", "capacity", "speed_m_per_s","occupancy","lift_type", "inclined_length_m", "vertical_m"]]

            df = df.dropna()

            condition_vitesse = (df["speed_m_per_s"] >= 1.0) & (df["speed_m_per_s"] <= 10.0)
            df = df[condition_vitesse]
        except Exception as erreur :  
            messagebox.showerror("Erreur dans le fichier choisi ", f"Assurez vous d'avoir les bonnes colonnes de OpenSkiData : {erreur}")

        #TODO FILTRER LE CHOIX

        df = df.reset_index(drop=True)

        


#TODO 
        #self.compare = Compare(self)
        #self.compare.grid(row=3, column=1)