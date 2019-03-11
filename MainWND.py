#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QMessageBox



class Ui_Widget(object):
    def setupUi(self):
        

        self.reportBtn = QPushButton("&Generate TOOL/BASE report", self)
        koniecBtn = QPushButton("&Close app", self)
        koniecBtn.resize(koniecBtn.sizeHint())

        # Labels
        wwwLbl = QLabel()
        wwwLbl.setText('''<a href='https://roboticsbook.com/RobotReport/'>RobotReport website - check for updates</a>''') 
        wwwLbl.setOpenExternalLinks(True)

        descLbl = QLabel()
        descLbl.setText("Generate reports from KUKA robot backups (*.zip)") 

        self.statusLbl = QLabel("Status", self)
        
        ukladT = QGridLayout()
        ukladT.addWidget(descLbl, 1, 0, 1, 3)
        ukladT.addWidget(self.statusLbl, 2, 0, 1, 3)
        ukladT.addWidget(self.reportBtn, 3, 0, 1, 3)
        ukladT.addWidget(koniecBtn, 4, 0, 1, 3)
        ukladT.addWidget(wwwLbl, 5,0,1,3)

        # przypisanie utworzonego układu do okna
        self.setLayout(ukladT)


        self.reportBtn.clicked.connect(self.generateReport)
        koniecBtn.clicked.connect(self.koniec)
        
        #self.liczba1Edt.setFocus()
        self.setGeometry(20, 20, 300, 100)
        self.setWindowIcon(QIcon('Robot_Icon.png'))
        self.setWindowTitle("Robot Report v0.2")
        self.show()