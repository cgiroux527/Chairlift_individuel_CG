import customtkinter as ctk

from Accueil import Accueil
from PageComparer import PageComparer
from PageCreation import PageCreation


class MainApp(ctk.CTk) :

    def __init__(self) :
        # Initialiser la fenêtre principale
        super().__init__()
        self.title("ELEVATE - Comparateur de remontée mécanique")
        self.geometry("1200x700")

        self.chairlifts_cree = []

        self.afficher_menu_principal()

    def detruire_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def afficher_menu_principal(self) :
        #Appeler instance du menu
        self.changer_page(Accueil)
        
    def afficher_createur(self) :
        #Appeler instance du createur
        self.changer_page(PageCreation)

        self.chairlifts_cree.append(self.page_courante.get_chairlift_courant())

    def afficher_comparer(self) :
        #Appeler instance du comparateur
        self.changer_page(PageComparer)
    
    def changer_page(self, choix) :
        self.detruire_frame()

        self.page_courante = choix(self)
        self.page_courante.pack(fill="both")

    def get_chairlifts(self) :
        return self.chairlifts_cree

    
#Loop du MainApp et choix de l'apparence du ctk
if __name__ == "__main__" :
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("dark-blue")
    application = MainApp()
    application.mainloop()
