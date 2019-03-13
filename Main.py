#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Michal Gurgul
Website: -
Version: 0.3 dev
Last edited: March 2019
"""

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QMessageBox
from MainWND import Ui_Widget

import sys
import os,zipfile
import time
import re
import shutil

#TODO:


class RobotReport(QWidget, Ui_Widget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi()

    # Obsługa zamkniecia - przycisk koniec
    def koniec(self):
        self.close()

    def generateReport(self):
        self.reportBtn.setEnabled(False)
        # self.reportBtn.update()
        self.reportBtn.repaint()

        calculations(self) # https://stackoverflow.com/questions/40027221/how-to-connect-pyqt-signal-to-external-function/40027367#40027367

        self.reportBtn.setEnabled(True)

    # przechwycenie zamkniecia - MessageBox
    def closeEvent(self, event):

        odp = QMessageBox.question(
            self, 'Message',
            "Do you want to close the application?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if odp == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # zamykanie przez ESC
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()


# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

def calculations(obj):
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
        pos=line.find(coord)+len(coord)
        return round_coord(line[pos:line[pos:].find(',')+pos])

    def get_jcoord(line,coord):
        pos=line.find(coord)+len(coord)
        return line[pos:line[pos:].find(',')+pos]

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

    def empty_guebergabe():
        guebergabe={}
        guebergabe['A1']=''
        guebergabe['A2']=''
        guebergabe['A3']=''
        guebergabe['A4']=''
        guebergabe['A5']=''
        guebergabe['A6']=''
        guebergabe['E1']=''
        guebergabe['name']=''
        return guebergabe

    def get_guebergabe(line):
        guebergabe={}
        #line=line[13:].replace('}',',')
        guebergabe['A1']=get_jcoord(line,'A1')
        guebergabe['A2']=get_jcoord(line,'A2')
        guebergabe['A3']=get_jcoord(line,'A3')
        guebergabe['A4']=get_jcoord(line,'A4')
        guebergabe['A5']=get_jcoord(line,'A5')
        guebergabe['A6']=get_jcoord(line,'A6')
        guebergabe['E1']=get_jcoord(line,'E1')
        return guebergabe

    # guebergabe={}
    # filename = "Backup/user_global.dat"
    # searchfile = open(filename, "r")
    # for line in searchfile:
    #     if line[19:30] == "XGUEBERGABE":
    #         fnum=int(line[30:line.find("=")-1])
    #         guebergabe[fnum]=get_guebergabe(line[30:])
    #         guebergabe[fnum]['name'] = 'GU'+str(fnum)
    #         print(guebergabe[fnum])


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
        backup=zipfile.ZipFile('ReportTemplate/OLP.docx','r')
        backup.extractall('Temp/')
        backup.close

        for i in range(64):
            if len(tcp[i]['x'])>0:
                inplace_change('Temp/word/document.xml','T_ID',str(i))

                inplace_change('Temp/word/document.xml','TCP_N',tcp[i]['name'])

                inplace_change('Temp/word/document.xml','TCP_X',tcp[i]['x']) 
                inplace_change('Temp/word/document.xml','TCP_Y',tcp[i]['y']) 
                inplace_change('Temp/word/document.xml','TCP_Z',tcp[i]['z'])   

                inplace_change('Temp/word/document.xml','TCP_A',tcp[i]['a']) 
                inplace_change('Temp/word/document.xml','TCP_B',tcp[i]['b']) 
                inplace_change('Temp/word/document.xml','TCP_C',tcp[i]['c'])  

            if len(base[i]['x'])>0:
                inplace_change('Temp/word/document.xml','B_ID',str(i))

                inplace_change('Temp/word/document.xml','BASE_N',base[i]['name'])
                inplace_change('Temp/word/document.xml','BASE_X',base[i]['x']) 
                inplace_change('Temp/word/document.xml','BASE_Y',base[i]['y']) 
                inplace_change('Temp/word/document.xml','BASE_Z',base[i]['z'])   

                inplace_change('Temp/word/document.xml','BASE_A',base[i]['a']) 
                inplace_change('Temp/word/document.xml','BASE_B',base[i]['b']) 
                inplace_change('Temp/word/document.xml','BASE_C',base[i]['c']) 

        inplace_change('Temp/word/document.xml','TCP_N',)
        inplace_change('Temp/word/document.xml','T_ID',)
        inplace_change('Temp/word/document.xml','TCP_X') 
        inplace_change('Temp/word/document.xml','TCP_Y') 
        inplace_change('Temp/word/document.xml','TCP_Z')   
        inplace_change('Temp/word/document.xml','TCP_A') 
        inplace_change('Temp/word/document.xml','TCP_B') 
        inplace_change('Temp/word/document.xml','TCP_C')  

        inplace_change('Temp/word/document.xml','BASE_N',)
        inplace_change('Temp/word/document.xml','B_ID',)
        inplace_change('Temp/word/document.xml','BASE_X',) 
        inplace_change('Temp/word/document.xml','BASE_Y',) 
        inplace_change('Temp/word/document.xml','BASE_Z',)   
        inplace_change('Temp/word/document.xml','BASE_A',) 
        inplace_change('Temp/word/document.xml','BASE_B',) 
        inplace_change('Temp/word/document.xml','BASE_C',) 


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

    backupsdir = 'Backups'
    files = os.listdir(backupsdir)



    for filename in files:
        if ('.zip' in filename): #and (len("gg") >5)
            print('Working on %s'%(filename))

            obj.statusLbl.setText('Working on %s'%(filename))
            obj.statusLbl.repaint()

            backup=zipfile.ZipFile('%s/%s'%(backupsdir,filename),'r')
            name=filename.replace('.zip','')


            tcp={}
            base={}
            programs={}

            for i in range(64):
                tcp[i]=empty_coords()
                base[i]=empty_coords()

            searchfile = backup.open('KRC/R1/System/$config.dat','r')
            
            #   REgexp example
            #   old method performance: ~0,92 - 1.0054 sec
            #   https://stackoverflow.com/questions/6186938/python-how-to-use-regexp-on-file-line-by-line-in-python

            #otp = searchfile
            #data = otp.read()
            #print(data)

            for line in searchfile.readlines():
                line = line.decode("utf-8") 
                if line[0:9]=='TOOL_DATA':  #search for TOOL_DATA
                    fnum=int(line[10:line.find(']')]) # obtain Tool No
                    if (fnum<=64 and not ('{X 0.0,Y 0.0,Z 0.0,A 0.0,B 0.0,C 0.0}' in line)):
                        tcp[fnum]=get_coords(line)
                        tcp[fnum]['name']=get_name(backup,fnum,'TOOL')
                                
                if line[0:9]=='BASE_DATA':
                    fnum=int(line[10:line.find(']')])
                    if (fnum<64 and not ('{X 0.0,Y 0.0,Z 0.0,A 0.0,B 0.0,C 0.0}' in line)):
                        base[fnum]=get_coords(line)
                        base[fnum]['name']=get_name(backup,fnum,'BASE')

            searchfile.close()
            
            write(name)


    print('TOOLS')
    for i in range(64):
        if len(tcp[i]['x']) > 0:
            print(tcp[i])

    # print('BASE')
    # for i in range(64):
    #     if len(base[i]['x']) > 0:
    #         print(base[i])

    # guebergabe={}

    # print('GU')
    # for i in range(30):
    #     print(guebergabe[i])


    print("")
    print("----- %s seconds -----" % (time.time() - start_time))
    print("Everything is done. This window will close in 3 sec")
    print("")
    print("=================================================")
    print("Robot Report v0.1. Check for updates at:")
    print("        www.fabryka-robotow.pl")
    #time.sleep(3)
    #obj.wynikEdt.setText('results') 


# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX    

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    Form = RobotReport()
    sys.exit(app.exec_())
