from etl.elt_process import ETLProcess


def start_etl_process() -> None:
    etl_process = ETLProcess()
    etl_process.run()


if __name__ == "__main__":
    start_etl_process()

