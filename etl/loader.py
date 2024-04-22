import random

import backoff
import elastic_transport
from elasticsearch import Elasticsearch, helpers

from config.elastic_index_schema import elastic_index_settings
from exceptions import ElasticConnectionError


class ElasticsearchLoader:
    """Класс загрузки данных в Elasticsearch."""
    def __init__(self, es_settings):
        self.elastic = Elasticsearch([es_settings.dict()], timeout=5)
        self.index_name = "movies"
        self.index_settings = elastic_index_settings

    @backoff.on_exception(
        backoff.expo,
        (elastic_transport.ConnectionError, elastic_transport.ConnectionTimeout),
        max_tries=10,
        max_time=10,
        jitter=lambda: random.uniform(0.2, 1),
    )
    def setup_index(self):
        """
        Если индекса еще нет - создает его.
        Бэкофф отрабатывает ретраи, и если они не помогли,
        райзит ошибку.
        """
        if not self.elastic.indices.exists(index=self.index_name):
            self.elastic.indices.create(
                index=self.index_name,
                body=self.index_settings
            )

    @backoff.on_exception(
        backoff.expo,
        (elastic_transport.ConnectionError, elastic_transport.ConnectionTimeout),
        max_tries=10,
        max_time=10,
        jitter=lambda: random.uniform(0.2, 1),
    )
    def _bulk_load(self, transformed_data):
        """
        Метод загрузки данных в эластик пачкой.
        Исключение для бэкоффа возникает только если transformed_data не пустая.
        """
        bulk_data = []
        for item in transformed_data:
            bulk_data.append({
                '_op_type': 'index',
                '_index': self.index_name,
                '_id': item.id,
                '_source': item.dict()
            })
        helpers.bulk(self.elastic, bulk_data)

    def load(self, transformed_data):
        """
        Метод загрузки данных в эластик.
        Вызывает методы класса с бэкофф. Если ретраи в бэкофф не помогают,
        ловим соответствующие ошибки и райзим кастомное
        исключение для обработки в etl.run.
        Для проверки отработки исключений можно поставить контейнер с эластиком на паузу,
        изменить поле modified в любом объекте в БД и посмотреть логи.
        """
        try:
            self.setup_index()
            self._bulk_load(transformed_data)
        except (elastic_transport.ConnectionError, elastic_transport.ConnectionTimeout) as error:
            raise ElasticConnectionError(
                f'Ошибка загрузки данных: {error}. Данные: '
                f'{transformed_data} не были загружены.'
            )
        finally:
            if self.elastic:
                self.elastic.close()
