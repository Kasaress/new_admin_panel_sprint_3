from etl.config.config import db_settings, es_settings
from etl.extractor import PostgresProducer, PostgresEnricher, PostgresMerger
from etl.loader import ElasticsearchLoader
from etl.tramsformer import PostgresToElasticTransformer


class ETLProcess:
    def __init__(self):
        self.producer = PostgresProducer(db_settings)
        self.enricher = PostgresEnricher()
        self.merger = PostgresMerger()
        self.transformer = PostgresToElasticTransformer()
        self.loader = ElasticsearchLoader(es_settings)

    def run(self) -> None:
        """
        Выполняет полный ETL процесс.
        """
        # data = self.producer.produce()
        # enriched_data = self.enricher.enrich(data)
        # merged_data = self.merger.merge(data, enriched_data)
        # transformed_data = self.transformer.transform(merged_data)
        # self.loader.load(transformed_data)
        print('run ETLProcess')
