# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

"""
@author: Loic SOKOUDJOU, Louis HAQUETTE

"""
nt = '♜'
nc = '♞'
nf = '♝'
nr = '♚'
nd = '♛'
np = '♟'
bt = '♖'
bc = '♘'
bf = '♗'
br = '♔'
bd = '♕'
bp = '♙'

pieceBlanc = [bp, bt, bf, bc, bd, br]
pieceNoir = [np, nt, nf, nc, nd, nr]


class Pieces:
    """
        classe abstraite qui crée une piece aux coordonnées désirées.

        Paramètres
        ----------
        abscisse, ordonnée: int
            Les coordonnées auxquelles la piece sera créé.
        couleur: str
            La couleur a laquelle la piece sera créé.
    """

    def __init__(self, ligne, colonne, couleur, echiquier):
        self.echiquier = echiquier
        self.couleur = couleur
        self.ligne = ligne
        self.colonne = colonne
        self.deplacement_ok = False


    @property
    def x(self):
        """
        x: nombre entier
            Abscisse de la piece
        """
        return self.ligne

    @property
    def y(self):
        """
        y: nombre entier
            Ordonnee de la piece
        """
        return self.colonne

    def coords(self):
        """
        coords: tuple
            Les coordonnées de la piece sur le plateau de jeu
        """
        return self.x, self.y

    def __str__(self):
        """
        Affiche l'état courant de la piece.

        Paramètres
        ----------
        Aucun

        Renvoie
        -------
        s: str
            La chaîne de caractères qui sera affichée via ''print''
        """
        return "{} : position ({}, {})".format(self.car(), self.x, self.y)

    @abstractmethod
    def Car(self):
        """
        Renvoie l'identifiant de la piece.

        Paramètres
        ----------
        Aucun

        Renvoie
        -------
        P: str
            Le caractère représentant la piece.
        listePieces=["♜","♞","♝","♚","♛","♟","♘","♙","♔","♕","♗","♖"]
        """
        pass
        

    def deplacement(self, x_new, y_new):
        """
        Met a jour le deplacement
        """
        if self.echiquier.tourCouleur != self.couleur:
            if self.couleur == 'B':
                colorName = 'noire'
            else:
                colorName = 'blanche'  #au cas ou la piece deplace n'est pas de la meme couleur
            print("Veillez deplacer une piece de couleur " + colorName)
            self.deplacement_ok = False  #verifie le deplacement dans le tour si ok et incremente avec le compteur nbTour dans echiquier
            
        elif not self.deplacement_Valide(x_new, y_new):
            print("Deplacement invalide, veillez resayer")
            self.deplacement_ok = False

        else:        
            if not self.echiquier.Case_vide(x_new, y_new):
                for piece in self.echiquier:
                    if piece.ligne == x_new and piece.colonne == y_new:
                        self.echiquier.remove(piece)
                        if self.couleur == 'B':
                            self.echiquier.pieceMangeNoire.append(piece)
                        else:
                            self.echiquier.pieceMangeBlanche.append(piece)                    
                   
            #MAJ du fichier PGN
            self.majFichier(x_new, y_new)

            self.ligne = x_new
            self.colonne = y_new
            self.promotion(x_new, y_new)
            self.deplacement_ok = True
            
            #Test d'echec pour savoir si on est en echec
            self.echiquier.testEchec()
    
    #Fonction appelée lorsqu'un coup est chargee lors de la lecture d'un fichier
    def deplacementForce(self, ligneArrive, colonneArrive, promu):
        
        #Si le coup est une promotion
        if promu != "":
            self.promotion(ligneArrive, colonneArrive, promu)
            return
        
        #Si c'est un coup classique on deplace la piece et on capture celle qui etait la avant (si elle existe)
        for piece in self.echiquier:
            if piece.ligne == ligneArrive and piece.colonne == colonneArrive:
                self.echiquier.remove(piece)
                if self.couleur == "B":
                    self.echiquier.pieceMangeNoire.append(piece)
                else:
                    self.echiquier.pieceMangeBlanche.append(piece)
                    
        self.ligne = ligneArrive
        self.colonne = colonneArrive
                    
    

    @abstractmethod
    def promotion(self):
        pass

    @abstractmethod
    def deplacement_Valide(self):
        """
        À instancier dans les classes filles
        """
        pass
        
    #Permet d'écrire le type de piece en format algebrique (pour le fichier PGN)
    def lettrePiece(self):
        car = self.car()

        if car in (nt, bt):
            return "R"
        if car in (nc, bc):
            return "N"
        if car in (nf, bf):
            return "B"
        if car in (nr, br):
            return "K"
        if car in (nd, bd):
            return "Q"
        if car in (np, bp):
            return ""
            
    #Permet d'écrire le position en format algebrique (pour le fichier PGN)
    def positionPGN(self, y, x):
        yPGN = str(y + 1)
        
        if x == 0:
            xPGN = "a"
        if x == 1:
            xPGN = "b"
        if x == 2:
            xPGN = "c"
        if x == 3:
            xPGN = "d"
        if x == 4:
            xPGN = "e"
        if x == 5:
            xPGN = "f"
        if x == 6:
            xPGN = "g"
        if x == 7:
            xPGN = "h"                 
            
        return xPGN + yPGN       
    
    #Est appelé à chaque nouveau coup pour mettre à jour le fichier
    def majFichier(self, x_new, y_new):
    #si x_new = -1 et y_new = -1, il s'agit d'un petit roque (convention personnelle et arbitraire)
    #si x_new = -2 et y_new = -2, il s'agit d'un grand roque (convention personnelle et arbitraire)
        
        #Si on est en train de charger une partie on n'ecrit rien sur le fichier
        if self.echiquier.enChargement:
            return

        with open(self.echiquier.fichier, mode='a') as f:
            nbTour = self.echiquier.nbCoup // 2 + 1
            if self.couleur == "B" :
                if nbTour != 1:
                    f.write(" ")
                f.write(str(nbTour) + ".")
            
            if x_new == -1 and y_new == -1:
                f.write(" " + "O-O")
            elif x_new == -2 and y_new == -2:
                f.write(" " + "O-O-O")
            else:
                f.write(" " + self.lettrePiece() + self.positionPGN(x_new, y_new))


class Roi(Pieces):
    """
    classe qui herite de Pieces permettant
    de creer une piece roi
    """

    def __init__(self, x, y, couleur, echiquier):
        super().__init__(x, y, couleur, echiquier)

    def car(self):
        if self.couleur == 'N':
            return '♚'
        elif self.couleur == 'B':
            return '♔'
        else:
            print('Veuillez entre une couleur valide \n N: Noire \n B: Blanche ')

    def deplacement_Valide(self, x_new, y_new):
        legalmoves = []
        if self.couleur == "N":
            color = pieceBlanc
        else:
            color = pieceNoir

        posroi = [self.ligne, self.colonne]

        deplacement = [[1, 1], [1, -1],
                       [0, 1], [0, -1], [1, 0], [-1, 0], [-1, 1], [-1, -1]]
        for possibilite in deplacement:
            row = posroi[0] + possibilite[0]
            column = posroi[1] + possibilite[1]
            if self.echiquier.Plateau_limit(row, column) and self.echiquier.Case_vide(row, column):
                legalmoves.append([row, column])
            elif self.echiquier.Plateau_limit(row, column) and self.echiquier.plateau[row][column] in color:
                legalmoves.append([row, column])
        return [x_new, y_new] in legalmoves

    def promotion(self, x_new, y_new):
        pass

class Dame(Pieces):
    """
    classe qui herite de Pieces permettantant
    de creer une piece dame
    """

    def __init__(self, x, y, couleur, echiquier):
        super().__init__(x, y, couleur, echiquier)

    def car(self):
        if self.couleur == 'N':
            return '♛'
        elif self.couleur == 'B':
            return '♕'
        else:
            print('Veuillez entre une couleur valide \n N: Noire \n B: Blanche ')

    def deplacement_Valide(self, x_new, y_new):
        legalmoves = []
        if self.couleur == "N":
            color = pieceBlanc
        else:
            color = pieceNoir
        postour = [self.ligne, self.colonne]
        deplacement = [[1, 0], [0, 1], [-1, 0],
                       [0, -1], [1, 1], [1, -1], [-1, -1], [-1, 1]]
        for possibilite in deplacement:
            i = 1
            while True:
                row = postour[0] + i * possibilite[0]
                column = postour[1] + i * possibilite[1]
                if self.echiquier.Plateau_limit(row, column) and self.echiquier.Case_vide(row, column):
                    legalmoves.append([row, column])
                    i += 1
                else:
                    if self.echiquier.Plateau_limit(row, column) and self.echiquier.plateau[row][column] in color:
                        legalmoves.append([row, column])
                    break
        return [x_new, y_new] in legalmoves

    def promotion(self, x_new, y_new):
        pass

class Cavalier(Pieces):
    """
    classe qui herite de Pieces permettantant
    de creer une piece cavalier
    """

    def __init__(self, x, y, couleur, echiquier):
        super().__init__(x, y, couleur, echiquier)

    def car(self):
        if self.couleur == 'N':
            return '♞'
        elif self.couleur == 'B':
            return '♘'
        else:
            print('Veuillez entre une couleur valide \n N: Noire \n B: Blanche ')

    def deplacement_Valide(self, x_new, y_new):
        legalmoves = []
        if self.couleur == "N":  # Si le cavalier est noir
            color = pieceBlanc  # il peut manger les pièces blanches
        else:  # si il n'est pas noir (donc forcément blanc)
            color = pieceNoir  # il peut manger les pièces noires

        poscavalier = [self.ligne, self.colonne]  # on prend la position du cavalier
        deplacement = [[2, 1], [2, -1], [-2, 1],
                       [-2, -1], [-1, -2], [1, -2], [1, 2],
                       [-1, 2]]  # on liste ici tous les déplacements possibles du cavalier
        for possibilite in deplacement:  # Pour chaque déplacement possible
            # la ligne équivaux à celle de départ + le déplacement possible pour la ligne
            row = poscavalier[0] + possibilite[0]
            column = poscavalier[1] + possibilite[1]  # pareil pour la colonne
            # Si cette position est comprise dans l'échiquier et que c'est Case_vide
            if self.echiquier.Plateau_limit(row, column) and self.echiquier.Case_vide(row, column):
                legalmoves.append([row, column])  # Le mouvement est possible
            # Sinon si on a une pièce qui est de la couleur adverse
            elif self.echiquier.Plateau_limit(row, column) and self.echiquier.plateau[row][column] in color:
                legalmoves.append([row, column])  # Le mouvement est possible
        # On renvoie un booléen qui regarde si le déplacement du joueur est possible
        return [x_new, y_new] in legalmoves

    def promotion(self, x_new, y_new):
        pass


class Tour(Pieces):
    """
    classe qui herite de Pieces permettantant
    de creer une piece tour
    """

    def __init__(self, x, y, couleur, echiquier):
        super().__init__(x, y, couleur, echiquier)

    def car(self):
        if self.couleur == 'N':
            return '♜'
        elif self.couleur == 'B':
            return '♖'
        else:
            print('Veuillez entre une couleur valide \n N: Noire \n B: Blanche ')

    def deplacement_Valide(self, x_new, y_new):
        legalmoves = []
        if self.couleur == "N":
            color = pieceBlanc
        else:
            color = pieceNoir
        postour = [self.ligne, self.colonne]
        deplacement = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        for possibilite in deplacement:
            i = 1
            while True:
                row = postour[0] + i * possibilite[0]
                column = postour[1] + i * possibilite[1]
                if self.echiquier.Plateau_limit(row, column) and self.echiquier.Case_vide(row, column):
                    legalmoves.append([row, column])
                    i += 1
                else:
                    if self.echiquier.Plateau_limit(row, column) and self.echiquier.plateau[row][column] in color:
                        legalmoves.append([row, column])
                    break
        return [x_new, y_new] in legalmoves

    def promotion(self, x_new, y_new):
        pass

class Fou(Pieces):
    """
    classe qui herite de Pieces permettantant
    de creer une piece Fou
    """

    def __init__(self, x, y, couleur, echiquier):
        super().__init__(x, y, couleur, echiquier)

    def car(self):
        if self.couleur == 'N':
            return '♝'
        elif self.couleur == 'B':
            return '♗'
        else:
            print('Veuillez entre une couleur valide \n N: Noire \n B: Blanche ')

    def deplacement_Valide(self, x_new, y_new):
        legalmoves = []
        if self.couleur == "N":  # si la couleur est noir
            color = pieceBlanc  # les adversaires sont blancs
        else:
            color = pieceNoir  # sinon les adversaires sont noirs
        posfou = [self.ligne, self.colonne]  # position actuelle de la pièce
        # déplacement possible du fou
        deplacement = [[1, 1], [1, -1], [-1, -1], [-1, 1]]
        for possibilite in deplacement:
            i = 1
            while True:  # boucle infinie
                # On va prendre la position de départ auquel on aditionne la possibilité * i
                row = posfou[0] + i * possibilite[0]
                column = posfou[1] + i * possibilite[1]
                # si c'est dans l'échiquier et que la case est self.echiquier.Case_vide
                if self.echiquier.Plateau_limit(row, column) and self.echiquier.Case_vide(row, column):
                    # on ajoute les coordoonées dans le tableau des mouvements possibles
                    legalmoves.append([row, column])
                    i += 1
                else:
                    # si on a une pièce dans l'échiquier et de couleur adverse
                    if self.echiquier.Plateau_limit(row, column) and self.echiquier.plateau[row][column] in color:
                        # on ajoute les coordoonées aux mouvements possibles
                        legalmoves.append([row, column])
                    break  # on stop la boucle infinie car on ne peut sauter au dessus des pièces
        # on renvoie si le mouvement du joueur est possible
        return [x_new, y_new] in legalmoves

    def promotion(self, x_new, y_new):
        pass

class Pion(Pieces):
    """
    classe qui herite de Pieces permettantant
    de creer une piece pion
    """

    def __init__(self, x, y, couleur, echiquier):
        super().__init__(x, y, couleur, echiquier)
        #Sert pour le coup "en passant"
        self.num_avanceDe2Cases = 0

    def car(self):
        if self.couleur == 'N':
            return '♟'
        elif self.couleur == 'B':
            return '♙'
        else:
            print('Veuillez entre une couleur valide \n N: Noire \n B: Blanche ')

    def deplacement_Valide(self, x_new, y_new):
        legalmoves = []
        pospion = [self.ligne, self.colonne]  # position de départ du pion
        if self.couleur == "B":  # pion blanc
            color = pieceNoir  # couleur des pions adverses
            # déplacement possible pour manger une pièce
            deplacement = [[1, -1], [1, 1]]
            if pospion[0] == 1:  # si le pion est à sa position de départ et donc il peut bouger soit de 1 ou de 2 cases au choix
                i = 1
                while i <= 2:  # Pareil que pour le fou/tour/dame boucle avec un i que l'on va incrémenter
                    # le pion avance uniquement en self.ligne et pour le pion noir on incrémente de 1
                    row = pospion[0] + i
                    column = pospion[1]  # la self.colonne ne change pas
                    # si c'est dans l'échiquier et self.echiquier.Case_vide
                    if self.echiquier.Plateau_limit(row, column) and self.echiquier.Case_vide(row, column):
                        # on ajoute les coordonnées aux mouvements possibles
                        legalmoves.append([row, column])
                        i += 1
                    else:
                        break  # si la case n'est pas self.echiquier.Case_vide alors on arrête la boucle car le pion ne mange pas en self.ligne droite
                for possibilite in deplacement:  # on voit si une pièce est en diagonal
                    rowDestroy = pospion[0] + possibilite[0]
                    columnDestroy = pospion[1] + possibilite[1]

                    # si une pièce est en diagonal alors on peut manger cette pièce
                    if self.echiquier.Plateau_limit(rowDestroy, columnDestroy) and self.echiquier.plateau[rowDestroy][
                        columnDestroy] in color:
                        legalmoves.append([rowDestroy, columnDestroy])
            else:  # si le pion n'est pas en position de départ
                # mouvement basique de pion de 1 en 1 en self.ligne
                row = pospion[0] + 1
                column = pospion[1]
                if self.echiquier.Plateau_limit(row, column) and self.echiquier.Case_vide(row, column):
                    legalmoves.append([row, column])
                for possibilite in deplacement:
                    rowDestroy = pospion[0] + possibilite[0]
                    columnDestroy = pospion[1] + possibilite[1]
                    if self.echiquier.Plateau_limit(rowDestroy, columnDestroy) and self.echiquier.plateau[rowDestroy][
                        columnDestroy] in color:
                        legalmoves.append([rowDestroy, columnDestroy])

        else:  # Si le pion est noir
            color = pieceBlanc
            # le pion blanc fait l'inverse du noir c'est donc des -1 et non des 1
            deplacement = [[-1, -1], [-1, 1]]
            pospion = [self.ligne, self.colonne]
            if pospion[0] == 6:  # position de départ du pion blanc
                i = -1
                while i >= -2:
                    # On ajoute des nombres négatifs mais on aurait pu  soustraire des nombres positifs
                    row = pospion[0] + i
                    column = pospion[1]
                    if self.echiquier.Plateau_limit(row, column) and self.echiquier.Case_vide(row, column):
                        legalmoves.append([row, column])
                        i -= 1  # on décrémente car pion blanc donc inverse du pion noir
                    else:
                        break
                for possibilite in deplacement:
                    rowDestroy = pospion[0] + possibilite[0]
                    columnDestroy = pospion[1] + possibilite[1]
                    if self.echiquier.Plateau_limit(rowDestroy, columnDestroy) and self.echiquier.plateau[rowDestroy][
                        columnDestroy] in color:
                        legalmoves.append([rowDestroy, columnDestroy])
            else:  # si le pion n'est pas en position de départ donc mouvement normal
                row = pospion[0] - 1
                column = pospion[1]
                if self.echiquier.Plateau_limit(row, column) and self.echiquier.Case_vide(row, column):
                    legalmoves.append([row, column])
                for possibilite in deplacement:
                    rowDestroy = pospion[0] + possibilite[0]
                    columnDestroy = pospion[1] + possibilite[1]
                    if self.echiquier.Plateau_limit(rowDestroy, columnDestroy) and self.echiquier.plateau[rowDestroy][
                        columnDestroy] in color:
                        legalmoves.append([rowDestroy, columnDestroy])

        return [x_new, y_new] in legalmoves

    def promotion(self, x_new, y_new, nouvellePiece = ""):

        if (x_new == 0 and self.couleur == 'N') or (x_new == 7 and self.couleur == 'B'):

            valable = True
            while valable:
                if nouvellePiece == "":
                    promu = input("Veillez entrer le nom de la piece de rechange 'Tour','Dame','Cavalier','Fou' ")
                    valable = not (promu in ['Tour', 'Dame', 'Cavalier', 'Fou'])
                else:
                    promu = nouvellePiece

            self.ligne = x_new
            self.colonne = y_new
            for piece in self.echiquier:
                if piece.ligne == x_new and piece.colonne == y_new:
                    self.echiquier.remove(piece)
                if promu in ('Tour', "R"):
                    t = Tour(self.ligne, self.colonne, self.couleur, self.echiquier)
                    self.echiquier.append(t)
                elif promu in ('Cavalier', "N"):
                    t = Cavalier(self.ligne, self.colonne, self.couleur, self.echiquier)
                    self.echiquier.append(t)
                elif promu in ('Fou', "B"):
                    t = Fou(self.ligne, self.colonne, self.couleur, self.echiquier)
                    self.echiquier.append(t)
                elif promu in ('Dame', "Q"):
                    t = Dame(self.ligne, self.colonne, self.couleur, self.echiquier)
                    self.echiquier.append(t)


if __name__ == "__main__":
    ligne = 8
    colonne = 8

    echiquier1 = []
    tourB = Tour(0, 0, "B", echiquier1)
    cavalierB = Cavalier(0, 1, "B", echiquier1)
    fourB = Fou(0, 2, "B", echiquier1)
    dameB = Dame(0, 3, "B", echiquier1)
    roiB = Roi(0, 4, "B", echiquier1)
    fouB = Fou(0, 5, "B", echiquier1)
    pionB = Pion(1, 0, "B", echiquier1)

    tourN = Tour(7, 0, "N", echiquier1)
    cavalierN = Cavalier(7, 1, "N", echiquier1)
    fourN = Fou(7, 2, "N", echiquier1)
    dameN = Dame(7, 3, "N", echiquier1)
    roiN = Roi(7, 4, "N", echiquier1)
    fouN = Fou(7, 5, "N", echiquier1)
    pionN = Pion(6, 0, "N", echiquier1)
