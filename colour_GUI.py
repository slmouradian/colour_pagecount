#!/usr/bin/env python

'''
    Copyright 2014 Simon Mouradian, Frank Milthaler
    This file is part of Colour Pagecount.

    Colour Pagecount is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Colour Pagecount is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Colour Pagecount.  If not, see <http://www.gnu.org/licenses/>.

'''

import Tkinter
import os
import tkFileDialog
import tkMessageBox
import colour_pagecount

class simpleapp_tk(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
        self.addMenus()

    def initialize(self):
        self.geometry('600x400+200+200')
        self.grid()
        
        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self, textvariable=self.entryVariable)
        self.entry.grid(column=0,row=0,sticky='EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(u"Enter filename here.")
        
        button = Tkinter.Button(self,text=u'Count!', command=self.OnButtonClick)
        button.grid(column=1,row=0)

        button = Tkinter.Button(self,text=u'Open', command=self.mOpen)
        button.grid(column=2,row=0)
        
        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelVariable,
                              anchor='w',fg='white',bg='blue')
        label.grid(column=0,row=1,columnspan=3,sticky='EW')
        self.labelVariable.set(u"Hello !")

        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)

    def addMenus(self):
        menubar = Tkinter.Menu(self)
        filemenu = Tkinter.Menu(menubar, tearoff = 0)
        filemenu.add_command(label='Open', command=self.mOpen)
        filemenu.add_command(label='Exit', command=self.mQuit)
        menubar.add_cascade(label='File',menu=filemenu)


        aboutmenu = Tkinter.Menu(menubar, tearoff = 0)
        aboutmenu.add_command(label='About', command=self.mAbout)
        aboutmenu.add_command(label='License', command=self.mLicense)
        menubar.add_cascade(label='About', menu=aboutmenu)
        self.config(menu=menubar)

    def OnButtonClick(self):
        if colour_pagecount.bad_version():
            tkMessageBox.showerror('Error', 'Incompatible version of gs')
            self.labelVariable.set( 'Incompatible version' )
            return
        filename = self.entryVariable.get()
        if not os.path.isfile(filename):
            tkMessageBox.showerror('Error', 'Please enter a valid filename')
            return
        colour_pages = colour_pagecount.count_pages(filename)
        self.labelVariable.set( colour_pagecount.print_pages(filename, colour_pages))
        return

    def OnPressEnter(self,event):
        self.labelVariable.set( self.entryVariable.get())

    def mOpen(self):
        self.entryVariable.set(tkFileDialog.askopenfilename())

    def mQuit(self):
        if tkMessageBox.askyesno('Quit', 'Are you sure?'):
            self.destroy()

    def mAbout(self):
        pass

    def mLicense(self):
        pass

if __name__=="__main__":
    app = simpleapp_tk(None)
    app.title('Colour Pagecount')
    try:
        app.wm_iconbitmap('@pagecount_icon.xbm')
    except Tkinter.TclError:
        print 'No icon found.'
    app.mainloop()
