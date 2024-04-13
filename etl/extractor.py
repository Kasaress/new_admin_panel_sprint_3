import psycopg2
from datetime import datetime

from etl.interfaces import PostgresProducer, PostgresEnricher, PostgresMerger


# Вставляем здесь ранее определённые абстрактные классы

import psycopg2
from datetime import datetime


class RealPostgresProducer(PostgresProducer):
    def __init__(self, db_settings):
        self.connection = psycopg2.connect(**db_settings)

    def produce(self):
        data = []
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("""
                SELECT fw.id, fw.title, fw.description, fw.rating, fw.type,
                       array_agg(DISTINCT g.name) AS genres,
                       json_agg(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name, 'role', pf.role)) AS persons
                FROM content.film_work AS fw
                LEFT JOIN content.genre_film_work AS gfw ON fw.id = gfw.film_work_id
                LEFT JOIN content.genre AS g ON gfw.genre_id = g.id
                LEFT JOIN content.person_film_work AS pf ON fw.id = pf.film_work_id
                LEFT JOIN content.person AS p ON pf.person_id = p.id
                GROUP BY fw.id;
            """)
            for record in cursor:
                data.append(dict(record))
        return data


class RealPostgresEnricher(PostgresEnricher):
    def enrich(self, data):
        enriched_data = []
        for item in data:
            item['extracted_time'] = datetime.now()
            enriched_data.append(item)
        return enriched_data



class RealPostgresMerger(PostgresMerger):
    def merge(self, data, additional_data):
        print("Merging data...")
        # Простейшее объединение данных; можно расширить логику в соответствии с требованиями
        return additional_data
