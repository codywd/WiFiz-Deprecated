#! /usr/bin/python2


# Importing Standard Libraries #
import os
import sys
import logging
import subprocess

# Importing Third Party Libraries #
from wx import *
from wx.lib.wordwrap import wordwrap

progVer = 0.11
logfile = os.getcwd() + '/iwlist.log'

class APopupMenu(wx.Menu):
    def __init__(self, parent):
        super(APopupMenu, self).__init__()
        
        self.parent = parent
        
        cnct = wx.MenuItem(self, wx.NewId(), 'Connect')
        self.AppendItem(cnct)
        self.Bind(wx.EVT_MENU, self.OnConnect, cnct)
        
        dcnct = wx.MenuItem(self, wx.NewId(), "Disconnect")
        self.AppendItem(dcnct)
        self.Bind(wx.EVT_MENU, self.OnDConnect, dcnct)
        
        self.AppendSeparator()
        
        edp = wx.MenuItem(self, wx.NewId(), 'Edit Profile')
        self.AppendItem(edp)
        self.Bind(wx.EVT_MENU, self.OnEditPro, edp)
        
    def OnConnect(self):
        pass
    
    def OnDConnect(self):
        pass
    
    def OnEditPro(self):
        pass

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
        ReScanAPs = toolbar.AddLabelTool(wx.ID_ANY, 'Scan', wx.Bitmap('stock_network_24.png'))
        connectSe = toolbar.AddLabelTool(wx.ID_ANY, 'Connect', wx.Bitmap('stock_connect_24.png'))
        dConnectSe = toolbar.AddLabelTool(wx.ID_ANY, 'Disconnect', wx.Bitmap('stock_disconnect_24.png'))
        toolbar.AddSeparator()
        prefTool = toolbar.AddLabelTool(wx.ID_PREFERENCES, 'Preferences', wx.Bitmap('stock_preferences_24.png'))
        quitTool = toolbar.AddLabelTool(wx.ID_EXIT, 'Quit', wx.ArtProvider.GetBitmap(wx.ART_QUIT))
        toolbar.Realize()
        # End Toolbar #
        
        panel = wx.Panel(self, wx.ID_ANY)
        
        self.APList = wx.ListCtrl(panel, size=(100, 300),
                             style=wx.LC_REPORT
                             | wx.BORDER_SUNKEN)
        self.APList.InsertColumn(0, "SSID", width=125)
        self.APList.InsertColumn(1, "Connection Strength", width=150)
        self.APList.InsertColumn(2, "Security Type", width=125)
        self.APList.InsertColumn(3, "Connected?", width=100)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.APList, 0, wx.ALL | wx.EXPAND, 0)
        panel.SetSizer(sizer)
        
        
        # Create Status Bar #
        self.CreateStatusBar()
        # End Status Bar #
        
        # Binding Events #
        self.Bind(wx.EVT_MENU, self.OnClose, fileQuit)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)
        self.Bind(wx.EVT_MENU, self.OnScan, ScanAPs)
        self.Bind(wx.EVT_TOOL, self.OnScan, ReScanAPs)
        
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        # End Bindings #
        
        self.SetSize((500,390))
        self.OnScan(self)
        self.Show()
        self.Center()
        
    def OnRightDown(self, e):
        self.PopupMenu(APopupMenu(self), e.GetPosition())
    
    def OnScan(self, e):
        if os.path.isfile(logfile):
            f = open(logfile, 'r+')
            f.truncate()
            f.close()
        else:
            logging.error("No file exists!!")
            
        output = str(subprocess.check_output("sudo iwlist wlan0 scan", shell=True))
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
            if "WPA2" in line:
                encrypt = "WPA2"
            if "WEP" in line:
                encrypt = "WEP"
            if "Address" in line:
                begin = line.replace(" ", "")
                mid = begin.replace("Cell01-Address:", "")
                Address = mid
        
        ilogfile = os.getcwd() + "/iwconfig.log"
        
        outputs = str(subprocess.check_output("iwconfig wlan0", shell=True))
        f = open(ilogfile, 'w')
        f.write(outputs)
        f.close()
        
        d = open(ilogfile, 'r')
        v = d.readline()
        v2 = d.readline()
        v3 = v2.replace(" ", "")
        print Address
        if Address in v3:
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
        description = """ WiFiz is a front end to easily connect to wireless networks. It keeps a simple, elegant interface intact while using the netcfg backend to connect to networks."""
        
        licence = """Copyright (c) 2012 Cody Dostal, Pivotraze
        
        Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
        
        The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. The end-user documentation included with the redistribution, if any, must include the following acknowledgment: "This product includes software developed by Cody Dostal https://github.com/codywd and its contributors", in the same place and form as other third-party acknowledgments. Alternatively, this acknowledgment may appear in the software itself, in the same form and location as other such third-party acknowledgments.
        
        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""
        
        info = wx.AboutDialogInfo()
        
        info.SetIcon(wx.Icon('stock_network_24.png', wx.BITMAP_TYPE_PNG))
        info.SetName('WiFiz')
        info.SetVersion(str(progVer))
        info.SetDescription(description)
        info.SetCopyright("(C) 2012 Cody Dostal (a.k.a. Pivotraze)")
        info.SetWebSite("https://www.github.com/codywd")
        info.SetLicence(wordwrap(licence, 350, wx.ClientDC(self)))
        info.AddDeveloper('Cody Dostal')
        info.AddDocWriter('Cody Dostal')
        info.AddArtist('Stock Gnome Icons')
        info.AddTranslator('Cody Dostal (English)')
        
        wx.AboutBox(info)
        
        
        
if __name__ == "__main__":
    app = wx.App()
    WiFiz(None, title="WiFiz")
    app.MainLoop()