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

        #Initialiser les 3 attributs pour la suite à des valeurs de bases
        self.page_courante = None
        self.chairlifts_cree = []
        self.nb_lift = 2

        #À l'ouverture c'est le menu principal
        self.afficher_menu_principal()

    #Méthode appelé pour détruire la page courante avant de passer à la prochaine
    def detruire_frame(self):
        if self.page_courante is not None :
            self.page_courante.destroy()

    def afficher_menu_principal(self) :
        #Appeler instance du menu
        self.changer_page(Accueil)
        
    def afficher_createur(self) :
        #Appeler instance du createur
        self.changer_page(PageCreation)

    def afficher_comparer(self) :
        #Appeler instance du comparateur
        self.nb_lift = self.page_courante.get_nb_lift()
        self.changer_page(PageComparer)

    #Créer les instances et modifier la classe appelée par la page courante
    def changer_page(self, choix) :
        self.detruire_frame()

        self.page_courante = choix(self)
        #Afficher ce qui est contenu dans la page courante et lui permettre d'étendre son contenu
        self.page_courante.pack(fill="both", expand=True)

    #Getter pour la suite dans PageComparer
    def get_chairlifts(self) :
        return self.chairlifts_cree

    #Mettre le chairlift créé dans le créateur dans la liste 
    def ajouter_chairlift(self, chairlift):
        self.chairlifts_cree.append(chairlift)
        

    