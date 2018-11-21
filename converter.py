#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#
##------- Importation des modules --------##
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from lxml import etree
import gzip
import shutil
import tempfile
import os

##------- Classes ------#
# class Voiture:
#     def __init__(self, X, Y, longueur, sens, couleur, valeur):
    
                


##------- Définition des fonctions --------##
def open_file(path):
    global filename
    tmp = tempfile.mkdtemp()
    filename = os.path.splitext(os.path.basename(path))[0]
    temp_fichier = tmp + '/' + filename

    if path: #Si un fichier est choisi
        with gzip.open(path, 'rb') as f_in:
            with open(temp_fichier, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        return etree.parse(temp_fichier)
    else: return None

def convert_data(projectFile, versionToConvert):
    global filename
    for project in (projectFile.xpath("/PremiereData/Project")):
        if project.get('Version'):
            project.set('Version', versionToConvert)
            return etree.tostring(projectFile, pretty_print=True)

def write_output_file(data, callback):
    output_file = filedialog.asksaveasfilename(initialdir = "./",title = "Enregistrer", defaultextension=".prproj", filetypes = (("Projets Premiere Pro","*.prproj"),("Tous les fichiers","*.*")))
    if output_file: # asksaveasfile return `None` if dialog closed with "cancel".
        if not output_file.endswith(".prproj"):
            output_file = output_file+".prproj"
        with gzip.open(output_file, 'wb') as f:
            f.write(data)
        callback()
    else: return


def get_src_version(projectFile):
    for project in (projectFile.xpath("/PremiereData/Project")):
        if project.get('Version'):
            return project.get('Version')

def get_src_file():
    global src_filename
    global projectFile
    src_filename = filedialog.askopenfilename(initialdir = "./",title = "Ouvrir un projet", filetypes = (("Projets Premiere Pro","*.prproj"),("Tous les fichiers","*.*")))
    if src_filename is None:
        return
    entryTextfile.set(src_filename)
    projectFile = open_file(src_filename)
    if projectFile:
        src_version = get_src_version(projectFile)
        fieldsrcversion.config(text=src_version)
        entryTextDestV.set(int(src_version)-1)
        file_menu.entryconfig("Fermer le fichier", state='normal')

def ok_message():
    messagebox.showinfo('Opération terminée', "L'enregistrement a été effectué")
    clear()

def convert():
    version = destinationversion.get()
    if version and projectFile:
        write_output_file(convert_data(projectFile, version), ok_message)
    else:
        messagebox.showerror("Erreur", "Veillez à remplir tous les champs.")
def clear():
    entryTextfile.set('Ouvrir un fichier...')
    entryTextDestV.set("")
    fieldsrcversion.config(text="")
    file_menu.entryconfig("Fermer le fichier", state='disabled')

def textToVersion(argument):
    version = 35
    switcher = {
        "CC 2018 (v12.0)" : "34",
        "CC 2018 (v12.1)" : "35",
        "CC 2019 (v13.0)" : "36",
    }
    return switcher.get(argument, version)

def setPreconf(var):
    entry = var.get()
    entryTextDestV.set(textToVersion(entry))

def display_version():
    temp_filename = filedialog.askopenfilename(initialdir = "./",title = "Ouvrir un projet", filetypes = (("Projets Premiere Pro","*.prproj"),("Tous les fichiers","*.*")))
    if temp_filename is None:
        return
    tempFile = open_file(temp_filename)
    if tempFile:
        messagebox.showinfo('Détection de version', "Le fichier de projet sélectionné utilise la version de fichier " + get_src_version(tempFile))

##------- Variables globales --------##


##------- Création de la fenêtre -------##
fen = Tk()
fen.title('Premiere Converter')                # ---> On donne un titre à la fenêtre

# ##-------- Création du menu ---------##
main_menu = Menu(fen)

file_menu = Menu(main_menu, tearoff=0)
file_menu.add_command(label="Ouvrir un fichier", command=get_src_file)
file_menu.add_command(label="Fermer le fichier", command=clear, state='disabled')
file_menu.add_separator()
file_menu.add_command(label="Quitter", command=fen.quit)

tools_menu = Menu(main_menu, tearoff=0)
tools_menu.add_command(label="Déterter la version d'un fichier...", command=display_version)

main_menu.add_cascade(label="Fichier", menu=file_menu)
main_menu.add_cascade(label="Options", menu=tools_menu)

fen.config(menu=main_menu)



# ##-------- Création des zones de texte ---------##
tmp = Label(fen, text='Convertir un projet Premiere Pro vers une ancienne verison')
tmp.grid(row= 0, column = 0, columnspan=2,padx=5, pady=5)

entryTextfile = StringVar()
fieldname = Entry(fen, text="", width=50, state="readonly", textvariable=entryTextfile)
entryTextfile.set('Ouvrir un fichier...')

fieldname.grid(row= 1, column = 0,padx=5, pady=5)

browse = Button(fen, text="Parcourir", command=get_src_file)
browse.grid(row= 1, column = 1,padx=5, pady=5)

tmp = Label(fen, text="Version du Projet source : ", justify="left")
tmp.grid(row= 2, column = 0 ,padx=5, pady=5)
fieldsrcversion = Label(fen, text="", width=3)
fieldsrcversion.grid(row= 2, column = 1 ,padx=5, pady=5)

tmp = Label(fen, text='Convertir vers: ', justify="right")
tmp.grid(row= 3, column = 0,padx=5, pady=5)

entryTextDestV= StringVar()
destinationversion = Entry(fen, width=3, textvariable=entryTextDestV)
destinationversion.grid(row= 3, column = 1 ,padx=5, pady=5)

choixdef = StringVar(fen)
choixdef.set("Personnalisé") # initial value
choixdef.trace("w", lambda name, index, mode, sv=choixdef: setPreconf(choixdef))
option = OptionMenu(fen, choixdef, "Personnalisé", "CC 2018 (v12.0)", "CC 2018 (v12.1)", "CC 2019 (v13.0)")
option.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

tmp = Button(fen, text="Quitter", command=fen.destroy)
tmp.grid(row=5, column=1, padx=5, pady=5)

tmp = Button(fen, text="Convertir", command=convert, width=30)
tmp.grid(row=5, column=0, padx=5, pady=5)


option.bind("Button-")
##------- Programme principal -------##
# converted_data = open_file(), convert_data)
# write_output_file(converted_data)

fen.resizable(width=False, height=False) # on veut une fenêtre non redimensionnable
fen.mainloop()
