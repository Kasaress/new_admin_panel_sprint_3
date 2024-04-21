from pydantic import Extra, Field
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    dbname: str = Field(alias='DB_NAME')
    user: str = Field(alias='DB_USER')
    password: str = Field(alias='DB_PASSWORD')
    host: str = Field(alias='DB_HOST')
    port: str = Field(alias='DB_PORT')

    class Config:
        env_file = '.env'
        extra = Extra.ignore


class ElasticsearchSettings(BaseSettings):
    scheme: str = Field(alias='ES_SCHEMA')
    host: str = Field(alias='ES_HOST')
    port: int = Field(alias='ES_PORT')

    class Config:
        env_file = '.env'
        extra = Extra.ignore


db_settings = DatabaseSettings()
es_settings = ElasticsearchSettings()
