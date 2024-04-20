from pydantic import Field
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    db_name: str = Field(..., env='DB_NAME')
    db_user: str = Field(..., env='DB_USER')
    db_password: str = Field(..., env='DB_PASSWORD')
    db_host: str = Field(..., env='DB_HOST')

    class Config:
        env_file = '.env'


class ElasticsearchSettings(BaseSettings):
    es_host: str = Field(..., env='ES_HOST')
    es_port: int = Field(..., env='ES_PORT')

    class Config:
        env_file = '.env'


db_settings = DatabaseSettings()
es_settings = ElasticsearchSettings()
