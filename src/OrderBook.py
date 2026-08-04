from queue import PriorityQueue
from typing import List

from Order import Order
from BuyOrSellEnum import BuyOrSell
import heapq

class OrderBook:
    _bestAsk: List[tuple[float, int]]
    _bestBid: List[tuple[float, int]] # im not sure yet how i'm going to deal with this
    _orderMap: dict[int, Order]
    _volumeMap: dict[tuple[float, BuyOrSell], int]
    _queueMap: dict[tuple[float, BuyOrSell], PriorityQueue]

    def __init__(self):
        pass

    def __init__(self, bestAsk, bestBid, orderMap, volumeMap, queueMap):
        pass

    def PlaceOrder(self, order: Order):
        pass

    def CancelOrder(self, orderID: int):
        pass

    def VolumeAtPrice(self, price: float, BuyingOrSelling: BuyOrSell):
        pass