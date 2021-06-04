# -*- coding: utf-8 -*-
import sys
import sys
from PyQt5.QtCore import Qt
from echiquier import *
from echiquier import Echiquier
from Piece import Pion, Roi, Fou,Tour, Dame, Cavalier, Pieces
from PyQt5 import QtGui, QtWidgets, uic, QtCore
import sys
from PyQt5.QtGui import QIcon
from Interface import Ui_menu_principal
from PyQt5.QtWidgets import (QAction, QFileDialog, QMenu,QToolBar)


class ChessUI(QtWidgets.QMainWindow):
    def __init__(self, ligne, colonne,*args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args)
        self.ui = Ui_menu_principal()
        self.ui.setupUi(self)
        self.echiquier = Echiquier(8,8)
        self.ligne = ligne
        self.colonne = colonne
        self.premierClick = True
        self.caseX1 = 0
        self.caseY1 = 0
        self.caseX0 = 0
        self.caseY0 = 0
        
        # self.setcentralWidget = (QtWidgets.QMainWindow)
        # self.menubar.setObjectName("menubar")
        pixmap = QtGui.QPixmap("ImagesN/board.png")
        pal = QtGui.QPalette()
        pal.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pixmap))
        self.ui.conteneur.lower()
        self.ui.conteneur.resize(640,640)
        self.ui.conteneur.stackUnder(self)
        self.ui.conteneur.setAutoFillBackground(True)
        self.ui.conteneur.setPalette(pal)
        # objet "peintre" pour les pieces
        self.painter = QtGui.QPainter()
        # self.resize(640,680)
        self.ui.conteneur.paintEvent = self.draw_chess  # "dessine_moi" se traduit par paintEvent
        # dico pour stocker les images
        self.img_dictN = {}
        self.img_dictB = {}
        self.setWindowIcon(QIcon('images/logo.png'))
        # print(self.ui.conteneur.width(), self.ui.conteneur.height())
        self.setWindowIcon(QIcon('images/chess.jfif'))
 

        # self.actionNew = QAction(
        #     QIcon.fromTheme('document-new',
        #                     QIcon('Images/filenew.png')),
        #     "&New", self, priority=QAction.LowPriority,
        #     shortcut=QKeySequence.New, triggered=self.fileNew)
        # tb.addAction(self.actionNew)
        # menu.addAction(self.actionNew)
        #
        # self.actionOpen = QAction(
        #     QIcon.fromTheme('document-open',
        #                     QIcon('Images/fileopen.png')),
        #     "&Open...", self, shortcut=QKeySequence.Open,
        #     triggered=self.fileOpen)
        # tb.addAction(self.actionOpen)
        # menu.addAction(self.actionOpen)
        # menu.addSeparator()
        #
        # self.actionSave = QAction(
        #     QIcon.fromTheme('document-save',
        #                     QIcon('Images/filesave.png')),
        #     "&Save", self, shortcut=QKeySequence.Save,
        #     triggered=self.fileSave, enabled=False)
        # tb.addAction(self.actionSave)
        # menu.addAction(self.actionSave)
        #
        # self.actionSaveAs = QAction("Save &As...", self,
        #                             priority=QAction.LowPriority,
        #                             shortcut=Qt.CTRL + Qt.SHIFT + Qt.Key_S,
        #                             triggered=self.fileSaveAs)
        # menu.addAction(self.actionSaveAs)
        # menu.addSeparator()
        #
        # self.actionPrint = QAction(
        #     QIcon.fromTheme('document-print',
        #                     QIcon('Images/fileprint.png')),
        #     "&Print...", self, priority=QAction.LowPriority,
        #     shortcut=QKeySequence.Print, triggered=self.filePrint)
        # tb.addAction(self.actionPrint)
        # menu.addAction(self.actionPrint)

    def createActions(self):
        self.newLetterAct = QAction(QIcon('images/new.png'), "&New Letter",
                self, shortcut=QKeySequence.New,
                statusTip="Create a new form letter", triggered=self.newLetter)

        self.saveAct = QAction(QIcon('images/save.png'), "&Save...", self,
                shortcut=QKeySequence.Save,
                statusTip="Save the current form letter", triggered=self.save)

        self.printAct = QAction(QIcon('images/print.png'), "&Print...", self,
                shortcut=QKeySequence.Print,
                statusTip="Print the current form letter",
                triggered=self.print_)

        self.undoAct = QAction(QIcon('images/undo.png'), "&Undo", self,
                shortcut=QKeySequence.Undo,
                statusTip="Undo the last editing action", triggered=self.undo)

        self.quitAct = QAction("&Quit", self, shortcut="Ctrl+Q",
                statusTip="Quit the application", triggered=self.close)

        self.aboutAct = QAction("&About", self,
                statusTip="Show the application's About box",
                triggered=self.about)

        self.aboutQtAct = QAction("About &Qt", self,
                statusTip="Show the Qt library's About box",
                triggered=QApplication.instance().aboutQt)

    def createMenus(self):
        self.fileMenu.addAction(self.newLetterAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAct)

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.undoAct)

        self.viewMenu = self.menuBar().addMenu("&View")

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def draw_chess(self, *args):
        # on informe le peintre qu'on veut dessiner dans le widget conteneur
        self.painter.begin(self.ui.conteneur)
        # variable intermédiraire pour alléger le code
        qp = self.painter
        # boucle pour parcourir les pieces et gérer les images (vu ci-dessus)
        cptN = 0
        i = 90
        cptB = 0
        for piece in self.echiquier:
            cls_name = piece.__class__.__name__
            if piece not in self.img_dictN:
                self.img_dictN[cls_name] = QtGui.QImage("ImagesN/" + cls_name + ".png")
            # self.img_dictN.pop()
            self.img_dictN[Pion] = QtGui.QImage("ImagesN/Pion.png")

            img1 = self.img_dictN[Pion]
            qp.drawImage(piece.x + cptN, piece.y + 480, img1)
            img = self.img_dictN[cls_name]
            # on demande au peintre d'afficher l'image aux coordonnées de la piece
            qp.drawImage(piece.x + cptN, piece.y + 565, img)
            cptN += i - 8
            # qp.drawImage(piece.ligne +100, piece.colonne +1000, img)
            if piece not in self.img_dictB:
                self.img_dictB[cls_name] = QtGui.QImage("ImagesB/" + cls_name + ".png")
            self.img_dictN[Pion] = QtGui.QImage("ImagesB/Pion.png")
            img2 = self.img_dictN[Pion]
            qp.drawImage(piece.x + cptB, piece.y + 80, img2)
            img = self.img_dictB[cls_name]
            # on demande au peintre d'afficher l'image aux coordonnées de la piece
            qp.drawImage(piece.x + cptB, piece.y + 2, img)
            cptB += i - 8
        # on informe le peintre qu'on a fini
        self.painter.end()


    def fileSaveAs(self):
        fn, _ = QFileDialog.getSaveFileName(self, "Save as...", None,
                                            "ODF files (*.pgn)")

        if not fn:
            return False

        lfn = fn.lower()
        if not lfn.endswith(('.odt', '.htm', '.html')):
            # The default.
            fn += '.pgn'

        self.setCurrentFileName(fn)
        return self.fileSave()

    def setupFileActions(self):
        self.actionNewGame = QAction(
                QIcon.fromTheme('Nouvelle Partie',
                        QIcon('chess1.png')),
                 self, priority=QAction.LowPriority,
                shortcut=Qt.CTRL + Qt.Key_N,
                triggered=self.NewGame)

    def Reset_Plateau(self):
        self.echiquier = Echiquier(8, 8)

    def mousePressEvent(self, event):
        """
        :param event:
        :return: genere le deplacement des pieces avec la sourie
        """
        coup = []
        x, y = event.x(), event.y()
        
        #la première case commence en y = 24 et la dernière finie en y = 664, chaque case fait 80 px de côté
        
        if self.premierClick :
            self.caseX0 = x // 80
            self.caseY0 = (y-24) // 80

            print(self.caseX0, self.caseY0)
            if self.echiquier.Case_vide(self.caseX0, self.caseY0):
                print('Aucune piece selectionnee')
            else:
                self.premierClick = False
        else :
            self.caseX1 = x // 80
            self.caseY1 = (y-24) // 80
            self.premierClick = True
            print(self.caseX1, self.caseY1)
        
            for piece in self.echiquier:
                if piece.ligne == self.caseX0 and piece.colonne == self.caseY0:
                    piece.deplacement(self.caseX1, self.caseY1)
                    valable = not piece.deplacement_ok
                    print(valable)
        
        		
        print(x,y)

        
        # x1, y1 = self.echiquier.ligne, self.echiquier.colonne
        # x2, y2 = self.ui.conteneur.width() , self.ui.conteneur.height()
        # for piece in self.echiquier:
        #     if x1 <= x <= x2 and y1 < y < y2:
        #         if event.button() == QtCore.Qt.LeftButton:
        #             d =(7 - (x // 105 - 1)),  (y // 105 - 1)
        #             coup.append(d)
        #             event = QtGui.QtMouseEvent(QtCore.QEvent.MouseButtonPress, event.pos(), QtCore.Qt.LeftButton,
        #                                        QtCore.Qt.LeftButton, QtCore.Qt.NoModifier)
        #             QtWidgets.QMainWindow.mousePressEvent(self,event)
        #
        #             if len(coup) == 2:
        #                 piece.deplacement_Valide(coup)
        #                 piece.deplacement(piece.deplacement_Valide)
        #                 coup = []






if __name__ == "__main__":
    # on créé une nouvelle application Qt
    app = QtWidgets.QApplication(sys.argv)
    # ici nous passons au constructeur de notre interface de jeu les
    # paramètres
    window = ChessUI(8,8)
    window.show()

    # et on lance l'application
    sys.exit(app.exec_())

