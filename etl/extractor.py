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
        """
        Установление соединения с БД.
        В случае возникновения исключения psycopg2.OperationalError
        бэкофф совершает несколько повторных попыток,
        если ретраи не помогли, райзит то же самое исключение.
        """
        return psycopg2.connect(**self.db_settings.dict(), connect_timeout=5)

    def extract(self, modified: str | None):
        """
        Извлечение данных из Postgres с учетом даты их последнего обновления.
        На этом методе нет декоратора бэкофф, он есть на self.connect().
        Если ретраи в нем не помогли, ловим в этом методе
        psycopg2.OperationalError и райзим выше кастомное исключение.
        Кастомное исключение будет обработано в etl.run().
        Проверить процесс ретраев и обработки исключений можно
        по логам контейнера etl, если поставить на паузу контейнер с постгрес.
        """
        data = []
        connection = None
        try:
            connection = self.connect()
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                if modified:
                    cursor.execute(
                        self.query_by_modified, (modified, modified, modified)
                    )
                else:
                    cursor.execute(self.query_all)
                for record in cursor:
                    data.append(dict(record))
        except psycopg2.OperationalError as error:
            raise PostgresConnectionError(f'Ошибка подключения к БД Postgres {error}.')
        finally:
            if connection:
                connection.close()
        return data
