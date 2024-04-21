import json
import random

import backoff
import elastic_transport
from elasticsearch import Elasticsearch

from etl.config.elastic_index_schema import elastic_index_settings
from etl.config.logging_settings import logger
from etl.exceptions import ElasticConnectionError


class ElasticsearchLoader:
    """Класс загрузки данных в Elasticsearch."""
    def __init__(self, es_settings):
        self.elastic = Elasticsearch([es_settings.dict()], timeout=5)
        self.index_name = "movies"
        self.index_settings = elastic_index_settings

    @backoff.on_exception(
        backoff.expo,
        elastic_transport.ConnectionTimeout,
        max_tries=10,
        max_time=10,
        jitter=lambda: random.uniform(0.2, 1),
    )
    def setup_index(self):
        """
        Если индекса еще нет - создает его.
        """
        if not self.elastic.indices.exists(index=self.index_name):
            self.elastic.indices.create(
                index=self.index_name,
                body=self.index_settings
            )

    @backoff.on_exception(
        backoff.expo,
        elastic_transport.ConnectionTimeout,
        max_tries=10,
        max_time=10,
        jitter=lambda: random.uniform(0.2, 1),
    )
    def load(self, transformed_data):
        """Метод пообъектной загрузки данных."""
        try:
            self.setup_index()
            for item in transformed_data:
                self.elastic.index(
                    index=self.index_name,
                    id=item.id,
                    body=item.dict()
                )
        except elastic_transport.ConnectionTimeout as error:
            raise ElasticConnectionError(
                f'Ошибка загрузки данных: {error}. Данные: '
                f'{transformed_data} не были загружены.'
            )
