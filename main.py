from MainApp import MainApp
import customtkinter as ctk

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
#TODO constantes entre les différents fichiers