import json
from elasticsearch import Elasticsearch, helpers


class ElasticsearchLoader:
    def __init__(self, es_settings):
        self.host = es_settings.host
        self.port = es_settings.port
        self.scheme = es_settings.scheme
        self.elastic = Elasticsearch([{'scheme': self.scheme, 'host': self.host, 'port': self.port}])
        self.index_name = "movies"
        self.setup_index()

    def setup_index(self):
        # Удалить индекс, если он уже существует
        if self.elastic.indices.exists(index=self.index_name):
            self.elastic.indices.delete(index=self.index_name)
        # Конфигурация индекса
        index_settings = {
            "settings": {
                "refresh_interval": "1s",
                "analysis": {
                    "filter": {
                        "english_stop": {"type": "stop", "stopwords": "_english_"},
                        "english_stemmer": {"type": "stemmer", "language": "english"},
                        "english_possessive_stemmer": {"type": "stemmer", "language": "possessive_english"},
                        "russian_stop": {"type": "stop", "stopwords": "_russian_"},
                        "russian_stemmer": {"type": "stemmer", "language": "russian"}
                    },
                    "analyzer": {
                        "ru_en": {
                            "tokenizer": "standard",
                            "filter": [
                                "lowercase",
                                "english_stop",
                                "english_stemmer",
                                "english_possessive_stemmer",
                                "russian_stop",
                                "russian_stemmer"
                            ]
                        }
                    }
                }
            },
            "mappings": {
                "dynamic": "strict",
                "properties": {
                    "id": {"type": "keyword"},
                    "imdb_rating": {"type": "float"},
                    "genres": {"type": "keyword"},
                    "title": {
                        "type": "text",
                        "analyzer": "ru_en",
                        "fields": {"raw": {"type": "keyword"}}
                    },
                    "description": {"type": "text", "analyzer": "ru_en"},
                    "directors_names": {"type": "text", "analyzer": "ru_en"},
                    "actors_names": {"type": "text", "analyzer": "ru_en"},
                    "writers_names": {"type": "text", "analyzer": "ru_en"},
                    "directors": {
                        "type": "nested",
                        "dynamic": "strict",
                        "properties": {
                            "id": {"type": "keyword"},
                            "name": {"type": "text", "analyzer": "ru_en"}
                        }
                    },
                    "actors": {
                        "type": "nested",
                        "dynamic": "strict",
                        "properties": {
                            "id": {"type": "keyword"},
                            "name": {"type": "text", "analyzer": "ru_en"}
                        }
                    },
                    "writers": {
                        "type": "nested",
                        "dynamic": "strict",
                        "properties": {"id": {"type": "keyword"},
                            "name": {"type": "text", "analyzer": "ru_en"}
                        }
                    }
                }
            }
        }
        # Создание индекса с этими настройками
        self.elastic.indices.create(index=self.index_name, body=index_settings)

    def load(self, transformed_data):
        print("Loading data into Elasticsearch...")
        for item in transformed_data:
            self.elastic.index(index=self.index_name, id=item['id'], body=item)
