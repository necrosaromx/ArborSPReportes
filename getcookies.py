#!/usr/bin/python
 # -*- coding: utf-8 -*-
#Autor: Saul Vargas Leon
"""
    Modulo para obtener cookies de sesion ArborSP una vez que se ha autenticado
"""
import mechanize
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

def getcookie(uri, user, password):
    """
        Funcion que hace login en url con user y password para regresar dict con cookies
    """
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(uri)
    br.select_form(name="auth")
    br["username"] = user
    br["password"] = password
    login = br.submit()
    cookie_name = br._ua_handlers['_cookies'].cookiejar[0].name
    cookie_value = br._ua_handlers['_cookies'].cookiejar[0].value
    return dict({'cookie_name': cookie_name, 'cookie_value': cookie_value})
