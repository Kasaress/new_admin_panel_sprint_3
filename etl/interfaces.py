from abc import ABC, abstractmethod


class PostgresETLComponent(ABC):
    """
    Общий абстрактный класс для компонентов ETL процесса в PostgreSQL.
    """
    pass


class PostgresProducer(PostgresETLComponent):
    @abstractmethod
    def produce(self):
        pass


class PostgresEnricher(PostgresETLComponent):
    @abstractmethod
    def enrich(self, data):
        pass


class PostgresMerger(PostgresETLComponent):
    @abstractmethod
    def merge(self, data, additional_data):
        pass


class ETLProcess(ABC):
    def __init__(self, producer: PostgresProducer, enricher: PostgresEnricher, merger: PostgresMerger):
        self.producer = producer
        self.enricher = enricher
        self.merger = merger

    def execute_etl(self):
        """
        Выполняет полный ETL процесс, используя атрибуты класса.
        """
        # Извлекаем данные
        data = self.producer.produce()

        # Обогащаем данные
        enriched_data = self.enricher.enrich(data)

        # Объединяем данные
        merged_data = self.merger.merge(data, enriched_data)

        return merged_data


class Transformer(ABC):
    @abstractmethod
    def transform(self, data):
        """
        Преобразует данные для загрузки в целевую систему.
        Принимает объединённые данные от Merger, возвращает трансформированные данные.
        """
        pass


class Loader(ABC):
    @abstractmethod
    def load(self, transformed_data):
        """
        Загружает трансформированные данные в Elasticsearch.
        Принимает данные от Transformer.
        """
        pass
