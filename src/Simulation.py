from datetime import datetime
import random
import time
from threading import Event

from OrderBook import OrderBook
from BuyOrSellEnum import BuyOrSell
from Order import Order

mid_price: float = 100 # base mid price
order_id = 0

name_list: list[str] = ['Techur', 'Tekur', 'Telur', 'Tefur', 'Tecur', 'Tequr', 'Tepur', 'Temur', 'Tehur', 'Tegur', 'Tedur', 'Tesur', 'Tewur', 'Tenur', 'Tebur']
order_output_list: list[str] = []

def simulate(orderbook: OrderBook, stop_event: Event, resume_event: Event, speed: float | None = None, aggressiveness: float | None = None):
    global mid_price, order_id, order_output_list # globalize mid price and order_ids
    order_output_list = []

    while not stop_event.is_set(): # since stop_event is false by default we have to get the opposite to run the simulation and when it's true we end it
        resume_event.wait() # if this is true the simulation will happen, if it isn't true then it'll just wait until it's true -> making a pause/resume feature

        # increment order_id by one to have a different id for each order
        order_id += 1
        # get the mid price and slightly change it to simulate market growth
        mid_price += random.gauss(0, .1)
        # randomly get whether buy or sell
        side: BuyOrSell = BuyOrSell.BUY if random.randint(0, 1) == 0 else BuyOrSell.SELL
        # average range is 5-20 with mean being 11.302 with some outliers - mu: 2.3 sigma: .5
        # to get more outliers (aggressive) increase sigma, decreasing will have the opposite effect
        volume = round(random.lognormvariate(mu=2.3, sigma=.5))

        # get a random number between 0-1.3 and add it subtract it based on if the order is a buy or sell
        offset_amount = random.uniform(0, .9)
        # make aggressive probability
        aggressive = random.randint(1,10) < 5 # aroudn 40 percent chance for an aggressive order (can change this around manually)

        if aggressive and orderbook._bestAsk and side == BuyOrSell.BUY: # order is a buy order so we want to match best ask price -> lowest price someone is willing to sell
            price = orderbook._bestAsk[0] # best price from orderbook
        elif aggressive and orderbook._bestBid and side == BuyOrSell.SELL: # order is a sell order so we want to match best bid price -> lowest price someone is willing to buy
            price = -orderbook._bestBid[0] # negate this since bestBid is in negatives
        else:
            price = mid_price-offset_amount if side == BuyOrSell.BUY else mid_price+offset_amount

        # make order
        o = Order(
            client=random.choice(name_list),
            timestamp=datetime.now(),
            orderID=order_id,
            price=price,
            side=side,
            volume=volume
        )

        # place order and print the output
        order_output = orderbook.PlaceOrder(o)

        if not order_output == "":
            order_output_list.append(order_output)

        # wait for a fraction of a second as to not overload the program
        time.sleep(.2)

    # order_output_list = []


def main():
    resume_event = Event()
    resume_event.set()
    simulate(OrderBook(), Event(), resume_event)
    pass

if __name__ == "__main__":
    main()
