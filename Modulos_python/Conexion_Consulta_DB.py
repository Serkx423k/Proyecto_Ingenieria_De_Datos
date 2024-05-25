# Inicialización de la conexión con la base de datos

import psycopg2
try:
    connection = psycopg2.connect(
        host = 'Localhost',
        user = 'postgres',
        password = '123456789',
        database = 'Video_Game_Sales',
        port = '5432'
    )


        
except Exception as ex:
    print(ex)
finally:
    connection.close()
    print("Conexión finalizada")


























    # Inicialización de la conexión con la base de datos

