#!/usr/bin/python
# -*- coding: utf-8 -*-
#Autor: Saul Vargas Leon
"""
    Script que usa curl para descargar los reportes (scrapping)
"""
import pycurl
import os
import urllib
from StringIO import StringIO

def _setheader(report_type, endpoint, page_url, cookie):
    """
        
        Inicializa los headers dependiendo el tipo de reporte
    """
    endpoint_uri = 'https://' + endpoint + '/'
    headers = [
        'Host: ' + endpoint,
        'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0', 
        'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
        'Accept-Language: en-US,en;q=0.5',  
        'Referer: ' + endpoint_uri + page_url , 
        'Content-Type: application/x-www-form-urlencoded',
        'Cookie: ' + cookie["cookie_name"] + '=' + cookie["cookie_value"],
        'Connection: keep-alive',
        'Upgrade-Insecure-Requests: 1',
        'DNT: 1'
        ]
    return headers

def _setpostdata(report_type, start_date, end_date, customer):
    """
       
       Inicializa el post-body de acuerdo al tipo de reporte
    """
    if report_type is 'summary':
        post_data = {
            'download_output_type': 'PDF', 
            'id': 'customer_summary', 
            'ContainerWidget_TrafficWidget_Container_889b1a3e07b07d5ec96c0978ae18d3a2_active_tab': '0',
            'ControlWidgetTimeframe_1b22834a75e912b90453a5ef163437c9_time_period': 'other',
            'ControlWidgetTimeframe_1b22834a75e912b90453a5ef163437c9_time_start' : start_date, 
            'ControlWidgetTimeframe_1b22834a75e912b90453a5ef163437c9_time_end' : end_date, 
            'ControlWidgetUnit_3f24a644dea974fac65aac8a216ef833_unit': 'bps',
            'ControlWidgetGraphType_ec873e91b2317542483fdfe3bf923464_graph_type_select': 'Detail',
            'ControlWidgetObjectSelect_e0114bd4a614338bf811cbefdf58d0b7_name': customer[1],  
            'ControlWidgetObjectSelect_e0114bd4a614338bf811cbefdf58d0b7_gid': customer[0], 
            'selected_gid': '',
            'selected_gid_changed': '0',
            'TrafficQueryWidget_ea22dec57073eec32be17532cd88f38e_query_md5': 'f2acc4685dcc92191871de3c0a05543d',
            'TrafficQueryWidget_ea22dec57073eec32be17532cd88f38e_results_filename': 'uberfetch.LOxoCV3876',
            'ClassTableWidget_9f541ed7163793ad8d45f291f43891cc_sort_column_id': 'total',
            'ResourceSelect_d41be746af56b50aa32ad05785d21d2f_filtergroupby': 'all',
            'ResourceSelect_d41be746af56b50aa32ad05785d21d2f_search_text': 'cloud',
            'ResourceSelect_d41be746af56b50aa32ad05785d21d2f_resource': customer[0]
            }
    elif report_type is 'applications':
        post_data = {
            'download_output_type': 'PDF',
            'id': 'customer_application',
            'ContainerWidget_TrafficWidget_Container_964cdf33e0915d29bb987c831c29d8d0_active_tab': '0',
            'ControlWidgetTimeframe_0aff26a635998c30f2ff1c264ca4cfff_time_period': 'other',
            'ControlWidgetTimeframe_0aff26a635998c30f2ff1c264ca4cfff_time_start' : start_date, 
            'ControlWidgetTimeframe_0aff26a635998c30f2ff1c264ca4cfff_time_end' : end_date, 
            'ControlWidgetUnit_f853c1c8b8819f089a8c2ab391ff5283_unit': 'bps',
            'ControlWidgetGraphType_aa6d8d424a0f0132503fba1b32f82105_graph_type_select': 'Stacked',
            'ControlWidgetGraphType_aa6d8d424a0f0132503fba1b32f82105_graph_class_select': 'In',
            'ControlWidgetObjectSelect_d6e585c3ac27a1ed9de7a07f1b100565_name': customer[1],
            'ControlWidgetObjectSelect_d6e585c3ac27a1ed9de7a07f1b100565_gid': customer[0],
            'selected_gid': '',
            'selected_gid_changed': '0',
            'TrafficQueryWidget_315bf3e9bf3e986576840af184d3fce4_query_md5': 'c74f51a07d5553e0913388fd8e5f29de',
            'TrafficQueryWidget_315bf3e9bf3e986576840af184d3fce4_results_filename': 'uberfetch.DwyPP62471',
            'TrafficTableWidget_f4d7b827b26ab87cf56a33ab68703d0e_sort_column_id': 'SumTotal',
            'ResourceSelect_c61fcd7d877ca2d0ae04e1952c21c40c_filtergroupby': 'all',
            'ResourceSelect_c61fcd7d877ca2d0ae04e1952c21c40c_search_text': '',
            'ResourceSelect_c61fcd7d877ca2d0ae04e1952c21c40c_resource': customer[0]
            } 
    elif report_type is 'alerts':
        post_data = {
            'download_output_type': 'PDF',
            'id': 'customer_alerts',
            'ContainerWidget_c_934eb365a6f3d58d18959d295aa7c97e_active_tab': '0',
            'ControlWidgetTimeframe_2e68cdf9a00018d1599760e16a6b7dba_time_period': 'other',
            'ControlWidgetTimeframe_2e68cdf9a00018d1599760e16a6b7dba_time_start': start_date, 
            'ControlWidgetTimeframe_2e68cdf9a00018d1599760e16a6b7dba_time_end': end_date,
            'ControlWidgetObjectSelect_71c2cde0c20efc862ca6a9b260861db3_name': customer[1],
            'ControlWidgetObjectSelect_71c2cde0c20efc862ca6a9b260861db3_gid': customer[0],
            'selected_gid': '',
            'selected_gid_changed': '0',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_alert_class_saved': 'all',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_alert_type_saved': 'all_types',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_start_wiz_dir_saved': 'between',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_stop_wiz_dir_saved': '',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_importance_high': 'on',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_importance_medium': 'on',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_importance_low': 'on',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_alert_class': 'all',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_alert_type': 'all_types',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_alert_classification': 'all',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_search_limit': '100',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_page_size':'100',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_ongoing': 'on',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_recent': 'on',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_use_start_wiz': 'on',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_start_wiz_dir': 'between',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_start_wiz_month1': '12',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_start_wiz_day1': '1',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_start_wiz_year1': '2017',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_start_wiz_hour1': '00:00',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_start_wiz_month2': '1',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_start_wiz_day2': '1',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_start_wiz_year2': '2018',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_start_wiz_hour2': '00:00',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_stop_wiz_dir': 'before',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_stop_wiz_month1': '1',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_stop_wiz_day1': '',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_stop_wiz_year1': '2018',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_stop_wiz_hour1': '00:00',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_lo_bps_wiz_base': '',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_lo_bps_wiz_scale': 'u',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_hi_bps_wiz_base': '',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_hi_bps_wiz_scale': 'u',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_lo_pps_wiz_base': '',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_lo_pps_wiz_scale': 'u',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_hi_pps_wiz_base': '',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_hi_pps_wiz_scale': 'u',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_low_sev_wiz': '',
            'AlertSearchPopIn_52100d1694ec0516d15f1344bcf6e441_high_sev_wiz': '',
            'ResourceSelect_44123392654d8d76d8f7b70ad83d7801_filtergroupby': 'all',
            'ResourceSelect_44123392654d8d76d8f7b70ad83d7801_search_text': '',
            'ResourceSelect_44123392654d8d76d8f7b70ad83d7801_resource': customer[0]
            } 
    elif report_type is 'toptalkers':
        post_data = {
            'download_output_type': 'PDF',
            'id': 'customer_toptalkers_external',
            'ContainerWidget_TrafficWidget_Container_ad3ec1cf1c07cad4162e3fcbc43ea958_active_tab': '0',
            'ControlWidgetTimeframe_69df78a48f4409b568a21bca903cea67_time_period': 'month',
            'ControlWidgetTimeframe_69df78a48f4409b568a21bca903cea67_time_start': '28+days+ago',
            'ControlWidgetTimeframe_69df78a48f4409b568a21bca903cea67_time_end': 'now',
            'ControlWidgetUnit_45302aa65733e4733dcc633212655f1a_unit': 'bps',
            'ControlWidgetGraphType_6255f5246a0ee3ce4c0f8ae53339ea02_graph_type_select': 'Bar',
            'ControlWidgetObjectSelect_cdf5728cbfccd6ca358afeeb305c8602_name': customer[1],
            'ControlWidgetObjectSelect_cdf5728cbfccd6ca358afeeb305c8602_gid': customer[0],
            'selected_gid': '',
            'selected_gid_changed': '0',
            'TrafficQueryWidget_d59d50899f6dbcc240c32f7c7a741532_query_md5': 'fec0c00a8f9bc842316aa66f06ccb5ab',
            'TrafficQueryWidget_d59d50899f6dbcc240c32f7c7a741532_results_filename': 'uberfetch.fFhot30911',
            'HostName_5e0c6cae3e5a4e8f1f510e4b40272d9e': 'desc',
            'Peak_893cc9c6f75deb698c4dda2790c86f78': 'desc',
            'Proportion_1c9d7962ef85f58409619385e086df97': 'desc',
            'Time_48194f7711fc2b6c0fe1b840f3d02aa5': 'desc',
            'TrafficTableWidget_4735cae5e8309e405643bcb4573109a5_sort_column_id': 'total',
            'ResourceSelect_473bfbca9e3041f7953b6fe15602a833_filtergroupby0': 'all',
            'ResourceSelect_473bfbca9e3041f7953b6fe15602a833_search_text': '',
            'ResourceSelect_473bfbca9e3041f7953b6fe15602a833_resource': customer[0]
            }
    else:
        pass 
    post_data_encoded = urllib.urlencode(post_data)
    return post_data_encoded


def getreport(endpoint, report_type, cookie, customer, start_date = '', end_date = ''):
    """

        recibe parametros de reporte y devuelve el buffer
    """
    try:
        if report_type is 'summary':
            page_url = 'page?id=customer_summary'
        elif report_type is 'alerts':
            page_url = 'page?id=customer_alerts'
        elif report_type is 'applications':
            page_url = 'page?id=customer_application'
        elif report_type is 'toptalkers':
            page_url = 'page?id=customer_toptalkers_external'
        else:
            raise ValueError('No se identifica el tipo de reporte solicitado')
    except ValueError as val:
        print(val)
        os.abort()
    
    endpoint_uri = 'https://' + endpoint + '/' + page_url
    headers = _setheader(report_type, endpoint, page_url, cookie)
    post_data = _setpostdata(report_type, start_date, end_date, customer)
    page_buffer = StringIO()
    c = pycurl.Curl()
    c.setopt(c.SSL_VERIFYHOST, 0)
    c.setopt(pycurl.SSL_VERIFYPEER, 0)
    c.setopt(c.WRITEDATA, page_buffer)
    c.setopt(c.URL, endpoint_uri)
    c.setopt(c.HTTPHEADER, headers)
    c.setopt(c.ACCEPT_ENCODING, "")
    c.setopt(c.POSTFIELDS, post_data)
    c.perform()
    c.close()
    return page_buffer









