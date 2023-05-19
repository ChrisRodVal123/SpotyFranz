# coding: utf-8
from flask import Flask, render_template, request, url_for,redirect, session, flash

class Usuario:
    def __init__(self, nombre, nickname, clave):
        self.nombre = nombre
        self.nickname = nickname
        self.clave = clave

usuario1= Usuario('Jair Sampaio', 'JS', 'patitofeo')
usuario2= Usuario('Rosa Flores', 'rosita', 'michifuz')
usuario3= Usuario('Yami Moto Nokamina', 'kamikaze', 'sayonara')
usuarios= { usuario1.nickname : usuario1,
            usuario2.nickname : usuario2,
            usuario3.nickname : usuario3
          }


class Cancion:
    def __init__(self, titulo, categoria, idioma):
        self.titulo = titulo
        self.categoria = categoria
        self.idioma = idioma

cancion1= Cancion('La guitarra', 'Pop', 'Castellano')
cancion2= Cancion('Para no verte más', 'Pop', 'Castellano')
cancion3= Cancion('Balada para un gordo', 'Balada', 'Castellano')
lista=[cancion1, cancion2, cancion3]

app = Flask(__name__)
app.secret_key = 'cochabamba'

@app.route('/')
def index():
    return render_template('listar.html',titulo= 'Canciones', musicas=lista)


@app.route('/nuevoregistro')
def nuevoregistro():
    if session['usuario_logueado'] == None:
        flash('Usuario no conectado.')
        return redirect(url_for('login', proxima = url_for('nuevoregistro')))
    else:
        flash('Usuario conectado.') 
        return render_template('nuevoRegistro.html', titulo='Nueva Canción')


@app.route('/crear', methods=['POST',])
def crear():
    titulo = request.form['titulo']
    categoria = request.form['categoria']
    idioma = request.form['idioma']
    cancion = Cancion(titulo, categoria, idioma)
    lista.append(cancion)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima = proxima)


@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['clave'] == usuario.clave:
            session['usuario_logueado'] = usuario.nickname
            flash(usuario.nickname + ' ¡conectado con éxito!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        else:
            flash('Usuario no conectado.')
            return redirect(url_for('login', proxima = url_for('nuevoregistro')))
    else:
        flash('Usuario no conectado.')
        return redirect(url_for('login', proxima = url_for('nuevoregistro')))

    
@app.route('/logout')
def logout():
    session['usuario_logueado'] = None
    flash('¡Logout efectuado exitosamente!')
    return redirect(url_for('index'))


app.run(host="0.0.0.0", port=5000)