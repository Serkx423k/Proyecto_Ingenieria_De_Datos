import dash 
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import psycopg2

try:
    connection = psycopg2.connect(
        host='localhost',
        user='postgres',
        password='123456789',
        database='Video_Games_Sale',
        port='5432'
    )

    query = """
    SELECT 
        g.nombre_genero,
        COUNT(v.id_videojuego) AS cantidad_videojuegos
    FROM 
        desarrolladora d
    JOIN 
        version_videojuego vv ON d.id_desarrolladora = vv.id_desarrolladora
    JOIN 
        videojuego v ON vv.id_videojuego_base = v.id_videojuego
    JOIN 
        genero g ON v.id_genero = g.id_genero
    WHERE 
        d.nombre_desarrolladora = 'Capcom'
    GROUP BY 
        g.nombre_genero
    ORDER BY 
        cantidad_videojuegos DESC
    LIMIT 3;
    """

    # Obtén los datos en un DataFrame
    df = pd.read_sql_query(query, connection)

except Exception as ex:
    print(ex)
finally:
    connection.close()
    print("Conexión finalizada")

# Crear la aplicación Dash
app = dash.Dash(__name__)

# Crear el gráfico de barras usando Plotly Express
fig = px.bar(df, x='nombre_genero', y='cantidad_videojuegos', title='Tres Géneros Más Desarrollados por Capcom')

# Definir el layout de la aplicación
app.layout = html.Div([
    html.H1('Géneros Más Desarrollados por Capcom'),
    dcc.Graph(
        id='bar-chart',
        figure=fig
    )
])

# Ejecutar el servidor
if __name__ == '__main__':
    app.run_server(debug=True)
