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
import re
import shutil
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

def get_name(path, n,tcp):

    i = len('%s_NAME[%s,]'%(tcp,n))

    sfile = path.open('KRC/R1/System/$config.dat','r')
    for sline in sfile.readlines():
        sline=sline.decode("utf-8") 
        if sline[0:i]=='%s_NAME[%s,]'%(tcp,n):
            return sline[i+1:].replace('"','').strip()
    return ''

def inplace_change(filename, old_string, new_string=''):
    # Safely read the input filename using 'with'
    with open(filename) as f:
        s = f.read()

    # Safely write the changed content, if found in the file
    with open(filename, 'w') as f:
        #print 'Changing "{old_string}" to "{new_string}" in {filename}'
        if len(new_string) == 0:
            s = re.sub(old_string, "", s)
            #s = s.replace(old_string, '') 
        else:
            s = re.sub(old_string, new_string, s, 1)
        f.write(s)

def write(filename):
    backup=zipfile.ZipFile('Output/OLP.docx','r')
    backup.extractall('Temp/')
    backup.close

    for i in range(64):
        if len(tcp[i]['x'])>0:
            inplace_change('Temp/word/document.xml','Tool_XX_TCP',tcp[i]['name'])

            inplace_change('Temp/word/document.xml','VAL_TCP_X',tcp[i]['x']) 
            inplace_change('Temp/word/document.xml','VAL_TCP_Y',tcp[i]['y']) 
            inplace_change('Temp/word/document.xml','VAL_TCP_Z',tcp[i]['z'])   

            inplace_change('Temp/word/document.xml','VAL_TCP_A',tcp[i]['a']) 
            inplace_change('Temp/word/document.xml','VAL_TCP_B',tcp[i]['b']) 
            inplace_change('Temp/word/document.xml','VAL_TCP_C',tcp[i]['c'])  

        if len(base[i]['x'])>0:
            inplace_change('Temp/word/document.xml','Base_XX',base[i]['name'])
            inplace_change('Temp/word/document.xml','V_BASE_X',tcp[i]['x']) 
            inplace_change('Temp/word/document.xml','V_BASE_Y',tcp[i]['y']) 
            inplace_change('Temp/word/document.xml','V_BASE_Z',tcp[i]['z'])   

            inplace_change('Temp/word/document.xml','V_BASE_A',tcp[i]['a']) 
            inplace_change('Temp/word/document.xml','V_BASE_B',tcp[i]['b']) 
            inplace_change('Temp/word/document.xml','V_BASE_C',tcp[i]['c']) 

    inplace_change('Temp/word/document.xml','Tool_XX_TCP',)
    inplace_change('Temp/word/document.xml','Base_XX',)

    inplace_change('Temp/word/document.xml','VAL_TCP_X',) 
    inplace_change('Temp/word/document.xml','VAL_TCP_Y',) 
    inplace_change('Temp/word/document.xml','VAL_TCP_Z',)   
    inplace_change('Temp/word/document.xml','VAL_TCP_A',) 
    inplace_change('Temp/word/document.xml','VAL_TCP_B',) 
    inplace_change('Temp/word/document.xml','VAL_TCP_C',)   

    inplace_change('Temp/word/document.xml','V_BASE_X',tcp[i]['x']) 
    inplace_change('Temp/word/document.xml','V_BASE_Y',tcp[i]['y']) 
    inplace_change('Temp/word/document.xml','V_BASE_Z',tcp[i]['z'])   

    inplace_change('Temp/word/document.xml','V_BASE_A',tcp[i]['a']) 
    inplace_change('Temp/word/document.xml','V_BASE_B',tcp[i]['b']) 
    inplace_change('Temp/word/document.xml','V_BASE_C',tcp[i]['c']) 


    backup = zipfile.ZipFile(filename+'.docx', 'w')
    for folder, subfolders, files in os.walk('Temp\\'):
 
        for file in files:
            backup.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), 'Temp\\'), compress_type = zipfile.ZIP_DEFLATED)
    backup.close()

    shutil.rmtree('Temp/') 

#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# MAIN PROGRAM
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX        

start_time = time.time()

backupsdir = 'Backup'
files = os.listdir(backupsdir)

for filename in files:
    if '.zip' in filename:
        print('Working on %s'%(filename))
        backup=zipfile.ZipFile('%s/%s'%(backupsdir,filename),'r')
        name=filename.replace('.zip','')


        tcp={}
        base={}
        programs={}

        for i in range(64):
            tcp[i]=empty_coords()
            base[i]=empty_coords()

        searchfile = backup.open('KRC/R1/System/$config.dat','r')
        
        for line in searchfile.readlines():
            line = line.decode("utf-8") 
            if line[0:9]=='TOOL_DATA':  #search for TOOL_DATA
                fnum=int(line[10:line.find(']')]) # obtain Tool No
                if (fnum<=64 and not ('{X 0.0,Y 0.0,Z 0.0,A 0.0,B 0.0,C 0.0}' in line)):
                    tcp[fnum]=get_coords(line)
                    tcp[fnum]['name']=get_name(backup,fnum,'TOOL')
                            
            if line[0:9]=='BASE_DATA':
                fnum=int(line[10:line.find(']')])
                if (fnum<32 and not ('{X 0.0,Y 0.0,Z 0.0,A 0.0,B 0.0,C 0.0}' in line)):
                    base[fnum]=get_coords(line)
                    base[fnum]['name']=get_name(backup,fnum,'BASE')

        searchfile.close()
        write(name)


print('TOOLS')
for i in range(64):
    if len(tcp[i]['x'])>0:
        print(tcp[i])

print('BASE')
for i in range(64):
    if len(base[i]['x'])>0:
        print(base[i])



print("--- %s seconds ---" % (time.time() - start_time))

    


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
    
    
    