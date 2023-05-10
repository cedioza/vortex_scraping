# Repositorio prueba técnica de VORTEX en Python


### Librerías :
- Selenium: [selenium](https://selenium-python.readthedocs.io)
- Request : [requests](https://pypi.org/project/requests)

## Estructura 
```
.
├── app_novedades.py
├── app_principal.py
├── driver
│   └── chromedriver.exe
├── helpers
│   ├── helper.py
│   └── __init__.py
├── venv
├── .env
├── .gitignore
└── requirements.txt


```
## Paso a Paso

Abre una terminal y navega a la carpeta raíz de tu proyecto.
Crea un nuevo entorno virtual con venv usando el siguiente comando:


```
python3 -m venv venv
```
Activa el entorno Virtual.
```
./venv/Scripts/Activate
```
Instalar con pip:
```
$ pip install -r requirements.txt
```
## Requisito 

Realizar web scraping de una página web a la siguiente página web:
https://freeditorial.com/
Construir un Bot en Selenium (Y otras herramientas que necesite) que pueda automatizar la
descarga de manera masiva de algunos libros
