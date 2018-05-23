#!/usr/bin/python
# -*- coding: utf-8 -*-
#Autor: Saul Vargas Leon

import argparse

def loadargs():
    parser = argparse.ArgumentParser(description='Herramienta para obtener report'\
                                     'es desde Arbor SP', 
                                     epilog='Las fechas establecidas por linea de'\
                                     ' comando tienen prioridad sobre las del arc'\
                                     'hivo de configuracion. Saul Vargas @ SCITUM 2018')
    parser.add_argument('-s', action='store', 
                        help='Fecha inicial en formato MM/DD/AA+hh:mm:ss', 
                        dest='start_date', default='empty')
    parser.add_argument('-e', action='store', 
                        help='Fecha final en formato MM/DD/AA+hh:mm:ss', 
                        dest='end_date', default='empty')
    parser.add_argument('--config', action='store', 
                        help='Archivo de configuracion a cargar', 
                        dest='config_file', default='ArborSP.conf')
    line_args = parser.parse_args()
    args = vars(line_args)
    return args

