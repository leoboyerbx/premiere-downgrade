#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#
##------- Importation des modules --------##
from tkinter import *
from tkinter import filedialog
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
            print(project.get('Version'))
            project.set('Version', versionToConvert)
            print(project.get('Version'))
            return etree.tostring(projectFile, pretty_print=True)

def write_output_file(data):
    output_file = filedialog.asksaveasfilename(initialdir = "./",title = "Enregistrer", defaultextension=".prproj", filetypes = (("Projets Premiere Pro","*.prproj"),("Tous les fichiers","*.*")))
    if output_file is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    if not output_file.endswith(".prproj"):
        output_file = output_file+".prproj"
    with gzip.open(output_file, 'wb') as f:
        f.write(data)


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
    src_version = get_src_version(projectFile)
    fieldsrcversion.config(text=src_version)
    entryTextDestV.set(int(src_version)-1)

def convert():
    version = destinationversion.get()
    write_output_file(convert_data(projectFile, version))

##------- Variables globales --------##


##------- Création de la fenêtre -------##
fen = Tk()
fen.title('Premiere Converter')                # ---> On donne un titre à la fenêtre

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

tmp = Button(fen, text="Quitter")
tmp.grid(row=4, column=0, padx=5, pady=5)

tmp = Button(fen, text="Convertir", command=convert)
tmp.grid(row=4, column=1, padx=5, pady=5)


##------- Programme principal -------##
# converted_data = open_file(), convert_data)
# write_output_file(converted_data)

fen.resizable(width=False, height=False) # on veut une fenêtre non redimensionnable
fen.mainloop()
