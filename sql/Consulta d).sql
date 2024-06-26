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