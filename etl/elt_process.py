from etl.interfaces import ETLProcess


class PostgresETLProcess(ETLProcess):
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