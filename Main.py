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

    def get_coords2(line):
        coords={}

        #  X\s(.*?),|Y\s(.*?),|Z\s(.*?),|A\s(.*?),|B\s(.*?),|C\s(.*?)}
        #XYZABC = re.findall('X\s(.*?),|Y\s(.*?),|Z\s(.*?),|A\s(.*?),|B\s(.*?),|C\s(.*?)}',line)
        #print(XYZABC)        
        #X = str(XYZABC.group(1))  
        #Y = str(XYZABC.group(2)) 
        #print (X + '   '+ Y)

        XX = re.search("X\s(.*?),", line)
        YY = re.search("Y\s(.*?),", line)
        ZZ = re.search("Z\s(.*?),", line)
        AA = re.search("A\s(.*?),", line)
        BB = re.search("B\s(.*?),", line)
        CC = re.search("C\s(.*?)}", line)

        coords['x']=str(XX.group(1))
        coords['y']=str(YY.group(1))
        coords['z']=str(ZZ.group(1))
        coords['a']=str(AA.group(1))
        coords['b']=str(BB.group(1))
        coords['c']=str(CC.group(1))
        return coords

    def get_name2(line):
        NN = re.search('[\"]([a-zA-Z0-9 ]+)',line) # any char (space included)   
        return str(NN.group(1))

    def get_folges(backup):
        flist={}
        path='KRC/R1/Folgen/'
        for ifile in backup.namelist():
            if ifile[0:len(path)]==path:
                if ifile[len(ifile)-4:].lower()=='.src':
                    filename = ifile[len(path):len(ifile)-4].upper()
                if filename!='CELL':
                    flist[filename]=get_program(backup,ifile,filename)
        return flist

    def get_ups(backup):
        flist={}
        path='KRC/R1/UPs/'
        for ifile in backup.namelist():
            if ifile[0:len(path)]==path:
                if ifile[len(ifile)-4:].lower()=='.src':
                    filename = ifile[len(path):len(ifile)-4].upper()
                    flist[filename]=get_program(backup,ifile,filename)
        return flist

    # def get_jcoord(line,coord):
    #     pos=line.find(coord)+len(coord)
    #     return line[pos:line[pos:].find(',')+pos]

    # def round_coord(text):
    #     return str(round(float(text),3))

    # def empty_guebergabe():
    #     guebergabe={}
    #     guebergabe['A1']=''
    #     guebergabe['A2']=''
    #     guebergabe['A3']=''
    #     guebergabe['A4']=''
    #     guebergabe['A5']=''
    #     guebergabe['A6']=''
    #     guebergabe['E1']=''
    #     guebergabe['name']=''
    #     return guebergabe

    # def get_guebergabe(line):
    #     guebergabe={}
    #     #line=line[13:].replace('}',',')
    #     guebergabe['A1']=get_jcoord(line,'A1')
    #     guebergabe['A2']=get_jcoord(line,'A2')
    #     guebergabe['A3']=get_jcoord(line,'A3')
    #     guebergabe['A4']=get_jcoord(line,'A4')
    #     guebergabe['A5']=get_jcoord(line,'A5')
    #     guebergabe['A6']=get_jcoord(line,'A6')
    #     guebergabe['E1']=get_jcoord(line,'E1')
    #     return guebergabe

    # guebergabe={}
    # filename = "Backup/user_global.dat"
    # searchfile = open(filename, "r")
    # for line in searchfile:
    #     if line[19:30] == "XGUEBERGABE":
    #         fnum=int(line[30:line.find("=")-1])
    #         guebergabe[fnum]=get_guebergabe(line[30:])
    #         guebergabe[fnum]['name'] = 'GU'+str(fnum)
    #         print(guebergabe[fnum])


    # def inplace_change(filename, old_string, new_string=''): #   old method performance: ~0,75 sec
        # Safely read the input filename using 'with'
        # with open(filename) as f:
        #     s = f.read()

        # Safely write the changed content, if found in the file
        # with open(filename, 'w') as f:
            #print 'Changing "{old_string}" to "{new_string}" in {filename}'
            # if len(new_string) == 0:
            #     s = re.sub("T_ID|TCP_N|TCP_X|TCP_Y|TCP_Z|TCP_A|TCP_B|TCP_C|B_ID|BASE_N|BASE_X|BASE_Y|BASE_Z|BASE_A|BASE_B|BASE_C", "", s) #clear all unused
            # else:
            #     s = re.sub(old_string, new_string, s, 1)
            # f.write(s)

    def write(filename):
        backup=zipfile.ZipFile('ReportTemplate/OLP.docx','r')
        backup.extractall('Temp/')
        backup.close

        sfile = open('Temp/word/document.xml','r')
        data = sfile.read()
        sfile.close()

        for i in tcp:
            if len(tcp[i]['x'])>0:
                data = re.sub('T_ID', str(i), data, 1)
                data = re.sub('TCP_N', tcp[i]['name'], data, 1)
                data = re.sub('TCP_X', tcp[i]['x'], data, 1)
                data = re.sub('TCP_Y', tcp[i]['y'], data, 1)
                data = re.sub('TCP_Z', tcp[i]['z'], data, 1)
                data = re.sub('TCP_A', tcp[i]['a'], data, 1)
                data = re.sub('TCP_B', tcp[i]['b'], data, 1)
                data = re.sub('TCP_C', tcp[i]['c'], data, 1)

        for i in base:
            if len(base[i]['x'])>0:
                data = re.sub('B_ID', str(i), data, 1)
                data = re.sub('BASE_N', base[i]['name'], data, 1)
                data = re.sub('BASE_X', base[i]['x'], data, 1)
                data = re.sub('BASE_Y', base[i]['y'], data, 1)
                data = re.sub('BASE_Z', base[i]['z'], data, 1)
                data = re.sub('BASE_A', base[i]['a'], data, 1)
                data = re.sub('BASE_B', base[i]['b'], data, 1)
                data = re.sub('BASE_C', base[i]['c'], data, 1)

        data = re.sub('T_ID|TCP_N|TCP_X|TCP_Y|TCP_Z|TCP_A|TCP_B|TCP_C|B_ID|BASE_N|BASE_X|BASE_Y|BASE_Z|BASE_A|BASE_B|BASE_C', '', data) #clear all unused
        
        f= open("Temp/word/document.xml","w+")
        f.write(data)
        f.close()

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

    tcp={}
    base={}

    for filename in files:
        if ('.zip' in filename):
            print('Working on %s'%(filename))

            obj.statusLbl.setText('Working on %s'%(filename))
            obj.statusLbl.repaint()

            backup=zipfile.ZipFile('%s/%s'%(backupsdir,filename),'r')
            name=filename.replace('.zip','')

            searchfile = backup.open('KRC/R1/System/$config.dat','r')

            data = searchfile.read()
            my_string = data.decode('utf-8')

            TD = re.findall("TOOL_DATA.*",my_string) # old method performance: ~0,92 - 1.0054 sec
            TN = re.findall("TOOL_NAME.*",my_string)
            BD = re.findall("BASE_DATA.*",my_string)
            BN = re.findall("BASE_NAME.*",my_string)

            searchfile.close()

            for j in range(1, len(TD)):
                result = str(TD[j]).find("{X 0.0,Y 0.0,Z 0.0,A 0.0,B 0.0,C 0.0}")
                if result < 0:
                    tcp[j] = get_coords2(TD[j])
                    tcp[j]['name'] = get_name2(TN[j])

            for j in range(1, len(BD)):
                result = str(BD[j]).find("{X 0.0,Y 0.0,Z 0.0,A 0.0,B 0.0,C 0.0}")
                if result < 0:
                    base[j] = get_coords2(BD[j])
                    base[j]['name'] = get_name2(BN[j])        
            
            write(name)


            
        # Get programs
        # i=0
        # folges = get_folges(backup)
        # ups = get_ups(backup)
        # for folge in sorted(folges):
        #     i+=1
        #     programs[i]=folges[folge]
        # for up in sorted(ups):
        #     i+=1
        #     programs[i]=ups[up]

        # backup.close()

    # print('TOOLS')
    # for index in tcp:
    #     print(index)
    #     print(tcp[index])

    # print('BASE')
    # for index in base:
    #     print(index)
    #     print(base[index])

    print("")
    print("----- %s seconds -----" % (time.time() - start_time))
    print("Everything is done. This window will close in 3 sec")
    print("")
    print("=================================================")
    print("Robot Report v0.3. Check for updates at:")
    print("        www.fabryka-robotow.pl")

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX    

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    Form = RobotReport()
    sys.exit(app.exec_())
