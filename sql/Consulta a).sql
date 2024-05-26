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