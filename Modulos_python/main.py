import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import psycopg2

# Función para obtener los datos del género más y menos desarrollado por una desarrolladora específica
def obtener_comparacion_generos(desarrolladora):
    try:
        # Conexión a la base de datos
        connection = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='123456789',
            database='Video_Game_Sales',
            port='5432'
        )

        # Consulta SQL para obtener la comparación
        query = """
        WITH Desarrolladora_Genero_Rank AS (
          SELECT 
            d.nombre_desarrolladora,
            g.nombre_genero,
            COUNT(v.id_videojuego) AS cantidad_videojuegos,
            RANK() OVER (PARTITION BY d.nombre_desarrolladora ORDER BY COUNT(v.id_videojuego) DESC) AS rank_mas_desarrollado,
            RANK() OVER (PARTITION BY d.nombre_desarrolladora ORDER BY COUNT(v.id_videojuego) ASC) AS rank_menos_desarrollado
          FROM 
            desarrolladora d
          JOIN 
            version_videojuego vv ON d.id_desarrolladora = vv.id_desarrolladora
          JOIN 
            videojuego v ON vv.id_videojuego_base = v.id_videojuego
          JOIN 
            genero g ON v.id_genero = g.id_genero
          GROUP BY 
            d.nombre_desarrolladora, g.nombre_genero
        )

        SELECT 
          dg.nombre_desarrolladora,
          dg.nombre_genero AS genero_mas_desarrollado,
          dg.cantidad_videojuegos AS cantidad_mas_desarrollado,
          dg2.nombre_genero AS genero_menos_desarrollado,
          dg2.cantidad_videojuegos AS cantidad_menos_desarrollado
        FROM 
          Desarrolladora_Genero_Rank dg
        JOIN 
          Desarrolladora_Genero_Rank dg2 
        ON 
          dg.nombre_desarrolladora = dg2.nombre_desarrolladora
        WHERE 
          dg.nombre_desarrolladora = %s AND dg.rank_mas_desarrollado = 1 AND dg2.rank_menos_desarrollado = 1;
        """

        # Obtener los datos en un DataFrame
        df = pd.read_sql_query(query, connection, params=(desarrolladora,))

        # Cerrar la conexión
        connection.close()

        return df
    except Exception as e:
        print(f"Error al obtener los datos: {e}")
        return pd.DataFrame(columns=['nombre_genero', 'cantidad_videojuegos'])

# Obtener lista de desarrolladoras
def obtener_desarrolladoras():
    try:
        # Conexión a la base de datos
        connection = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='123456789',
            database='Video_Game_Sales',
            port='5432'
        )

        # Consulta SQL para obtener la lista de desarrolladoras
        query = "SELECT DISTINCT nombre_desarrolladora FROM desarrolladora;"

        # Obtener los datos en un DataFrame
        df = pd.read_sql_query(query, connection)

        # Cerrar la conexión
        connection.close()

        return df['nombre_desarrolladora'].tolist()
    except Exception as e:
        print(f"Error al obtener las desarrolladoras: {e}")
        return []
    


def obtener_datos():
    try:
        # Conexión a la base de datos
        connection = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='123456789',
            database='Video_Game_Sales',
            port='5432'
        )

        # Consulta SQL
        query = """
        WITH GeneroJuegos AS (
            SELECT g.nombre_genero, COUNT(v.id_videojuego) AS total_juegos
            FROM genero g
            LEFT JOIN videojuego v ON g.id_genero = v.id_genero
            GROUP BY g.nombre_genero
        ), VentasPromedio AS (
            SELECT g.nombre_genero,
                   AVG(vt.ventas_na) AS promedio_ventas_na,
                   AVG(vt.ventas_eu) AS promedio_ventas_eu,
                   AVG(vt.ventas_jp) AS promedio_ventas_jp,
                   AVG(vt.otras_ventas) AS promedio_otras_ventas,
                   AVG(vt.ventas_globales) AS promedio_ventas_globales
            FROM venta vt
            INNER JOIN version_videojuego vv ON vt.id_version_videojuego = vv.id_version
            INNER JOIN videojuego v ON vv.id_videojuego_base = v.id_videojuego
            INNER JOIN genero g ON v.id_genero = g.id_genero
            GROUP BY g.nombre_genero
        )
        SELECT gj.nombre_genero, gj.total_juegos,
               vp.promedio_ventas_na, vp.promedio_ventas_eu, vp.promedio_ventas_jp,
               vp.promedio_otras_ventas, vp.promedio_ventas_globales
        FROM GeneroJuegos gj
        LEFT JOIN VentasPromedio vp ON gj.nombre_genero = vp.nombre_genero
        ORDER BY gj.total_juegos DESC;
        """

        # Obtener los datos en un DataFrame
        df = pd.read_sql_query(query, connection)

        # Cerrar la conexión
        connection.close()

        return df
    except Exception as e:
        print(f"Error al obtener los datos: {e}")
        return pd.DataFrame()

# Obtener los datos
df_b = obtener_datos()



    

# Crear la aplicación Dash
app = dash.Dash(__name__)

# Crear el layout de la aplicación
app.layout = html.Div(className="main-content", children=[
    html.Div(className="app-title", children=[
        html.H1("Proyecto Ingenieria de")
    ]),
    html.H1('Comparación de Géneros por Desarrolladora'),
    dcc.Dropdown(
        id='desarrolladora-dropdown',
        options=[{'label': desarrolladora, 'value': desarrolladora} for desarrolladora in obtener_desarrolladoras()],
        value='Capcom'  # Valor por defecto
    ),
    dcc.Graph(id='bar-chart'),
    html.H1("Análisis de Juegos por Género y Ventas Promedio por Región"),
    dcc.Graph(
        id='bar-chart-ventas',
        figure={
            'data': [
                go.Bar(
                    x=df_b['nombre_genero'],
                    y=df_b['total_juegos'],
                    name='Total Juegos Desarrollados',
                    marker_color='blue'
                ),
                go.Bar(
                    x=df_b['nombre_genero'],
                    # Ventas Promedio NA
                    y=df_b['promedio_ventas_na'],
                    name='Ventas Promedio NA',
                    marker_color='orange'
                ),
                go.Bar(
                    x=df_b['nombre_genero'],
                    y=df_b['promedio_ventas_eu'],
                    name='Ventas Promedio EU',
                    marker_color='green'
                ),
                go.Bar(
                    x=df_b['nombre_genero'],
                    y=df_b['promedio_ventas_jp'],
                    name='Ventas Promedio JP',
                    marker_color='red'
                ),
                go.Bar(
                    x=df_b['nombre_genero'],
                    y=df_b['promedio_otras_ventas'],
                    name='Otras Ventas Promedio',
                    marker_color='purple'
                ),
                go.Bar(
                    x=df_b['nombre_genero'],
                    y=df_b['promedio_ventas_globales'],
                    name='Ventas Globales Promedio',
                    marker_color='gray'
                )
            ],
            'layout': {
                'title': 'Cantidad de Juegos Desarrollados y Ventas Promedio por Género y Región',
                'barmode': 'group',
                'xaxis': {'title': 'Género'},
                'yaxis': {'title': 'Cantidad / Promedio de Ventas'}
            }
        }
    )
])

# Callback para actualizar la gráfica cuando se selecciona una nueva desarrolladora
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('desarrolladora-dropdown', 'value')]
)
def update_bar_chart(selected_desarrolladora):
    df = obtener_comparacion_generos(selected_desarrolladora)
    if df.empty:
        fig = px.bar(title=f'No se encontraron datos para {selected_desarrolladora}')
    else:
        # Unificar los datos en un formato adecuado para Plotly
        data = {
            'Género': ['Más Desarrollado', 'Menos Desarrollado'],
            'Nombre': [df['genero_mas_desarrollado'][0], df['genero_menos_desarrollado'][0]],
            'Cantidad': [df['cantidad_mas_desarrollado'][0], df['cantidad_menos_desarrollado'][0]]
        }
        df_plot = pd.DataFrame(data)
        fig = px.bar(df_plot, x='Nombre', y='Cantidad', color='Género', title=f'Comparación de Géneros por {selected_desarrolladora}')
    return fig

# Ejecutar el servidor
if __name__ == '__main__':
    app.run_server(debug=True)

