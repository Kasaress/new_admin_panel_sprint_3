from etl.extractor import RealPostgresProducer, RealPostgresEnricher, RealPostgresMerger
from etl.interfaces import PostgresETLProcess
from etl.loader import ElasticsearchLoader


def start_etl_process() -> None:
    producer = RealPostgresProducer()
    enricher = RealPostgresEnricher()
    merger = RealPostgresMerger()
    loader = ElasticsearchLoader()

    etl_process = PostgresETLProcess(producer, enricher, merger)
    data = etl_process.execute_etl()

    loader.load(data)


if __name__ == "__main__":
    start_etl_process()

