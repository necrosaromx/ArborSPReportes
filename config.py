#!/usr/bin/python
# -*- coding: utf-8 -*-
#Autor: Saul Vargas Leon
"""
    Cargador de configuracion para ArborSPreportes.py
"""
import ConfigParser
import os

def load_config(file_name = 'ArborSP.conf'):
    """ 
        Carga la configuracion del archivo especificado y lo regresa en dict
    """
    currentwd = os.getcwd()
    config = ConfigParser.ConfigParser()
    try:
        if len(config.read(currentwd + '/' + file_name)) == 0:
            raise ValueError('No se pudo leer el contenido del archivo de configuracion ' + file_name)
        if not config.has_section('SP'):
            raise ValueError('No se encontro la seccion [SP] en el archivo de configuracion')
        configuracion = dict(config.items("SP"))
        if len(configuracion) == 0: 
            raise ValueError('No existen atributos en la seccion SP del archivo de configuracion')
        return configuracion
    except ValueError as val:
        print(val)
        os.abort()
