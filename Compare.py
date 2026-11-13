import customtkinter as ctk
import pandas as pd

from tkinter import filedialog

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
        chemin = filedialog.askopenfilename(defaultextension=".csv",
        filetypes=[("Fichiers CSV", "*.csv")])
        if chemin:
            try :
                df_lecture = pd.read_csv(chemin)
                self.importer(df_lecture)

            except (OSError, ValueError, KeyError) as erreur:
                print("Chargement impossible :", erreur)


    def importer(self, df) :
        print(df.loc[:10, ["duration_sec", "capacity", "speed_m_per_s","occupancy","lift_type", "inclined_length_m", "vertical_m"]])
