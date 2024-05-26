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
        connection = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='123456789',
            database='Video_Games_Sales',
            port='5432'
        )

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

        df = pd.read_sql_query(query, connection, params=(desarrolladora,))
        return df
    except Exception as e:
        print(f"Error al obtener los datos: {e}")
        return pd.DataFrame(columns=['nombre_genero', 'cantidad_videojuegos'])
    finally:
        if connection:
            connection.close()

# Obtener lista de desarrolladoras
def obtener_desarrolladoras():
    try:
        connection = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='123456789',
            database='Video_Games_Sales',
            port='5432'
        )

        query = "SELECT DISTINCT nombre_desarrolladora FROM desarrolladora;"
        df = pd.read_sql_query(query, connection)
        return df['nombre_desarrolladora'].tolist()
    except Exception as e:
        print(f"Error al obtener las desarrolladoras: {e}")
        return []
    finally:
        if connection:
            connection.close()

# Obtener los datos del análisis de juegos por género y ventas promedio por región
def obtener_datos():
    try:
        connection = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='123456789',
            database='Video_Games_Sales',
            port='5432'
        )

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

        df = pd.read_sql_query(query, connection)
        return df
    except Exception as e:
        print(f"Error al obtener los datos: {e}")
        return pd.DataFrame()
    finally:
        if connection:
            connection.close()

df_b = obtener_datos()

# Obtener las ventas anuales del género con mayor número de juegos desarrollados
def obtener_ventas_anuales_genero_mayor():
    try:
        connection = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='123456789',
            database='Video_Games_Sales',
            port='5432'
        )

        query = """
        WITH GeneroMasDesarrollado AS (
            SELECT 
                g.id_genero, 
                g.nombre_genero, 
                COUNT(v.id_videojuego) AS total_juegos
            FROM genero g
            JOIN videojuego v ON g.id_genero = v.id_genero
            GROUP BY g.id_genero, g.nombre_genero
            ORDER BY total_juegos DESC
            LIMIT 1
        ),
        VentasAnuales AS (
            SELECT 
                EXTRACT(YEAR FROM to_date(vv.ano_lanzamiento::text, 'YYYY')) AS ano,
                SUM(vt.ventas_globales) AS ventas_globales
            FROM venta vt
            JOIN version_videojuego vv ON vt.id_version_videojuego = vv.id_version
            JOIN videojuego v ON vv.id_videojuego_base = v.id_videojuego
            WHERE v.id_genero = (SELECT id_genero FROM GeneroMasDesarrollado)
            GROUP BY EXTRACT(YEAR FROM to_date(vv.ano_lanzamiento::text, 'YYYY'))
            HAVING EXTRACT(YEAR FROM to_date(vv.ano_lanzamiento::text, 'YYYY')) >= 1985
            ORDER BY ano
        )
        SELECT (SELECT nombre_genero FROM GeneroMasDesarrollado) AS nombre_genero, ano, ventas_globales FROM VentasAnuales;
        """

        df = pd.read_sql_query(query, connection)
        return df
    except Exception as e:
        print(f"Error al obtener los datos: {e}")
        return pd.DataFrame()
    finally:
        if connection:
            connection.close()

# Obtener el videojuego con el mayor número de ventas totales y la plataforma asociada
def obtener_videojuego_mayores_ventas():
    try:
        connection = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='123456789',
            database='Video_Games_Sales',
            port='5432'
        )

        query = """
        WITH VentasTotales AS (
            SELECT vv.id_version, vv.nombre_videojuego,
                   SUM(vt.ventas_globales) AS total_ventas_globales
            FROM venta vt
            INNER JOIN version_videojuego vv ON vt.id_version_videojuego = vv.id_version
            GROUP BY vv.id_version, vv.nombre_videojuego
        ), MaxVentas AS (
            SELECT MAX(total_ventas_globales) AS max_ventas_globales
            FROM VentasTotales
        )
        SELECT vt.nombre_videojuego, vt.total_ventas_globales, r.id_consola, c.nombre_consola
        FROM VentasTotales vt
        INNER JOIN requiere r ON vt.id_version = r.id_videojuego
        INNER JOIN consola c ON r.id_consola = c.id_consola
        CROSS JOIN MaxVentas mv
        WHERE vt.total_ventas_globales = mv.max_ventas_globales;
        """

        df = pd.read_sql_query(query, connection)
        return df
    except Exception as e:
        print(f"Error al obtener los datos: {e}")
        return pd.DataFrame(columns=['nombre_videojuego', 'total_ventas_globales', 'nombre_consola'])
    finally:
        if connection:
            connection.close()



app = dash.Dash(__name__)

app.layout = html.Div(className="main-content", children=[
    html.Div(className="app-title", children=[
        html.H1("Game Analitycs")
    ]),
    html.H1('Comparación de Géneros por Desarrolladora'),
    html.Div(className="text-container", children=[html.P(''' Por cada desarrolladora, determinar cuál es el género, para el que más
han desarrollado videojuegos, y para el que menos han desarrollado
videojuegos. Para así tomar el contraste que existe sobre la cantidad de
unidades vendidas entre el género con más desarrollo y el género con
menos desarrollo. Este caso analiza la relación entre el género de los
videojuegos desarrollados por cada compañía y las unidades vendidas.''', className="text-p")]),
    dcc.Dropdown(
        id='desarrolladora-dropdown',
        options=[{'label': desarrolladora, 'value': desarrolladora} for desarrolladora in obtener_desarrolladoras()],
        value='Capcom'
    ),
    dcc.Graph(id='pie-chart'),
    html.H1("Análisis de Juegos por Género y Ventas Promedio por Región"),
    html.Div(className="text-container", children=[html.P(''' Encontrar la cantidad de juegos desarrollados por género, y realizar un
promedio de copias vendidas por región de cada género. Este caso nos
permite entender como el genero de un juego afecta sus ventas en
diferentes partes del mundo.''', className="text-p")]),
    dcc.Graph(
        id='bar-chart-total-ventas',
        figure={
            'data': [
                go.Bar(
                    x=df_b['nombre_genero'],
                    y=df_b['total_juegos'],
                    name='Total Juegos Desarrollados',
                    marker_color='blue'
                )
            ],
            'layout': {
                'title': 'Cantidad de Juegos Desarrollados por Género',
                'xaxis': {'title': 'Género'},
                'yaxis': {'title': 'Cantidad de Juegos'}
            }
        }
    ),
    html.H2("Ventas Promedio por Región según Género"),
    dcc.Dropdown(
        id='genero-dropdown',
        options=[{'label': genero, 'value': genero} for genero in df_b['nombre_genero']],
        value=df_b['nombre_genero'][0]
    ),
    dcc.Graph(id='bar-chart-ventas-promedio'),
    html.H1("Ventas Anuales del Género con Mayor Número de Juegos Desarrollados"),
    html.Div(className="text-container", children=[html.P('''Hacer una gráfica sobre las ventas anuales del género con mayor número
de juegos desarrollados. Este caso busca analizar el rendimiento de ventas
de un género específico a lo largo del tiempo. Es útil para comprender la
evolución y el éxito relativo de un género en particular.
 ''', className="text-p")]),
    dcc.Graph(id='line-chart-ventas-anuales'),
    html.H1("Videojuego con Mayor Número de Ventas Totales y su Plataforma"),
    html.Div(className="text-container", children=[html.P('''Determinar cuál ha sido el videojuego con el mayor número de ventas
totales y la plataforma para la cual se da este escenario. Este caso se
enfoca en identificar el videojuego más exitoso en términos de ventas
totales y la plataforma asociada. Es útil para comprender qué juegos y
plataformas han sido más populares entre los consumidores. ''', className="text-p")]),
    html.Div(id='videojuego-mayores-ventas')
])

@app.callback(
    Output('pie-chart', 'figure'),
    [Input('desarrolladora-dropdown', 'value')]
)
def update_pie_chart(selected_desarrolladora):
    df = obtener_comparacion_generos(selected_desarrolladora)
    if df.empty:
        fig = px.pie(title=f'No se encontraron datos para {selected_desarrolladora}')
    else:
        labels = ['Más Desarrollado', 'Menos Desarrollado']
        values = [df['cantidad_mas_desarrollado'][0], df['cantidad_menos_desarrollado'][0]]
        hover_data = {
            'Nombre del Género': [df['genero_mas_desarrollado'][0], df['genero_menos_desarrollado'][0]],
            'Cantidad': values,
            'Porcentaje': [f"{(val/sum(values))*100:.2f}%" for val in values]
        }
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hoverinfo='label+value+percent+text',
            textinfo='value+percent',
            textposition='inside',
            marker=dict(colors=['#1f77b4', '#ff7f0e'])
        )])
        fig.update_layout(
            title=f'Comparación de Géneros por {selected_desarrolladora}',
            annotations=[
                dict(text=f"Género más desarrollado: {df['genero_mas_desarrollado'][0]}<br>Cantidad de juegos desarrollados: {values[0]}",
                     x=0.1, y=-0.1, showarrow=False),
                dict(text=f"Género menos desarrollado: {df['genero_menos_desarrollado'][0]}<br>Cantidad de juegos desarrollados: {values[1]}",
                     x=0.9, y=-0.1, showarrow=False)
            ]
        )
    return fig

@app.callback(
    Output('bar-chart-ventas-promedio', 'figure'),
    [Input('genero-dropdown', 'value')]
)
def update_bar_chart_ventas_promedio(selected_genero):
    df_filtered = df_b[df_b['nombre_genero'] == selected_genero]
    if df_filtered.empty:
        fig = px.bar(title=f'No se encontraron datos para {selected_genero}')
    else:
        fig = go.Figure(data=[
            go.Bar(name='Ventas Promedio NA', x=['NA'], y=df_filtered['promedio_ventas_na'], marker_color='orange'),
            go.Bar(name='Ventas Promedio EU', x=['EU'], y=df_filtered['promedio_ventas_eu'], marker_color='green'),
            go.Bar(name='Ventas Promedio JP', x=['JP'], y=df_filtered['promedio_ventas_jp'], marker_color='red'),
            go.Bar(name='Otras Ventas Promedio', x=['Otras'], y=df_filtered['promedio_otras_ventas'], marker_color='purple'),
            go.Bar(name='Ventas Globales Promedio', x=['Globales'], y=df_filtered['promedio_ventas_globales'], marker_color='gray')
        ])
        fig.update_layout(
            title=f'Ventas Promedio por Región para {selected_genero}',
            barmode='group',
            xaxis_title='Región',
            yaxis_title='Promedio de Ventas'
        )
    return fig

@app.callback(
    Output('line-chart-ventas-anuales', 'figure'),
    [Input('desarrolladora-dropdown', 'value')]
)
def update_line_chart_ventas_anuales(selected_desarrolladora):
    df_ventas_anuales = obtener_ventas_anuales_genero_mayor()
    if df_ventas_anuales.empty:
        fig = px.line(title='No se encontraron datos de ventas anuales')
    else:
        genero = df_ventas_anuales['nombre_genero'][0]
        fig = px.line(df_ventas_anuales, x='ano', y='ventas_globales', title=f'Ventas Anuales del Género "{genero}" con Mayor Número de Juegos Desarrollados')
        fig.update_layout(
            xaxis_title='Año',
            yaxis_title='Ventas Globales',
            xaxis=dict(tickmode='linear', dtick=1),
            xaxis_range=[1985, df_ventas_anuales['ano'].max()]
        )
    return fig

@app.callback(
    Output('videojuego-mayores-ventas', 'children'),
    [Input('desarrolladora-dropdown', 'value')]
)
def update_videojuego_mayores_ventas(selected_desarrolladora):
    df_videojuego = obtener_videojuego_mayores_ventas()
    if df_videojuego.empty:
        return html.Div('No se encontraron datos del videojuego con mayores ventas.')
    else:
        nombre_videojuego = df_videojuego['nombre_videojuego'][0]
        total_ventas_globales = df_videojuego['total_ventas_globales'][0]
        nombre_consola = df_videojuego['nombre_consola'][0]
        return html.Div([
            html.H3(f"Videojuego con Mayores Ventas Totales: {nombre_videojuego}"),
            html.P(f"Ventas Totales: {total_ventas_globales}"),
            html.P(f"Plataforma: {nombre_consola}")
        ])

if __name__ == '__main__':
    app.run_server(debug=True)