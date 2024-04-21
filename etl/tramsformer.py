from etl.config.logging_settings import logger
from etl.schemas import FilmWorkSchema


class PostgresToElasticTransformer:
    def transform(self, rows_from_postgres_query):
        data = []
        for row in rows_from_postgres_query:
            try:
                data.append(FilmWorkSchema(**row))
            except Exception as er:
                logger.error(f'Ошибка {row=}, {er=}')
                continue
        return data
