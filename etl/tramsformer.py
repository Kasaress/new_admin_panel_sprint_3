from etl.schemas import FilmWorkSchema


class PostgresToElasticTransformer:
    def transform(self, rows_from_postgres_query):
        data = []
        for row in rows_from_postgres_query:
            data.append(FilmWorkSchema(**row))
        return data
