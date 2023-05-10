import os
import requests
import re


def name_file(url):


    # Aplicamos la expresión regular a la URL
    match = re.search(r"books\/(.*?)\/downloadbookepub", url)

    if match:
        # Si se encontró un match, extraemos el texto capturado
        book_name = match.group(1)
    else:
        print("No se encontró un match")
    
    return book_name


def pdf_downloader(urls):


    # Crear la carpeta principal para los archivos PDF
    pdf_folder = 'PDFs'
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)

    # Descargar y guardar cada archivo PDF en su carpeta correspondiente
    for url in urls:
        # Obtener el nombre del archivo PDF
        pdf_name = name_file(url).replace("-", " ")

        # Crear la carpeta para el archivo PDF
        pdf_dir = os.path.join(pdf_folder, pdf_name)
        if not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)

        # Descargar el archivo PDF y guardarlo en la carpeta correspondiente
        response = requests.get(url)
        with open(os.path.join(pdf_dir, pdf_name + '.pdf'), 'wb') as f:
            f.write(response.content)
