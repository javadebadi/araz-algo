class BaseDMList:

    def __init__(self):
        self.collection = []

    def append(self, obj):
        self.collection.append(obj)

    def reset(self):
        self.collection = []

    def set(self, values: list):
        self.reset()
        pass

    def to_list_of_values(self):
        return [vars(obj) for obj in self.collection]

    def __dict__(self):
        return [vars(obj) for obj in self.collection]

    def __str__(self) -> str:
        s = ""
        for dm_obj in self.collection:
            s += dm_obj.__str__()
        return s