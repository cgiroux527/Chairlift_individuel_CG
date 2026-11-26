import customtkinter as ctk

from PIL import Image

from tkinter import messagebox

NOMBRES_LIFTS = ["2","3"]

class Accueil(ctk.CTkFrame) :

    def __init__(self, parent) :
        self.parent = parent
        super().__init__(parent, fg_color="transparent")

        ctk.CTkButton(self, text="Créateur de remontée",  font=("Arial", 21), command=parent.afficher_createur, height=40, width= 300).grid(column=0, row=2, padx=20, pady=20)

        ctk.CTkLabel(self, text="ELEVATE", font=("Arial", 60, "bold")).grid(row=0, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")

        img_lift = ctk.CTkImage(light_image=Image.open("skilift.png"), size=(400,400))
        label_img_lift = ctk.CTkLabel(self, image=img_lift, text="")
        label_img_lift.grid(row=1, column=0, padx=20, pady=20, columnspan=3, sticky="nsew")

        frame_comparer = ctk.CTkFrame(self, fg_color="transparent")
        frame_comparer.grid(row=2, column=2, padx=20, pady=20)
        ctk.CTkButton(frame_comparer, text="Comparateur de remontées", font=("Arial", 21), command=self.quand_comparer, height=40, width= 300).grid(column=0, row=0, padx=(10,2))
        self.nb_est_choisi = False
        option_nb_lift = ctk.CTkOptionMenu(frame_comparer, values=NOMBRES_LIFTS, command=self.quand_option_nb, height=40, width=65)
        option_nb_lift.set("2")
        option_nb_lift.grid(row=0, column=1, padx=(2,10))
        self.nb_lift = 2

        for i in range(3) :
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)

    def quand_option_nb(self, choix) :
        nb = int(choix)
        if nb >=2 and nb <= 4 :
            self.nb_lift = int(choix)
        else :
            messagebox.showerror(title="Erreur", message="Valeur invalide")

    def get_nb_lift(self) :
        nb_str = [int(n) for n in NOMBRES_LIFTS]
        if self.nb_lift >= min(nb_str) and self.nb_lift <= max(nb_str) :
            return self.nb_lift
        else : 
            return 2

    def quand_comparer(self) :
            self.parent.afficher_comparer()


