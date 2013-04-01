"""
Thanks to FogleBird from stackoverflow.
He responded to another questions that gave me the idea on how to do most of this.
http://stackoverflow.com/questions/6389580/quick-and-easy-trayicon-with-python
"""

import wx
import os

class Icon(wx.TaskBarIcon):

    def __init__(self, parent, icon, tooltip):
        wx.TaskBarIcon.__init__(self)
        self.SetIcon(icon, tooltip)
        self.parent = parent
        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.OnLeftDClick)
        self.CreateMenu()

    def CreateMenu(self):
        self.Bind(wx.EVT_TASKBAR_RIGHT_UP, self.OnPopup)
        self.menu = wx.Menu()
        topen = self.menu.Append(wx.ID_ANY, '&Open')
        self.menu.Bind(wx.EVT_MENU, self.OnOpen, topen)
        self.menu.AppendSeparator()
        profiles = os.listdir("/etc/netctl/")
        for i in profiles:
            if os.path.isfile("/etc/netctl/" + i):
                profile = self.menu.Append(wx.ID_ANY, i)
                self.menu.Bind(wx.EVT_MENU, self.OnConnect, profile)
            else:
                pass
        self.menu.AppendSeparator()
        texit = self.menu.Append(wx.ID_EXIT, 'E&xit')
        self.menu.Bind(wx.EVT_MENU, self.OnExit, texit)
    
    def OnConnect(self, e):
        item = self.menu.FindItemById(e.GetId())
        profile = item.GetText()
        os.system("netctl stop-all")
        os.system("netctl start " + profile)
    
    def OnExit(self, e):
        wx.CallAfter(self.Destroy)
        self.parent.Destroy()

    def OnOpen(self, e):
        self.parent.Show()
    def OnPopup(self, event):
        self.PopupMenu(self.menu)

    def OnLeftDClick(self, event):
        if self.parent.IsIconized():
            self.parent.Iconize(False)
        if not self.parent.IsShown():
            self.parent.Show(True)
            self.parent.Raise()
        else:
            self.parent.Show(False)