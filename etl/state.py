import datetime

from config.logging_settings import logger


class Storage:
    def __init__(self, file_path: str):
        self.file_path: str = file_path

    def write(self, modified: str) -> None:
        with open(self.file_path, 'w') as file:
            file.write(
                f"{modified}"
            )
            logger.info(f'write new state {modified}')

    def read(self) -> str | None:
        with open(self.file_path, 'r') as file:
            res = file.read()
        return res


class State:
    def __init__(self, storage: Storage):
        self.storage = storage

    def get_state(self) -> str | None:
        return self.storage.read()

    def set_state(self) -> None:
        modified = datetime.datetime.utcnow()
        modified = modified.strftime("%Y-%m-%d %H:%M:%S.%f+00")
        self.storage.write(modified)
        return None

