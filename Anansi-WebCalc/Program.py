#!/usr/bin/python

## Importing Standard Libraries
import sys
import os
import time
import math

## Importing 3rd party libraries
from PyQt4 import QtGui
from PyQt4 import QtCore

## Importing Local Files
from mainAnan import Ui_AnansiWebCalc

# Setting the Variables #

class AnansiCalc(QtGui.QMainWindow):
    #Instance Vars
    lcdString = ''      #Stores string for lcd display
    operation = ''      #Current operation
    currentNum = 0
    previousNum = 0
    ans = 0


    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_AnansiWebCalc()
        self.ui.setupUi(self)
        self.initUI()
    
    def initUI(self):
        ## Connecting the Signals ##
            QtCore.QObject.connect(self.ui.btnAdd,QtCore.SIGNAL("clicked()"), self.opClicked)
            QtCore.QObject.connect(self.ui.btnMinus, QtCore.SIGNAL("clicked()"), self.opClicked)
            QtCore.QObject.connect(self.ui.btnMult, QtCore.SIGNAL("clicked()"), self.opClicked)
            QtCore.QObject.connect(self.ui.btnDiv, QtCore.SIGNAL("clicked()"), self.opClicked)
            QtCore.QObject.connect(self.ui.equalsBtn, QtCore.SIGNAL("clicked()"),self.enterClicked)
            QtCore.QObject.connect(self.ui.btn1,QtCore.SIGNAL("clicked()"),self.numBtnClicked)
            QtCore.QObject.connect(self.ui.btn2,QtCore.SIGNAL("clicked()"),self.numBtnClicked)
            QtCore.QObject.connect(self.ui.btn3,QtCore.SIGNAL("clicked()"),self.numBtnClicked)
            QtCore.QObject.connect(self.ui.btn4,QtCore.SIGNAL("clicked()"),self.numBtnClicked)
            QtCore.QObject.connect(self.ui.btn5,QtCore.SIGNAL("clicked()"),self.numBtnClicked)
            QtCore.QObject.connect(self.ui.btn6,QtCore.SIGNAL("clicked()"),self.numBtnClicked)
            QtCore.QObject.connect(self.ui.btn7,QtCore.SIGNAL("clicked()"),self.numBtnClicked)
            QtCore.QObject.connect(self.ui.btn8,QtCore.SIGNAL("clicked()"),self.numBtnClicked)
            QtCore.QObject.connect(self.ui.btn9,QtCore.SIGNAL("clicked()"),self.numBtnClicked)
            QtCore.QObject.connect(self.ui.btn0,QtCore.SIGNAL("clicked()"),self.numBtnClicked)
            QtCore.QObject.connect(self.ui.btnClearCur,QtCore.SIGNAL("clicked()"),self.mreset)
            QtCore.QObject.connect(self.ui.btnClearAll,QtCore.SIGNAL("clicked()"),self.mreset)
            QtCore.QObject.connect(self.ui.btnDecimal,QtCore.SIGNAL("clicked()"),self.numBtnClicked)
            QtCore.QObject.connect(self.ui.actionClear_All,QtCore.SIGNAL("triggered()"),self.mreset)
            QtCore.QObject.connect(self.ui.actionExit,QtCore.SIGNAL("triggered()"),self.close)
            QtCore.QObject.connect(self.ui.btnPi,QtCore.SIGNAL("clicked()"),self.mpi)
            QtCore.QObject.connect(self.ui.btnXSq,QtCore.SIGNAL("clicked()"),self.mXSq)
            QtCore.QObject.connect(self.ui.btnBack, QtCore.SIGNAL("clicked()"),self.bkSpce)
    

    def aggregateNews(self):
        pass

    def numBtnClicked(self):
        self.lcdString = self.lcdString + self.sender().text()
        self.ui.lcdNumber.display(self.lcdString)
        self.currentNum = float(self.lcdString)
  
    def bkSpce(self):
        pass

    def mreset(self):
        #update vars
        self.lcdString = ''
        self.currentNum = 0
        self.previousNum = 0
        #update display
        self.ui.lcdNumber.display(0)
    
    def opClicked(self):
        self.previousNum = self.currentNum
        self.currentNum = 0
        self.lcdString = ''
        self.operation = self.sender().text()

    def mpi(self):
        if self.operation == '*':
            self.ans = self.previousNum * math.pi
            self.ui.lcdNumber.display(self.ans)     
        elif self.operation == "":
            self.ans = self.currentNum * math.pi
            self.ui.lcdNumber.display(self.ans)

    def mXSq(self):
        if self.operation == '*':
            self.ans = self.currentNum*self.currentNum
            self.ui.lcdNumber.display(self.ans)
    
    
    def enterClicked(self):
        if self.operation == '+':
            self.ans = self.previousNum + self.currentNum
      
        if self.operation == '-':
            self.ans = self.previousNum - self.currentNum
      
        if self.operation == '*':
            self.ans = self.previousNum * self.currentNum
      
        if self.operation == '/':
            self.ans = self.previousNum / self.currentNum
       
        self.currentNum = self.ans
        self.ui.lcdNumber.display(self.ans)
        self.lcdString = ''
    
 
if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  myapp = AnansiCalc()
  myapp.show()
  sys.exit(app.exec_())