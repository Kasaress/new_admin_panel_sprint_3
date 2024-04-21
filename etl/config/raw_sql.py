query_by_modified = """
    SELECT fw.id, fw.title, fw.description, fw.rating, fw.type,
           array_agg(DISTINCT g.name) AS genres,
           CASE
               WHEN COUNT(pf.person_id) > 0
                   THEN jsonb_agg(
                       DISTINCT jsonb_build_object(
                            'id', p.id, 'name', p.full_name, 'role', pf.role
                       )
                   )
               ELSE NULL
           END AS persons
    FROM content.film_work AS fw
    LEFT JOIN content.genre_film_work AS gfw ON fw.id = gfw.film_work_id
    LEFT JOIN content.genre AS g ON gfw.genre_id = g.id
    LEFT JOIN content.person_film_work AS pf ON fw.id = pf.film_work_id
    LEFT JOIN content.person AS p ON pf.person_id = p.id
    WHERE fw.modified > %s OR g.modified > %s OR p.modified > %s
    GROUP BY fw.id
    ORDER BY fw.modified;
"""


query_all = """
    SELECT fw.id, fw.title, fw.description, fw.rating, fw.type,
           array_agg(DISTINCT g.name) AS genres,
           CASE
               WHEN COUNT(pf.person_id) > 0
                   THEN jsonb_agg(
                       DISTINCT jsonb_build_object(
                            'id', p.id, 'name', p.full_name, 'role', pf.role
                       )
                   )
               ELSE NULL
           END AS persons
    FROM content.film_work AS fw
    LEFT JOIN content.genre_film_work AS gfw ON fw.id = gfw.film_work_id
    LEFT JOIN content.genre AS g ON gfw.genre_id = g.id
    LEFT JOIN content.person_film_work AS pf ON fw.id = pf.film_work_id
    LEFT JOIN content.person AS p ON pf.person_id = p.id
    GROUP BY fw.id
    ORDER BY fw.modified;
"""
