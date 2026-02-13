class FakeQuery:
    def __init__(self, storage):
        self._storage = storage

    def all(self):
        return list(self._storage.values())

class FakeSession:
    def __init__(self):
        self.added = []
        self.committed = False
        self.refreshed = []
        self.storage = {}
        self.model_storage = {}
        self.next_id = 1
        self.deleted = []

    def add(self, obj):
        self.added.append(obj)

    def flush(self):
        for obj in list(self.added):
            if getattr(obj, "id", None) is None:
                obj.id = self.next_id
                self.next_id += 1
            model_type = type(obj).__name__
            if model_type not in self.model_storage:
                self.model_storage[model_type] = {}
            self.model_storage[model_type][obj.id] = obj
            self.storage[obj.id] = obj

    def commit(self):
        self.committed = True

    def refresh(self, obj):
        if getattr(obj, "id", None) is None:
            obj.id = self.next_id
            self.next_id += 1
        model_type = type(obj).__name__
        if model_type not in self.model_storage:
            self.model_storage[model_type] = {}
        self.model_storage[model_type][obj.id] = obj
        self.storage[obj.id] = obj
        self.refreshed.append(obj)

    def get(self, model, id_):
        obj = self.storage.get(id_)
        return obj

    def query(self, model):
        model_type = model.__name__
        filtered_storage = self.model_storage.get(model_type, {})
        return FakeQuery(filtered_storage)

    def delete(self, obj):
        model_type = type(obj).__name__
        if getattr(obj, "id", None) in self.storage:
            del self.storage[obj.id]
            if model_type in self.model_storage and obj.id in self.model_storage[model_type]:
                del self.model_storage[model_type][obj.id]
            self.deleted.append(obj)
