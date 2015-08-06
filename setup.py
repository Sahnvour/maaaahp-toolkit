#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python 2.7
# 02/2011
 
import sys, os
from cx_Freeze import setup, Executable
 
#############################################################################
# préparation des options 
 
# chemins de recherche des modules
path = sys.path + []
 
# options d'inclusion/exclusion des modules
includes = []
excludes = []
packages = []
 
 
# inclusion éventuelle de bibliothèques supplémentaires
binpathincludes = []
if sys.platform == "linux2":
    # pour que les bibliothèques de /usr/lib soient copiées aussi
    binpathincludes += ["/usr/lib"]
 
# construction du dictionnaire des options
options = {"path": path,
           "includes": includes,
           "excludes": excludes,
           "packages": packages,
           "bin_path_includes": binpathincludes
           }
 
#############################################################################
# préparation des cibles
base = None
if sys.platform == "win32":
    base = "Win32GUI"
 
cible_1 = Executable(
    script = "yamaxanadu.py",
    base = base,
    compress = True,
    icon = None,
    )
 
#############################################################################
# création du setup
setup(
    name = "yamaxanadu",
    version = "1",
    description = "Traitement de concours photo sous Windows et Linux",
    author = "Tyrtamos",
    options = {"build_exe": options},
    executables = [cible_1]
    )