from datetime import date, datetime
import random
import time

from OrderBook import OrderBook
from BuyOrSellEnum import BuyOrSell
from Order import Order

mid_price: float = 100 # base mid price
order_id = 999

name_list: list[str] = ['Techur', 'Tekur', 'Telur', 'Tefur', 'Tecur', 'Tequr', 'Tepur', 'Temur', 'Tehur', 'Tegur', 'Tedur', 'Tesur', 'Tewur', 'Tenur', 'Tebur']

def simulate( ):
    global mid_price, order_id # globalize this price
    ob = OrderBook()

    while True:
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
        offset_amount = random.uniform(0, 1.3)

        # make order
        o = Order(
            client=random.choice(name_list),
            timestamp=datetime.now(),
            orderID=order_id,
            price=mid_price-offset_amount if side == BuyOrSell.BUY else mid_price+offset_amount,
            side=side,
            volume=volume
        )

        # place order and print the output
        order_output = ob.PlaceOrder(o)

        if not order_output == "":
            print(order_output)

        # sleep for 500 miliseconds as to not overload the program
        time.sleep(.2)


def main():
    simulate()

if __name__ == "__main__":
    simulate()
