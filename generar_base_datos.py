import mysql.connector
from mysql.connector import errorcode

print("Conectando...")
try:
    conn = mysql.connector.connect(
           host='127.0.0.1',
           user='root'
           #password='admin'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe un error en el nombre de usuario o en la clave')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `spotyfranz`;")

cursor.execute("CREATE DATABASE `spotyfranz`;")

cursor.execute("USE `spotyfranz`;")

# creando las tablas
TABLES = {}
TABLES['Canciones'] = ('''
      CREATE TABLE `canciones` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `titulo` varchar(50) NOT NULL,
      `categoria` varchar(40) NOT NULL,
      `idioma` varchar(20) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Usuarios'] = ('''
      CREATE TABLE `usuarios` (
      `nombre` varchar(20) NOT NULL,
      `nickname` varchar(8) NOT NULL,
      `clave` varchar(100) NOT NULL,
      PRIMARY KEY (`nickname`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabla_nombre in TABLES:
      tabla_sql = TABLES[tabla_nombre]
      try:
            print('Creando tabla {}:'.format(tabla_nombre), end=' ')
            cursor.execute(tabla_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Ya existe la tabla')
            else:
                  print(err.msg)
      else:
            print('OK')


# insertando usuarios
usuario_sql = 'INSERT INTO usuarios (nombre, nickname, clave) VALUES (%s, %s, %s)'

usuarios = [
      ("Jair Sampaio", "JS", "patitofeo"),
      ("Rosa Flores", "rosita", "michifuz"),
      ("Yami Moto Nokamina", "kamikaze", "sayonara")
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute('select * from spotyfranz.usuarios')
print(' -------------  Usuarios:  -------------')
for user in cursor.fetchall():
    print(user[1])

# insertando canciones
canciones_sql = 'INSERT INTO canciones (titulo, categoria, idioma) VALUES (%s, %s, %s)'

canciones = [
      ('La guitarra', 'Pop', 'Castellano'),
      ('Para no verte más', 'Pop', 'Castellano'),
      ('Balada para un gordo', 'Balada', 'Castellano'),
      ]
cursor.executemany(canciones_sql, canciones)

cursor.execute('select * from spotyfranz.canciones')
print(' -------------  Canciones:  -------------')
for cancion in cursor.fetchall():
    print(cancion[1])

# commitando si no hay nada que tenga efecto
conn.commit()

cursor.close()
conn.close()