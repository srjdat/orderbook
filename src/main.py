from dash import Dash, Input, Output, State, callback, dcc, html

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
                            html.Div(children='techur'), # title
                            html.Div( # chart of the lists
                                children=[

                                ]
                            )
                        ],
                        style={
                            'textAlign':'center',
                            'border':'2px solid black',
                            'borderRadius':'5px',
                            'height':'89vh',
                    }),
                    html.Div( # graph of the market depth
                        children='Depth Chart',
                        style={
                            'textAlign':'center',
                            'border':'2px solid black',
                            'borderRadius':'5px',
                            'height':'89vh',
                    }),
                    html.Div( # right hand side, will include the transactions and ability to manually enter bids and asks
                        children=[
                            html.Div(
                                children='hello3',
                                style={
                                    'textAlign':'center',
                                    'border':'2px solid black',
                                    'borderRadius':'5px',
                                    'height':'44vh',
                                }
                            ),
                            html.Div(
                                children='hello4',
                                style={
                                    'textAlign':'center',
                                    'border':'2px solid black',
                                    'borderRadius':'5px',
                                    'height':'44vh',
                                    'margin-top':'5px'
                                }
                            ),
                        ]

                    ),
                ],
                style={
                    'display':'grid',
                    'grid-template-columns':'1fr 3fr 1fr',
                    'gap':'5px'
                }
            )
        ],
        style={

        }
    )
]

if __name__ == "__main__":
    app.run(debug=True)
