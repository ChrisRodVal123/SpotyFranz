SECRET_KEY = 'cochabamba'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{clave}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        clave = '',
        servidor = 'localhost',
        database = 'spotyfranz'
    )