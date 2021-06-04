from Piece import *

import numpy as np


class Echiquier(list):
    """
    self.plateau contenant les pieces

    """

    def __init__(self, ligne = 8, colonne = 8):
        self.ligne = ligne
        self.colonne = colonne
        self.plateau = np.asarray(np.column_stack([['☺' for i in range(ligne)] for j in range(colonne)]))
        self.tourCouleur = 'B'
        self.pieceMangeBlanche = []
        self.pieceMangeNoire = []
        self.userName = ['', '']
        self.nbCoup = 0
        self.fichier = ""
        self.enChargement = False
        self.blancEstEnEchec = False
        self.noirEstEnEchec = False
        self.petitRoqueBlancEncorePossible = True
        self.grandRoqueBlancEncorePossible = True
        self.petitRoqueNoirEncorePossible = True
        self.grandRoqueNoirEncorePossible = True

        self.append(Tour(0, 0, "B", self)) #self pour ajouter l'echiquier
        self.append(Cavalier(0, 1, "B", self))
        self.append(Fou(0, 2, "B", self))
        self.append(Dame(0, 3, "B", self))
        self.append(Roi(0, 4, "B", self))
        self.append(Fou(0, 5, "B", self))
        self.append(Cavalier(0, 6, "B", self))
        self.append(Tour(0, 7, "B", self))

        self.append(Pion(1, 0, "B", self))
        self.append(Pion(1, 1, "B", self))
        self.append(Pion(1, 2, "B", self))
        self.append(Pion(1, 3, "B", self))
        self.append(Pion(1, 4, "B", self))
        self.append(Pion(1, 5, "B", self))
        self.append(Pion(1, 6, "B", self))
        self.append(Pion(1, 7, "B", self))

        self.append(Tour(7, 0, "N", self))
        self.append(Cavalier(7, 1, "N", self))
        self.append(Fou(7, 2, "N", self))
        self.append(Dame(7, 3, "N", self))
        self.append(Roi(7, 4, "N", self))
        self.append(Fou(7, 5, "N", self))
        self.append(Cavalier(7, 6, "N", self))
        self.append(Tour(7, 7, "N", self))

        self.append(Pion(6, 0, "N", self))
        self.append(Pion(6, 1, "N", self))
        self.append(Pion(6, 2, "N", self))
        self.append(Pion(6, 3, "N", self))
        self.append(Pion(6, 4, "N", self))
        self.append(Pion(6, 5, "N", self))
        self.append(Pion(6, 6, "N", self))
        self.append(Pion(6, 7, "N", self))

    def __str__(self):

        self.Affichage_Plateau()


    def Affichage_Plateau(self):
        print(39 * "-")
        print("   a   b   c   d   e   f   g   h")
        print(39 * "-")
        self.plateau = np.asarray(np.column_stack([['☺' for i in range(self.ligne)] for j in range(self.colonne)]))
        for piece in self:
            self.plateau[piece.ligne][piece.colonne] = piece.car()
        for l in range(self.ligne):
            p = ''
            L = l + 1
            print(L, end="")
            for c in range(self.colonne):
                p += "| " + self.plateau[l][c] + ' '
            print(p + "|")
            print(39 * "-")
        print("   a   b   c   d   e   f   g   h")
        print(39 * "-")


    def Plateau_limit(self, ligneArrive, colonneArrive):
        """
        limite de l'échiquier {0 - 7}

        """
        return -1 < ligneArrive < 8 and -1 < colonneArrive < 8

    def case(self,x,y):

        return self.plateau[x][y]

    def Case_vide(self, ligneArrive, colonneArrive):
        """
        si c'est un "☺" la case est vide donc on vérifie si c'est un tiret

        """
        return self.plateau[ligneArrive][colonneArrive] == "☺"

    def UnTourUser(self, nbTour = 0, fichier = "", coords = ""):

        self.Affichage_Plateau()
        valable = False
        while not valable:

            try:
                if coords == '':
                    print("exemple de coup : a2 a4")
                    coord = input("Jouer votre coup : ").split(" ")
                else:
                    coord = coords.split(" ")
                ligne = int(coord[0][1]) - 1  # Ici on récupere les ligne qui son [1-8] auxquelles ont retire 1 car l'index des tabeau commence a 0 alors que l'échequier commence a 1
                ligneArrive = int(coord[1][1]) - 1
                colonne = ord(coord[0][0]) - 97  # ici on récuper les colonnes [A-H]
                colonneArrive = ord(coord[1][0]) - 97
                    
                #Test du type de deplacement
                if self.Case_vide(ligne, colonne):
                    print('Aucune piece selectionnee')
                        
                #Si c'est un roque
                #petitRoqueBlanc
                elif (ligne == 0 and colonne == 7 and ligneArrive == 0 and colonneArrive == 4) or (ligne == 0 and colonne == 4 and ligneArrive == 0 and colonneArrive == 7):
                    valable = self.petitRoqueBlanc()
                        
                #grandRoqueBlanc
                elif (ligne == 0 and colonne == 0 and ligneArrive == 0 and colonneArrive == 4) or (ligne == 0 and colonne == 4 and ligneArrive == 0 and colonneArrive == 0):
                    valable = self.grandRoqueBlanc()
                        
                #petitRoqueNoir
                elif (ligne == 7 and colonne == 7 and ligneArrive == 7 and colonneArrive == 4) or (ligne == 7 and colonne == 4 and ligneArrive == 7 and colonneArrive == 7):
                    valable = self.petitRoqueNoir()
                        
                #grandRoqueNoir
                elif (ligne == 7 and colonne == 0 and ligneArrive == 7 and colonneArrive == 4) or (ligne == 7 and colonne == 4 and ligneArrive == 7 and colonneArrive == 0):
                    valable = self.grandRoqueNoir()
                    
                #Sinon c'est une tantative de deplacement "classique" ou un en passant
                else:
                    for piece in self:
                        if piece.ligne == ligne and piece.colonne == colonne:
                            #Dans le cas suivant c'est peut-être un en passant d'un pion blanc
                            if (piece.car() == '♙' and ligne == 4 and ligneArrive == 5 and self.Case_vide(ligneArrive, colonneArrive) and colonneArrive in (colonne + 1, colonne - 1)):
                                for piece2 in self:
                                    if piece2.ligne == 4 and piece2.colonne == colonneArrive and piece2.car() == '♟' and piece2.num_avanceDe2Cases == self.nbCoup - 1:
                                        #C'est un en passant
                                        piece.majFichier(ligneArrive, colonneArrive)
                                        self.remove(piece2)
                                        self.pieceMangeNoire.append(piece2)
                                        piece.ligne = ligneArrive
                                        piece.colonne = colonneArrive
                                        valable = True
                                if not valable:
                                    print("Le 'En passant' n'est pas possible ici, coup invalide.")
                                        
                            elif (piece.car() == '♟' and ligne == 3 and ligneArrive == 2 and self.Case_vide(ligneArrive, colonneArrive) and colonneArrive in (colonne + 1, colonne - 1)):
                                for piece2 in self:
                                    if piece2.ligne == 3 and piece2.colonne == colonneArrive and piece2.car() == '♙' and piece2.num_avanceDe2Cases == self.nbCoup - 1:
                                        #C'est un en passant
                                        piece.majFichier(ligneArrive, colonneArrive)
                                        self.remove(piece2)
                                        self.pieceMangeNoire.append(piece2)
                                        piece.ligne = ligneArrive
                                        piece.colonne = colonneArrive
                                        valable = True
                                if not valable:
                                    print("Le 'En passant' n'est pas possible ici, coup invalide.")
                                   
                                        
                            #coup "classique" (i.e. pas en passant ni roque)
                            else:
                                piece.deplacement(ligneArrive, colonneArrive)
                                valable = piece.deplacement_ok
                            
                            #Cas ou un pion vient d'avancer de 2 cases (pour le coup du en passant)
                            if valable:
                                if (piece.car() == '♙' and ligneArrive == ligne + 2) or (piece.car() == '♟' and ligneArrive == ligne - 2):
                                    piece.num_avanceDe2Cases = self.nbCoup 
                                    

            except IndexError:  # Ici on récupère l'erreur qu'il n'ait pas assez d'arguments et on affiche un message explicatif de l'erreur
                print("Il faut quatre arguments pour jouer et séparer d'un espace les coordonnées de départ et d'arriver")

            except ValueError:  # Ici le joueur a mit des lettres pour les lignes
                print("Veillez entrer la bonne syntaxe : c4 d6")

            except KeyError:  # Ici le joueur a mit des chiffres pour les colonnes
                print("Voici un exemple de coup valide : a1 a5")


    def FinPartie(self):
        """
        determine la fin de la partie du jeux
        """

        finPartie = False
        if self.pieceMangeBlanche:
            if len(self.pieceMangeBlanche) == 16 or self.pieceMangeBlanche[-1].car() == '♔':
                print(39 * "*")
                print(10 * ' ' + 'Victoire de :', self.userName[1])
                print(39 * "*")
                finPartie = True
        if self.pieceMangeNoire:
            if len(self.pieceMangeNoire) == 16 or self.pieceMangeNoire[-1].car() == '♚':
                print(39 * "*")
                print(10 * ' ' + 'Victoire du :',self.userName[0])
                print(39 * "*")
                finPartie = True
        return finPartie

    #Initialise le fichier de sauvegarde
    #Cela correspond a y indiquer toutes les informations qui doivent etre dans l'entete
    def initialisationFichier(self, joueur1, joueur2):
        with open(self.fichier, mode="w") as f:
            f.write('[Event "?"]\n')
            f.write('[Site "?"]\n')
            f.write('[Date "????.??.??"]\n')
            f.write('[Round "?"]\n')
            f.write('[White "' + str(joueur1) + '"]\n')
            f.write('[Black "' + str(joueur2) + '"]\n')
            f.write('[Result "?-?"]\n\n')

    def Partie(self):
        """
        Verifie si le joueur va jouer avec la machine ou l'humain et implemente le jeu

        """
        finPartie = False
        #Si c'est une nouvelle partie aucun nom n'a ete rentre
        if self.userName[0] == "":
            joueur1 = input("veillez entrer le nom du joueur blanc ou 'robot' pour la machine : ").upper()
            joueur2 = input("veillez entrer le nom du joueur noir ou 'robot' pour la machine : ").upper()
            self.userName = (joueur1, joueur2)
        
        joueur1 = self.userName[0]
        joueur2 = self.userName[0]
        
        if self.fichier == "":
            self.fichier = input("veuillez entrer le nom du fichier de sauvegarde de la partie : ") + ".pgn"
            self.initialisationFichier(joueur1, joueur2)

            
        userType = (joueur1=='ROBOT', joueur2=='ROBOT')
        nbTour = self.nbCoup // 2 + 1
        colorType = ('B','N')
        
   
        while (not finPartie):
            print(39 * "*")
            print(10 * ' ' + 'Tour:', nbTour)
            print(10 * ' ' + '', self.userName[self.nbCoup%2])
            if self.blancEstEnEchec :
                print("ATTENTION : les blancs sont en echec")
            if self.noirEstEnEchec :
                print("ATTENTION : les noirs sont en echec")
            print(39 * "*")
            
            self.tourCouleur = colorType[self.nbCoup%2]
            
            if userType[self.nbCoup%2]:
                self.UnTourIA(nbTour)
            else:
                self.UnTourUser(nbTour)
                
            self.testRoqueEncorePossible()
                
            finPartie = self.FinPartie()
            
            self.nbCoup += 1
            
            nbTour = self.nbCoup // 2 + 1
                
    #On regarde ici si un roi ou si une tour a bougee
    def testRoqueEncorePossible(self):
        PieceEn07Existe = False
        PieceEn04Existe = False
        PieceEn77Existe = False
        PieceEn74Existe = False
        PieceEn00Existe = False
        PieceEn70Existe = False
        
        #A chaque fois, on regarde si toutes les pieces qui permettent de roquer ont bougé (i.e. si elles ne sont plus sur leurs positions initiales)
        #Si elles ont bougé alors on l'indique en changeant la variable booleenne correspondante
        
        for piece in self:
            if (piece.ligne == 0 and piece.colonne == 7):
                PieceEn07Existe = True
                if (piece.car() != '♖'):
                    self.petitRoqueBlancEncorePossible = False
             
            if (piece.ligne == 0 and piece.colonne == 4):
                PieceEn04Existe = True
                if (piece.car() != '♔'):
                    self.petitRoqueBlancEncorePossible = False
                    self.grandRoqueBlancEncorePossible = False
             
            if (piece.ligne == 7 and piece.colonne == 7):
                PieceEn77Existe = True
                if (piece.car() != '♜'):
                    self.petitRoqueNoirEncorePossible = False
             
            if (piece.ligne == 7 and piece.colonne == 4):
                PieceEn74Existe = True
                if (piece.car() != '♚'):
                    self.petitRoqueNoirEncorePossible = False
                    self.grandRoqueNoirEncorePossible = False
             
            if (piece.ligne == 0 and piece.colonne == 0):
                PieceEn00Existe = True
                if (piece.car() != '♖'):
                    self.grandRoqueBlancEncorePossible = False
             
            if (piece.ligne == 7 and piece.colonne == 0):
                PieceEn70Existe = True
                if (piece.car() != '♜'):
                    self.grandRoqueNoirEncorePossible = False
                    
        #Si les pieces sensees etre a leur position n'existent pas alors elles ne peuvent
        #plus roquer car cela signifie quelles ont deja bouge
        if not PieceEn07Existe:
            petitRoqueBlancEncorePossible = False
        if not PieceEn04Existe:
            self.petitRoqueBlancEncorePossible = False
            self.grandRoqueBlancEncorePossible = False
        if not PieceEn77Existe:
            self.petitRoqueNoirEncorePossible = False
        if not PieceEn74Existe:
            self.petitRoqueNoirEncorePossible = False
            self.grandRoqueNoirEncorePossible = False
        if not PieceEn00Existe:
            self.grandRoqueBlancEncorePossible = False
        if not PieceEn70Existe:
            self.grandRoqueNoirEncorePossible = False
      
    #Il y a 4 methodes de roques
    #A chaque fois on verrifie si toures les conditions pour pouvoir roquer sont reunies
    #Si c'est le cas on applique le roque
    
    def petitRoqueBlanc(self):
        if self.blancEstEnEchec:
            print("Vous ne pouvez pas roquer en echec.")
            return False
    
        if self.tourCouleur == "N":
            print("Vous ne pouvez pas roquer avec les pieces de votre adversaire.")
            return False
        
        if not self.petitRoqueBlancEncorePossible:
            print("Vous ne pouvez pas roquer car une des piece a deja ete deplacee.")
            return False
        
        for piece in self:
            if piece.ligne == 0:
                if piece.colonne in (5, 6):
                    print("Vous ne pouvez pas roquer.")
                    return False
        
        if self.testSeraEnEchec(0, 4, 0, 7):
            print("Vous ne pouvez pas roquer car le roque vous mettrait en echec.")
            return False
            
        for piece1 in self:
            if piece1.ligne == 0 and piece1.colonne == 4:
                for piece2 in self:
                    if piece2.ligne == 0 and piece2.colonne == 7:
                        piece1.colonne, piece2.colonne = piece2.colonne, piece1.colonne
                        piece1.majFichier(-1, -1)
                        return True
                
        
    def grandRoqueBlanc(self):
        if self.blancEstEnEchec:
            print("Vous ne pouvez pas roquer en echec.")
            return False
            
        if self.tourCouleur == "N":
            print("Vous ne pouvez pas roquer avec les pieces de votre adversaire.")
            return False
            
        if not self.grandRoqueBlancEncorePossible:
            print("Vous ne pouvez pas roquer car une des piece a deja ete deplacee.")
            return False
           
        for piece in self:
            if piece.ligne == 0:
                if piece.colonne in (1, 2, 3):
                    print("Vous ne pouvez pas roquer.")
                    return False
                    
        if self.testSeraEnEchec(0, 4, 0, 0):
            print("Vous ne pouvez pas roquer car le roque vous mettrait en echec.")
            return False
            
        for piece1 in self:
            if piece1.ligne == 0 and piece1.colonne == 4:
                for piece2 in self:
                    if piece2.ligne == 0 and piece2.colonne == 0:
                        piece1.colonne, piece2.colonne = piece2.colonne, piece1.colonne
                        piece1.majFichier(-2, -2)
                        return True
    
    def petitRoqueNoir(self):
        if self.noirEstEnEchec:
            print("Vous ne pouvez pas roquer en echec.")
            return False
   
        if self.tourCouleur == "B":
            print("Vous ne pouvez pas roquer avec les pieces de votre adversaire.")
            return False
            
        if not self.petitRoqueNoirEncorePossible:
            print("Vous ne pouvez pas roquer car une des piece a deja ete deplacee.")
            return False
            
        for piece in self:
            if piece.ligne == 7:
                if piece.colonne in (5, 6):
                    print("Vous ne pouvez pas roquer.")
                    return False
                    
        if self.testSeraEnEchec(7, 4, 7, 7):
            print("Vous ne pouvez pas roquer car le roque vous mettrait en echec.")
            return False
            
        for piece1 in self:
            if piece1.ligne == 7 and piece1.colonne == 4:
                for piece2 in self:
                    if piece2.ligne == 7 and piece2.colonne == 7:
                        piece1.colonne, piece2.colonne = piece2.colonne, piece1.colonne
                        piece1.majFichier(-1, -1)
                        return True
    
    def grandRoqueNoir(self):
        if self.noirEstEnEchec:
            print("Vous ne pouvez pas roquer en echec.")
            return False
    
        if self.tourCouleur == "B":
            print("Vous ne pouvez pas roquer avec les pieces de votre adversaire.")
            return False
            
        if not self.grandRoqueNoirEncorePossible:
            print("Vous ne pouvez pas roquer car une des piece a deja ete deplacee.")
            return False
           
        for piece in self:
            if piece.ligne == 7:
                if piece.colonne in (1, 2, 3):
                    print("Vous ne pouvez pas roquer.")
                    return False
                   
        if self.testSeraEnEchec(7, 4, 7, 0):
            print("Vous ne pouvez pas roquer car le roque vous mettrait en echec.")
            return False
            
        for piece1 in self:
            if piece1.ligne == 7 and piece1.colonne == 4:
                for piece2 in self:
                    if piece2.ligne == 7 and piece2.colonne == 0:
                        piece1.colonne, piece2.colonne = piece2.colonne, piece1.colonne
                        piece1.majFichier(-2, -2)
                        return True
                

    #Couleur correspond l'autre couleur que celle du roi dont on veut tester l'echec
    def testEchec(self, couleur = ""):
        if couleur == "":
            couleur = self.tourCouleur
        ligneRoiAdverse = 0
        colonneRoiAdverse = 0
        couleurRoiAdverse = ""
        echec = False
        
        #Premiere boucle pour determiner ou se trouve le roi adverse et sa couleur
        for piece in self:
            if (piece.couleur != couleur) and (piece.car() == '♚' or piece.car() == '♔'):
                ligneRoiAdverse = piece.ligne
                colonneRoiAdverse = piece.colonne
                couleurRoiAdverse = piece.couleur
        
        #Deuxieme boucle pour tester les deplacement possible du joueur qui vient de jouer
        for piece in self:
            if (piece.couleur == couleur):
                #Test particulier pour les pions car leurs déplacement n'est pas le même si il peuvent manger une piece
                if piece.car() == '♙':
                    if (ligneRoiAdverse == piece.ligne + 1) and ((colonneRoiAdverse in (piece.colonne + 1, piece.ligne - 1))):
                        echec = True
                elif piece.car() == '♟':
                    if (ligneRoiAdverse == piece.ligne - 1) and ((colonneRoiAdverse in (piece.colonne + 1, piece.ligne - 1))):
                        echec = True
                
                #Si la piece n'est pas un pion    
                elif piece.deplacement_Valide(ligneRoiAdverse, colonneRoiAdverse):
                    echec = True
                
        #Resultat
        if couleurRoiAdverse == "B" :
            self.blancEstEnEchec = echec
        
        if couleurRoiAdverse == "N" :
            self.noirEstEnEchec = echec
            
    #Methode typiquement appelee pour savoir si le deplacement d'un roi va le mettre lui-meme en echec (par exemple)
    def testSeraEnEchec(self, oldX, oldY, newX, newY):
        seraEnEchec = False
        
        for piece in self:
            if piece.ligne == oldX and piece.colonne == oldY:
                #Ici piece est la piece dont on veut anticiper le deplacement
                #On considere que le deplacement est legal et qu'on a fait les verifications avant d'appeler cette methode
                #On modifie donc la position momentanément (avant affichage) et on appelle testEchec dans cette nouvelle configuration
                piece.ligne = newX
                piece.colonne = newY
                
                if piece.couleur == "B":
                    couleurTestEchec = "N"
                else:
                    couleurTestEchec = "B"
                    
                self.testEchec(couleurTestEchec)
                
                if piece.couleur == "B":
                    seraEnEchec = self.blancEstEnEchec
                else:
                    seraEnEchec = self.noirEstEnEchec
                
                #Maintenant on remet l'etat du jeu comme avant
                piece.ligne = oldX
                piece.colonne = oldY
                self.testEchec(couleurTestEchec)
                
        return seraEnEchec
        
    def chargerFichier(self):
        self.fichier = input("Veuillez entrer le nom du fichier a charger (sans l'extension .pgn) : ") + ".pgn"
        curseur = 0
        lignesCoups = []
        chaineDeCoups = ""
        coups = []
        partieFini = False
        self.enChargement = True
            
        with open(self.fichier, mode="r") as f:
           
            #Lecture de l'entête pour recuper les noms de joueurs
            while (curseur == 0):
                ligneLue = f.readline()
                if "White " in ligneLue:
                    self.userName[0] = ligneLue.split('"')[1]
                if "Black " in ligneLue:
                    self.userName[1] = ligneLue.split('"')[1]
                if not "[" in ligneLue:
                    curseur = f.tell()
                        
            f.seek(curseur)
            lignesCoups = f.readlines()
            
        #On ajoute toutes les lignes du fichier dans une seule chaine de caractere en les separant d'un espace
        for ligneCoups in lignesCoups:
            chaineDeCoups += ligneCoups
            chaineDeCoups += " "
        
        #Si le fichier PGN est formater de telle sorte a ce qu'il n'y est pas d'espace apres les numeros des tours, on en met un
        #Cela permet de traiter des fichier PGN toujours formates de la meme maniere
        if chaineDeCoups[chaineDeCoups.find(".") + 1] != " ":
            chaineDeCoups = chaineDeCoups.replace(".", ". ")
            
        #On recupere alors tous les coups dans une liste
        coups = chaineDeCoups.split(" ")
            
            
        for coup in coups:
            
            #Si le score est indique dans le fichier, c'est que la partie est fini (sinon on la continue a la fin)
            if len(coup) >= 3 and coup[0:3] in ("1/2", "1-0", "0-1"):
                partieFini = True
            
            #On enleve les coups qui n'en sont pas (commentaires et numero du tour a chaque fois)
            if "." in coup or "{" in coup or "?" in coup or "(" in coup or len(coup) <= 1:
                coups.remove(coup)
                
        
        if coups != []:
            #On analyse alors le coup si on recupere une liste non vide, sinon c'est qu'il y a eu un probleme ou que le fichier est vide
            self.analyserCoups(coups, partieFini)
        else:
            print("Il a eu un probleme dans le chargement du fichier. Nouvelle partie.")
            self.Partie()
            
    def analyserCoups(self, coups, partieFini):
        colonnes = ("a", "b", "c", "d", "e", "f", "g", "h")
        lignes = ("1", "2", "3", "4", "5", "6", "7", "8")
       
        #Pour chaque coup, on va extraire les informations qu'il contient 
        for coup in coups:
            couleur = ("B", "N")[self.nbCoup % 2]
            typeDePiece = ""
            nouvellePiece = ""
            prerequisColonne = -1
            prerequisLigne = -1
            colonneArrive = 0
            ligneArrive = 0
            
            
            #Si le coup est en fait le score, on ne fait rien
            if len(coup) >= 3 and coup[0:3] in ("1/2", "1-0", "0-1"):
                continue
            
            #Si c'est un petit roque
            if len(coup) >= 3 and coup[0:3] == "O-O":
                if couleur == "B":
                    self.petitRoqueBlanc()
                else:
                    self.petitRoqueNoir()
                self.affichagePartieEnChargement()
                self.nbCoup += 1
                continue
                
            #Si c'est un grand roque
            elif len(coup) >= 5 and coup[0:5] == "O-O-O":
                if couleur == "B":
                    self.grandRoqueBlanc()
                else:
                    self.grandRoqueNoir()
                self.affichagePartieEnChargement()
                self.nbCoup += 1
                continue

            #Si ce n'est pas un roque, on exploite les informations sur le type de piece (premier caractere)
            elif coup[0] in ("K", "Q", "B", "N", "R"):
                typeDePiece = coup[0]
                coup = coup.replace(coup[0], '')
            #Si il n'y a pas de caractere correspondant au type de piece, alors c'est un pion
            else:
                typeDePiece = "P"
            
            #Recherche du prerequis
            if coup[0] in colonnes and (coup[1] == "x" or coup[1] in colonnes):
                prerequisColonne = ord(coup[0]) - 97
                coup = coup.replace(coup[0], '')
            elif coup[0] in lignes and (coup[1] == "x" or coup[1] in colonnes):
                prerequisLigne = int(coup[0]) -1
                coup = coup.replace(coup[0], '')
            elif len(coup) >= 3 and coup[0] in colonnes and coup[1] in lignes and (coup[2] in colonnes or coup[2] == "x"):
                prerequisColonne = ord(coup[0]) - 97
                prerequisLigne = int(coup[1]) -1
                coup = coup.replace(prerequisColonne, '')
                coup = coup.replace(prerequisLigne, '')
                
            #Le x correspond a une capture, cette information ne nous est pas utile car on gere automatique si il y a capture
            if len(coup) >= 1 and coup[0] == "x":
                coup = coup.replace("x", '')
            
            #On recupere les position sous forme de coordonnees exploitables par le programme
            colonneArrive = ord(coup[0]) - 97
            coup = coup.replace(coup[0], '')
            ligneArrive = int(coup[0]) -1
            coup = coup.replace(coup[0], '')
            
            #Si il y a un = alors c'est une promotion de pion
            if len(coup) >= 1 and coup[0] == "=":
                nouvellePiece = coup[1]
                coup = coup.replace("=", '')
                coup = coup.replace(nouvellePiece, '')
            
            #Une fois qu'on a analyse le coup, on l'applique
            self.appliquerCoup(prerequisColonne, prerequisLigne, colonneArrive, ligneArrive, typeDePiece, nouvellePiece)
            
            #On affiche l'echiquier
            self.affichagePartieEnChargement()
            
            self.nbCoup += 1
        
        if not partieFini:
            #Si la partie n'est pas finie, on la reprend ou elle s'est arrete
            print("Fin du chargement de la partie, à vous de jouer.")
            self.enChargement = False
            self.Partie()
        else:
            print("fin de la partie.")
        
    #Permet de d'exploiter l'information sur le type de piece en renvoyer le couple de caractere correspondant
    def lettreToTypeDePiece(self, lettre):
        if lettre == "R":
            return (nt, bt)
        if lettre == "N":
            return (nc, bc)
        if lettre == "B":
            return (nf, bf)
        if lettre == "K":
            return (nr, br)
        if lettre == "Q":
            return (nd, bd)
        if lettre == "P":
            return ('♟', '♙')
            
    #Est appelee pour afficher la partie qui est en train de charger a partir d'un fichier
    def affichagePartieEnChargement(self):
        print(39 * "*")
        print(10 * ' ' + 'Tour : ', self.nbCoup // 2 + 1)
        print(8 * ' ' + '', self.userName[self.nbCoup%2])
        print(39 * "*")
        self.Affichage_Plateau()
        input("Appuyez sur entree pour voir le coup suivant. ")
        
    #Permet d'appliquer un coup charge a partir d'un fichier une fois que ce coup a ete analyse
    def appliquerCoup(self, prerequisColonne, prerequisLigne, colonneArrive, ligneArrive, typeDePiece, nouvellePiece):
        couleur = ("B", "N")[self.nbCoup % 2]

        
        #Cas ou la position de depart est indiquee
        if prerequisColonne != -1 and prerequisLigne != -1:
            for piece in self:
                if piece.colonne == prerequisColonne and piece.ligne == prerequisLigne:
                    piece.deplacementForce(ligneArrive, colonneArrive, nouvellePiece)
                    
                            
        #Cas ou il y a un prerequis sur la ligne           
        elif prerequisLigne != -1:
            for piece in self:
                if (piece.couleur == couleur and piece.car() in self.lettreToTypeDePiece(typeDePiece)):
                    if piece.deplacement_Valide(ligneArrive, colonneArrive) and piece.ligne == prerequisLigne:
                        piece.deplacementForce(ligneArrive, colonneArrive, nouvellePiece)
                    
        #Cas ou il y a un prerequis sur la colonne 
        elif prerequisColonne != -1:
            for piece in self:
                if (piece.couleur == couleur and piece.car() in self.lettreToTypeDePiece(typeDePiece)):
                    if piece.deplacement_Valide(ligneArrive, colonneArrive) and piece.colonne == prerequisColonne:
                        piece.deplacementForce(ligneArrive, colonneArrive, nouvellePiece)

        
        #Pas de prerequis
        else:
            for piece in self:
                if piece.couleur == couleur and piece.car() in self.lettreToTypeDePiece(typeDePiece):
                    if piece.deplacement_Valide(ligneArrive, colonneArrive):
                        piece.deplacementForce(ligneArrive, colonneArrive, nouvellePiece)

