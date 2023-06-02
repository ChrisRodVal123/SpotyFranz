import os
from app import app

def recuperar_audio(id):
    for nombre_archivo in os.listdir('./static/upload/'):
        if f'{id}' in nombre_archivo:
            return nombre_archivo

    return 'nombre_patron.mp3'

def eliminar_archivo(id):
    archivo = recuperar_audio(id)
    if archivo != 'nombre_patron.mp3':
        os.remove("./static/upload/"+archivo)       # ... borrra archivo