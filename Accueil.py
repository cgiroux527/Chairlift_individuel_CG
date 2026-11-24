import customtkinter as ctk

from PIL import Image

class Accueil(ctk.CTkFrame) :

    def __init__(self, parent) :
        super().__init__(parent, fg_color="transparent")

        ctk.CTkButton(self, text="Créateur de remontée",  font=("Arial", 21), command=parent.afficher_createur, height=40, width= 300).grid(column=0, row=2, padx=20, pady=20)
        ctk.CTkButton(self, text="Comparateur de remontées", font=("Arial", 21), command=parent.afficher_comparer, height=40, width= 300).grid(column=2, row=2, padx=20, pady=20)

        ctk.CTkLabel(self, text="ELEVATE", font=("Arial", 60, "bold")).grid(row=0, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")

        img_lift = ctk.CTkImage(light_image=Image.open("skilift.png"), size=(400,400))
        label_img_lift = ctk.CTkLabel(self, image=img_lift, text="")
        label_img_lift.grid(row=1, column=0, padx=20, pady=20, columnspan=3, sticky="nsew")
        for i in range(3) :
            self.grid_rowconfigure(i, weight=1)
            self.grid_columnconfigure(i, weight=1)
        
