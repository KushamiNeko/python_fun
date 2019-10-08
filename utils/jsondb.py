import json
import os
from typing import Dict, List, Optional


class JsonDB:
    def __init__(self, database_root: str):

        assert database_root != ""
        assert os.path.exists(database_root)

        self._database_root = database_root

        self._database: List[Dict[str, str]] = []

    def _read(self, database: str, collection: str) -> None:
        path = os.path.join(self._database_root, f"{database}_{collection}.json")

        if os.path.exists(path):
            with open(path, "r") as f:
                self._database = json.load(f)

    def _write(self, database: str, collection: str) -> None:
        path = os.path.join(self._database_root, f"{database}_{collection}.json")

        with open(path, "w") as f:
            json.dump(self._database, f, indent=2)

    def insert(self, database: str, collection: str, *entities: Dict[str, str]) -> None:
        self._read(database, collection)
        self._database.extend(entities)
        self._write(database, collection)

    def replace(
        self,
        database: str,
        collection: str,
        query: Dict[str, str],
        new_entity: Dict[str, str],
    ) -> None:

        assert query is not None
        assert len(query.keys()) is not None

        assert new_entity is not None
        assert len(new_entity.keys()) is not None

        self._read(database, collection)

        found = True

        for i, entity in enumerate(self._database):
            for k, v in query.items():
                found = found and (entity.get(k, None) == v)
            if found:
                self._database[i] = new_entity
                break

        self._write(database, collection)

    def find(
        self, database: str, collection: str, query: Dict[str, str]
    ) -> Optional[List[Dict[str, str]]]:

        assert query is not None
        assert len(query.keys()) is not None

        self._read(database, collection)

        entities = []

        for entity in self._database:
            found = True
            for k, v in query.items():
                found = found and (entity.get(k, None) == v)
            if found:
                entities.append(entity)

        if entities:
            return entities
        else:
            return None

    def delete(self, database: str, collection: str, query: Dict[str, str]) -> None:

        assert query is not None
        assert len(query.keys()) is not None

        self._read(database, collection)

        for i, entity in enumerate(self._database):
            found = True
            for k, v in query.items():
                found = found and (entity.get(k, None) == v)

            if found:
                del self._database[i]
                break

        self._write(database, collection)

    def drop_collection(self, database: str, collection: str) -> None:
        path = os.path.join(self._database_root, f"{database}_{collection}.json")
        os.remove(path)
