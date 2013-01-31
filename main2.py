import sys
from PySide import QtGui

class WiFiz(QtGui.QMainWindow):
    def __init__(self):
        super(WiFiz, self).__init__()
        
        self.InitUI()
        
    def InitUI(self):
        self.resize(500, 390)
        self.center()
        self.setWindowTitle('WiFiz')
        self.setWindowIcon(QtGui.QIcon('icon.gif'))
        
        # Menu Bar #
        mainMenu = self.menuBar()
        
        fileMenu = mainMenu.addMenu("File")
        
        scanForAPs = QtGui.QAction("Scan for APs", self)
        scanForAPs.setStatusTip("Scan for new Access Points.")
        #scanForAPs.triggered.connect(self.OnScan)
        fileMenu.addAction(scanForAPs)
        
        fileMenu.addSeparator()
        
        exitAction = QtGui.QAction("Exit", self)
        exitAction.setStatusTip("Quit the Application (Will Minimize to Status Area")
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)
        
        editMenu = mainMenu.addMenu("Edit")
        
        preferencesAction = QtGui.QAction("Preferences", self)
        preferencesAction.setStatusTip("Set your Preferences for WiFiz")
        #preferencesAction.triggered.connect(self.PreferencesDialog)
        editMenu.addAction(preferencesAction)
        
        helpMenu = mainMenu.addMenu("Help")
        
        programHelpAction = QtGui.QAction("Help with WiFiz", self)
        programHelpAction.setStatusTip("Get Help with WiFiz")
        #programHelpAction.triggered.connect(self.helpDialog)
        helpMenu.addAction(programHelpAction)
        helpMenu.addSeparator()
        
        checkForUpdatesAction = QtGui.QAction("Check for Updates...", self)
        checkForUpdatesAction.setStatusTip("Check for Updates to WiFiz")
        #checkForUpdatesAction.triggered.connect(self.UpdateDialog)
        helpMenu.addAction(checkForUpdatesAction)
        
        reportIssueAction = QtGui.QAction("Report an Issue...", self)
        reportIssueAction.setStatusTip("Report an Issue you have found with WiFiz")
        #reportIssueAction.triggered.connect(self.ReportIssueDialog)
        helpMenu.addAction(reportIssueAction)
        helpMenu.addSeparator()
        
        aboutWifizAction = QtGui.QAction("About WiFiz...", self)
        aboutWifizAction.setStatusTip("About the program.")
        #aboutWifizAction.triggered.connect(self.aboutDialog)
        helpMenu.addAction(aboutWifizAction)
        
        # End Menu #
        
        #Begin Toolbar#
        newProfile = QtGui.QAction(QtGui.QIcon("newprofile.png"), "New Profile", self)
        newProfile.setStatusTip("Manually create a New Profile.")        
        #newProfile.triggered.connect(self.CreateDialog)
        
        scanForAPs = QtGui.QAction(QtGui.QIcon("APScan.png"), "Scan for APs", self)
        scanForAPs.setStatusTip("Scan for new Access Points.")
        #scanForAPs.triggered.connect(self.OnScan)
        
        connectAction = QtGui.QAction(QtGui.QIcon("connect.png"), "Connect to selected network.", self)
        connectAction.setStatusTip("Connect to the currently selected network.")
        #connectAction.triggered.connect(self.connect)
        
        dConnectAction = QtGui.QAction(QtGui.QIcon("disconnect.png"), "Disconnect from the selected network.", self)
        dConnectAction.setStatusTip("Disconnect from the currently selected network.")
        #dConnectAction.triggered.connect(self.dconnect)
        
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(newProfile)
        self.toolbar.addAction(scanForAPs)
        self.toolbar.addAction(connectAction)
        self.toolbar.addAction(dConnectAction)
        
        SSIDList = QtGui.QTableWidget(0, 4, self)
        labels = ["SSID", "Connection Strength", "Security", "Connected?"]
        SSIDList.setHorizontalHeaderLabels(labels)        
        SSIDList.verticalHeader().setVisible(False)
        #SSIDList.horizontalHeader().setResizeMode(
        self.setCentralWidget(SSIDList)
        self.statusBar()        
        self.show()
        
    def center(self): 
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft()) 
        
def main():
    app = QtGui.QApplication(sys.argv)
    Wi = WiFiz()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()