import time
from datetime import datetime
from kucoin.client import Client

from config import (
    API_SECRET,
    API_PASSPHRASE,
    API_KEY
)

class KucoinClient(Client):
    def __init__(self) -> None:
        super().__init__(API_KEY, API_SECRET, API_PASSPHRASE)