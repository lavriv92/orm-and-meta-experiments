from collections.abc import MutableMapping

import hazelcast


class HazelcastManager(MutableMapping):
    def __init__(self, rmap_name: str):
        self.client = hazelcast.HazelcastClient()
        self.rmap = self.client.get_replicated_map(rmap_name).blocking()

    def __setitem__(self, key: str, value):
        self.rmap.put(key, value)

    def __getitem__(self, key):
        return self.rmap.get(key)

    def __delitem__(self, key: str) -> None:
        return self.rmap.delete(key)

    def __len__(self) -> int:
        return len(self.rmap.values())

    def __iter__(self):
        return iter(self.rmap.entry_set())

    def __enter__(self):
        return self

    def __exit__(self):
        self.client.shutdown()


with HazelcastManager("my_map") as my_map:
    my_map["key"] = "value"
