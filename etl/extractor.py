import random

import backoff
import psycopg2
from psycopg2.extras import DictCursor
from pydantic_settings import BaseSettings

from config.raw_sql import query_all, query_by_modified
from exceptions import PostgresConnectionError


class PostgresExtractor:
    """Класс получения данных из Postgres."""
    def __init__(self, db_settings: BaseSettings) -> None:
        self.db_settings = db_settings
        self.query_by_modified: str = query_by_modified
        self.query_all: str = query_all

    @backoff.on_exception(
        backoff.expo,
        psycopg2.OperationalError,
        max_tries=10,
        max_time=10,
        jitter=lambda: random.uniform(0.2, 1),
    )
    def connect(self):
        """Установление соединения с БД."""
        return psycopg2.connect(**self.db_settings.dict(), connect_timeout=5)

    def extract(self, modified: str | None):
        """Извлечение данных из Postgres с учетом даты их последнего обновления."""
        data = []
        try:
            connection = self.connect()
        except psycopg2.OperationalError as error:
            raise PostgresConnectionError(f'Ошибка подключения к БД Postgres {error}.')
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            if modified:
                cursor.execute(
                    self.query_by_modified, (modified, modified, modified)
                )
            else:
                cursor.execute(self.query_all)
            for record in cursor:
                data.append(dict(record))
        return data
