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