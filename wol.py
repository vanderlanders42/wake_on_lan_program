import wollib
import wx
from os import system, getenv
import socket
from time import sleep
from pathlib import Path

#Wake On Lan Program
#Copyright 2017,2018 Red Ponies A.F.
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
print ("Wake On Lan Program Debug")
print ("2017,2018 Red Ponies A.F.")
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
                wx.MessageBox("Veuillez créer un fichier nommé 'macs.txt'")
                error.MainLoop()
                

class MainFrame(wx.Frame):

    def load_choix(self):
        self.choixmac.InsertColumn(0, 'Machine Distante', width=130)
        self.choixmac.InsertColumn(1, 'Adresse MAC', width=110)
        l = 0
        i = 0
        for element in liste_even:
                self.choixmac.InsertItem(l, element)
                l += 1
                
        for element in liste_odd:
                self.choixmac.SetItem(i, 1, element)
                i += 1

    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title = title,size = (360,302))

        pnl = wx.Panel(self)

        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap("prg.ico", wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)

        #Barre de menu
        self.BarreMenu()
        
        #Entrée rapide
        textecon1 = wx.StaticText(pnl, 1, "Entrée Rapide :",pos = (5, 5)) 
        self.entreerapide = wx.TextCtrl (pnl,pos = (90, 2))
        reveil_b_r = wx.Button(pnl, 1,  "Réveiller", (205, 1), (135, 25))
        reveil_b_r.Bind(wx.EVT_BUTTON,self.OnReveilR)

        #Ajout
        textecon2 = wx.StaticText(pnl, 1, "Nom :",pos = (50, 32))
        self.name_machine = wx.TextCtrl (pnl,pos = (90, 29))
        add_b = wx.Button(pnl, 1, "Ajouter aux addresses", (205, 28), (135, 25))
        add_b.Bind(wx.EVT_BUTTON,self.OnAdd)

        gandalf = wx.StaticLine(pnl, 1, (0, 57), (360, 2), style=wx.LI_HORIZONTAL)

        #Liste des addresses MAC
        self.choixmac = wx.ListCtrl(pnl, 1,pos = (5, 65), size = (244,150), style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        self.load_choix()
                
        reveil_b = wx.Button(pnl, 1,  "Réveiller", (252, 65))
        reveil_b.Bind(wx.EVT_BUTTON,self.OnReveil)

        #Barre d'état
        self.CreateStatusBar()
        self.SetStatusText("soos.")

    def BarreMenu(self):

        fileMenu = wx.Menu()

        editItem = fileMenu.Append(-1, "&Editer les adresses...\tCtrl-E",
                "Ouvre un éditeur de texte pour editer les addresses MAC.")
        fileMenu.AppendSeparator()
        
        exitItem = fileMenu.Append(-1, "&Quitter...\tCtrl-Q",
                "Quitte le programme.")
        
        helpMenu = wx.Menu()
        
        aboutItem = helpMenu.Append(1, "&A propos...\tCtrl-A",
                "Ouvre les crédits du programme.")

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&Fichier")
        menuBar.Append(helpMenu, "&Aide")

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnEdit, editItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)

    def OnAbout(self, event):
        """A propos"""
        wx.MessageBox("Wake On Lan Program\n2.0\n2017,2018 Red Ponies A.F.\n\nUnder GPL 2 License",
                      "About Wake On Lan Program",
                      wx.OK|wx.ICON_INFORMATION)
        
    def OnEdit(self, event):
        editor = getenv('EDITOR')
        if editor:
            system('%s %s' % (getenv('EDITOR'), 'macs.txt'))
        else:
            system('nano macs.txt')
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
            self.SetStatusText("Adresse ajouté")
            sleep(.5)
            self.SetStatusText("soos.")
        else :
             wx.MessageBox("Ce n'est pas une adresse MAC !")

app = wx.App()
frm = MainFrame(None, title='Wake On Lan Program')
frm.Show()
app.MainLoop()
