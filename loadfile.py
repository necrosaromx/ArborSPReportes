#!/usr/bin/python
 # -*- coding: utf-8 -*-
#Autor: Saul Vargas Leon
#SCITUM 2018
import os
""" Lectura de archivo de nombres de MO para ArborSPReportes.py

"""

def loadidnames(file_name):
    """
        Lee las lineas de (file_name) en formato ID:NOMBRE sin campos vaciones y regresa en una tupla
    """
    try:
        with open(file_name) as f:
            mos_ids = [tuple(map(str.strip, i.split(':'))) for i in f]
        while mos_ids[-1][0] in '':
            mos_ids.pop()
        return mos_ids
    except:
        print 'No se pudo leer el archivo' + file_name
        os.abort() 
