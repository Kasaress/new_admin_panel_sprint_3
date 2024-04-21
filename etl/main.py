import time
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from elt_process import ETLProcess
from state import State, Storage


scheduler = BackgroundScheduler()


def start_etl() -> None:
    storage = Storage('modified_storage.txt')
    state = State(storage)
    etl = ETLProcess(state)
    etl.run()


def run_tasks() -> None:
    scheduler.add_job(
        start_etl,
        'interval',
        minutes=1,
        max_instances=1,
        misfire_grace_time=5 * 60,
        next_run_time=datetime.now()
    )


if __name__ == '__main__':
    run_tasks()
    scheduler.start()
    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        scheduler.shutdown()
