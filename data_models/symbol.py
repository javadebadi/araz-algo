"""Data models for symbol table"""

class SymbolDM:
    def __init__(
        self,
        symbol:str = None,
        ):
        self.symbol = symbol

    def set(self, data: dict):
        self.symbol = data.get('symbol')

    def __str__(self) -> str:
        return self.symbol


class SymbolDMList:
    def __init__(self, values:list = None):
        self.collection = None
        if values is not None:
            self.set(values)

    def set(self, values: list):
        self.collection = []
        for value in values:
            symbol_obj = SymbolDM()
            symbol_obj.set(value)
            self.collection.append(symbol_obj)

    def to_list_of_values(self):
        return [vars(obj) for obj in self.collection]

    def __dict__(self):
        return [vars(obj) for obj in self.collection]

    def __str__(self) -> str:
        s = ""
        for dm_obj in self.collection:
            s += dm_obj.__str__()
        return s