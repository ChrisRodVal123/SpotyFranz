# coding: utf-8
from flask import Flask, render_template, request, url_for,redirect, session, flash
from app import app, db
from models import Canciones, Usuarios
          
@app.route('/')
def index():
    lista = Canciones.query.order_by(Canciones.id)
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

    cancion = Canciones.query.filter_by(titulo=titulo).first()

    if cancion:
        flash('Esta canción ya existe!')
        return redirect(url_for('index'))

    nueva_cancion = Canciones(titulo=titulo, categoria=categoria, idioma=idioma)
    db.session.add(nueva_cancion)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logueado' not in session or session['usuario_logueado'] == None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    cancion = Canciones.query.filter_by(id=id).first()
    return render_template('editar.html', titulo='Editando Canción', cancion=cancion)

@app.route('/actualizar', methods=['POST',])
def actualizar():
    cancion = Canciones.query.filter_by(id=request.form['id']).first()
    cancion.titulo = request.form['titulo']
    cancion.categoria = request.form['categoria']
    cancion.idioma = request.form['idioma']

    db.session.add(cancion)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/eliminar/<int:id>')
def eliminar(id):
    if 'usuario_logueado' not in session or session['usuario_logueado'] == None:
        return redirect(url_for('login'))

    Canciones.query.filter_by(id=id).delete()
    db.session.commit()
    flash('¡Canción eliminada con éxito!')

    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima = proxima)


@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario:
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
