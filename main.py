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

        #À l'ouverture c'est le menu principale
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

    
#Loop du MainApp et choix de l'apparence du ctk
if __name__ == "__main__" :
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("midnight.json") #créé par a13xe : https://github.com/a13xe/CTkThemesPack/blob/main/themes/midnight.json
    application = MainApp()
    application.mainloop()


#TODO les prints dans la console à enlever
#TODO separer en plus de fonctions et fichiers, UNE CLASSE PAR FICHIER
#TODO mettre ça dans un meilleur ordre
#TODO condition où ils ne peuvent pas avoir le même nom
#TODO commenter ligne 308
#TODO alignement des afficherselection
#TODO est ce que le graph change vraiment, car pas destroy
#TODO enlever les selfs inutiles
#TODO tout bien tester et tester presentation orale