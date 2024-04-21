from config.logging_settings import logger
from schemas import FilmWorkSchema


class PostgresToElasticTransformer:
    """Класс для преобразования данных из Postgres для загрузки в Elastic."""
    @staticmethod
    def transform(rows_from_postgres: list[dict]) -> list[FilmWorkSchema]:
        """Преобразование сырых данных из БД в объекты для загрузки в Elastic."""
        data = []
        for row in rows_from_postgres:
            try:
                data.append(FilmWorkSchema(**row))
            except Exception as er:
                logger.error(f'Ошибка преобразования данных {row=}, {er=}')
                continue
        return data
