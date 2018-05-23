#!/usr/bin/python
# -*- coding: utf-8 -*-
#Autor: Saul Vargas Leon
"""
    Modulo para validar / crear directorio de deposito de archivos
"""
import os

def checkmkdir(dir_name):
    """
        
        Crea el directorio dir_name ne caso de que no exista, ruta relativa
    """
    currentwd = os.getcwd()
    output_dir = currentwd + '/' + dir_name

    try:
        os.makedirs(output_dir)
    except OSError:
        if os.path.exists(output_dir):
            pass
        else:
            raise
