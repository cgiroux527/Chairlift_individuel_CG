from MainApp import MainApp
import customtkinter as ctk

#Loop du MainApp et choix de l'apparence du ctk
if __name__ == "__main__" :
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("midnight.json") #créé par a13xe : https://github.com/a13xe/CTkThemesPack/blob/main/themes/midnight.json
    application = MainApp()
    application.mainloop()

#TODO on dirait que ce qui est choisi dans le createur n'arrive pas a bonne chose dans comparer
#TODO plus de fonctions???
#TODO mettre ça dans un meilleur ordre
#TODO commenter ligne 92 graph
#TODO alignement des afficherselection
#TODO est ce que le graph change vraiment, car pas destroy
#TODO enlever les selfs inutiles
#TODO tout bien tester et tester presentation orale
#TODO constantes entre les différents fichiers