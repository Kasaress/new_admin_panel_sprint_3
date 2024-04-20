import json
from elasticsearch import Elasticsearch, helpers

from etl.config.elastic_index_schema import elastic_index_settings
from etl.config.logging_settings import logger


class ElasticsearchLoader:
    def __init__(self, es_settings):
        self.elastic = Elasticsearch([es_settings.dict()])
        self.index_name = "movies"
        self.index_settings = elastic_index_settings
        self.setup_index()

    def setup_index(self):
        if not self.elastic.indices.exists(index=self.index_name):
            self.elastic.indices.create(index=self.index_name, body=self.index_settings)

    def load(self, transformed_data):
        print("Loading data into Elasticsearch...")
        for item in transformed_data:
            logger.info(f'{item.dict()=}')
            self.elastic.index(index=self.index_name, id=item.id, body=item.dict())
