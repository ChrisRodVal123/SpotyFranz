from app import db

class Canciones(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(40), nullable=False)
    idioma = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


class Usuarios(db.Model):
    nickname = db.Column(db.String(8), primary_key=True)
    nombre = db.Column(db.String(20), nullable=False)
    clave = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name