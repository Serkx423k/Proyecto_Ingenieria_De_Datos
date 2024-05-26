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