from dash import Dash, Input, Output, State, callback, ctx, dcc, html
from OrderBook import OrderBook
from Simulation import simulate
from threading import Thread, Event


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
                            html.Div(children='Best Bid/Ask', style={'margin-top':'5px'}), # title
                            html.Div( # chart of the lists
                                children=[
                                    dcc.Textarea(id='best-ask', style={'margin-left':'2px', 'margin-right':'2px', 'width':'90%', 'height':'40%'})
                                ],
                                style={'height':'100%'}
                            )
                        ],
                        style={
                            'textAlign':'center',
                            'border':'2px solid black',
                            'borderRadius':'5px',
                            'height':'89vh',
                            'display':'flex',
                            'flexDirection':'column'
                    }),
                    html.Div( # graph of the market depth
                        children=[
                            html.Div('Depth Chart'),
                            dcc.Graph(id='depth-chart', style={'height':'90%'})
                        ],
                        style={
                            'textAlign':'center',
                            'border':'2px solid black',
                            'borderRadius':'5px',
                            'height':'89vh',
                    }),
                    html.Div( # right hand side, will include the transactions and ability to manually enter bids and asks
                        children=[
                            html.Div(
                                children='Transaction History',
                                style={
                                    'textAlign':'center',
                                    'border':'2px solid black',
                                    'borderRadius':'5px',
                                    'height':'33%',
                                }
                            ),
                            html.Div(
                                children='Manual Order',
                                style={
                                    'textAlign':'center',
                                    'border':'2px solid black',
                                    'borderRadius':'5px',
                                    'height':'33%',
                                    'margin-top':'5px'
                                }
                            ),
                            html.Div( # simulation start, stop, speed, aggression, etc.
                                children=[
                                    html.Div(
                                        children='Simulation'
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
                                    'height':'31.25%',
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
                    'gap':'5px'
                }
            )
        ],
    )
]

@callback(
    Output('start-button', 'children'),
    Output('start-button', 'n_clicks'),
    Input('start-button', 'n_clicks'),
    Input('stop-button', 'n_clicks')
)
def run_simulation(start_clicks: int, stop_clicks: int):
    global ob, thread # globalize these variables cause we're reinstantiating them

    if ctx.triggered_id == "start-button":
        if start_clicks > 1:
            if start_clicks % 2 == 0: # simulation will be paused
                resume_event.clear() # make it false so the while loop runs but it waits until we make this true meaning we resume the simulation
                return ('Resume', start_clicks)
            else: # simulation will be resumed
                resume_event.set() # make it true -> resume the program
                return ('Pause', start_clicks)
        elif start_clicks == 1: # simulation will be started
            # start the simulation by creating a new thread and start that every time
            ob = OrderBook() # create a new instance of orderbook since we're restarting simulation from the start
            thread = Thread(target=simulate, args=(ob,stop_event,resume_event)) # create a new thread with all the same stuff
            stop_event.clear() # make this false for while loop to work
            # have the set the flag first otherwise in the thread it will start off as false
            resume_event.set() # resume flag is true -> code will run
            thread.start() # start the simulation
            return ('Pause', start_clicks)
        elif start_clicks == 0: # base level
            # this will only ever be hit once at the start of the program
            return ('Start', start_clicks)
    elif ctx.triggered_id == "stop-button": # stop the simulation
        resume_event.set() # resume previous thread from suspended state if it had been so we can run that out
        stop_event.set() # stop event = true -> while loop fails; simulation stops
        return ('Start', 0)


    # nclicks = 0: nothing
    # nclicks = 1: sim started
    # nclicks = 2: sim paused
    # nclicks = 3: sim resumed



if __name__ == "__main__":
    app.run(debug=True, )
