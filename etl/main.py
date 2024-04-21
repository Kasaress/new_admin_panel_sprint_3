from apscheduler.schedulers.background import BackgroundScheduler

from etl.elt_process import ETLProcess
import time
from datetime import datetime
from apscheduler.executors.pool import ProcessPoolExecutor

from etl.state import State

executors = {
    'default': ProcessPoolExecutor(max_workers=1),
}
scheduler = BackgroundScheduler(executors=executors)


def start_etl() -> None:
    state = State()
    etl = ETLProcess(state)
    etl.run()


def run_tasks() -> None:
    scheduler.add_job(
        start_etl,
        'cron',
        minute=1,
        max_instances=1,
        misfire_grace_time=5 * 60,
        next_run_time=datetime.now()
    )


if __name__ == '__main__':
    start_etl()
    # run_tasks()
    # scheduler.start()
    # try:
    #     while True:
    #         time.sleep(1)
    #
    # except KeyboardInterrupt:
    #     scheduler.shutdown()
