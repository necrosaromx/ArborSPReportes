#!/usr/bin/python
# -*- coding: utf-8 -*-
#Saul Vargas Leon
#Script para listar MO de SP arbor y sus ID
import logging
import sys 
import json
import pycurl
import config
import savefile
import argparse
import checkconn
import os
from StringIO import StringIO

def main():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    
    
    parser = argparse.ArgumentParser(description='Herramienta para obtener el lis'\
                                     'ado de MOs del SP', 
                                     epilog='Saul Vargas @ SCITUM 2018')
    parser.add_argument('--config', action='store', 
                        help='Archivo de configuracion a cargar', 
                        dest='config_file', default='ArborSP.conf')
    
    line_args = parser.parse_args()
    args = vars(line_args)
    logging.info("Cargando configuracion desde %s", args["config_file"])
    if args["config_file"] is not 'ArborSP.conf':
        configuracion = config.load_config(args["config_file"])
    else: 
        configuracion = config.load_config() 
        
    args.pop("config_file")
    
    logging.info('Validando conexion al endpoint %s', configuracion["endpoint"])
    if checkconn.internet(configuracion["endpoint"], 443, 10):
        logging.info('Conexion con exito.')
        pass
    else:
        logging.info('No hay conexion a %s por el puerto TCP 443', configuracion["endpoint"])
        os.abort()
    
    page_response_buffer = StringIO()
    while_response_buffer = StringIO()
    
    request_data = 'api_key=' + configuracion["api_key"]
    
    c = pycurl.Curl()
    c.setopt(c.SSL_VERIFYHOST, 0)
    c.setopt(pycurl.SSL_VERIFYPEER, 0)
    c.setopt(c.WRITEDATA, page_response_buffer)
    c.setopt(c.URL, 'https://' + configuracion["endpoint"] + '/arborws/admin/managed_object')
    c.setopt(c.POSTFIELDS, request_data)
    logging.debug('ejecutando Curl')
    logging.info('Solicitando listado de MOs a %s', configuracion["endpoint"])
    c.perform()
    
    j = json.loads(page_response_buffer.getvalue())
    
    number_pages = j["total_pages"]
    logging.debug('total de paginas %s', number_pages)
    mo_details = j["data"]
    p = 2
    while p <= int(number_pages):
        while_response_buffer.truncate()
        u = pycurl.Curl()
        u.setopt(c.SSL_VERIFYHOST, 0)
        u.setopt(pycurl.SSL_VERIFYPEER, 0)
        u.setopt(c.WRITEDATA, while_response_buffer)
        u.setopt(c.URL, 'https://' + configuracion["endpoint"] + '/arborws/admin/managed_object')
        u.setopt(c.POSTFIELDS, request_data + '&page=' + str(p))
        logging.debug('solicitando pagina %s', p)
        logging.info('Resolviendo paginado de respuesta (puede tardar algunos minutos)')
        u.perform()
        new_p = json.loads(while_response_buffer.getvalue())
        logging.debug('concatenando pagina %s', p)
        mo_details.extend(new_p["data"])
        while_response_buffer.flush()
        p += 1
    logging.info('Total de MOs encontrados: %s', len(mo_details))
    with open(configuracion["lista_mo"], "wb") as fh:
        for m in mo_details:
            item =  m["id"] + ':' + m["name"]
            logging.debug(item)
            fh.write('%s\n' %  item)
    logging.info('El listado de %d MOs se ha guardado en el archivo %s', len(mo_details), configuracion["lista_mo"])
    
if __name__ == "__main__":
    main()
    
