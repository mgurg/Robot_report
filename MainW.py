# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 20:48:39 2017

@author: Michal
"""

import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton
from PyQt5.uic import loadUi


class MainWND(QMainWindow):
    def __init__(self):
        super(MainWND,self).__init__()
        loadUi('MainWND.ui', self)
        self.setWindowTitle('Aaa')
        self.btn_OK.clicked.connect(self.printham)
        
        
    def printham(self):
        f_path = 'Backup/$config.dat'
    
        with open(f_path) as f:
            lines = list(f)
        
        for x in range(181, 212):
            #tcp[x]=get_coords(lines[x])
            print(lines[x])
            #print (tcp[x])
    
        f.close()
        
        
#---------------END OF GUI--------------
        
    def empty_coords():
        coords={}
        coords['x']=''
        coords['y']=''
        coords['z']=''
        coords['a']=''
        coords['b']=''
        coords['c']=''
        coords['name']=''
        return coords

    def get_coords(line):
        coords={}
        line=line[13:].replace('}',',')
        coords['x']=get_coord(line,'X')
        coords['y']=get_coord(line,'Y')
        coords['z']=get_coord(line,'Z')
        coords['a']=get_coord(line,'A')
        coords['b']=get_coord(line,'B')
        coords['c']=get_coord(line,'C')
        return coords
        
        
    def get_coord(line,coord):
        pos=line.find(coord)+1
        return round_coord(line[pos:line[pos:].find(',')+pos])
        
        def round_coord(text):
            return str(round(float(text),3))
        
    tcp={}
    base={}
    programs={}
    for i in range(10):
        tcp[i]=empty_coords()
        #print (tcp[i])
        base[i]=empty_coords()

        
    def openf(self):
        f_path = 'Backup/$config.dat'
    
        with open(f_path) as f:
            lines = list(f)
        
        for x in range(181, 212):
            tcp[x]=get_coords(lines[x])
            print(lines[x])
            print (tcp[x])
    
        f.close()
        
app = QApplication(sys.argv)
w = MainWND()
w.show()
sys.exit(app.exec_())        
