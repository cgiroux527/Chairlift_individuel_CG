import customtkinter as ctk

class Accueil(ctk.CTkFrame) :

    def __init__(self, parent) :
        super().__init__(parent)

        ctk.CTkButton(self, text="Test creation", command=parent.afficher_createur).grid(column=1, row=1)
        ctk.CTkButton(self, text="Test compare", command=parent.afficher_comparer).grid(column=1, row=2)
