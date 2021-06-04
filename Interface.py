# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_menu_principal(object):
    def setupUi(self, menu_principal):
        menu_principal.setObjectName("menu_principal")
        menu_principal.setMinimumSize(QtCore.QSize(640,690))
        menu_principal.setMaximumSize(QtCore.QSize(640,690))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/chess1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        menu_principal.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(menu_principal)
        self.centralwidget.setObjectName("centralwidget")
        self.conteneur = QtWidgets.QWidget(self.centralwidget)
        self.conteneur.setGeometry(QtCore.QRect(0, 0, 640, 640))
        self.conteneur.setObjectName("conteneur")
        menu_principal.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(menu_principal)
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        menu_principal.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(menu_principal)
        self.statusbar.setObjectName("statusbar")
        menu_principal.setStatusBar(self.statusbar)
        self.actionNew = QtWidgets.QAction(menu_principal)
        self.actionNew.setCheckable(False)
        self.actionNew.setEnabled(True)
        self.actionNew.setShortcutVisibleInContextMenu(False)
        self.actionNew.setObjectName("actionNew")
        self.actionQuiter = QtWidgets.QAction(menu_principal)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("images/quitter.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionQuiter.setIcon(icon1)
        self.actionQuiter.setObjectName("actionQuiter")
        self.actionSave = QtWidgets.QAction(menu_principal)
        self.actionSave.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_As = QtWidgets.QAction(menu_principal)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionOpen = QtWidgets.QAction(menu_principal)
        self.actionOpen.setObjectName("actionOpen")
        self.menuMenu.addAction(self.actionNew)
        self.menuMenu.addAction(self.actionOpen)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionSave)
        self.menuMenu.addAction(self.actionSave_As)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionQuiter)
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(menu_principal)
        self.actionQuiter.triggered.connect(menu_principal.close)
        self.actionNew.triggered.connect(self.actionNew.trigger)
        self.actionOpen.triggered.connect(self.actionOpen.trigger)
        self.actionSave.triggered.connect(self.actionSave.trigger)
        QtCore.QMetaObject.connectSlotsByName(menu_principal)

    def retranslateUi(self, menu_principal):
        _translate = QtCore.QCoreApplication.translate
        menu_principal.setWindowTitle(_translate("menu_principal", "Chess"))
        self.menuMenu.setTitle(_translate("menu_principal", "File"))
        self.actionNew.setText(_translate("menu_principal", "New "))
        self.actionNew.setIconText(_translate("menu_principal", "New"))
        self.actionNew.setShortcut(_translate("menu_principal", "Ctrl+N"))
        self.actionQuiter.setText(_translate("menu_principal", "Quit"))
        self.actionSave.setText(_translate("menu_principal", "Save "))
        self.actionSave.setShortcut(_translate("menu_principal", "Ctrl+S"))
        self.actionSave_As.setText(_translate("menu_principal", "Save As.."))
        self.actionSave_As.setShortcut(_translate("menu_principal", "Ctrl+Shift+S"))
        self.actionOpen.setText(_translate("menu_principal", "Open"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    menu_principal = QtWidgets.QMainWindow()
    ui = Ui_menu_principal()
    ui.setupUi(menu_principal)
    menu_principal.show()
    sys.exit(app.exec_())
