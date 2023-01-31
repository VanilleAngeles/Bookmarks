#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Source: https://waytolearnx.com/category/python/interface-graphique-python
import os, configparser, json
import requests
import shutil
import datetime
import math
import CryptMac
import re
import wget
import tkinter as tk
# standard process Image from library PIL is on conflict with a other library (tkinter ?). It's necessary to import them on a another name
from PIL import Image as PilImage
from PIL import ImageFont as PilImageFont
from PIL import ImageDraw as PilImageDraw
# End PIL import
from ftplib import FTP
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import font as tkfont
from tkinter import filedialog
###################################################################################
# Classe définissant l'objet représentant la fenêtre principale de l'application
###################################################################################
class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Bookmarks Generator')   # Le titre de la fenêtre
        self.minsize(500,300)      #taille de fenêtre
        # Acces to Preferences File
        self.configFile()
        # Une méthode séparée pour construire le contenu de la fenêtre
        self.createWidgets()
        # remove '#' if list of items is dispalyed in first access
        # self.listItems(False)
    # Méthode de création des widgets
    def configFile(self):
		# Change Directory to be on the same place than de current program
        Dir = os.path.dirname(__file__)
        if Dir != "":
            os.chdir(Dir)
        # Check for Params file and get them
        self.Contener = configparser.ConfigParser()	
        if not os.path.exists('config.ini'):
            messagebox.showerror("Fatal error", "No bkm.ini file")
            exit()
        self.Contener.read('config.ini')
        self.JsonFileName = self.Contener['Files']['JsonFileName']
        if not self.JsonFileName: self.JsonFileName='link.json'
        self.HtmlFileName = self.Contener['Files']['HtmlFileName']
        if not self.HtmlFileName: self.HtmlFileName='index.html'
        self.IconSize     = self.Contener['Pictures']['IconSize']
        if not self.IconSize: self.IconSize='128'
        self.IconDirectory = self.Contener['Pictures']['IconDirectory']
        if not self.IconDirectory: self.IconDirectory = './ico/'
        self.SpecificIconDirectory = self.Contener['Pictures']['SpecificIconDirectory']
        if not self.SpecificIconDirectory: self.SpecificIconDirectory = './img/'
        self.SaveDirectory = self.Contener['Pictures']['SaveDirectory']
        if not self.SaveDirectory: self.SaveDirectory = './sav/'
        if not os.path.exists(self.JsonFileName):
            messagebox.showerror('Fatal error', 'No json file')
            exit()

    def createWidgets(self):
        # Tollbar
        self.Toolbar = Menu(self)
        # Action menu
        menuAction = Menu(self.Toolbar, tearoff=0)
        menuAction.add_command(label="Add", command=self.addItem)
        menuAction.add_command(label="Delete", command=self.delItem)
        menuAction.add_command(label="List", command=lambda:self.listItems(False))
        menuAction.add_separator()
        menuAction.add_command(label="Generate", command=self.FileGenerator)
        menuAction.add_command(label="Send", command=self.FileSender)
        menuAction.add_separator()
        menuAction.add_command(label="Quit", command=self.quit)
        self.Toolbar.add_cascade(label="File", menu=menuAction)
        # Tools menu
        self.menuTools = Menu(self.Toolbar, tearoff=0)
        self.menuTools.add_command(label="Icons loader", command=self.IconsLoader)
        self.menuTools.add_command(label="Preferences", command=self.Preferences)
        self.menuTools.add_command(label="Restore", command=self.FileRestore)
        self.menuTools.add_separator()
        self.menuTools.add_command(label="Quit", command=self.quit)
        self.Toolbar.add_cascade(label="Tools", menu=self.menuTools)
        # Help
        self.menuHelp = Menu(self.Toolbar, tearoff=0)
        self.menuHelp.add_command(label="A propos", command=self.aPropos)
        self.menuHelp.add_command(label="Help", command=self.Help)
        self.menuHelp.add_separator()
        self.menuHelp.add_command(label="Quit", command=self.quit)
        self.Toolbar.add_cascade(label="Help", menu=self.menuHelp)
        self.config(menu=self.Toolbar)
        #
        return()

###################################################################################
# Main menus
###################################################################################
    #---------- add item after checking validation
    def addItem(self):
        #---------- cleaning window
        self.WindowCleaning()
        #---------- choices
        self.grid()
        Label(self, text='Category').grid(row=0)
        Label(self, text='Name').grid(row=1)
        Label(self, text='Link').grid(row=2)
        Label(self, text='Icon').grid(row=3)
        lCategory = self.loadCategories(self.JsonFileName)
        Category = ttk.Combobox(self,values=lCategory)
        Name     = Entry(self)
        Link     = Entry(self)
        Icon     = Entry(self)
        Category.grid(row=0, column=1, padx=5)
        Name.grid(row=1, column=1)
        Link.grid(row=2, column=1)
        Icon.grid(row=3, column=1)
        #---------- Buttons
        Button(self, text='ℹ', command = lambda: self.helpMessage('Category')).grid(row=0, column=2)
        Button(self, text='ℹ', command = lambda: self.helpMessage('Name')).grid(row=1, column=2)
        Button(self, text='ℹ', command = lambda: self.helpMessage('Link')).grid(row=2, column=2)
        Button(self, text='ℹ', command = lambda: self.helpMessage('Icon')).grid(row=3, column=2)
        quitButton = Button(self, text = "Quit", 
                                 command = lambda: self.WindowCleaning())
        quitButton.grid(row=4, column=0)
        submitButton = Button(self, text = "Submit", 
                                 command = lambda: self.submitAddLink(Category.get(),Name.get(),Link.get(),Icon.get()))
        submitButton.grid(row=4, column=1)
        return()

    #---------- del item after inquire  
    def delItem(self):
        #---------- cleaning window
        self.WindowCleaning()
        #---------- choices
        self.grid()
        Label(self, text='Category').grid(row=0)
        Label(self, text='Name').grid(row=1)
        lCategory = self.loadCategories(self.JsonFileName)
        Category = ttk.Combobox(self,values=lCategory,state = 'readonly')
        lItems = []
        self.Items = ttk.Combobox(self,values=lItems,state = 'readonly')
        Category.grid(row=0, column=1, padx=5)
        Category.current()
        Category.bind("<<ComboboxSelected>>", self.loadItems)
        self.Items.grid(row=1,column=1)
        quitButton = Button(self, text = "Quit", 
                                 command = lambda: self.WindowCleaning())
        quitButton.grid(row=2, column=0)
        submitButton = Button(self, text = "Submit", 
                                 command = lambda: self.submitDelLink(Category.get(),self.Items.get()))
        submitButton.grid(row=2, column=1)
        return()

    def listItems(self,FullListItemsMode):
        #---------- cleaning window
        self.WindowCleaning()
        self.grid()
        with open(self.JsonFileName, 'r') as f:
            Links = json.load(f)
        f.close()
        Links.sort(key=lambda x: (x.get('Category'),x.get('Name')))
        l = -1; c = 0; i = -1
        nbColumns = 14
        if not FullListItemsMode: nbColumns = int(nbColumns / 2)
        Colors=['Snow','Snow3']
        PrevCategory = ''
        TitleFont = tkfont.Font(family='Carlito', size=12)
        ItemFont  = tkfont.Font(family='Carlito', size=8)
        for Item in Links:
            i += 1
            if Item['Category'] != PrevCategory:
                PrevCategory = Item['Category']
                l += 1
                c = 0
                Cell = Entry(self, justify=CENTER, width=64, borderwidth=1, font=TitleFont, bg='Silver', relief='ridge')
                Cell.insert(END, Item['Category'])
                Cell.grid(row=l, columnspan=nbColumns)
                l += 1
            if c == nbColumns:
                l += 1
                c = 0
            if FullListItemsMode:
                Cell = Button(self, justify=CENTER, borderwidth=1, bg=Colors[i%2], font=ItemFont, text=format(i,'3'),relief='raised') 
                Cell.grid(row=l,column=c)
                c += 1
            Cell = Entry(self, justify=CENTER, borderwidth=1, bg=Colors[i%2], font=ItemFont, relief='raised')
            Cell.insert(END, Item['Name'])
            Cell.grid(row=l,column=c,ipady=4)
            c += 1
        return()
    def FileGenerator(self):
        """
        Source: https://vidigest.com/2018/12/02/generating-an-html-table-from-file-data-using-python-3/
        Generate the Html file from Json file.
        """
        filein = self.JsonFileName
        fileout = open(self.HtmlFileName, "w")
        with open(self.JsonFileName, 'r') as f:
            Links = json.load(f)
        Links.sort(key=lambda x: (x.get('Category'),x.get('Name')))
        maxColumn = 8
        nbColumn = 1
        previousCategory = ''
        # Colors are in css file; [l/i/j]Colors for loop on color list
        Colors = ['rose','gold','gris','marron','bleu','jaune','violet','vert','rouge','marine']
        lColors=len(Colors)
        iColors=-1
        iCategory = 0
        iLink = 0
        tabCategory = []
        iLinkPerCategory = 0

        # Count number of Categories, number of Links and Links per Category
        for Item in Links:
            iLink += 1
            Category = Item['Category']
            if (Category != previousCategory):
                iCategory += 1
                if previousCategory != '':
                    tabCategory += [previousCategory, iLinkPerCategory]
                iLinkPerCategory = 0
                previousCategory = Category
            iLinkPerCategory += 1

        tabCategory += [previousCategory, iLinkPerCategory]
        # Calculate number of lines/columns et a 16/9 screen format
        maxLines = round(math.sqrt(iLink/14*9)+0.5)
        previousCategory = ''
        iCategory = 0
        iLines = 1
        # write the Html header
        table = ''
        headerFile = open('header.html', 'r')
        records = headerFile.readlines()
        for record in records:
            table += record
        headerFile.close()
        
        # Javascript in Html - necessary because the number of icons (iLink) is variable
        table+= '<script type=\"text/javascript\">\n'
        table += 'ICONE=Math.round(Math.sqrt(screen.width * screen.height * 0.7 / '
        table += str(iLink)
        table += ') * 0.6)\n'
        table += 'document.write(\"<style>img { border: 0px solid black; margin-left: 0px; margin-right: 0px; width: \"+ICONE+\"px; height: \"+ICONE+\"px } </style>\")\n'
        table += '</script>\n'

        # Main table
        table += "<table  class=\"Coral\"><tr><td>\n"
        # Create the table's row data
        for Item in Links:
            Category = Item['Category']
            Name = Item['Name']
            Link = Item['Link']
            Icon = Item['Icon']
            if (Category != previousCategory):
                if previousCategory != '':
                    # Fill empty cells until maxLines for previous Category
                    while iLines < maxLines:
                        table += "    </tr><tr><td><img src=\"null.png\"></td>"
                        iLines += 1
                    table += "  </td></table><td>\n"
                    iLines = 1
                # Compute number of cells per line for this category
                iCells = tabCategory[iCategory+1]
                iCellsPerLine = int((iCells/maxLines)+0.99)
                iColors += 1
                jColors = iColors%lColors
                table += "  <table class=\""
                table += Colors[jColors]
                table += "\">\n"
                table += "    <tr align=\"center\">\n"
                table += "      <th colspan=\""
                table += str(iCellsPerLine)
                table += "\"><h2><center>"
                table += Category
                table += " </h2></center></th>\n"
                table += "    </tr><tr>\n"
                previousCategory = Category
                iCategory += 2
                iTd = 0
                nbColumn = 0
            if iTd == iCellsPerLine:
                table += "    </tr><tr>\n"
                iLines += 1
                iTd = 1
            else:
                iTd +=1
            table += "        <td><a data-title=\""
            table += Name
            table += "\" href=\""
            table += Link
            table += "\" target=\"_blank\"><img src=\""
            if Icon == '':
                table += self.IconDirectory
                table += Name
                table += ".png\" ></a> </td>\n"
            else:
                table += self.SpecificIconDirectory
                table += Icon
                table += "\"></a> </td>\n"
        # close the last category
        while iLines < maxLines:
            table += "    </tr><tr><td><img src=\"null.png\"></td>"
            iLines += 1
        table += "  </tr>\n"
        table += "</td></tr></table>"

        fileout.writelines(table)
        fileout.close()
        f.close()
        messagebox.showinfo('Generator', 'Html file has been generated')
        return()

    def FileSender(self):
        """
        General purpose: 
            Generate files list to transfer
        ftp parameters are in a crypted file named .ftp.
            Exemple of file generating: python3 Crypt.py .ftp '{ "Host": "giveYourOwn", "Port": "giveYourOwn", "ftpUsername": "giveYourOwn", "ftpPassword": "giveYourOwn" }'
        """
        ftpParameters = CryptMac.Uncrypt('.ftp')
        dictParameters = json.loads(ftpParameters)
        ftpHost = dictParameters['Host']
        ftpPort = dictParameters['Port']
        ftpUsername = dictParameters['Username']
        ftpPassword = dictParameters['Password']
        ftp=FTP(ftpHost,ftpUsername,ftpPassword)
        ftp.cwd('b')
        f=open(self.HtmlFileName, 'rb')
        ftp.storbinary('STOR ' + self.HtmlFileName, f)
        f.close()
        ftp.cwd(self.IconDirectory)
        listFilesToTransfer = list()
        listFiles = os.listdir(self.IconDirectory)
        refDate = os.path.getctime(os.path.join('LastUpdateDate.txt'))
        for File in listFiles:
            fileDate = os.path.getctime(os.path.join(self.IconDirectory+File))
            if fileDate >= refDate:
                listFilesToTransfer.append(self.IconDirectory+File)
                f=open(self.IconDirectory + File, 'rb')
                ftp.storbinary('STOR ' + File, f)
                f.close()
        ftp.cwd('..')
        ftp.cwd(self.SpecificIconDirectory)
        listFilesToTransfer = list()
        listFiles = os.listdir(self.SpecificIconDirectory)
        refDate = os.path.getctime(os.path.join('LastUpdateDate.txt'))
        for File in listFiles:
            fileDate = os.path.getctime(os.path.join(self.SpecificIconDirectory+File))
            if fileDate >= refDate:
                listFilesToTransfer.append(self.SpecificIconDirectory+File)
                f=open(self.SpecificIconDirectory + File, 'rb')
                ftp.storbinary('STOR ' + File, f)
                f.close()
        listFilesToTransfer = list()
        listFiles = os.listdir(self.SpecificIconDirectory)
        refDate = os.path.getctime(os.path.join('LastUpdateDate.txt'))
        for File in listFiles:
            fileDate = os.path.getctime(os.path.join(self.SpecificIconDirectory+File))
            if fileDate >= refDate:
                listFilesToTransfer.append(self.SpecificIconDirectory+File)
                f=open(self.SpecificIconDirectory+File, 'rb')
                ftp.storbinary('STOR ' + File, f)
                f.close()
        ftp.quit()
        os.remove('LastUpdateDate.txt')
        with open('LastUpdateDate.txt', "w") as f:
            f.write('')
        f.close()
        messagebox.showinfo('Gender', 'Files have been send')
        return()

    def IconsLoader(self):
        font = PilImageFont.truetype("Ubuntu-M.ttf", 28)
        with open(self.JsonFileName, 'r') as f:
            Links = json.load(f)
        f.close()
        for Item in Links:
            Name = Item['Name']
            Link = Item['Link']
            icoFile = self.IconDirectory
            icoFile += Name
            icoFile += '.png'
            try:
                os.remove(icoFile)
            except:
                print('[I]', icoFile, 'not removed')
            paraSentence = 'https://www.google.com/s2/favicons?sz='
            paraSentence += str(self.IconSize)
            paraSentence += '&domain_url='
            paraSentence += Link
            try:
                FN=wget.download(url=paraSentence,out=icoFile)
                img = PilImage.open(icoFile)
            except:
                print('[I]', Link, ' not found')
                img = PilImage.new('RGB', (int(self.IconSize), int(self.IconSize)), color = 'red')
                draw = PilImageDraw.Draw(img)
                draw.text((3, 23),Name,(0,0,0),font=font)
                img.save(icoFile)
        messagebox.showinfo('IconsLoader', 'All icons have been generated')
        return()	

    def Preferences(self):
        #---------- sources: https://docs.python.org/3/library/configparser.html
        self.WindowCleaning()
        self.grid()
        Label(self, text='Files', bg='red', padx=50).grid(row=0, columnspan=2)
        Label(self, text='jsonfilename').grid(row=1, column=0)
        Label(self, text='htmlfilename').grid(row=2, column=0)
        Label(self, text='Pictures', bg='red', padx=40).grid(row=3, columnspan=2)
        Label(self, text='iconsize').grid(row=4, column=0)
        Label(self, text='icondirectory').grid(row=5, column=0)
        Label(self, text='specificicondirectory').grid(row=6, column=0)
        Label(self, text='savedirectory').grid(row=7, column=0)
        JsonFileName    = Entry(self)
        JsonFileName.insert(END, self.JsonFileName)
        JsonFileName.grid(row=1, column=1)

        HtmlFileName    = Entry(self)
        HtmlFileName.insert(END, self.HtmlFileName) 
        HtmlFileName.grid(row=2, column=1)
        
        IconSize        = Entry(self)
        IconSize.insert(END,self.IconSize)
        IconSize.grid(row=4, column=1)
        
        IconDirectory   = Entry(self)
        IconDirectory.insert(END, self.IconDirectory)
        IconDirectory.grid(row=5, column=1)
        
        SpecificIconDirectory = Entry(self)
        SpecificIconDirectory.insert(END, self.SpecificIconDirectory)
        SpecificIconDirectory.grid(row=6, column=1)
        
        SaveDirectory   = Entry(self, textvariable=self.SaveDirectory)
        SaveDirectory.insert(END, self.SaveDirectory)  
        SaveDirectory.grid(row=7, column=1)

        Button(self, text='Update', command=lambda: self.UpdatePreferences(JsonFileName,HtmlFileName,IconSize,IconDirectory,SpecificIconDirectory,SaveDirectory)).grid(row=8, column=0)
        Button(self, text='Quit', command=lambda: self.WindowCleaning()).grid(row=8, column=1)

        return()


    def FileRestore(self):
        self.WindowCleaning()
        fileToBeRestored = filedialog.askopenfilename(initialdir= self.SaveDirectory,title="Select File",filetypes=(('link files','link.json*'),('all files','*.*'))) 
        if not fileToBeRestored:
            return()
        SavedFile = self.SaveDirectory + self.JsonFileName + datetime.datetime.now().strftime("%y%m%d%H%M%S")
        shutil.copy(self.JsonFileName, SavedFile)
        messagebox.showinfo('FileSave', 'File '+ self.JsonFileName + ' has been saved')
        shutil.copy(fileToBeRestored, self.JsonFileName)
        messagebox.showinfo('FileRestore', 'File '+ fileToBeRestored + ' has been restored')
        return()
        
    def aPropos(self):
        AboutWindow = tk.Toplevel()
        AboutWindow.title('About')
        tAbout = '''
        Programme existant en deux versions:
        - une en interface graphique (bkmUI) à base de tkinter
        - une en ligne de commande (bkm)
        Il est écrit en python3, il se sert:
        - des bibliothèques standard (os, time, tkinter...)
        - de bibliothèques installées (json, ftplib...)
        - de sous-programmes locaux (CheckFileLocation, CryptMac)
        '''
        tAbout = re.sub("\n\s*", "\n", tAbout) # remove leading whitespace from each line
        Label(AboutWindow,text=tAbout,width=100,height=10, justify=LEFT).pack()
        Button(AboutWindow, text='OK', command=AboutWindow.destroy).pack()
        return()
    def Help(self):
        HelpWindow = tk.Toplevel()
        HelpWindow.title('Help')
        tHelp = '''
        Ce programme construit une base Json qui sert ensuite à générer un fichier html.
        La base Json est construite de la manière suivante (par en registrement non hiérarchisé):
        - la Catégorie: permet de regrouper les liens par famille
        - le nom: permet d'identifier le lien et l'icône associée
        - le lien: qui pointe vers le site à atteindre
        - [l'icône]: si on ne prend pas le favicon du site, fichier qui servira d'icône
        Le process naturel est de créer des signets, de générer le fichier Html qu'on publiera.
        Le fichier config.ini désigne les paramètres, fichiers et répertoires à utiliser 
        '''
        tHelp = re.sub("\n\s*", "\n", tHelp) # remove leading whitespace from each line
        Label(HelpWindow,text=tHelp,width=100,height=10, justify=LEFT).pack()
        Button(HelpWindow, text='OK', command=HelpWindow.destroy).pack()
        return()

###################################################################################
# Utilities
####################################################################################
    def helpMessage(self,Item):
        match Item:
            case 'Category':
                messagebox.showinfo('Category', 'Use a choice or enter a new category\nCategory is not mandatory, must use letters (replaced by \"_\"),lowercase (transformed)')
            case "Name":
                messagebox.showinfo('Name', 'Name is not mandatory, must use letters (replaced by \"_\"),lowercase (transformed)')
            case 'Link':
                messagebox.showinfo('Link', 'Link must be valid (checked)')
            case 'Icon':
                messagebox.showinfo('Icon', 'Icon name in specificicondirectory\n(check config.ini)')
            case _:
                messagebox.showinfo('Other', 'No help file')
        return()
    
    def WindowCleaning(self):
        #---------- cleaning window
        for Widget in self.winfo_children():
            Widget.destroy()
        #---------- Restore header
        self.createWidgets()
        return()

    def submitAddLink(self,Category,Name,Link,Icon):
        #---------- check and transform strings
        Category=self.checkString(Category)
        Name=self.checkString(Name)
        Link=self.checkLink(Link)
        if Icon != '':
            Icon=self.checkIcon(Icon)
        #---------- check arguments
        if Category == '' or Name == '' or Link == '':
            messagebox.showerror("Error", "Category/Name/Link\n are not mandatory\n or not available")
            return()
        #------------------------------
        font = PilImageFont.truetype("Ubuntu-M.ttf", 28)
        JsonVersion = str(datetime.datetime.now().time())
        with open(self.JsonFileName, 'r') as f:
            Links = json.load(f)
        f.close()

        if Icon == '':
            iconFile = self.IconDirectory
            iconFile += Name
            iconFile += ".png"
            paraSentence = 'https://www.google.com/s2/favicons?sz='
            paraSentence += str(self.IconSize)
            paraSentence += '&domain_url='
            paraSentence += Link
            try:
                FN=wget.download(url=paraSentence,out=iconFile)
                img = PilImage.open(iconFile)
                '''
                if (img.size != 64):
                    img=img.resize((64,64))
                    img.save(icoFile)
                '''
            except:
                img = PilImage.new('RGB', (int(self.IconSize), int(self.IconSize)), color = 'red')
                draw = PilImageDraw.Draw(img)
                draw.text((3, 23),Name,(0,0,0),font=font)
                img.save(iconFile)

        # Save previous Json file
        SavedFile = self.SaveDirectory + self.JsonFileName + datetime.datetime.now().strftime("%y%m%d%H%M%S")
        shutil.copy(self.JsonFileName, SavedFile)
        # Add new record in Json file
        addRecord = {'Category': Category , 'Name': Name, 'Link': Link, 'Icon': Icon}
        Links.append(addRecord)
    #	Links.sort(key=lambda x: (x.get('Category'),x.get('Name')))
        f = open(self.JsonFileName,'w')
        json.dump(Links, f, indent=4)
        f.close()
        messagebox.showinfo('Add Link', 'Item '+Category+' '+Name+' created')
        return()

    def submitDelLink(self,Category,Name):
        with open(self.JsonFileName, 'r') as f:
            self.Links = json.load(f)
        f.close()
        iDelete = 0
        for Item in self.Links:
            if Category == Item['Category'] and Name == Item['Name']:
                # Delete Icon File
#                Name = Links[int(iDelete)]['Name']
                icoToDelete = self.IconDirectory
                icoToDelete += Name
                icoToDelete += '.png'
                try:
                    os.remove(icoToDelete)
                except:
                    messagebox.showinfo('Icon deleted', 'No icon file to remove')
                # remove record from list 
                del self.Links[int(iDelete)]
            iDelete += 1
        self.SaveSortDump()
        return()

    def SaveSortDump(self):
        # save previous json file
        SavedFile = self.SaveDirectory + self.JsonFileName + datetime.datetime.now().strftime("%y%m%d%H%M%S")
        shutil.copy(self.JsonFileName, SavedFile)
        f = open(self.JsonFileName,'w')
        json.dump(self.Links, f, indent=4)
        f.close()
        # sort and save json file
        self.Links.sort(key=lambda x: (x.get('Category'),x.get('Name')))
        f = open(self.JsonFileName,'w')
        json.dump(self.Links, f, indent=4)
        f.close()
        messagebox.showinfo('Item deleted', 'Json file saved \nIcon removed \nNew Json file on line')
        return()

    def checkString(self,String):
        newString = ''
        String = String.lower()
        for c in String:
            if not c.isalpha():
                newString = newString + '_'
            else:
                newString = newString + c
        return(newString)

    def checkLink(self,Link):
        try:
            r = requests.get(Link)
            return(Link)
        except:
            return('')

    def checkIcon(self, Icon):
        specificIconFile = self.SpecificIconDirectory + Icon
        if not os.path.exists(specificIconFile):
            messagebox.showwarning('No icon file found','Default file will be used')
            return('')
        return(Icon)

    def loadCategories(self,JsonFileName):
        with open(JsonFileName, 'r') as f:
            Links = json.load(f)
        f.close()
        lCategory = []
        prevCategory = ''
        for Item in Links:
            if Item['Category'] != prevCategory:
                lCategory.append(Item['Category'])
                prevCategory = Item['Category']
        return(lCategory)

    def loadItems(self,event):
        Category = event.widget.get()
        with open(self.JsonFileName, 'r') as f:
            Links = json.load(f)
        f.close()
        lItems = []
        for Item in Links:
            if Item['Category'] == Category:
                lItems.append(Item['Name'])
        self.Items['values'] = lItems
        return()

    def UpdatePreferences(self,JsonFileName,HtmlFileName,IconSize,IconDirectory,SpecificIconDirectory,SaveDirectory):
        #---------- get all values and put them in Contener
        self.Contener.set('Files','jsonfilename',JsonFileName.get())
        self.Contener.set('Files','htmlfilename',HtmlFileName.get())
        self.Contener.set('Pictures','iconsize',IconSize.get())
        self.Contener.set('Pictures','icondirectory',IconDirectory.get())
        self.Contener.set('Pictures','specificicondirectory',SpecificIconDirectory.get())
        self.Contener.set('Pictures','savedirectory',SaveDirectory.get())
        #---------- write Contener
        with open('bkm.ini', 'w') as f:
            self.Contener.write(f)
        #---------- Update variables
        self.JsonFileName = self.Contener['Files']['JsonFileName']
        self.HtmlFileName = self.Contener['Files']['HtmlFileName']
        self.IconSize     = self.Contener['Pictures']['IconSize']
        self.IconDirectory = self.Contener['Pictures']['IconDirectory']
        self.SpecificIconDirectory = self.Contener['Pictures']['SpecificIconDirectory']
        self.SaveDirectory = self.Contener['Pictures']['SaveDirectory']

        return()

app = Application()
app.mainloop()