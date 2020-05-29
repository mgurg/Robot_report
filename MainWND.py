#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QRadioButton

class Ui_Widget(object):
    def setupUi(self):
        
        self.reportBtn = QPushButton("&Generate TOOL/BASE report", self)
        koniecBtn = QPushButton("&Close app", self)
        koniecBtn.resize(koniecBtn.sizeHint())

        # Labels
        wwwLbl = QLabel()
        wwwLbl.setText('''<a href='https://roboticsbook.com/Robot-Utilities/'>Robot Utilities website - check for updates</a>''') 
        wwwLbl.setOpenExternalLinks(True)

        descLbl = QLabel()
        descLbl.setText("Generate reports from KUKA robot backups (*.zip)") 

        self.statusLbl = QLabel("Status", self)

        #Radiobutton
        vagRb = QRadioButton("VW (V)KRC - VASS")
        dagRb = QRadioButton("Daimler - Integra")
        miscRb= QRadioButton("KUKA KRC - General")

        
        ukladT = QGridLayout()
        ukladT.addWidget(descLbl, 1, 0, 1, 3)
        # ukladT.addWidget(miscRb, 2,0,1,3)
        # ukladT.addWidget(vagRb, 3,0,1,3)
        # ukladT.addWidget(dagRb, 4,0,1,3)
        ukladT.addWidget(self.statusLbl, 5, 0, 1, 3)
        ukladT.addWidget(self.reportBtn, 6, 0, 1, 3)
        ukladT.addWidget(koniecBtn, 7, 0, 1, 3)
        ukladT.addWidget(wwwLbl, 8,0,1,3)


        # przypisanie utworzonego układu do okna
        self.setLayout(ukladT)


        self.reportBtn.clicked.connect(self.generateReport)
        koniecBtn.clicked.connect(self.koniec)
        
        #self.liczba1Edt.setFocus()
        self.setGeometry(20, 20, 300, 100)
        self.setWindowIcon(QIcon('Robot_Icon.png'))
        self.setWindowTitle("Robot Utilities v0.3")
        self.show()