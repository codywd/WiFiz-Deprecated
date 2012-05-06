## Standard Libraries ##
import math
import os
import sys
import urllib
import webbrowser
import tempfile

## Third-Party Libraries ##
import wx
import wx.stc

SB_INFO = 0
progVer = 1.1

class storyPadView(wx.Frame):
    def __init__(self, parent, title):
        super(storyPadView, self).__init__(wx.GetApp().TopWindow, title="Anansi StoryPad(r)", style = wx.DEFAULT_FRAME_STYLE)
        self.InitUI()
        
    def InitUI(self):
        if os.path.exists(os.getcwd() + "/icon.ico"):
            pass
        else:
            wx.MessageBox("There has been an error loading the icon. We are going to try downloading it to this directory.", "Error with Icon.", wx.OK)
            iconLoc = "https://github.com/Seafire-Software/Anansi-CalcPad/blob/master/icon.ico?raw=true"
            urllib.urlretrieve(iconLoc, os.getcwd() + "/icon.ico")
            if os.path.exists(os.getcwd() + "/icon.ico"):
                wx.MessageBox("We successfully downloaded the icon. Next time, you won't get this error.", "Icon downloaded.", wx.OK)
                iconFile = "./icon.ico"
            else:
                wx.MessageBox("Oops! We could not download it, please download it from our github.", "Error... Again.", wx.OK)
                
        if os.path.exists(os.getcwd() + "/aboutIcon.png"):
            pass
        else:
            fileLoc = "https://github.com/Seafire-Software/Anansi-CalcPad/raw/master/aboutIcon.png"
            urllib.urlretrieve(fileLoc, os.getcwd(), "/aboutIcon.png")
      
        self.aboutIcon = wx.Icon("./aboutIcon.png", wx.BITMAP_TYPE_PNG)       
        
        iconFile = "./icon.ico"
        mainIcon = wx.Icon(iconFile, wx.BITMAP_TYPE_ICO)
        self.SetIcon(mainIcon)
        
        ## Menu Bar ##
        mainMenu = wx.MenuBar()
        
        fileMenu = wx.Menu()
        newItem = fileMenu.Append(wx.ID_NEW, "New Window", "Open a new, blank window.")
        self.saveItem = fileMenu.Append(wx.ID_SAVE, "Save", "Save an ASTF file. Only available in StoryPad View.")
        self.saveItem.Enable(False)
        self.openItem = fileMenu.Append(wx.ID_OPEN, "Open", "Open an ASTF file. Only available in StoryPad View.")
        self.openItem.Enable(False)
        clearItem = fileMenu.Append(wx.ID_CLEAR, "Clear All", "Clear the current data.")
        fileMenu.AppendSeparator()
        exitItem = fileMenu.Append(wx.ID_EXIT, "Exit", "Quit the program.")
        mainMenu.Append(fileMenu, "&File")
        
        viewMenu = wx.Menu()
        self.storyViewItem = viewMenu.Append(wx.ID_ANY, "StoryPad(R) View", "Use the StoryPad journal view.", wx.ITEM_RADIO)
        self.storyViewItem.Enable(False)
        self.calcViewItem = viewMenu.Append(wx.ID_ANY, "Calculator View", "Use the calculator view.", wx.ITEM_RADIO)
        self.aggViewItem = viewMenu.Append(wx.ID_ANY, "News Aggregator View", "Use the news aggregator view.", wx.ITEM_RADIO)
        mainMenu.Append(viewMenu, "&View")
        
        helpMenu = wx.Menu()
        helpItem = helpMenu.Append(wx.ID_HELP, "Help with Anansi CalcPad...", "Get help with Anansi CalcPad.")
        updateItem = helpMenu.Append(wx.ID_ANY, "Check for Updates...", "Check for Updates to Anansi CalcPad.")
        reportItem = helpMenu.Append(wx.ID_ANY, "Report an Issue...", "Report an issue.")
        helpMenu.AppendSeparator()
        specCredits = helpMenu.Append(wx.ID_ANY, "Special Credits...", "Special credits for some awesome people.")
        aboutBox = helpMenu.Append(wx.ID_ABOUT, "About Anansi CalcPad", "Read about Anansi CalcPad.")        
        mainMenu.Append(helpMenu, "&Help")
        
        self.SetMenuBar(mainMenu)
        ## End Menu Bar ##
        
        ## Main GUI ##
        self.SPVSizer = wx.BoxSizer()
        self.SPVSizer.SetMinSize((450, 400))
        self.richtext = wx.stc.StyledTextCtrl(self, wx.ID_ANY, style=wx.TE_MULTILINE | wx.EXPAND)
        self.SPVSizer.Add(self.richtext, 1, wx.EXPAND)
        self.richtext.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
        self.richtext.SetMarginWidth(1, 25)        
        self.dirName = ""
        self.fileName = ""    
        
        self.SetSizerAndFit(self.SPVSizer)        
        ## End Main GUI ##
        
        ## Status Bar ##
        sb = self.CreateStatusBar()
        ## End Status Bar ##
        
        ## Binding Events ##
        self.Bind(wx.EVT_MENU, self.OnClose, exitItem)
        self.Bind(wx.EVT_MENU, self.aboutWin, aboutBox)
        self.Bind(wx.EVT_MENU, self.reportWin, reportItem)
        self.Bind(wx.EVT_MENU, self.calcView, self.calcViewItem)
        self.Bind(wx.EVT_MENU, self.newsAggView, self.aggViewItem)
        self.Bind(wx.EVT_MENU, self.helpPage, helpItem)
        self.Bind(wx.EVT_MENU, self.updateWin, updateItem)
        self.Bind(wx.EVT_MENU, self.saveNow, self.saveItem)
        self.Bind(wx.EVT_MENU, self.openASTF, self.openItem)
        self.Bind(wx.EVT_MENU, self.specialCredits, specCredits)
        self.Bind(wx.EVT_MENU, self.newWin, newItem)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        ## End Binding Section ##
        self.Center()
        self.Show()
        
    def newWin(self, e):
        newWin = storyPadView(self, wx.ID_ANY)
        newWin.Show(True)        
    
    def reportWin(self, e):
        reportn = reportIssueDialog(None, title="Report an Issue...")
        reportn.ShowModal()
        reportn.Destroy()        

    def helpPage(self, e):
        webbrowser.open("http://seafiresoftware.org/hesk/knowledgebase.php?category=3")
    
    def aboutWin(self, e):
        description = """Anansi CalcPad is a brand new program developed in tandem with Raindolf Owusu and his company, Oasis WebSoft, for his Anansi Project."""
        
        licensed = """Anansi CalcPad is free software; you can redistribute 
it and/or modify it under the terms of the GNU General Public License as 
published by the Free Software Foundation; either version 3 of the License, 
or (at your option) any later version.

Anansi CalcPad is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
See the GNU General Public License for more details. You should have 
received a copy of the GNU General Public License along with Anansi CalcPad; 
if not, write to the Free Software Foundation, Inc., 59 Temple Place, 
Suite 330, Boston, MA  02111-1307  USA"""
        
        info = wx.AboutDialogInfo()
        
        info.SetIcon(self.aboutIcon)
        info.SetName('Anansi CalcPad')
        info.SetVersion('1.1')
        info.SetDescription(description)
        info.SetCopyright('(C) 2012 Cody Dostal')
        info.SetWebSite('http://www.seafiresoftware.org')
        info.SetLicense(licensed)
        info.AddDeveloper('Cody Dostal')
        info.AddDocWriter('Cody Dostal')
        info.AddArtist('Raindolf Owusu')
        info.AddTranslator('Cody Dostal')
        
        wx.AboutBox(info)

    def updateWin(self, e):
        try:
            upFile = "https://raw.github.com/Seafire-Software/Anansi-CalcPad/master/curVersion"
            tempDir = tempfile.gettempdir()
            webFile = urllib.urlretrieve(upFile, tempDir + '/curVersion')
            basVer = open(tempDir + '/curVersion')
            ver = float(basVer.read())
            
            if progVer < ver:
                dlg = wx.MessageDialog(None, "You must update. Your version is " + str(progVer) + ", and the latest version is " + str(ver) + ", Do you wish to update?", "Update Required.", wx.YES_NO | wx.ICON_INFORMATION)
               
                result = dlg.ShowModal()
                dlg.Destroy()
                if result == wx.ID_YES:
                    upgradeFile = "https://raw.github.com/Seafire-Software/Anansi-CalcPad/master/AnansiCalc.py"
                        
                    urllib.urlretrieve(upgradeFile, os.path.join(os.getcwd(), sys.argv[0]))
                    dlg = wx.MessageDialog(None, "Update successful. Please restart the program!", "Restart manually.", wx.YES_NO)
                else:
                    wx.MessageBox("You chose not to upgrade. Please upgrade later!", "Upgrade later.", wx.OK)
            elif ver == progVer:
                wx.MessageBox("You do not need to update. Your version is " + str(progVer) + ", which is equal to the latest version of " + str(ver), "No Update Required.", wx.OK | wx.ICON_INFORMATION)
            elif progVer > ver: 
                wx.MessageBox("What happened here? Your version is " + str(progVer) + " which is greater than the latest version of " + str(ver), "Your version is greater than ours?", wx.OK | wx.ICON_QUESTION)
            else:
                wx.MessageBox("Something went wrong with the update. Please try again. If it happens again, file a bug report please.", "Error!", wx.OK | wx.ICON_ERROR)            
        except:
            wx.MessageBox("There was an error (Error 10152). Maybe you are not connected to the internet? Try again please.", "Try again.", wx.OK)
                    
    def specialCredits(self, e):
        spec = specCredits(None, title="Special Credits")
        spec.ShowModal()
        spec.Destroy()       
        
    def OnClose(self, e):
        app.Exit()
        
    def calcView(self, e):
        self.dlg1 = AnansiCalc(self, wx.ID_ANY)
        self.dlg1.Show()
        self.Show(False)
    
    def newsAggView(self, e):
        webbrowser.open("http://www.google.com/reader")
        
    def quickSave(self ,e):
            if (self.fileName != "") and (self.dirName !=""):
                try:
                    f = file(os.path.join(self.dirName, self.fileName), 'w')
                    f.write(self.richtext.GetText())
                    self.PushStatusText("Saved file: " + str(self.richtext.GetTextLength()) + " characters as " + self.fileName + ".", SB_INFO)
                    f.close()
                    return True
                except:
                    self.PushStatusText("Error in saving file!", SB_INFO)
                    return False
                else:
                    return self.saveNow(e)
                        
    def saveNow(self, e):
        ret = False
        dlg = wx.FileDialog(self, "Save A Journal", self.dirName, self.fileName, "Anansi StoryPad Text(.ASTF)|.ASTF", wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            self.fileName = dlg.GetFilename()
            self.dirName = dlg.GetDirectory()
            if self.quickSave(e):
                self.SetTitle("Anansi StoryPad(r)" + " - [" + self.fileName + "]")
                ret = True
        dlg.Destroy()
        return ret
            
    def openASTF(self, e):
        dlg = wx.FileDialog(self, "Open a journal", self.dirName, self.fileName, "Anansi StoryPad Text(.ASTF)|*.ASTF|All Files(*.*)|*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.fileName = dlg.GetFilename()
            self.dirName = dlg.GetDirectory()
            
            if self.richtext.LoadFile(os.path.join(self.dirName, self.fileName)):
                self.SetStatusText("Read " + str(self.richtext.GetTextLength()) + " characters. File named: " + dlg.GetFilename() + ".", SB_INFO)
            else:
                self.SetStatusText("Error in opening file.", SB_INFO)  
                
class specCredits(wx.Dialog):
    def __init__(self, parent, title):
        super(specCredits, self).__init__(parent=parent, title=title, size=(310, 330))
        self.InitUI()
        
    def InitUI(self):
        wx.StaticText(self, label="I want to give a HUGE thanks to Wingware.", pos=(5, 5))
        wx.StaticText(self, label="They provided us with a professional license", pos=(5, 25))
        wx.StaticText(self, label="to their Wing IDE Professional. We love it.", pos=(5, 45))
        wingImg = wx.Image("coded-with-logo.png", wx.BITMAP_TYPE_PNG)
        setImg = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(wingImg), size=(129, 66))
        setImg.Center()
        
        btnOK = wx.Button(self, label="OK", pos=(215, 265))
        btnVisit = wx.Button(self, label="Visit", pos=(125, 265))
        
        self.Bind(wx.EVT_BUTTON, self.visitWing, btnVisit)
        self.Bind(wx.EVT_BUTTON, self.closeDialog, btnOK)
        
    def visitWing(self, e):
        webbrowser.open("http://www.wingware.com")
        
    def closeDialog(self, e):
        self.Destroy()
class reportIssueDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(reportIssueDialog, self).__init__(parent=parent, title=title, size=(300, 300))
        panel = wx.Panel(self)
        posIssues = ["Bug", "Suggestion", "Crash", "Other..."]
        posLevels = ["Application Breaking", "Severe", "Major", "Neutral", "Minor", "Miniscule"]
        conEmailLbl = wx.StaticText(self, label="e-Mail:", pos=(10, 20))
        self.conEmail = wx.TextCtrl(self, size=(190, 25), pos=(100, 20))
        issueLbl = wx.StaticText(self, label="Issue:", pos=(10, 50))
        self.issue = wx.ComboBox(self, value="Suggestion", choices=posIssues, size=(190, 25), style=wx.CB_READONLY, pos=(100, 50))
        descripLbl = wx.StaticText(self, label="Description:", pos=(10, 80))
        self.descrip = wx.TextCtrl(self, size=(190, 90), pos=(100, 80), style=wx.TE_MULTILINE)
        issLvlLbl = wx.StaticText(self, label="Severity:", pos=(10, 178))
        self.issLvl = wx.ComboBox(self, value="Neutral", choices=posLevels, size=(190, 25), pos=(100, 175), style=wx.CB_READONLY)
        sendBtn = wx.Button(self, label="Send Report", pos=(200, 230))
        cancelBtn = wx.Button(self, label="Cancel", pos=(10, 230))
        
        ## Bind Events ##
        self.Bind(wx.EVT_BUTTON, self.OnClose, cancelBtn)
        self.Bind(wx.EVT_BUTTON, self.sendReport, sendBtn)
        
    def OnClose(self, e):
        self.Show(False)
        
    def sendReport(self, e):
        webbrowser.open("http://www.seafiresoftware.org/bugtracker/bug_report_page.php")

class AnansiCalc(wx.Frame):
    def __init__(self, parent, title):
        super(AnansiCalc, self).__init__(wx.GetApp().TopWindow, title="Anansi CalcPad(r)", style = wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.InitUI()
        
    def InitUI(self):
        if os.path.exists(os.getcwd() + "/icon.ico"):
            pass
        else:
            wx.MessageBox("There has been an error loading the icon. We are going to try downloading it to this directory.", "Error with Icon.", wx.OK)
            iconLoc = "https://github.com/Seafire-Software/Anansi-CalcPad/blob/master/icon.ico?raw=true"
            urllib.urlretrieve(iconLoc, os.getcwd() + "/icon.ico")
            if os.path.exists(os.getcwd() + "/icon.ico"):
                wx.MessageBox("We successfully downloaded the icon. Next time, you won't get this error.", "Icon downloaded.", wx.OK)
                iconFile = "./icon.ico"
            else:
                wx.MessageBox("Oops! We could not download it, please download it from our github.", "Error... Again.", wx.OK)

        
        if os.path.exists(os.getcwd() + "/aboutIcon.png"):
            pass
        else:
            fileLoc = "https://github.com/Seafire-Software/Anansi-CalcPad/raw/master/aboutIcon.png"
            urllib.urlretrieve(fileLoc, os.getcwd(), "/aboutIcon.png")
        
        iconFile = "./icon.ico"
        self.aboutIcon = wx.Icon("./aboutIcon.png", wx.BITMAP_TYPE_PNG)  
        mainIcon = wx.Icon(iconFile, wx.BITMAP_TYPE_ICO)
        self.SetIcon(mainIcon)
        
        if sys.platform == "win32":
            self.SetSize((320, 350))
        else:
            self.SetSize((310, 310))
        
        ## Menu Bar ##
        mainMenu = wx.MenuBar()
        
        fileMenu = wx.Menu()
        newItem = fileMenu.Append(wx.ID_NEW, "New Window", "Open a new, blank window.")
        clearItem = fileMenu.Append(wx.ID_CLEAR, "Clear All", "Clear the current data.")
        fileMenu.AppendSeparator()
        exitItem = fileMenu.Append(wx.ID_EXIT, "Exit", "Quit the program.")
        mainMenu.Append(fileMenu, "&File")
        
        viewMenu = wx.Menu()
        self.calcViewItem = viewMenu.Append(wx.ID_ANY, "Calculator View", "Use the calculator view.", wx.ITEM_RADIO)
        self.calcViewItem.Enable(False)
        self.storyViewItem = viewMenu.Append(wx.ID_ANY, "StoryPad(R) View", "Use the StoryPad journal view.", wx.ITEM_RADIO)
        self.aggViewItem = viewMenu.Append(wx.ID_ANY, "News Aggregator View", "Use the news aggregator view.", wx.ITEM_RADIO)
        mainMenu.Append(viewMenu, "&View")
        
        helpMenu = wx.Menu()
        helpItem = helpMenu.Append(wx.ID_HELP, "Help with Anansi CalcPad...", "Get help with Anansi CalcPad.")
        updateItem = helpMenu.Append(wx.ID_ANY, "Check for Updates...", "Check for Updates to Anansi CalcPad.")
        reportItem = helpMenu.Append(wx.ID_ANY, "Report an Issue...", "Report an issue.")
        helpMenu.AppendSeparator()
        specCredits = helpMenu.Append(wx.ID_ANY, "Special Credits...", "Special credits for some awesome people.")
        aboutBox = helpMenu.Append(wx.ID_ABOUT, "About Anansi CalcPad", "Read about Anansi CalcPad.")        
        mainMenu.Append(helpMenu, "&Help")
        
        self.SetMenuBar(mainMenu)
        ## End Menu Bar ##
        
        ## Main GUI ##
        mPanel = wx.Panel(self)
        mPanel.SetSize((320, 350))
        SPVSizer = wx.BoxSizer()
        SPVSizer.SetMinSize((310, 310))
        
        self.txtItem = wx.TextCtrl(mPanel, size=(300, 25), pos=(5, 5))
        SPVSizer.Add(self.txtItem)
        btn7 = wx.Button(mPanel, label="7", pos=(5, 35), size=(45, 45))
        SPVSizer.Add(btn7)
        btn8 = wx.Button(mPanel, label="8", pos=(55, 35), size=(45, 45))
        SPVSizer.Add(btn8)
        btn9 = wx.Button(mPanel, label="9", pos=(105, 35), size=(45, 45))
        SPVSizer.Add(btn9)
        btnDiv = wx.Button(mPanel, label="/", pos=(155, 35), size=(45, 45))
        SPVSizer.Add(btnDiv)
        btnBk = wx.Button(mPanel, label="Back", pos=(205, 35), size=(45, 45))
        SPVSizer.Add(btnBk)
        btnCE = wx.Button(mPanel, label="CE", pos=(255, 35), size=(45, 45))
        SPVSizer.Add(btnCE)
        
        btn4 = wx.Button(mPanel, label="4", pos=(5, 90), size=(45, 45))
        SPVSizer.Add(btn4)
        btn5 = wx.Button(mPanel, label="5", pos=(55, 90), size=(45, 45))
        SPVSizer.Add(btn5)
        btn6 = wx.Button(mPanel, label="6", pos=(105, 90), size=(45, 45))
        SPVSizer.Add(btn6)
        btnMult = wx.Button(mPanel, label="x", pos=(155, 90), size=(45, 45))
        SPVSizer.Add(btnMult)
        btnParOpen = wx.Button(mPanel, label="(", pos=(205, 90), size=(45, 45))
        SPVSizer.Add(btnParOpen)
        btnParClose = wx.Button(mPanel, label=")", pos=(255, 90), size=(45, 45))
        
        btn1 = wx.Button(mPanel, label="1", pos=(5, 150), size=(45, 45))
        SPVSizer.Add(btn1)
        btn2 = wx.Button(mPanel, label="2", pos=(55, 150), size=(45, 45))
        SPVSizer.Add(btn2)
        btn3 = wx.Button(mPanel, label="3", pos=(105, 150), size=(45, 45))
        SPVSizer.Add(btn3)        
        btnMin = wx.Button(mPanel, label="-", pos=(155, 150), size=(45, 45))
        SPVSizer.Add(btnMin)
        btnSq = wx.Button(mPanel, label="x" + u"\u00B2", pos=(205, 150), size=(45, 45))
        SPVSizer.Add(btnSq)        
        btnSqR = wx.Button(mPanel, label=u"\u221A", pos=(255, 150), size=(45, 45))
        SPVSizer.Add(btnSqR)
        
        btn0 = wx.Button(mPanel, label="0", pos=(5, 210), size=(45, 45))
        SPVSizer.Add(btn0)        
        btnDec = wx.Button(mPanel, label=".", pos=(55, 210), size=(45, 45))
        SPVSizer.Add(btnDec)        
        btnPlus = wx.Button(mPanel, label="+", pos=(155, 210), size=(45, 45))
        SPVSizer.Add(btnPlus)
        btnEq = wx.Button(mPanel, label="=", pos=(205, 210), size=(95, 45))
        SPVSizer.Add(btnEq)
        ## End Main GUI ##
        
        ## Status Bar ##
        self.sb = self.CreateStatusBar()
        self.sb.PushStatusText("Ready.")
        ## End Status Bar ##
        
        ## Binding Events ##
        self.Bind(wx.EVT_MENU, self.OnClose, exitItem)
        self.Bind(wx.EVT_MENU, self.aboutWin, aboutBox)
        self.Bind(wx.EVT_MENU, self.reportWin, reportItem)
        self.Bind(wx.EVT_MENU, self.storyPadView, self.storyViewItem)
        self.Bind(wx.EVT_MENU, self.newsAggView, self.aggViewItem)
        self.Bind(wx.EVT_MENU, self.helpPage, helpItem)
        self.Bind(wx.EVT_MENU, self.updateWin, updateItem)
        self.Bind(wx.EVT_MENU, self.specialCredits, specCredits)
        self.Bind(wx.EVT_MENU, self.newWin, newItem)
        self.Bind(wx.EVT_MENU, self.clearData, clearItem)
        self.Bind(wx.EVT_BUTTON, self.xSq, btnSq)
        self.Bind(wx.EVT_BUTTON, self.xSqR, btnSqR)
        self.Bind(wx.EVT_BUTTON, self.btn0Clicked, btn0)
        self.Bind(wx.EVT_BUTTON, self.btn1Clicked, btn1)
        self.Bind(wx.EVT_BUTTON, self.btn2Clicked, btn2)
        self.Bind(wx.EVT_BUTTON, self.btn3Clicked, btn3)
        self.Bind(wx.EVT_BUTTON, self.btn4Clicked, btn4)
        self.Bind(wx.EVT_BUTTON, self.btn5Clicked, btn5)
        self.Bind(wx.EVT_BUTTON, self.btn6Clicked, btn6)
        self.Bind(wx.EVT_BUTTON, self.btn7Clicked, btn7)
        self.Bind(wx.EVT_BUTTON, self.btn8Clicked, btn8)
        self.Bind(wx.EVT_BUTTON, self.btn9Clicked, btn9)
        self.Bind(wx.EVT_BUTTON, self.btnPlusClicked, btnPlus)
        self.Bind(wx.EVT_BUTTON, self.btnMinClicked, btnMin)
        self.Bind(wx.EVT_BUTTON, self.btnDivClicked, btnDiv)
        self.Bind(wx.EVT_BUTTON, self.btnMultClicked, btnMult)
        self.Bind(wx.EVT_BUTTON, self.btnDecClicked, btnDec)
        self.Bind(wx.EVT_BUTTON, self.btnBkClicked, btnBk)
        self.Bind(wx.EVT_BUTTON, self.clearData, btnCE)
        self.Bind(wx.EVT_BUTTON, self.btnEqClicked, btnEq)
        self.Bind(wx.EVT_BUTTON, self.btnOpPaClicked, btnParOpen)
        self.Bind(wx.EVT_BUTTON, self.btnClPaClicked, btnParClose)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        ## End Binding Section ##
        
        self.Center()
        self.Show()      
        
    def btnOpPaClicked(self, e):
        self.txtItem.AppendText("(")
        
    def btnClPaClicked(self, e):
        self.txtItem.AppendText(")")
    
    def btnBkClicked(self, e):
        self.txtItem.Remove(self.txtItem.GetLastPosition()-1, (self.txtItem.GetLastPosition()))
    
    def btnEqClicked(self, e):
        str1 = self.txtItem.GetValue()     
        if '/' in str1 and '1' not in str1:
            str1 = str1 + '.0'        
        while str1[0] == '0':
            str1 = str1[1:]
        try:
            self.txtItem.SetValue(str(float(eval(str1))))
            self.sb.PushStatusText("Successfully evaluated your math problem.")
        except ZeroDivisionError:
            self.txtItem.SetValue("You can't divide by zero!")
            self.sb.PushStatusText("Error! Seems you tried to divide by zero!")
        except:
            self.txtItem.SetValue("Error!")
            self.sb.PushStatusText("Error! Something has gone wrong here...")
    
    def btn0Clicked(self, e):
        self.txtItem.AppendText("0")
            
    def btn1Clicked(self, e):
        self.txtItem.AppendText("1")
        
    def btn2Clicked(self, e):
        self.txtItem.AppendText("2")
    
    def btn3Clicked(self, e):
        self.txtItem.AppendText("3")
        
    def btn4Clicked(self, e):
        self.txtItem.AppendText("4")
        
    def btn5Clicked(self, e):
        self.txtItem.AppendText("5")
        
    def btn6Clicked(self, e):
        self.txtItem.AppendText("6")
        
    def btn7Clicked(self, e):
        self.txtItem.AppendText("7")
        
    def btn8Clicked(self, e):
        self.txtItem.AppendText("8")
        
    def btn9Clicked(self, e):
        self.txtItem.AppendText("9")
        
    def btnDecClicked(self, e):
        self.txtItem.AppendText(".")
        
    def btnPlusClicked(self, e):
        self.txtItem.AppendText("+")
        
    def btnMinClicked(self, e):
        self.txtItem.AppendText("-")
        
    def btnDivClicked(self, e):
        self.txtItem.AppendText("/")
        
    def btnMultClicked(self, e):
        self.txtItem.AppendText("*")
    
    def xSq(self, e):
        if self.txtItem.GetValue() == "":
            self.txtItem.SetValue("Please enter something first!")
        elif self.txtItem.GetValue() == "/":
            self.txtItem.SetValue("You must enter a number, not '/'!")
        elif self.txtItem.GetValue() == "*":
            self.txtItem.SetValue("You must enter a number, not '*'!")
        else:
            try:
                self.txtItem.SetValue(str(eval(self.txtItem.GetValue())))
                num = float(self.txtItem.GetValue())     
                ans = num * num
                self.txtItem.SetValue(str(ans))
            except:
                self.txtItem.SetValue("Error!")
                self.sb.PushStatusText("Error! Something has gone wrong here...")        
        
    def xSqR(self, e):
        if self.txtItem.GetValue() == "":
            self.txtItem.SetValue("Please enter something first!")
        elif self.txtItem.GetValue() == "/":
            self.txtItem.SetValue("You must enter a number, not '/'!")
        elif self.txtItem.GetValue() == "*":
            self.txtItem.SetValue("You must enter a number, not '*'!")        
        else:        
            try:
                self.txtItem.SetValue(str(eval(self.txtItem.GetValue())))
                num = float(self.txtItem.GetValue())
                ans = math.sqrt(num)
                self.txtItem.SetValue(str(ans))
            except:
                self.txtItem.SetValue("Error!")
                self.sb.PushStatusText("Error! Something has gone wrong here...")        
        
    def specialCredits(self, e):
        spec = specCredits(None, title="Special Credits")
        spec.ShowModal()
        spec.Destroy()         
    
    def OnClose(self, e):
        app.Exit()
            
    def storyPadView(self, e):
        if self.storyViewItem.IsChecked():
            self.dlg1 = storyPadView(self, wx.ID_ANY)
            self.dlg1.Show()
            self.Show(False)
            
    def newsAggView(self, e):
        webbrowser.open("http://www.google.com/reader")   
    
    def newWin(self, e):
        newWin = AnansiCalc(self, wx.ID_ANY)
        newWin.Show(True)
    
    def clearData(self, e):
        self.txtItem.Clear()
    
    def reportWin(self, e):
        reportn = reportIssueDialog(None, title="Report an Issue...")
        reportn.ShowModal()
        reportn.Destroy()        

    def helpPage(self, e):
        webbrowser.open("http://seafiresoftware.org/hesk/knowledgebase.php?category=3")
    
    def aboutWin(self, e):
        description = """Anansi CalcPad is a brand new program developed in tandem with Raindolf Owusu and his company, Oasis WebSoft, for his Anansi Project."""
        
        licensed = """Anansi CalcPad is free software; you can redistribute 
it and/or modify it under the terms of the GNU General Public License as 
published by the Free Software Foundation; either version 3 of the License, 
or (at your option) any later version.

Anansi CalcPad is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
See the GNU General Public License for more details. You should have 
received a copy of the GNU General Public License along with Anansi CalcPad; 
if not, write to the Free Software Foundation, Inc., 59 Temple Place, 
Suite 330, Boston, MA  02111-1307  USA"""
        
        info = wx.AboutDialogInfo()
        
        info.SetIcon(self.aboutIcon)
        info.SetName('Anansi CalcPad')
        info.SetVersion('1.1')
        info.SetDescription(description)
        info.SetCopyright('(C) 2012 Cody Dostal')
        info.SetWebSite('http://www.seafiresoftware.org')
        info.SetLicense(licensed)
        info.AddDeveloper('Cody Dostal')
        info.AddDocWriter('Cody Dostal')
        info.AddArtist('Raindolf Owusu')
        info.AddTranslator('Cody Dostal')
        
        wx.AboutBox(info)
    
    def updateWin(self, e):
        try:
            upFile = "https://raw.github.com/Seafire-Software/Anansi-CalcPad/master/curVersion"
            tempDir = tempfile.gettempdir()
            webFile = urllib.urlretrieve(upFile, tempDir + '/curVersion')
            basVer = open(tempDir + '/curVersion')
            ver = float(basVer.read())
            
            if progVer < ver:
                dlg = wx.MessageDialog(None, "You must update. Your version is " + str(progVer) + ", and the latest version is " + str(ver) + ", Do you wish to update?", "Update Required.", wx.YES_NO | wx.ICON_INFORMATION)
               
                result = dlg.ShowModal()
                dlg.Destroy()
                if result == wx.ID_YES:
                    upgradeFile = "https://raw.github.com/Seafire-Software/Anansi-CalcPad/master/AnansiCalc.py"
                        
                    urllib.urlretrieve(upgradeFile, os.path.join(os.getcwd(), sys.argv[0]))
                    dlg = wx.MessageDialog(None, "Update successful. Please restart the program!", "Restart manually.", wx.YES_NO)
                else:
                    wx.MessageBox("You chose not to upgrade. Please upgrade later!", "Upgrade later.", wx.OK)
            elif ver == progVer:
                wx.MessageBox("You do not need to update. Your version is " + str(progVer) + ", which is equal to the latest version of " + str(ver), "No Update Required.", wx.OK | wx.ICON_INFORMATION)
            elif progVer > ver: 
                wx.MessageBox("What happened here? Your version is " + str(progVer) + " which is greater than the latest version of " + str(ver), "Your version is greater than ours?", wx.OK | wx.ICON_QUESTION)
            else:
                wx.MessageBox("Something went wrong with the update. Please try again. If it happens again, file a bug report please.", "Error!", wx.OK | wx.ICON_ERROR)            
        except:
            wx.MessageBox("There was an error (Error 10152). Maybe you are not connected to the internet? Try again please.", "Try again.", wx.OK)
            
if __name__ == "__main__":
    app = wx.App()
    AnansiCalc(None, title="Anansi CalcPad(r)")
    app.MainLoop()
    