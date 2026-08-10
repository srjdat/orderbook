from gc import disable

import plotly.graph_objects as go
import Simulation # won't trigger the entire file since we have the if __name__ == "__main__": block at the end

from dash import Dash, Input, Output, State, callback, ctx, dcc, html, dash_table
from OrderBook import OrderBook
from Simulation import simulate
from threading import Thread, Event
from BuyOrSellEnum import BuyOrSell

# make the orderbook and create the thread but don't start it
ob = OrderBook()
stop_event = Event() # initially false
resume_event = Event() # initially false
thread = Thread(target=simulate, args=(ob,stop_event,resume_event)) # create it in a thread so we don't interfere with the dash thread

app = Dash()

app.layout = [
    html.Div(
        children=[
            html.H1(children='Order Book', style={'textAlign':'center'}),
            html.Div(
                # make three columns
                children=[ # list of bid and ask prices
                    html.Div(
                        children=[
                            html.Div(children='Market Depth', style={'margin-top':'5px', 'margin-bottom':'5px'}), # title
                            html.Div( # chart of the lists
                                children=[
                                    dash_table.DataTable( # ask table
                                        id='depth-table',
                                        data=[],
                                        style_cell={
                                            'textAlign':'center',
                                            'padding':'0px 12px'   # top/bottom 0, left/right 12px
                                        },
                                    )
                                ],
                                style={'height':'100%', 'margin-left':'5px', 'margin-right':'5px'}
                            )
                        ],
                        style={
                            'textAlign':'center',
                            'border':'2px solid black',
                            'borderRadius':'5px',
                            'height':'100%',
                            'display':'flex',
                            'flexDirection':'column',
                    }),
                    html.Div( # graph of the market depth
                        children=[
                            html.Div('Cumulative Depth', style={'margin-top':'5px'}),
                            html.Div(children='', style={'margin-y':'5px'}, id='mid-price'),
                            dcc.Interval(id='interval-tick', interval=200, n_intervals=0), # refresh interval is the same speed as the simulation speed
                            dcc.Graph(id='depth-chart', style={'height':'90%'}),
                        ],
                        style={
                            'textAlign':'center',
                            'border':'2px solid black',
                            'borderRadius':'5px',
                            'height':'100%',
                    }),
                    html.Div( # right hand side, will include the transactions and start and stop
                        children=[
                            html.Div(
                                children=[
                                    html.Div(
                                        'Transaction History',
                                        style={
                                        'margin-top':'5px',
                                        'margin-bottom':'5px'
                                    }),
                                    dcc.Textarea(id='transactions',
                                        style={'margin-left':'2px', 'margin-right':'2px', 'width':'95%', 'height':'95%'},
                                        value="",
                                        disabled=True
                                    )
                                ],
                                style={
                                    'textAlign':'center',
                                    'border':'2px solid black',
                                    'borderRadius':'5px',
                                    'height':'86%',
                                }
                            ),
                            html.Div( # simulation start, stop, speed, aggression, etc.
                                children=[
                                    html.Div(
                                        children='Simulation',
                                        style={
                                            'margin-top':'5px',
                                            'margin-bottom':'5px'
                                        }
                                    ),
                                    dcc.Button(
                                        id='start-button',
                                        n_clicks=0,
                                        children='Start',
                                        style={
                                            'margin-right':'5px',
                                            'width':'47.5%'
                                        }
                                    ),
                                    dcc.Button(
                                        id='stop-button',
                                        n_clicks=0,
                                        children='Stop',
                                        style={
                                            'width':'47.5%'
                                        }
                                    )
                                ],
                                style={
                                    'textAlign':'center',
                                    'border':'2px solid black',
                                    'borderRadius':'5px',
                                    'height':'13%',
                                    'margin-top':'5px'
                                }
                            ),
                        ],
                        style={
                            'height':'100%'
                        }
                    ),
                ],
                style={
                    'display':'grid',
                    'grid-template-columns':'1fr 3fr 1fr',
                    'gap':'5px',
                    'height':'100%'
                }
            )
        ],
        style={
            'height':'89vh'
        }
    )
]

@callback(
    Output('start-button', 'children'),
    Output('start-button', 'n_clicks'),
    Output('transactions', 'value', allow_duplicate=True),
    Input('start-button', 'n_clicks'),
    Input('stop-button', 'n_clicks'),
    State('transactions', 'value'),
    prevent_initial_call = True
)
def run_simulation(start_clicks: int, stop_clicks: int,  transaction_str: str):
    global ob, thread # globalize these variables cause we're reinstantiating them

    if ctx.triggered_id == "start-button":
        if start_clicks > 1:
            if start_clicks % 2 == 0: # simulation will be paused
                resume_event.clear() # make it false so the while loop runs but it waits until we make this true meaning we resume the simulation
                return ('Resume', start_clicks, transaction_str)
            else: # simulation will be resumed
                resume_event.set() # make it true -> resume the program
                return ('Pause', start_clicks, transaction_str)
        elif start_clicks == 1: # simulation will be started
            # start the simulation by creating a new thread and start that every time
            ob = OrderBook() # create a new instance of orderbook since we're restarting simulation from the start
            thread = Thread(target=simulate, args=(ob,stop_event,resume_event)) # create a new thread with all the same stuff
            stop_event.clear() # make this false for while loop to work
            # have the set the flag first otherwise in the thread it will start off as false
            resume_event.set() # resume flag is true -> code will run
            thread.start() # start the simulation
            return ('Pause', start_clicks, "")
        elif start_clicks == 0: # base level
            # this will only ever be hit once at the start of the program
            return ('Start', start_clicks, "")
    elif ctx.triggered_id == "stop-button": # stop the simulation
        resume_event.set() # resume previous thread from suspended state if it had been so we can run that out
        stop_event.set() # stop event = true -> while loop fails; simulation stops
        return ('Start', 0, "")

    # nclicks = 0: nothing
    # nclicks = 1: sim started
    # nclicks = 2: sim paused
    # nclicks = 3: sim resumed

@callback(
    Output('depth-chart', 'figure'),
    Output('mid-price', 'children'),
    Output('transactions', 'value'),
    Output('depth-table', 'data'),
    Input('interval-tick', 'n_intervals'),
)
def refresh_display(n):
    global ob, book_mid_price

    # book mid price
    bid_list = sorted([-item for item in ob._bestBid], reverse=True) # descending order
    ask_list = sorted(ob._bestAsk) # ascending order

    if bid_list and ask_list:
        for price in bid_list: # get the highest bid price
            volume = ob._volumeMap.get((price, BuyOrSell.BUY))
            if volume is not None:
                highest_bid = price
                break
        for price in ask_list: # get the lowers ask price
            volume = ob._volumeMap.get((price, BuyOrSell.SELL))
            if volume is not None:
                lowest_ask = price
                break

        book_mid_price = (highest_bid + lowest_ask) / 2 # if they both exist calculate the book mid price # type: ignore (what i'm doing here is bad practice to just ignore the unbound property of this but it's going to be bound to something )
    else:
        book_mid_price = Simulation.mid_price # if they don't exist fall back to the underlying price that i make the trades around

    # transactions
    length = min(40, len(Simulation.order_output_list))
    order_output_str = ""
    lines = reversed([Simulation.order_output_list[i] for i in range(-length, 0, 1)]) # get list of lines
    order_output_str = "\n".join(lines) # join the lines with a new line between them

    return (build_cumulative_depth_chart(ob), f"mid {round(book_mid_price, 2)}", order_output_str, built_depth_table(ob))

def built_depth_table(ob: OrderBook):
    # bid price ask
    #     100   2
    #     99    3
    #     0.5
    # 2   98
    # 3   99

    bid_list = sorted([-item for item in ob._bestBid], reverse=True) # ascending order
    ask_list = sorted(ob._bestAsk) # descending order

    display_bid_list = [] # ascending
    display_bid_volume = []
    display_ask_list = [] # descending
    display_ask_volume = []

    i = 0
    for price in bid_list:
        if i == 10: break
        else:
            # check if this is stale price or not
            if ob._volumeMap.get((price, BuyOrSell.BUY)) is not None:
                display_bid_list.append(price)
                display_bid_volume.append(ob._volumeMap.get((price, BuyOrSell.BUY)))
                i += 1 # increment

    i = 0 # reset
    for price in ask_list:
        if i == 10: break
        else:
            # check if stale price
            if ob._volumeMap.get((price, BuyOrSell.SELL)) is not None:
                display_ask_list.append(price)
                display_ask_volume.append(ob._volumeMap.get((price, BuyOrSell.SELL)))
                i += 1 # increment

    display_ask_list = display_ask_list[::-1]
    display_ask_volume = display_ask_volume[::-1]

    if display_bid_list and display_ask_list:
        spread_val: float =display_ask_list[-1] - display_bid_list[0]
    else: spread_val = 0.0

    ask_rows = []
    bid_rows = []
    spread_row = []

    for price, volume in zip(display_ask_list, display_ask_volume):
        ask_rows.append({'bid_size':None, 'price':round(price,2), 'ask_size':volume})
    for price, volume, in zip(display_bid_list, display_bid_volume):
        bid_rows.append({'bid_size':volume, 'price':round(price,2), 'ask_size':None})
    spread_row = {'bid_size':'-', 'price':round(spread_val, 3), 'ask_size':'-'}

    rows = ask_rows + [spread_row] + bid_rows

    return rows

def build_cumulative_depth_chart(ob: OrderBook):

    # get bid and ask lists
    bid_list = sorted([-item for item in ob._bestBid], reverse=True) # reverse because this is going on the left
    ask_list = sorted(ob._bestAsk)

    # get cumulative depth
    bid_cumulative_list = []
    curr_vol = 0
    for price in bid_list: # bid cumulative depth
        volume = ob._volumeMap.get((price, BuyOrSell.BUY))
        if volume is None:
            continue  # no volume for this price
        curr_vol += volume
        bid_cumulative_list.append(curr_vol)
    curr_vol = 0 # set it back to 0
    ask_cumulative_list = []
    for price in ask_list: # ask cumulative depth
        volume = ob._volumeMap.get((price, BuyOrSell.SELL))
        if volume is None:
            continue  # no volume for this price
        curr_vol += volume
        ask_cumulative_list.append(curr_vol)

    # build final figure
    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=bid_list,
            y=bid_cumulative_list,
            fill='tozeroy',
            line_shape='hv',
            line_color='green',
            name='Bids'
        ),
    )
    figure.add_trace(
        go.Scatter(
            x=ask_list,
            y=ask_cumulative_list,
            fill='tozeroy',
            line_shape='hv',
            line_color='red',
            name='Asks'
        ),
    )
    figure.add_vline(
        x=book_mid_price,
        line_width=2,
        line_dash="dash",
    )


    # keep mid_price at the middle of the graph
    # get cheapest bid price
    bid_window, ask_window = .5, .5
    if bid_list:
        for price in reversed(bid_list): # have to reverse it because it's in descending order right now and we want the smallest value here
            volume = ob._volumeMap.get((price, BuyOrSell.BUY)) # check if it's stale price
            if volume is not None:
                bid_window = max(.5, book_mid_price - price) # last one is the smallest
                break
    # get largest ask price
    if ask_list:
        for price in reversed(ask_list): # have to reverse it because it is in ascending order and we want the largest value here
            volume = ob._volumeMap.get((price, BuyOrSell.SELL)) # check if it's stale price
            if volume is not None:
                ask_window = max(.5, price - book_mid_price) # last one is the smallest
                break

    window = max(ask_window, bid_window) # get max of the two to keep mid price at the middle and not moving around
    figure.update_xaxes(range=[book_mid_price - window, book_mid_price + window])

    return figure


if __name__ == "__main__":
    app.run(debug=True, )
