from datetime import date, datetime
from BuyOrSellEnum import BuyOrSell

class Order:
    _orderID: int
    _timestamp: date
    _side: BuyOrSell
    _price: float
    _volume: int
    _client: str

    def __init__(self, orderID: int, timestamp: datetime, side: BuyOrSell, price: float, volume: int, client: str):
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

    # java to_string() function for python
    def __str__(self):
        return f"order_id: {self._orderID}, timestamp: {self._timestamp}, side: {self._side}, price: {self._price}, volume: {self._volume}, client: {self._client}"
