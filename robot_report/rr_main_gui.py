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
        exitBtn = QPushButton("&Close app", self)
        exitBtn.resize(exitBtn.sizeHint())

        # Labels
        wwwLbl = QLabel()
        wwwLbl.setText('''<a href='https://roboticsbook.com/Robot-Utilities/'>Robot Utilities website - check for updates</a>''')
        wwwLbl.setOpenExternalLinks(True)

        descLbl = QLabel()
        descLbl.setText("Generate reports from KUKA robot backups (*.zip)")

        self.statusLbl = QLabel("Status", self)

        vagRb = QRadioButton("VW (V)KRC - VASS")
        dagRb = QRadioButton("Daimler - Integra")
        miscRb= QRadioButton("KUKA KRC - General")

        appLayout = QGridLayout()
        appLayout.addWidget(descLbl, 1, 0, 1, 3)
        appLayout.addWidget(self.statusLbl, 5, 0, 1, 3)
        appLayout.addWidget(self.reportBtn, 6, 0, 1, 3)
        appLayout.addWidget(exitBtn, 7, 0, 1, 3)
        appLayout.addWidget(wwwLbl, 8,0,1,3)

        # przypisanie utworzonego układu do okna
        self.setLayout(appLayout)

        self.reportBtn.clicked.connect(self.generate_report)
        exitBtn.clicked.connect(self.close_app)

        self.setGeometry(20, 20, 300, 100)
        self.setWindowIcon(QIcon('robot_icon.png'))
        self.setWindowTitle("Robot Utilities v0.3")
        self.show()