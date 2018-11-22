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
import webbrowser
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
        fieldsrcversion.config(text="Version du Projet source : " + src_version)
        entryTextDestV.set(34)
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
    fieldsrcversion.config(text="Version du Projet source : ")
    file_menu.entryconfig("Fermer le fichier", state='disabled')

def textToVersion(argument):
    version = ""
    switcher = {
        "Multi-compatible (si version inconnue)" : "1",
        "Version IUT" : "34",
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

def about():
    global about_window
    about_window = Tk() # On crée la fenêtre et on ajoute les éléments
    about_window.title('À propos')
    info = Label(about_window, text='PremiereDowngrade par Léo Boyer')
    info.pack(pady=3, padx=10, fill=BOTH)
    info = Label(about_window, text='Distribué sous License MIT')
    info.pack(pady=3, padx=10, fill=BOTH)
    lien = Label(about_window, text="Le projet sur GitHub", fg="blue", cursor="hand2")
    lien.pack(pady=3, padx=10, fill=BOTH)
    lien.bind("<Button-1>", lambda event:webbrowser.open_new(r"https://www.github.com/leoboyerbx/premiere-downgrade"))


    valider = Button(about_window, text='Ok', command=about_window.destroy)
    valider.pack(pady=5, padx=10, fill=BOTH)

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
tools_menu.add_command(label="Détecter la version d'un fichier...", command=display_version)
help_menu = Menu(main_menu, tearoff=0)
help_menu.add_command(label="À propos", command=about)

main_menu.add_cascade(label="Fichier", menu=file_menu)
main_menu.add_cascade(label="Options", menu=tools_menu)
main_menu.add_cascade(label="Aide", menu=help_menu)

fen.config(menu=main_menu)



# ##-------- Création des zones de texte ---------##
tmp = Label(fen, text='Convertir un projet Premiere Pro vers une ancienne verison')
tmp.pack()


# Source 
zone_input = LabelFrame(fen, text="Fichier source", padx=7, pady=7)
zone_input.pack(fill="both", expand="yes", padx=10, pady=10)

file_chooser = Frame(zone_input)
file_chooser.pack(pady=5)

entryTextfile = StringVar()
fieldname = Entry(file_chooser, text="", width=50, state="readonly", textvariable=entryTextfile)
entryTextfile.set('Ouvrir un fichier...')

fieldname.pack(side=LEFT, padx=10)

browse = Button(file_chooser, text="Parcourir", command=get_src_file)
browse.pack(side=RIGHT)

fieldsrcversion = Label(zone_input, text="Version du Projet source : ")
fieldsrcversion.pack(pady=5)
# Destination
zone_output = LabelFrame(fen, text="Fichier de destination", padx=7, pady=7)
zone_output.pack(fill="both", expand="yes", padx=10, pady=10)

preconfig_chooser = Frame(zone_output)
preconfig_chooser.pack(pady=5)

tmp = Label(preconfig_chooser, text='Préconfiguration: ')
tmp.pack(side=LEFT)

choixdef = StringVar()
choixdef.set("Version IUT") # initial value
choixdef.trace("w", lambda name, index, mode, sv=choixdef: setPreconf(choixdef))
option = OptionMenu(preconfig_chooser, choixdef, "Version IUT", "Personnalisé", "CC 2018 (v12.0)", "CC 2018 (v12.1)", "CC 2019 (v13.0)", "Multi-compatible (si version inconnue)")
option.pack(side=RIGHT)

version_chooser = Frame(zone_output)
version_chooser.pack(pady=5)

tmp = Label(version_chooser, text='Convertir vers: ')
tmp.pack(side=LEFT)

entryTextDestV= StringVar()
destinationversion = Entry(version_chooser, width=3, textvariable=entryTextDestV)
destinationversion.pack(side=RIGHT)

bottom_buttons = Frame(fen)
bottom_buttons.pack(side=RIGHT, pady=10, padx=10)

tmp = Button(bottom_buttons, text="Convertir", command=convert, width=30)
tmp.pack(side=RIGHT)

tmp = Button(bottom_buttons, text="Quitter", command=fen.destroy, width=10)
tmp.pack(side=LEFT, padx=10)

##------- Programme principal -------##
# converted_data = open_file(), convert_data)
# write_output_file(converted_data)

fen.resizable(width=False, height=False) # on veut une fenêtre non redimensionnable
fen.mainloop()
