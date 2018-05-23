#!/usr/bin/python
# -*- coding: utf-8 -*-
#Autor: Saul Vargas Leon
import logging
import config
import loadfile
import getcookies
import setoutput
import getreport
import savefile
import cmdparser
from tqdm import tqdm 

def main():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    
    args = cmdparser.loadargs()
    
    logging.info("Cargando configuracion desde %s", args["config_file"])
    configuracion = config.load_config(args["config_file"])
    
    if args["start_date"] is  'empty':
        args.pop("start_date")
    if args["end_date"] is 'empty':
        args.pop("end_date")
    args.pop("config_file")
    configuracion.update(args)
    
    logging.debug(configuracion)
    
    endpoint_uri = 'https://' + configuracion["endpoint"] + '/'
    
    mos_ids = loadfile.loadidnames(configuracion["lista_mo"])
    logging.info('Cargados %s Mos de archivo %s', len(mos_ids), configuracion["lista_mo"])
    logging.debug(mos_ids)
    
    cookie = getcookies.getcookie(endpoint_uri, configuracion["web_user"], configuracion["web_pass"]) 
    
    logging.debug('Nombre: %s', cookie["cookie_name"])
    logging.debug('Valor: %s', cookie["cookie_value"])
    
    setoutput.checkmkdir(configuracion["output_dir"])
    logging.info('Los reportes se depositaran en el directorio %s', configuracion["output_dir"])
    
    
    logging.info('Descargando reportes Summary, Applications, Alerts y Top Talkers')
    logging.info('Del %s al %s para %d MOs', configuracion["start_date"], 
                 configuracion["end_date"], len(mos_ids))
     
    
    for customer in tqdm(mos_ids, desc='Reportes', unit='MO'):
        report_output_dir = configuracion["output_dir"] + '/' + customer[1] + '/'
        setoutput.checkmkdir(report_output_dir)
        for reporte in tqdm(['summary', 'alerts', 'applications', 'toptalkers'], desc='PDF', unit='pdf'):
            logging.debug('Enviando a generar reporte tipo: %s', reporte)
            report_data = getreport.getreport(configuracion["endpoint"], 
                                              reporte, 
                                              cookie, 
                                              customer, 
                                              configuracion["start_date"],  
                                              configuracion["end_date"])
            savefile.savefile(report_output_dir +  '/' + customer[1] + '_' + reporte + '.pdf', report_data) 
    
    logging.info('Se ha finalizado la generacion de reportes')
   
if __name__ == "__main__":
    main()
 
