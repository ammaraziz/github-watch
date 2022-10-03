import json
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class DB:
    path: Path
    db: dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.path.exists():
            self._create_db()
        if not self.db:
            self._load()

    def transaction(func):
        def wrapper(self, *args, **kwargs):
            self._load()
            res = func(self, *args, **kwargs)
            self._save()
            return res
        return wrapper

    def __iter__(self):
        self.current_index = 0
        self.keys = list(self.db.keys())
        return self

    def __next__(self):
        if self.current_index < len(self.keys):
            key = self.keys[self.current_index]
            self.current_index += 1
            return key
        raise StopIteration


    def _create_db(self):
        with open(self.path, "w") as f:
            json.dump(self.db, f)

    def _load(self):
        with open(self.path) as f:
            db = json.load(f)
            self.db = db

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.db, f, indent=6)

    @transaction
    def get(self, key):
        return self.db.get(key)

    @transaction
    def put(self, id, data):
        self.db[id] = data

        
