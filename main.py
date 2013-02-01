#! /usr/bin/python2


# Importing Standard Libraries #
import os
import sys
import logging
import subprocess

# Importing Third Party Libraries #
from wx import *
from wx.lib.wordwrap import wordwrap
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
from wx import wizard as wiz
progVer = 0.12
logfile = os.getcwd() + '/iwlist.log'

euid = os.geteuid()

if euid != 0:
    args = ['gksudo', sys.executable] + sys.argv + [os.environ]
    os.execlpe('sudo', *args)

class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("iwlist.log", "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def close(self):
        self.terminal.close()
        self.log.close()

class WiFiz(wx.Frame):
    def __init__(self, parent, title):
        super(WiFiz, self).__init__(None, title="WiFiz", style = wx.DEFAULT_FRAME_STYLE)
        logging.basicConfig(format='%(asctime)s \n %(levelname)s:%(message)s',filename="logfile.log", level=logging.DEBUG)
        sys.stdout = Logger()
        self.index = 0

        self.InitUI()

    def InitUI(self):

        iconFile = "./icon.gif"
        mainIcon = wx.Icon(iconFile, wx.BITMAP_TYPE_GIF)
        self.SetIcon(mainIcon)
        tbicon = wx.TaskBarIcon()
        tbicon.SetIcon(mainIcon, "WiFiz")

        # Menu Bar #
        mainMenu = wx.MenuBar()

        fileMenu = wx.Menu()
        ScanAPs = fileMenu.Append(wx.ID_ANY, "Scan for New Networks", "Scan for New Wireless Networks.")
        fileMenu.AppendSeparator()
        fileQuit = fileMenu.Append(wx.ID_EXIT, "Quit", "Exit the Program.")
        mainMenu.Append(fileMenu, "&File")

        editMenu = wx.Menu()
        prefItem = editMenu.Append(wx.ID_PREFERENCES, "Preferences", "Edit the preferences for this application.")
        mainMenu.Append(editMenu, "&Edit")

        helpMenu = wx.Menu()
        helpItem = helpMenu.Append(wx.ID_HELP, "Help with WiFiz", "Get help with WiFiz")
        helpMenu.AppendSeparator()
        updateCheck = helpMenu.Append(wx.ID_ANY, "Check for Updates...", "Check for Updates to WiFiz")
        reportIssue = helpMenu.Append(wx.ID_ANY, "Report an Issue...", "Report a bug, or give a suggestion.")
        helpMenu.AppendSeparator()
        aboutItem = helpMenu.Append(wx.ID_ABOUT, "About WiFiz", "About this program...")
        mainMenu.Append(helpMenu, "&Help")

        self.SetMenuBar(mainMenu)

        # End Menu Bar #

        # Create Toolbar #
        toolbar = self.CreateToolBar()
        newTool = toolbar.AddLabelTool(wx.ID_NEW, 'New', wx.ArtProvider.GetBitmap(wx.ART_NEW))
        ReScanAPs = toolbar.AddLabelTool(wx.ID_ANY, 'Scan', wx.Bitmap('APScan.png'))
        connectSe = toolbar.AddLabelTool(wx.ID_ANY, 'Connect', wx.Bitmap('connect.png'))
        dConnectSe = toolbar.AddLabelTool(wx.ID_ANY, 'Disconnect', wx.Bitmap('disconnect.png'))
        toolbar.AddSeparator()
        prefTool = toolbar.AddLabelTool(wx.ID_PREFERENCES, 'Preferences', wx.Bitmap('preferences.png'))
        quitTool = toolbar.AddLabelTool(wx.ID_EXIT, 'Quit', wx.ArtProvider.GetBitmap(wx.ART_QUIT))
        toolbar.Realize()
        # End Toolbar #

        self.APList = AutoWidthListCtrl(self)
        self.APList.setResizeColumn(1)
        self.APList.InsertColumn(0, "SSID", width=125)
        self.APList.InsertColumn(1, "Connection Strength", width=150)
        self.APList.InsertColumn(2, "Security Type", width=125)
        self.APList.InsertColumn(3, "Connected?", width=100)


        # Create Status Bar #
        self.CreateStatusBar()
        # End Status Bar #

        # Binding Events #
        self.Bind(wx.EVT_MENU, self.OnClose, fileQuit)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)
        self.Bind(wx.EVT_MENU, self.OnScan, ScanAPs)
        self.Bind(wx.EVT_TOOL, self.OnScan, ReScanAPs)
        self.Bind(wx.EVT_TOOL, self.OnNew, newTool)
        self.Bind(wx.EVT_TOOL, self.OnDConnect, dConnectSe) 
        # End Bindings #

        self.SetSize((500,390))
        self.Show()
        self.Center()
        self.UID = wx.TextEntryDialog(self, "What is your Interface Name? (wlan0, wlp2s0)",
                                 "Wireless Interface",
                                 "")
        if self.UID.ShowModal() == wx.ID_OK:
            self.UIDValue = self.UID.GetValue()
        self.OnScan(self)

    def OnDConnect(self, e):
        pass

    def OnNew(self, e):
        newProf = NewProfile(parent=None)       

    def OnScan(self, e):
        if os.path.isfile(logfile):
            f = open(logfile, 'r+')
            f.truncate()
            f.close()
        else:
            logging.error("No file exists!!")

        output = str(subprocess.check_output("iwlist scan", shell=True))
        f = open(logfile, 'w')
        f.write(output)
        f.close()        

        f = open(logfile).read()
        for line in open(logfile):
            if "ESSID" in line:
                begin = line.replace(" ", "")
                mid = begin.replace("ESSID:", "")
                final = mid.replace('"', "")
            if "Quality" in line:
                s = str(line)
                s2 = s[28:33]
            if "Encryption" in line:
                if "WPA2" in line:
                    encrypt = "WPA2"
                else:
                    encrypt = "WEP"
            self.index + 1

        ilogfile = os.getcwd() + "/iwconfig.log"
        
        outputs = str(subprocess.check_output("iwconfig | grep " + self.UIDValue, shell=True))
        f = open(ilogfile, 'w')
        f.write(outputs)
        f.close()

        d = open(ilogfile, 'r')
        v = d.read()
        if final in v:
            connect = "yes"
        else:
            connect = "no"

        lines = "Line %s" % self.index
        self.APList.InsertStringItem(self.index, lines)
        self.APList.SetStringItem(self.index, 0, final)  
        self.APList.SetStringItem(self.index, 1, s2)
        self.APList.SetStringItem(self.index, 2, encrypt)
        self.APList.SetStringItem(self.index, 3, connect)

        logging.info("AP Scan completed, and saved.")





    def OnClose(self, e):
        f = open(logfile, 'r+')
        f.truncate()
        f.close()        
        app.Exit()

    def OnAbout(self, e):
        description = """WiFiz is a simple to use, elegant, and powerful frontend for NetCTL. NetCTL is a fork of NetCFG that focuses on being very well integrated into systemd."""

        licence = """Copyright (c) 2013 Cody Dostal, Pivotraze

        Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. The end-user documentation included with the redistribution, if any, must include the following acknowledgment: "This product includes software developed by Cody Dostal https://github.com/codywd and its contributors", in the same place and form as other third-party acknowledgments. Alternatively, this acknowledgment may appear in the software itself, in the same form and location as other such third-party acknowledgments.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""

        info = wx.AboutDialogInfo()

        info.SetIcon(wx.Icon('./aboutIcon.gif', wx.BITMAP_TYPE_GIF))
        info.SetName('WiFiz')
        info.SetVersion(str(progVer))
        info.SetDescription(description)
        info.SetCopyright("(C) 2012 Cody Dostal (a.k.a. Pivotraze)")
        info.SetWebSite("https://www.github.com/codywd")
        info.SetLicence(wordwrap(licence, 350, wx.ClientDC(self)))
        info.AddDeveloper('Cody Dostal')
        info.AddDocWriter('Cody Dostal')
        info.AddArtist('Sam Stuewe')
        info.AddTranslator('Cody Dostal (English)')

        wx.AboutBox(info)



class NewProfile(wx.Dialog):
    def __init__(self, parent):
        super(NewProfile, self).__init__(None)
        self.InitUI()

    def InitUI(self):
            wizard = wx.wizard.Wizard(None, -1, "New Profile Wizard")
            page1 = TitledPage(wizard, "Interface")
            page1.Sizer.Add(wx.StaticText(page1, -1, "Please type the name of the interface you will be \nusing to connect to the network. Examples are \nwlan0, eth0, etc..."))
            page1.Sizer.Add(wx.StaticText(page1, -1, ""))
            interfaceNameV = wx.TextCtrl(page1)
            page1.Sizer.Add(interfaceNameV, flag=wx.EXPAND)
            self.interfaceName = interfaceNameV.GetValue()
            page2 = TitledPage(wizard, "Connection Type")
            page2.Sizer.Add(wx.StaticText(page2, -1, "Please type the type of connection you will be using. \nOnly use wireless or ethernet."))
            page2.Sizer.Add(wx.StaticText(page2, -1, ""))
            connectionName = wx.TextCtrl(page2)
            page2.Sizer.Add(connectionName, flag=wx.EXPAND)  
            self.connectionType = connectionName.GetValue()
            page3 = TitledPage(wizard, "Security Type")
            page3.Sizer.Add(wx.StaticText(page3, -1, "Please type the security type of the connection. \nOnly use wep or wpa."))
            page3.Sizer.Add(wx.StaticText(page3, -1, ""))
            securityTypeV = wx.TextCtrl(page3)
            page3.Sizer.Add(securityTypeV, flag=wx.EXPAND) 
            securityType = securityTypeV.GetValue()
            page4 = TitledPage(wizard, "SSID")
            page4.Sizer.Add(wx.StaticText(page4, -1, "Please type the name of the network you wish to connect to."))
            page4.Sizer.Add(wx.StaticText(page4, -1, ""))
            SSIDV = wx.TextCtrl(page4)
            page4.Sizer.Add(SSIDV, flag=wx.EXPAND)  
            SSID = SSIDV.GetValue()
            page5 = TitledPage(wizard, "Security Key")
            page5.Sizer.Add(wx.StaticText(page5, -1, "Please type the password of the network you wish to connect to."))
            page5.Sizer.Add(wx.StaticText(page5, -1, ""))
            securePass = wx.TextCtrl(page5, style=wx.TE_PASSWORD)
            showPassBtn = wx.Button(page5, -1, "Show Password")
            page5.Sizer.Add(securePass, flag=wx.EXPAND)
            page5.Sizer.Add(showPassBtn)
            password = securePass.GetValue()
            page6 = TitledPage(wizard, "Hidden Network")
            page6.Sizer.Add(wx.StaticText(page6, -1, "Is the network hidden? If so, check the checkbox."))
            page6.Sizer.Add(wx.StaticText(page6, -1, ""))
            page6.Sizer.Add(wx.CheckBox(page6, -1, "Network is Hidden"))
            
            wx.wizard.WizardPageSimple.Chain(page1, page2)
            wx.wizard.WizardPageSimple.Chain(page2, page3)
            wx.wizard.WizardPageSimple.Chain(page3, page4)
            wx.wizard.WizardPageSimple.Chain(page4, page5)
            wx.wizard.WizardPageSimple.Chain(page5, page6)
            wizard.FitToPage(page1)
            wizard.RunWizard(page1)
            wizard.Destroy()
            
            self.Bind(self, wiz.EVT_WIZARD_CANCEL, self.closeDialog)
            self.Bind(self, wiz.EVT_WIZARD_FINISHED, self.saveProfile)

    def saveProfile(self, e):
        wx.MessageBox(self.interfaceName, self.interfaceName, wx.ID_OK)
        wx.MessageBox(self.connectionType, self.connectionType, wx.ID_OK)

    def closeDialog(self, e):
        dial = wx.MessageDialog(None, "Are you sure you want to cancel?", "Cancel?", wx.YES_NO|wx.NO_DEFAULT|wx.ICON_QUESTION)
        ret = dial.ShowModal()
        if ref == wx.ID_YES:
            self.Destroy()
        else:
            e.Veto()



class AutoWidthListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        ListCtrlAutoWidthMixin.__init__(self)

class UserInterfaceDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(UserInterfaceDialog, self).__init__(parent=parent, title=title, size=(310, 100))
        self.InitUI()
    
    def InitUI(self):
        interfaceNameLbl = wx.StaticText(self, label="Wireless Interface:", pos=(5, 10))
        interfaceNameLbl.SetToolTip(wx.ToolTip("What is the name of your wireless interface? E.G. wlan0, wlp2s0, etc..."))
        self.interfaceNameTxt = wx.TextCtrl(self, wx.ID_ANY, value="wlan0", pos=(130, 5))

        btnSave = wx.Button(self, wx.ID_SAVE, label="Save", pos=(215, 50))
        
        self.Bind(wx.EVT_BUTTON, self.saveIN, btnSave)      
        
    def saveIN(self, e):
        uInterface = self.interfaceNameTxt.GetValue()
        self.Destroy()
               
        
class TitledPage(wiz.WizardPageSimple):
    def __init__(self, parent, title):
        wiz.WizardPageSimple.__init__(self, parent)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        title = wx.StaticText(self, -1, title)
        title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        sizer.Add(title, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 5)
if __name__ == "__main__":
    app = wx.App()
    WiFiz(None, title="WiFiz")
    app.MainLoop()