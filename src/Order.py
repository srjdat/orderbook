from datetime import date
from BuyOrSellEnum import BuyOrSell

class Order:
    _orderID: int
    _timestamp: date
    _side: BuyOrSell
    _price: float
    _volume: int
    _client: str

    def __init__(self, orderID: int, timestamp: date, side: BuyOrSell, price: float, volume: int, client: str):
        self._orderID = orderID
        self._timestamp = timestamp
        self._side = side
        self._price = price
        self._volume = volume
        self._client = client

    # all the getters might make setters too
    @property
    def order_id(self):
        return self._orderID

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def side(self):
        return self._side

    @property
    def price(self):
        return self._price

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, volume):
        self._volume = volume

    @property
    def client(self):
        return self._client