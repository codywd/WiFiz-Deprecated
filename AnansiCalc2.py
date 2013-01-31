#!/usr/bin/python2

## Standard Libraries ##
import math
import os
import sys
import urllib
import webbrowser
import tempfile

## Third-Party Libraries ##
from PySide import QtGui

SB_INFO = 0
progVer = 2.00

class AnansiCalc(QtGui.QMainWindow):
    def __init__(self):
        super(AnansiCalc, self).__init__()
        self.InitUI()
        
    def InitUI(self):
        self.resize(310, 310)
        self.center()
        
        self.setWindowTitle("Anansi CalcPad")
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.show()
        
    def center(self): 
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())   
        
def main():
    app = QtGui.QApplication(sys.argv)
    AC = AnansiCalc()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
        