import wollib
import wx
import socket
from pathlib import Path
from subprocess import run

#WOLP (Wake On Lan Program) 2.1
#Copyright 2017,2018 Vladimir Vanderlanders
"""This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>."""
#Attention, commentaires en Franglais.

#Init
print ("WOLP Debug")
print ("2017,2018 Vladimir Vanderlanders")
testfile = Path("macs.txt")
if testfile.is_file():
                conffile = open("macs.txt","r")
                content = conffile.readlines()
                print(content)
                liste = [x.strip() for x in content] 
                conffile.close
                liste_even = liste[::2]
                print(liste_even)
                liste_odd = liste[1:][::2]
                print(liste_odd)
else :
                error = wx.App()
                wx.MessageBox("Please create a file named 'macs.txt'")
                error.MainLoop()
                

class MainFrame(wx.Frame):

    def load_choix(self):
        self.choixmac.InsertColumn(0, 'Computer Name', width=130)
        self.choixmac.InsertColumn(1, 'MAC Address', width=110)
        l = 0
        i = 0
        for element in liste_even:
                self.choixmac.InsertItem(l, element)
                l += 1
                
        for element in liste_odd:
                self.choixmac.SetItem(i, 1, element)
                i += 1

    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title = title,size = (360,302), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)

        pnl = wx.Panel(self)

        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap("lib/prg.ico", wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)

        #Barre de menu
        self.BarreMenu()
        
        #Entrée rapide
        textecon1 = wx.StaticText(pnl, 1, "Address :",pos = (5, 5)) 
        self.entreerapide = wx.TextCtrl (pnl,pos = (60, 2), size = (140,-1))
        reveil_b_r = wx.Button(pnl, 1,  "Wake", (205, 1), (135, 25))
        reveil_b_r.Bind(wx.EVT_BUTTON,self.OnReveilR)

        #Ajout
        textecon2 = wx.StaticText(pnl, 1, "Name :",pos = (15, 32))
        self.name_machine = wx.TextCtrl (pnl,pos = (60, 29), size = (140,-1))
        add_b = wx.Button(pnl, 1, "Add to list", (205, 28), (135, 25))
        add_b.Bind(wx.EVT_BUTTON,self.OnAdd)

        gandalf = wx.StaticLine(pnl, 1, (0, 57), (360, 2), style=wx.LI_HORIZONTAL)

        #Liste des addresses MAC
        self.choixmac = wx.ListCtrl(pnl, 1,pos = (5, 65), size = (244,150), style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        self.load_choix()
                
        reveil_b = wx.Button(pnl, 1,  "Wake", (252, 65))
        reveil_b.Bind(wx.EVT_BUTTON,self.OnReveil)

        #Barre d'état
        self.CreateStatusBar()
        self.SetStatusText("Ready.")

    def BarreMenu(self):

        fileMenu = wx.Menu()

        editItem = fileMenu.Append(-1, "&Edit list\tCtrl-E",
                "Opens text editor for editing MAC addresses.")
        fileMenu.AppendSeparator()
        
        exitItem = fileMenu.Append(-1, "&Exit...\tCtrl-Q",
                "Tired already ?")
        
        helpMenu = wx.Menu()
        
        aboutItem = helpMenu.Append(1, "&About...\tCtrl-A",
                "About WOLP.")

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnEdit, editItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)

    def OnAbout(self, event):
        """A propos"""
        wx.MessageBox("WOLP 2.1\nCopyright 2017,2018 Vladimir Vanderlanders\n\nUnder GNU GPL 2 License (see COPYING or LICENSE file)",
                      "About Wake On Lan Program",
                      wx.OK|wx.ICON_INFORMATION)
        
    def OnEdit(self, event):
        run(['nano','./macs.txt'])
        #Reload
        conffile = open("macs.txt","r")
        content = conffile.readlines()
        liste = [x.strip() for x in content] 
        conffile.close
        global liste_even
        liste_even = liste[::2]
        global liste_odd
        liste_odd = liste[1:][::2]
        self.choixmac.ClearAll()
        self.load_choix()
               

    def OnReveilR(self, event):
        MAC = self.entreerapide.GetValue()
        wollib.wake(MAC)

    def OnReveil(self, event):
        print("wol: Item No. : ", self.choixmac.GetFocusedItem())
        num = self.choixmac.GetFocusedItem()
        MAC = self.choixmac.GetItemText(num, 1)
        print("wol: Address Used : ", MAC) 
        MAC = MAC.replace("\n", "")
        wollib.wake(MAC)

    def OnAdd(self, event):
        addr = '\n' + self.entreerapide.GetValue() + '\n'
        nom = self.name_machine.GetValue()
        verif = len(addr)
        if verif == 14 or verif == 19 :
            with open('macs.txt', 'a') as file:
                file.write(nom)
                file.write(addr)
                file.close
            #Reload
            conffile = open("macs.txt","r")
            content = conffile.readlines()
            liste = [x.strip() for x in content] 
            conffile.close
            global liste_even
            liste_even = liste[::2]
            global liste_odd
            liste_odd = liste[1:][::2]
            self.choixmac.ClearAll()
            self.load_choix()
            self.SetStatusText("Sucessfully added !")
        else :
             wx.MessageBox("This isn't a MAC address !")

app = wx.App()
frm = MainFrame(None, title='Wake On Lan Program')
frm.Show()
app.MainLoop()
