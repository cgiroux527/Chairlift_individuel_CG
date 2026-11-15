import customtkinter as ctk
import pandas as pd

from tkinter import filedialog, messagebox

from Chairlift import Chairlift

class Compare(ctk.CTkFrame) :

    def __init__(self, parent) :

        super().__init__(parent)

        self.chairlift_1 = Chairlift()
        self.chairlift_2 = Chairlift()

        self.creer_widgets()


    def creer_widgets(self) :

        #Bouton importer 
        self.bouton_donnee = ctk.CTkButton(self, text="Choisir base donnée", command=self.quand_importer)
        self.bouton_donnee.grid(row=0, column=0)

        #Radio button pour chairlift 1 

        #Radio buttons pour chairlift 2

    def quand_importer(self) :
        self.chemin = filedialog.askopenfilename(defaultextension=".csv",
        filetypes=[("Fichiers CSV", "*.csv")])
        if self.chemin:
            try :
                df_lecture = pd.read_csv(self.chemin)
                self.importer(df_lecture)

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