from datetime import date
from BuyOrSellEnum import BuyOrSell

class Order:
    _orderID: int
    _timestamp: date
    _side: BuyOrSell
    _price: float
    _volume: int
    _client: str

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

    @property
    def client(self):
        return self._client