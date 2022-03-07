import os
from collections.abc import MutableMapping
from contextlib import suppress
from pathlib import Path


class FileStorage(MutableMapping):
    def __init__(self, dirname) -> None:
        with suppress(FileExistsError):
            os.mkdir(dirname)

        self.dirname = Path(dirname)

    def __setitem__(self, name: str, value) -> None:
        with open(self.dirname / name, "w+") as f:
            f.write(value)

    def __getitem__(self, name: str):
        with open(self.dirname / name, "r+") as f:
            return f.read()

    def __len__(self) -> int:
        return len(os.listdir(self.dirname))

    def __iter__(self):
        return iter(os.listdir(self.dirname))

    def __delitem__(self, name):
        with suppress(FileNotFoundError):
            os.remove(self.dirname / name)


storage = FileStorage("test-app")

storage["starks"] = "Winter is coming"
storage["baratheons"] = "Ours is the Fury"

print(storage["starks"])

for file in storage:
    print(file)

# del f["starks"]
