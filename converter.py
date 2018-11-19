#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#
##------- Importation des modules --------##
# from tkinter import *
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



##------- Variables globales --------##




##------- Création de la fenêtre -------##
# fen = Tk()
# fen.title('Rush Hour')                # ---> On donne un titre à la fenêtre
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

tmp = tempfile.mkdtemp()

fichier_source = filedialog.askopenfilename(initialdir = "./",title = "Ouvrir un projet", filetypes = (("Projets Premiere Pro","*.prproj"),("Tous les fichiers","*.*")))  # Dialogue qui ouvre un choix de fichier
nom_fichier_seul = os.path.splitext(os.path.basename(fichier_source))[0]
temp_fichier = tmp + '/' + nom_fichier_seul

if fichier_source: #Si un fichier est choisi
    with gzip.open(fichier_source, 'rb') as f_in:
        with open(temp_fichier, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    projectFile = etree.parse(temp_fichier)
    # Fonction convertir
    for project in (projectFile.xpath("/PremiereData/Project")):
        if project.get('Version'):
            print(project.get('Version'))
            project.set('Version', '34')
            print(project.get('Version'))
            result = etree.tostring(projectFile, pretty_print=True)
            # with open(temp_fichier, 'wb') as f_out:
            #     f_out.write(result)
            with gzip.open('./out/'+nom_fichier_seul+'_converted.prproj', 'wb') as f:
                f.write(result)


##------- Programme principal -------##



# fen.resizable(width=False, height=False) # on veut une fenêtre non redimensionnable
# fen.mainloop()
