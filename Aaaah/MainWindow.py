# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created: Sun Oct 27 17:02:27 2013
#      by: PyQt5 UI code generator 5.1.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(1000, 630)
        MainWindow.setMinimumSize(QtCore.QSize(1000, 630))
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.map_view = QtWidgets.QGraphicsView(self.centralwidget)
        self.map_view.setGeometry(QtCore.QRect(10, 10, 800, 400))
        self.map_view.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.map_view.setMouseTracking(True)
        self.map_view.setAutoFillBackground(False)
        self.map_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.map_view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.map_view.setRenderHints(QtGui.QPainter.Antialiasing)
        self.map_view.setObjectName("map_view")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 420, 111, 181))
        self.groupBox.setObjectName("groupBox")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 85, 107))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.line = QtWidgets.QRadioButton(self.layoutWidget)
        self.line.setEnabled(True)
        self.line.setMouseTracking(False)
        self.line.setChecked(True)
        self.line.setObjectName("line")
        self.primitives_group = QtWidgets.QButtonGroup(MainWindow)
        self.primitives_group.setObjectName("primitives_group")
        self.primitives_group.addButton(self.line)
        self.verticalLayout.addWidget(self.line)
        self.curve = QtWidgets.QRadioButton(self.layoutWidget)
        self.curve.setEnabled(True)
        self.curve.setMouseTracking(False)
        self.curve.setObjectName("curve")
        self.primitives_group.addButton(self.curve)
        self.verticalLayout.addWidget(self.curve)
        self.rectangle = QtWidgets.QRadioButton(self.layoutWidget)
        self.rectangle.setEnabled(True)
        self.rectangle.setMouseTracking(False)
        self.rectangle.setObjectName("rectangle")
        self.primitives_group.addButton(self.rectangle)
        self.verticalLayout.addWidget(self.rectangle)
        self.ellipse = QtWidgets.QRadioButton(self.layoutWidget)
        self.ellipse.setEnabled(True)
        self.ellipse.setMouseTracking(False)
        self.ellipse.setObjectName("ellipse")
        self.primitives_group.addButton(self.ellipse)
        self.verticalLayout.addWidget(self.ellipse)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 130, 46, 21))
        self.label.setObjectName("label")
        self.thickness = QtWidgets.QSpinBox(self.groupBox)
        self.thickness.setGeometry(QtCore.QRect(60, 130, 42, 22))
        self.thickness.setMinimum(1)
        self.thickness.setMaximum(10000)
        self.thickness.setProperty("value", 1)
        self.thickness.setObjectName("thickness")
        self.isFull = QtWidgets.QCheckBox(self.groupBox)
        self.isFull.setGeometry(QtCore.QRect(10, 160, 81, 17))
        self.isFull.setObjectName("isFull")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(820, 10, 171, 121))
        self.groupBox_2.setObjectName("groupBox_2")
        self.layoutWidget1 = QtWidgets.QWidget(self.groupBox_2)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 20, 101, 89))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.clipboard = QtWidgets.QPushButton(self.layoutWidget1)
        self.clipboard.setObjectName("clipboard")
        self.verticalLayout_2.addWidget(self.clipboard)
        self.file = QtWidgets.QPushButton(self.layoutWidget1)
        self.file.setEnabled(False)
        self.file.setCheckable(False)
        self.file.setObjectName("file")
        self.verticalLayout_2.addWidget(self.file)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(820, 140, 171, 181))
        self.groupBox_3.setObjectName("groupBox_3")
        self.ruler = QtWidgets.QCheckBox(self.groupBox_3)
        self.ruler.setGeometry(QtCore.QRect(10, 20, 70, 17))
        self.ruler.setObjectName("ruler")
        self.opacity = QtWidgets.QSlider(self.groupBox_3)
        self.opacity.setGeometry(QtCore.QRect(10, 70, 141, 20))
        self.opacity.setMaximum(90)
        self.opacity.setOrientation(QtCore.Qt.Horizontal)
        self.opacity.setObjectName("opacity")
        self.label_2 = QtWidgets.QLabel(self.groupBox_3)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 51, 16))
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 21))
        self.menubar.setMouseTracking(False)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Maaaahp Toolkit"))
        self.groupBox.setTitle(_translate("MainWindow", "Formes primitives"))
        self.line.setText(_translate("MainWindow", "Ligne"))
        self.curve.setText(_translate("MainWindow", "Courbe"))
        self.rectangle.setText(_translate("MainWindow", "Rectangle"))
        self.ellipse.setText(_translate("MainWindow", "Ellipse"))
        self.label.setText(_translate("MainWindow", "Epaisseur"))
        self.isFull.setText(_translate("MainWindow", "Forme Pleine"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Copier vers"))
        self.clipboard.setText(_translate("MainWindow", "Presse papiers"))
        self.file.setText(_translate("MainWindow", "Fichier ..."))
        self.groupBox_3.setTitle(_translate("MainWindow", "Affichage"))
        self.ruler.setText(_translate("MainWindow", "Règle"))
        self.label_2.setText(_translate("MainWindow", "Opacité :"))

