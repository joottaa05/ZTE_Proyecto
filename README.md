# ZTE_Proyecto
Recoger tickets y mostrar listas ordenadas por grupos en una web

Creamos un entorno virtual para instalar librerias de python y no generar posibles conflictos con otros proyectos
A continuación, se detalla cómo configurar el entorno y las dependencias.
### Crear y activar un entorno virtual ###
Crear el entorno virtual en el directorio del proyecto:
python -m venv venv
###Activar el entorno virtual###
Windows (PowerShell):
.\venv\Scripts\Activate.ps1
Windows (cmd):
.\venv\Scripts\activate.bat
macOS / Linux:
source venv/bin/activate
Al activar el entorno, deberías ver (venv) al inicio de la línea de comandos.
##Actualizar pip##
python -m pip install --upgrade pip
Instalar dependencias principales
pip install reflex pandas
reflex → framework principal del proyecto.
pandas → para análisis y manipulación de datos.
#Instalar cliente de base de datos (opcional)
#Dependiendo de la base de datos que uses:
SQLite (ya incluido en Python, no requiere instalación)
#PostgreSQL:
pip install psycopg2-binary
#MySQL:
pip install mysql-connector-python
#Guardar dependencias
Para que otros puedan instalar las mismas librerías:
pip freeze > requirements.txt
Y luego se instalan con:
pip install -r requirements.txt
###Verificación rápida###
Dentro de Python:
import reflex
import pandas as pd
print("¡Todo listo!")
--- Si no aparecen errores, la configuración está correcta ---
