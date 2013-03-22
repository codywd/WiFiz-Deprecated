#! /usr/bin/python2


# Importing Standard Libraries #
import os
import sys
import re
import subprocess
import fcntl

# Importing Third Party Libraries #
from wx import *
from wx.lib.wordwrap import wordwrap
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
import wx.lib.mixins.listctrl as listmix
from wx import wizard as wiz
import taskbar as tbi

# Setting some base app information #
progVer = 0.8
logfile = os.getcwd() + '/iwlist.log'
intFile = os.getcwd() + "/interface.cfg"

pid_file = 'program.pid'

# Lets make sure we're root as well #
euid = os.geteuid()
if euid != 0:
	args = ['gksudo', sys.executable] + sys.argv + [os.environ]
	os.execlpe('sudo', *args)

# Allow only one instance #
fp = open(pid_file, 'w')
try:
	fcntl.lockf(fp, fcntl.LOCK_EX|fcntl.LOCK_NB)
except IOError:
	# TODO Add current pid incase the user needs to kill it 
	print "We only allow one instance of WiFiz at a time for now."
	sys.exit(1)

# main class #
class WiFiz(wx.Frame):
	def __init__(self, parent, title):
		super(WiFiz, self).__init__(None, title="WiFiz", style = wx.DEFAULT_FRAME_STYLE)
		self.TrayIcon = tbi.Icon(self, wx.Icon("./imgs/logo.png", wx.BITMAP_TYPE_PNG), "WiFiz")
		self.index = 0
		self.InitUI()

	def InitUI(self):

		iconFile = "./imgs/logo.png"
		mainIcon = wx.Icon(iconFile, wx.BITMAP_TYPE_PNG)
		self.SetIcon(mainIcon)

		# Menu Bar #
		self.mainMenu = wx.MenuBar()

		fileMenu = wx.Menu()
		ScanAPs = fileMenu.Append(wx.ID_ANY, "Scan for New Networks", "Scan for New Wireless Networks.")
		fileMenu.AppendSeparator()
		fileQuit = fileMenu.Append(wx.ID_EXIT, "Quit", "Exit the Program.")
		self.mainMenu.Append(fileMenu, "&File")
		
		profilesMenu = wx.Menu()
		profiles = os.listdir("/etc/network.d/")
		for i in profiles:
			if os.path.isfile("/etc/network.d/" + i):
				profile = profilesMenu.Append(wx.ID_ANY, i)
				self.Bind(wx.EVT_MENU, self.OnMConnect, profile)
		self.mainMenu.Append(profilesMenu, "Profiles")

		helpMenu = wx.Menu()
		helpItem = helpMenu.Append(wx.ID_HELP, "Help with WiFiz", "Get help with WiFiz")
		helpItem.Enable(False)
		helpMenu.AppendSeparator()
		reportIssue = helpMenu.Append(wx.ID_ANY, "Report an Issue...", "Report a bug, or give a suggestion.")
		helpMenu.AppendSeparator()
		aboutItem = helpMenu.Append(wx.ID_ABOUT, "About WiFiz", "About this program...")
		self.mainMenu.Append(helpMenu, "&Help")

		self.SetMenuBar(self.mainMenu)

		# End Menu Bar #

		# Create Popup Menu #
		self.PopupMenu = wx.Menu()
		popCon = self.PopupMenu.Append(wx.ID_ANY, "Connect to Network", "Connect to selected network.")
		popDCon = self.PopupMenu.Append(wx.ID_ANY, "Disconnect from Network", "Disconnect from selected network.")

		# Create Toolbar #
		toolbar = self.CreateToolBar()
		newTool = toolbar.AddLabelTool(wx.ID_NEW, 'New', wx.ArtProvider.GetBitmap(wx.ART_NEW), wx.NullBitmap, wx.ITEM_NORMAL, 'New Connection')
		ReScanAPs = toolbar.AddLabelTool(wx.ID_ANY, 'Scan', wx.Bitmap('imgs/APScan.png'), wx.NullBitmap, wx.ITEM_NORMAL, 'Scan')
		connectSe = toolbar.AddLabelTool(wx.ID_ANY, 'Connect', wx.Bitmap('imgs/connect.png'), wx.NullBitmap, wx.ITEM_NORMAL, 'Connect')
		dConnectSe = toolbar.AddLabelTool(wx.ID_ANY, 'Disconnect', wx.Bitmap('imgs/disconnect.png'), wx.NullBitmap, wx.ITEM_NORMAL, 'Disconnect')
		toolbar.AddSeparator()
		quitTool = toolbar.AddLabelTool(wx.ID_EXIT, 'Quit', wx.ArtProvider.GetBitmap(wx.ART_QUIT), wx.NullBitmap, wx.ITEM_NORMAL, 'Quit')
		toolbar.Realize()
		# End Toolbar #

		self.APList = AutoWidthListCtrl(self)

		self.APList.setResizeColumn(0)
		self.APList.InsertColumn(0, "SSID", width=150)
		self.APList.InsertColumn(1, "Connection Strength", width=200)
		self.APList.InsertColumn(2, "Security Type", width=150)
		self.APList.InsertColumn(3, "Connected?", width=150)

		# Create Status Bar #
		self.CreateStatusBar()
		# End Status Bar #

		# Binding Events #
		self.Bind(wx.EVT_MENU, self.OnClose, fileQuit)
		self.Bind(wx.EVT_TOOL, self.OnConnect, connectSe)
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)
		self.Bind(wx.EVT_MENU, self.OnScan, ScanAPs)
		self.Bind(wx.EVT_TOOL, self.OnScan, ReScanAPs)
		self.Bind(wx.EVT_TOOL, self.OnNew, newTool)
		self.Bind(wx.EVT_TOOL, self.OnDConnect, dConnectSe) 
		self.Bind(wx.EVT_CONTEXT_MENU, self.OnShowPopup)
		self.Bind(wx.EVT_CONTEXT_MENU, self.OnConnect, popCon)
		self.Bind(wx.EVT_CONTEXT_MENU, self.OnDConnect, popDCon)
		self.Bind(wx.EVT_MENU, self.OnReport, reportIssue)
		# End Bindings #

		self.SetSize((700,390))
		self.Center()
		self.Show()
		if os.path.isfile(intFile):
			f = open(intFile)
			self.UIDValue = f.readline()
			str(self.UIDValue).strip()
			f.close()
		else:
			self.UID = wx.TextEntryDialog(self, "What is your Interface Name? (wlan0, wlp2s0)",
						                  "Wireless Interface",
						                  "")
			if self.UID.ShowModal() == wx.ID_OK:
				self.UIDValue = self.UID.GetValue()
				f = open(intFile, 'w')
				f.write(self.UIDValue)
				f.close()
		os.system("ifconfig " + self.UIDValue + " up")
		self.OnScan(self)
		
	def OnMConnect(self, e):
		item = self.mainMenu.FindItemById(e.GetId())
		profile = item.GetText()
		os.system("netctl stop-all")
		os.system("netctl start " + profile)		
	
	def OnPref(self, e):
		prefWindow = Preferences(self, wx.ID_ANY, title="Preferences")
		prefWindow.CenterOnParent()
		prefWindow.Show()
		
	def OnEdit(self, e):
		editWindow = EditProfile(None)
		
	def OnConnect(self, e):
		index = str(self.getSelectedIndices()).strip('[]')
		index = int(index)
		nmp = self.APList.GetItem(index, 0)
		nameofProfile = nmp.GetText()
		tos = self.APList.GetItem(index, 2)
		typeofSecurity = tos.GetText()
		typeofSecurity = str(typeofSecurity).strip()
		typeofSecurity = typeofSecurity.lower()

		workDir = "/etc/network.d/"
		filename = str("wifiz-" + nameofProfile).strip()
		filename = filename.strip()
		if os.path.isfile(workDir + filename):
			os.system("ifconfig " + self.UIDValue + " down")
			os.system("netctl start wifiz-" + str(nameofProfile).strip())
			self.OnScan(self)
			wx.MessageBox("You are now connected to " + str(nameofProfile).strip() + ".", "Connected.")
		else:
			f = open(workDir + filename, "w")
			f.write("Description='A profile made by Wifiz for " + str(nameofProfile).strip() + "'\n")
			f.close()
			f = open(workDir + filename, 'a')
			f.write("Interface=" + str(self.UIDValue).strip() + "\n")
			f.write("Connection=wireless\n")
			f.write("Security=" + typeofSecurity + "\n")
			f.write("ESSID='" + str(nameofProfile).strip() + "'\n")
			if str(typeofSecurity).strip() != "none":  
				passw = wx.TextEntryDialog(self, "What is the password?",
								           "Password",
								           "")
				if passw.ShowModal() == wx.ID_OK:
					thepass = passw.GetValue()	
				else:
					f.close()
				f.write(r'Key=\"' + thepass + "\n")
			else:
				f.write(r'Key=None\n')
			pref = wx.TextEntryDialog(self, "Is this network preferred? (In range of multiple profiles, connect to this first?)"
			                          "Preferred Network?",
			                          "")
			if pref.ShowModal() == wx.ID_OK:
				f.write("#preferred=yes\n")
			else:
				f.write("#preferred=no\n")
			f.write("IP=dhcp\n")
			f.close()
			os.system("ifconfig " + self.UIDValue + " down")
			os.system("netctl enable wifiz-" + str(nameofProfile).strip())
			os.system("netctl start wifiz-" + str(nameofProfile).strip())
			wx.MessageBox("You are now connected to " + str(nameofProfile).strip() + ".", "Connected.")
			self.OnScan(self)

	def getSelectedIndices( self, state =  wx.LIST_STATE_SELECTED):
		indices = []
		lastFound = -1
		while True:
			index = self.APList.GetNextItem(
				lastFound,
				wx.LIST_NEXT_ALL,
				state,
			)
			if index == -1:
				break
			else:
				lastFound = index
				indices.append( index )
		return indices	

	def OnReport(self, e):
		wx.MessageBox("To report a message, send an email to cody@seafiresoftware.org", "e-Mail")

	def OnShowPopup(self, e):
		x, y = e.GetPosition()
		pos = self.APList.ScreenToClientXY(x, y)
		self.APList.PopupMenu(self.PopupMenu, pos)

	def OnDConnect(self, e):
		index = str(self.getSelectedIndices()).strip('[]')
		index = int(index)
		item = self.APList.GetItem(index, 0)
		nameofProfile = item.GetText()
		os.system("netctl stop wifiz-" + nameofProfile)
		os.system("ifconfig " + self.UIDValue + " up")
		self.OnScan(self)
		wx.MessageBox("You are now disconnected from " + nameofProfile + ".", "Disconnected.")

	def OnNew(self, e):
		newProf = NewProfile(parent=None)       

	def OnScan(self, e):
		if os.path.isfile(logfile):
			f = open(logfile, 'r+')
			f.truncate()
			f.close()
		else:
			pass

		output = str(subprocess.check_output("iwlist " + self.UIDValue + " scan", shell=True))
		f = open(logfile, 'w')
		f.write(output)
		f.close()

		self.APList.DeleteAllItems()
		self.index = 0 
		ilogfile = os.getcwd() + "/iwconfig.log"
		outputs = str(subprocess.check_output("iwconfig " + self.UIDValue , shell=True))  
		d = open(ilogfile, 'w')
		d.write(outputs)
		d.close()
		v = open(ilogfile).read()
		f = open(logfile).read()
		for line in open(logfile):
			if "ESSID" in line:
				begin = line.replace(" ", "")
				mid = begin.replace("ESSID:", "")
				final = mid.replace('"', "")
				self.APList.SetStringItem(self.index, 0, final)
				line = open(ilogfile).readline()
				if final.strip() in line.strip():
					connect = "yes"
				else:
					connect = "no"
				self.APList.SetStringItem(self.index, 3, connect) 
				profiles = os.listdir("/etc/network.d/")				
			if "Quality" in line:
				lines = "Line %s" % self.index 
				self.APList.InsertStringItem(self.index, lines)
				self.index + 1                
				s = str(line)
				s2 = s[28:33]
				s3 = str(int(round(float(s2[0]) / float(s2[3]) * 100))).rjust(3) + " %" # Courtesy of gohu's iwlistparse.py, slightly modified. https://bbs.archlinux.org/viewtopic.php?id=88967
				self.APList.SetStringItem(self.index, 1, s3)
			if "Encryption" in line:
				if "WPA2" in line:
					encrypt = "WPA"
				elif "off" in line:
					encrypt = "None"
				else:
					encrypt = "WEP"
				self.APList.SetStringItem(self.index, 2, encrypt)
			else:
				pass

		f = open(ilogfile, 'w')
		f.write(outputs)
		f.close()




	def OnClose(self, e):
		self.Hide()

	def OnFullClose(self, e):
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

		info.SetIcon(wx.Icon('./imgs/aboutLogo.png', wx.BITMAP_TYPE_PNG))
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
		intFaces = os.listdir("/sys/class/net")
		for i in intFaces:
			page1.Sizer.Add(wx.RadioButton(page1, -1, i))
		page2 = TitledPage(wizard, "Connection Type")
		page2.Sizer.Add(wx.StaticText(page2, -1, "Please type the type of connection you will be using."))
		page2.Sizer.Add(wx.StaticText(page2, -1, ""))
		choiceWiFi = wx.RadioButton(page2, -1, "Wireless", style=wx.RB_GROUP)
		choiceEth = wx.RadioButton(page2, -1, "Ethernet")
		page2.Sizer.Add(choiceWiFi)
		page2.Sizer.Add(choiceEth)
		page3 = TitledPage(wizard, "Security Type")
		page3.Sizer.Add(wx.StaticText(page3, -1, "Please type the security type of the connection."))
		page3.Sizer.Add(wx.StaticText(page3, -1, ""))
		choiceWEP = wx.RadioButton(page3, -1, "WEP", style=wx.RB_GROUP)
		choiceWPA = wx.RadioButton(page3, -1, "WPA/WPA2")
		page3.Sizer.Add(choiceWEP)
		page3.Sizer.Add(choiceWPA)
		page4 = TitledPage(wizard, "SSID")
		page4.Sizer.Add(wx.StaticText(page4, -1, "Please type the name of the network you wish to connect to."))
		page4.Sizer.Add(wx.StaticText(page4, -1, ""))
		SSIDV = wx.TextCtrl(page4)
		page4.Sizer.Add(SSIDV, flag=wx.EXPAND)  
		SSID = SSIDV.GetValue()
		page5 = TitledPage(wizard, "Security Key")
		page5.Sizer.Add(wx.StaticText(page5, -1, "Please type the password of the network you wish to connect to."))
		page5.Sizer.Add(wx.StaticText(page5, -1, ""))
		self.securePass = wx.TextCtrl(page5, style=wx.TE_PASSWORD)
		page5.Sizer.Add(self.securePass, flag=wx.EXPAND)
		self.password = self.securePass.GetValue()
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

		self.Bind(wiz.EVT_WIZARD_CANCEL, self.closeDialog)
		self.Bind(wiz.EVT_WIZARD_FINISHED, self.saveProfile)

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

class TitledPage(wiz.WizardPageSimple):
	def __init__(self, parent, title):
		wiz.WizardPageSimple.__init__(self, parent)

		sizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(sizer)

		title = wx.StaticText(self, -1, title)
		title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
		sizer.Add(title, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)
		sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 5)

# Start App #
if __name__ == "__main__":
	app = wx.App()
	WiFiz(None, title="WiFiz")
	app.MainLoop()