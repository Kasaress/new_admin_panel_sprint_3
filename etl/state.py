
class Storage:
    def __init__(self):
        self.file_path: str = ''

    def write(self, modified: str) -> None:
        pass

    def read(self) -> str | None:
        pass


class State:
    def __init__(self):
        self.storage = Storage()

    def get_state(self) -> str | None:
        return self.storage.read()

    def set_state(self, modified: str) -> None:
        self.storage.write(modified)
        return None

