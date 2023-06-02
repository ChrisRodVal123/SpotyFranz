import os
from app import app

from flask_wtf import FlaskForm
from  wtforms import StringField, SubmitField, PasswordField, validators

class FormularioCancion(FlaskForm):
    titulo = StringField('Título de la canción', [validators.DataRequired(), validators.Length(min=1, max=50)])
    categoria = StringField('Categoría', [validators.DataRequired(), validators.Length(min=1, max=40)])
    idioma = StringField('Idioma', [validators.DataRequired(), validators.Length(min=1, max=20)])
    grabar = SubmitField('Grabar')
  
class FormularioUsuario(FlaskForm):
    nickname = StringField('Nickname', [validators.DataRequired(), validators.Length(min=1, max=8)])
    clave = PasswordField('Clave', [validators.DataRequired(), validators.Length(min=1, max=100)])
    ###nickname = StringField('Nickname', [validators.DataRequired()])
    ###clave = PasswordField('Clave', [validators.DataRequired()])
    login = SubmitField('Login')    
     
    
def recuperar_audio(id):
    for nombre_archivo in os.listdir('./static/upload/'):
        if f'{id}' in nombre_archivo:
            return nombre_archivo

    return 'nombre_patron.mp3'

def eliminar_archivo(id):
    archivo = recuperar_audio(id)
    if archivo != 'nombre_patron.mp3':
        os.remove("./static/upload/"+archivo)       # ... borrra archivo