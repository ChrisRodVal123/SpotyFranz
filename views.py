# coding: utf-8
from flask import Flask, render_template, request, url_for,redirect, session, flash
from app import app, db
from models import Canciones, Usuarios

from helpers import recuperar_audio, eliminar_archivo, FormularioCancion, FormularioUsuario
import time

        
@app.route('/')
def index():
    lista = Canciones.query.order_by(Canciones.id)

    nombres_archivos=[]
    for item in lista:
        nombres_archivos.append(recuperar_audio(item.id))
        print(recuperar_audio(item.id))

    return render_template('listar.html',titulo= 'Canciones', musicas=lista, audio= nombres_archivos)


@app.route('/nuevoregistro')
def nuevoregistro():
    if session['usuario_logueado'] == None:
        flash('Usuario no conectado.')
        return redirect(url_for('login', proxima = url_for('nuevoregistro')))
    
    form = FormularioCancion()
    return render_template('nuevoRegistro.html', titulo='Nueva Canción', form=form)


@app.route('/crear', methods=['POST',])
def crear():
    form = FormularioCancion(request.form)
    
    if not form.validate_on_submit():
        return redirect(url_for('nuevoregistro'))

    
    titulo = form.titulo.data
    categoria = form.categoria.data
    idioma = form.idioma.data

    cancion = Canciones.query.filter_by(titulo=titulo).first()

    if cancion:
        flash('Esta canción ya existe!')
        return redirect(url_for('index'))

    nueva_cancion = Canciones(titulo=titulo, categoria=categoria, idioma=idioma)
    db.session.add(nueva_cancion)
    db.session.commit()

    timestamp = time.time()
    archivo = request.files['archivo']
    #archivo.save(f'static/upload/{nueva_cancion.id}-{timestamp}.mp3')
    archivo.save(f'static/upload/{nueva_cancion.id}.mp3')

    return redirect(url_for('index'))


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logueado' not in session or session['usuario_logueado'] == None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    cancion = Canciones.query.filter_by(id=id).first()
    
    form = FormularioCancion()
    form.titulo.data = cancion.titulo
    form.categoria.data = cancion.categoria
    form.idioma.data = cancion.idioma
    audio_cancion = recuperar_audio(id)
    
    return render_template('editar.html', titulo='Editando Canción', cancion=cancion, form=form )

@app.route('/actualizar', methods=['POST',])
def actualizar():
    form = FormularioCancion(request.form)
    
    if form.validate_on_submit():
        cancion = Canciones.query.filter_by(id=request.form['id']).first()
        cancion.titulo = form.titulo.data
        cancion.categoria = form.categoria.data
        cancion.idioma = form.idioma.data

        db.session.add(cancion)
        db.session.commit()

        timestamp = time.time()
        eliminar_archivo(cancion.id)   # borra archivo de audio
        archivo = request.files['archivo']
        #archivo.save(f'static/upload/{cancion.id}-{timestamp}.mp3')
        archivo.save(f'static/upload/{cancion.id}.mp3')

    return redirect(url_for('index'))

@app.route('/eliminar/<int:id>')
def eliminar(id):
    if 'usuario_logueado' not in session or session['usuario_logueado'] == None:
        return redirect(url_for('login'))

    eliminar_archivo(id)   # borra archivo de audio
    Canciones.query.filter_by(id=id).delete()
    db.session.commit()
    flash('¡Canción eliminada con éxito!')

    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    form = FormularioUsuario()
    return render_template('login.html', proxima=proxima, form=form)


@app.route('/autenticar', methods=['POST',])
def autenticar():
    form = FormularioUsuario(request.form)
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    
    if usuario:
        if form.clave.data == usuario.clave:
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
