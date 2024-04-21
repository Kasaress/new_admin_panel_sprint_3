from config.config import db_settings, es_settings
from config.logging_settings import logger
from exceptions import ElasticConnectionError, PostgresConnectionError
from extractor import PostgresExtractor
from loader import ElasticsearchLoader
from state import State
from tramsformer import PostgresToElasticTransformer


class ETLProcess:
    def __init__(self, state_manager: State):
        self.extractor = PostgresExtractor(db_settings)
        self.transformer = PostgresToElasticTransformer()
        self.loader = ElasticsearchLoader(es_settings)
        self.state_manager = state_manager

    def run(self) -> None:
        """
        Выполняет полный ETL процесс.
        """
        state = self.state_manager.get_state()
        logger.info(f'Run ETLProcess with state {state}.')
        try:
            data = self.extractor.extract(state)
            transformed_data = self.transformer.transform(data)
            self.loader.load(transformed_data)
        except (PostgresConnectionError, ElasticConnectionError) as error:
            logger.error(f'Complete ETLProcess with error: {error}')
        except Exception as error:
            logger.exception(f'Complete ETLProcess with unknown error: {error}')
        else:
            self.state_manager.set_state()
        logger.info('Complete ETLProcess')
