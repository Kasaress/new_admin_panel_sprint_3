import datetime

from etl.config.config import db_settings, es_settings
from etl.config.logging_settings import logger
from etl.extractor import PostgresExtractor
from etl.loader import ElasticsearchLoader
from etl.tramsformer import PostgresToElasticTransformer


class ETLProcess:
    def __init__(self):
        self.extractor = PostgresExtractor(db_settings)
        self.transformer = PostgresToElasticTransformer()
        self.loader = ElasticsearchLoader(es_settings)
        self.state = None

    def run(self) -> None:
        """
        Выполняет полный ETL процесс.
        """
        logger.info('run ETLProcess')
        if not self.state:
            modified = None
        else:
            modified = datetime.datetime.utcnow() - datetime.timedelta(minutes=10)
        data = self.extractor.extract(modified)
        transformed_data = self.transformer.transform(data)
        self.loader.load(transformed_data)
        logger.info('complite ETLProcess')
