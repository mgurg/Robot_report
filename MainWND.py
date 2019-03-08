#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QGridLayout
from PyQt5.QtWidgets import QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
import os

class Ui_Widget(object):
    def interfejs(self):
        
        # etykiety
        etykieta1 = QLabel("Backups:", self)
        etykieta2 = QLabel("Template:", self)
        etykieta3 = QLabel("Output:", self)

        # przypisanie widgetów do układu tabelarycznego
        ukladT = QGridLayout()
        ukladT.addWidget(etykieta1, 0, 0)
        ukladT.addWidget(etykieta2, 0, 1)
        ukladT.addWidget(etykieta3, 0, 2)

        # 1-liniowe pola edycyjne
        self.liczba1Edt = QLineEdit("text", self)
        self.liczba2Edt = QLineEdit(os.getcwd())
        self.wynikEdt = QLineEdit()

        self.wynikEdt.readonly = True
        self.wynikEdt.setToolTip('test <b>message</b>')

        ukladT.addWidget(self.liczba1Edt, 1, 0)
        ukladT.addWidget(self.liczba2Edt, 1, 1)
        ukladT.addWidget(self.wynikEdt, 1, 2)

        # przyciski
        dodajBtn = QPushButton("&Add", self)
        odejmijBtn = QPushButton("&Remove", self)
        dzielBtn = QPushButton("&Multiply", self)
        mnozBtn = QPushButton("&Division", self)
        reportBtn = QPushButton("&Generate", self)
        koniecBtn = QPushButton("&Close app", self)
        koniecBtn.resize(koniecBtn.sizeHint())



        ukladH = QHBoxLayout()
        ukladH.addWidget(dodajBtn)
        ukladH.addWidget(odejmijBtn)
        ukladH.addWidget(dzielBtn)
        ukladH.addWidget(mnozBtn)

        ukladT.addLayout(ukladH, 2, 0, 1, 3)
        ukladT.addWidget(reportBtn, 3, 0, 1, 3)
        ukladT.addWidget(koniecBtn, 4, 0, 1, 3)

        # przypisanie utworzonego układu do okna
        self.setLayout(ukladT)

        #dodajBtn.clicked.connect(self.dzialanie)
        #odejmijBtn.clicked.connect(self.dzialanie)
        #mnozBtn.clicked.connect(self.dzialanie)
        #dzielBtn.clicked.connect(self.dzialanie)

        reportBtn.clicked.connect(self.generateReport)
        koniecBtn.clicked.connect(self.koniec)
        
        self.liczba1Edt.setFocus()
        self.setGeometry(20, 20, 300, 100)
        self.setWindowIcon(QIcon('Robot_Icon.png'))
        self.setWindowTitle("Robot Report V0.2")
        self.show()