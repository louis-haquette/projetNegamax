from echiquier import Echiquier

"""
-------------------------------------------
Lancement du programme depuis cette classe 
-------------------------------------------
"""


if __name__ == "__main__":
    ligne = 8
    colonne = 8
    table = Echiquier(ligne, colonne)
    
    choix = ""
    while choix not in ("1", "2"):
        choix = input("Entrez 1 pour jouer une nouvelle partie, entrez 2 pour charger une partie : ")
        if choix not in ("1", "2"):
            print("Entrez 1 ou 2")
    
    if choix == "1":
        table.Partie()
    elif choix == "2":
        table.chargerFichier()
