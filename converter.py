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
def open_file(path, callback):
    global filename
    tmp = tempfile.mkdtemp()
    filename = os.path.splitext(os.path.basename(path))[0]
    temp_fichier = tmp + '/' + filename

    if path: #Si un fichier est choisi
        with gzip.open(path, 'rb') as f_in:
            with open(temp_fichier, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        return callback(etree.parse(temp_fichier))

def convert_data(projectFile):
    global filename
    for project in (projectFile.xpath("/PremiereData/Project")):
        if project.get('Version'):
            print(project.get('Version'))
            project.set('Version', '34')
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

##------- Variables globales --------##




##------- Création de la fenêtre -------##
fen = Tk()
fen.title('Premiere Converter')                # ---> On donne un titre à la fenêtre
# # ---> La fenêtre fait 400*400px, et est située à 200px de la gauche de l'écran, à 100px du haut
# fen.geometry('800x700+200+100')

# ##-------- Création de la barre de menu ---------##
# barre_menu = Menu(fen)
# menu_fichier = Menu(barre_menu, tearoff=0)
# menu_fichier.add_command(label="Ouvrir un niveau", command=ouvrir_niveau)
# menu_fichier.add_command(label="Fermer le niveau", command=init_jeu, state='disabled')
# menu_fichier.add_separator()
# menu_fichier.add_command(label="Quitter", command=fen.quit)
# barre_menu.add_cascade(label="Fichier", menu=menu_fichier)

# fen.config(menu=barre_menu)

# ##-------- Création des zones de texte ---------##
# bienvenue = Label(fen, text='Bienvenue sur RushHour, déplacez les véhicules pour faire sortir la voiture rouge !')
# bienvenue.pack()



##------- Programme principal -------##
converted_data = open_file(filedialog.askopenfilename(initialdir = "./",title = "Ouvrir un projet", filetypes = (("Projets Premiere Pro","*.prproj"),("Tous les fichiers","*.*"))), convert_data)
write_output_file(converted_data)

# fen.resizable(width=False, height=False) # on veut une fenêtre non redimensionnable
# fen.mainloop()
