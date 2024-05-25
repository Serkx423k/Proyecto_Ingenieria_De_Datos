# Inicialización de la conexión con la base de datos

import psycopg2
try:
    connection = psycopg2.connect(
        host = 'Localhost',
        user = 'postgres',
        password = '123456789',
        database = 'Video_Games_Sale',
        port = '5432'
    )


#------------------------------#

# Consulta a las tablas
    
    # Tabla genero
    print("Conexión exitosa")
    cursor = connection.cursor()
    cursor.execute("select * from genero")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        
    # Tabla videojuego
    print("Conexión exitosa")
    cursor = connection.cursor()
    cursor.execute("select * from videojuego")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        
    # Tabla version_videojuego
    print("Conexión exitosa")
    cursor = connection.cursor()
    cursor.execute("select * from version_videojuego")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        
    # Tabla desarrolladora
    print("Conexión exitosa")
    cursor = connection.cursor()
    cursor.execute("select * from desarrolladora")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        
    # Tabla requiere
    print("Conexión exitosa")
    cursor = connection.cursor()
    cursor.execute("select * from requiere")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        
    # Tabla venta
    print("Conexión exitosa")
    cursor = connection.cursor()
    cursor.execute("select * from venta")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        
    # Tabla consola
    print("Conexión exitosa")
    cursor = connection.cursor()
    cursor.execute("select * from consola")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        
except Exception as ex:
    print(ex)
finally:
    connection.close()
    print("Conexión finalizada")


























    # Inicialización de la conexión con la base de datos

