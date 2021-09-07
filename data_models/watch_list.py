class WatchListDM:
    def __init__(self, symbol:str = None, user_id:int = None) -> None:
        self.symbol = symbol
        self.user_id = user_id

    def set(self, data: dict) -> None:
        self.symbol = data.get('symbol')
        self.user_id = data.get('user_id')

    def __str__(self) -> str:
        return self.symbol
