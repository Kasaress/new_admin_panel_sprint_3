import datetime

from etl.config.config import db_settings, es_settings
from etl.config.logging_settings import logger
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
        self.state = None

    def run(self) -> None:
        """
        Выполняет полный ETL процесс.
        """
        if not self.state:
            modified = datetime.datetime.utcnow() - datetime.timedelta(weeks=900)
        else:
            modified = datetime.datetime.utcnow() - datetime.timedelta(hours=1)
        data = self.producer.produce(modified)
        # logger.info(data)
        # logger.info(len(data))
        # enriched_data = self.enricher.enrich(data)
        # merged_data = self.merger.merge(data, enriched_data)
        merged_data = data
        transformed_data = self.transformer.transform(merged_data)
        logger.info(transformed_data)
        # logger.info(len(transformed_data))
        self.loader.load(transformed_data)
        logger.info('run ETLProcess')
