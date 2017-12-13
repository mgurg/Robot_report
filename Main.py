#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Michal Gurgul
Website: -
Last edited: August 2017
"""

import sys
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QPushButton
import os,zipfile
import time
#from MainWND import Ui_MainWindow

# Create empty table (x, y, z, a, b, c, name)
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

# Fill table with values
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

# Find sign: X, Y, Z etc. in line  
# Search for value till "," sign
# Return round value 
def get_coord(line,coord):
    pos=line.find(coord)+1
    return round_coord(line[pos:line[pos:].find(',')+pos])

def round_coord(text):
    return str(round(float(text),3))

def get_name(n,tcp):
    i = len('%s_NAME[%s,]'%(tcp,n))

    sfile = open("Backup/$config.dat", "r")
    for sline in sfile.readlines():
        if sline[0:i]=='%s_NAME[%s,]'%(tcp,n):
            return sline[i+1:].replace('"','').strip()
    return ''

tcp={}
base={}
programs={}
for i in range(64):
    tcp[i]=empty_coords()
    base[i]=empty_coords()
    

#def get_name(backup, n,tcp):
#    curfile = backup.open('Backup/$config.dat','r')

searchfile = open("Backup/$config.dat", "r")
for line in searchfile:
    if line[0:9]=='TOOL_DATA':  #search for TOOL_DATA
        fnum=int(line[10:line.find(']')]) # obtain Tool No
        if (fnum<=64 and not ('{X 0.0,Y 0.0,Z 0.0,A 0.0,B 0.0,C 0.0}' in line)):
            tcp[fnum]=get_coords(line)
            tcp[fnum]['name']=get_name(fnum,'TOOL')
                    
    if line[0:9]=='BASE_DATA':
        fnum=int(line[10:line.find(']')])
        if (fnum<32 and not ('{X 0.0,Y 0.0,Z 0.0,A 0.0,B 0.0,C 0.0}' in line)):
            base[fnum]=get_coords(line)
            base[fnum]['name']=get_name(fnum,'BASE')

searchfile.close()

print(tcp[1])
print(tcp[2])
print(tcp[19])

print(base[1])
    

def inplace_change(filename, old_string, new_string):
    # Safely read the input filename using 'with'
    with open(filename) as f:
        s = f.read()

    # Safely write the changed content, if found in the file
    with open(filename, 'w') as f:
        #print 'Changing "{old_string}" to "{new_string}" in {filename}'
        s = s.replace(old_string, new_string)
        f.write(s)

    
def write():
    start_time = time.time()

    backup=zipfile.ZipFile('Output/OLP.docx','r')
    backup.extractall('Temp/')
    backup.close

    inplace_change('Temp/word/document.xml','GRP_01','ALA')

    backup = zipfile.ZipFile('archive.docx', 'w')
    for folder, subfolders, files in os.walk('Temp\\'):
 
        for file in files:
            backup.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), 'Temp\\'), compress_type = zipfile.ZIP_DEFLATED)
    backup.close()

    print("--- %s seconds ---" % (time.time() - start_time))

    
#write()
 



# class AppWindow(QMainWindow):
#    def __init__(self):
#        super().__init__()
#        self.ui = Ui_MainWindow()
#        self.ui.setupUi(self)
#        self.show() 
        

#app = QApplication(sys.argv)
#w = AppWindow()
#w.show()
#sys.exit(app.exec_())
    
    
    