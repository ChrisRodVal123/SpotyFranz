from flask import Flask, render_template, request

class Cancion:
    def __init__(self,titulo,categoria,idioma):
        self.titulo=titulo
        self.categoria= categoria
        self.idioma=idioma

cancion1=Cancion('La guitarra','pop','castellano')
cancion2=Cancion('para no verte mas','pop','castellano')
cancion3=Cancion('balada para un gordo','balada','castellano')
lista=[cancion1,cancion2,cancion3]    
        
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('listar.html', titulo='Canciones',musicas=lista)

@app.route('/nuevoregistro')
def nuevoregistro():
    return render_template('nuevoregistro.html', titulo='Nueva Canción')
    #return 'estoy en nuevo registro' 


@app.route('/crear', methods=['POST',])
def crear():
    titulo = request.form['titulo']
    categoria = request.form['categoria']
    idioma = request.form['idioma']
    cancion = Cancion(titulo, categoria, idioma)
    lista.append(cancion)
    return render_template('listar.html', titulo='Canciones', musicas=lista)
    

app.run(host="0.0.0.0", port=5000)











