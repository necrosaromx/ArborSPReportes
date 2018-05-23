# ArborSPReportes
A webscrapping tool to retrieve some reports from arbor peakflow platform that aren't available from API

En el directorio, se encuentran los scripts que conforman la herramienta, en
general se requiere que se cumplan los siguientes requisitos:

- Contar con Python 2.7
- Contar con las siguientes librerías de python
- tqdm
- mechanize
- pycurl
Éstas últimas se pueden instalar mediante los siguientes comandos:
- pip install tqdm
- pip install mechanize
- pip install pycurl

Éste último se recomienda instalar de forma “manual” descargando el
paquete oficial: http://pycurl.io/

La herramienta realiza la descarga de reportes a partir de la configuración establecida en
un archivo de configuración, el archivo se puede generar en un bloc de notas con formato
texto plano y debe tener la siguiente estructura:

Las secciones deben estar definidas con el nombre entre corchetes cuadrados [ ]
Para esta versión solo manejamos la sección SP y es obligatoria
Los nombres de los atributos deben ser sin espacios, seguidos de un ‘=’ y el valor, el cual
puede contener espacios.

Atributos del archivo:
- endpoint: Dirección IP del SP a consultar
- web_user: Usuario web del SP, debe contar con privilegios para generar
reportes
- web_pass: Contraseña del web_user
- api_key: Clave del API, esta se genera directamente en la interfaz del SP
- start_date y end_date: Fechas de inicio y fin de los reportes a generar, en

formato 'MM/DD/AA+hh:mm:ss'
Dónde:
MM: Mes en 2 dígitos
DD: Día en 2 dígitos
AA: Año últimos 2 dígitos
hh: hora en 2 dígitos formato 24 hrs
mm: minuto en 2 dígitos
ss: segundos en 2 dígitos

- lista_mo: Ruta/Nombre del archivo que contiene la lista de MOs a consultar
Si no se especifica la ruta, el archivo se buscará en el directorio actual
El archivo debe ser texto plano y debe tener un MO por línea, en formato
ID:Nombre de MO
Este archivo se obtiene automáticamente con el script Listado-MOs

- output_dir: Ruta/Nombre de directorio donde se depositarán los reportes
descargados, se generarán subdirectorios con los nombres de los MO del
archivo definido en lista_mo
Si no se especifica la ruta, el directorio se creará bajo el directorio actual
Es importante validar que se tengan permisos de escritura en la ruta indicada.
Todas las líneas que comiencen con # se consideran comentarios y son
ignorados por el script, se pueden usar como guías.
Para generar el valor API_KEY, revisar el manual de usuario de Arbor SP



Para generar el archivo con el listado de MOs debemos ejecutar Listado-MOs,
este script leerá el archivo de configuración por lo que de manera obligatoria deben existir al
menos los siguientes atributos con valores ejemplo:

endpoint = 192.168.10.1

lista_mo = LISTA.txt

api_key = 63Ghgwtrgs$%W

El script se debe ejecutar mediante ‘./Listado-MOs.py

Si se desea usar un archivo de configuración distinto se debe indicar con la ruta
mediante el argumento ‘--config’, ej.: ‘./Listado-MOs.py --config Alternativa.conf’

El script descargará la lista de MOs con ID y la guardará en el archivo especificado
en lista_mo
NOTA: Si el archivo ya existe, éste será sobrescrito

Una vez generado el archivo se puede editar para dejar los MO de interés.

En el prompt de línea de comando se ejecuta la herramienta con el comando
‘./ArborSPReportes.py’, al ejecutarlo de esta manera tomará la configuración del archivo default
‘ArborSP.conf’, es importante contar al menos con los siguientes atributos configurados:

endpoint
web_user
web_pass
lista_mo
output_dir
start_date
end_date

Si se desea utilizar un archivo de configuración distinto, se debe indicar el mismo
mediante la opción ‘--config’:
También es posible indicar la fecha de inicio y fin desde la línea de comando, mediante las
opciones ‘-s’ para indicar la fecha de inicio y ‘-e’ para indicar la fecha de fin, dichas fechas
deben seguir el mismo formato que en el archivo de configuración
