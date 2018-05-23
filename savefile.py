#!/usr/bin/python
# -*- coding: utf-8 -*-
#Autor: Saul Vargas Leon
"""
    Modulo para guardar el archivo recibe de un buffer
"""

def savefile(file_name, data):
    """
     
       Recibe nomrbe de archivo y bufer de datos a guardar
    """
    with open(file_name, "wb") as fh:
	fh.write(data.getvalue())
    

