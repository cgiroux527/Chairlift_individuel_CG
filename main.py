from Sliders import Sliders
from Chairlift import Chairlift
from GraphControl import GraphControl

import customtkinter as ctk


class MainApp(ctk.CTk) :

    def __init__(self) :
        # Initialiser la fenêtre principale
        super().__init__()
        self.title("ELEVATE - Comparateur de remontée mécanique")
        self.geometry("1200x700")

        self.afficher_menu_principal()

    def detruire_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def afficher_menu_principal(self) :
        #Appeler instance du menu
        
    def afficher_createur(self) :
        #Appeler instance du createur

    def afficher_comparer(self) :
        #Appeler instance du comparateur
    
    def changer_page(self, choix) :
        self.detruire_frame()

        self.page_courante = choix(self)
        self.page_courante.pack(fill="both")

    
#Loop du MainApp et choix de l'apparence du ctk
if __name__ == "__main__" :
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("green")
    application = MainApp()
    application.mainloop()
