import psycopg2
from datetime import datetime

from psycopg2.extras import DictCursor

from etl.config.raw_sql import query_by_modified, query_all


class PostgresExtractor:
    def __init__(self, db_settings):
        self.connection = psycopg2.connect(**db_settings.dict())
        self.query_by_modified: str = query_by_modified
        self.query_all: str = query_all

    def extract(self, modified: datetime | None):
        data = []
        with self.connection.cursor(cursor_factory=DictCursor) as cursor:
            if modified:
                cursor.execute(
                    self.query_by_modified, (modified, modified, modified)
                )
            else:
                cursor.execute(self.query_all)

            for record in cursor:
                data.append(dict(record))
        return data
