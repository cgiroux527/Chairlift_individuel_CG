from tkinter import filedialog, messagebox, IntVar

import customtkinter as ctk
import pandas as pd

from Chairlift import Chairlift


class Compare(ctk.CTkFrame) :

    def __init__(self, parent) :

        super().__init__(parent)

        self.chairlift = Chairlift()

        self.radio_var = IntVar(value=0)

        self.creer_widgets()


    def creer_widgets(self) :

        

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

    

        
class CompareWindow(ctk.CTkFrame) :

    def __init__(self, parent) :

        super().__init__(parent)

        self.choix1 = Compare(self)
        self.choix1.grid(row=0, column=0)

        self.choix2 = Compare(self)
        self.choix2.grid(row=1, column=0)

        self.est_donnee_importee = False

        def quand_importer(self) :
            self.chemin = filedialog.askopenfilename(defaultextension=".csv",
            filetypes=[("Fichiers CSV", "*.csv")])
            if self.chemin:
                try :
                    df_lecture = pd.read_csv(self.chemin)
                    self.importer(df_lecture)
                    self.est_donnee_importee = True
    
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