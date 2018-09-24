#######
# First Milestone Project: Develop a Stock Ticker
# dashboard that either allows the user to enter
# a ticker symbol into an input box, or to select
# item(s) from a dropdown list, and uses pandas_datareader
# to look up and display stock data on a graph.
######

# EXPAND STOCK SYMBOL INPUT TO PERMIT MULTIPLE STOCK SELECTION
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import base64


from datetime import datetime
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web # requires v0.6.0 or later

app = dash.Dash(name='Bootstrap_docker_app',
                url_base_pathname='/dash/',
                csrf_protect=False)
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
nsdq = pd.read_csv('NASDAQcompanylist.csv')
nsdq.set_index('Symbol', inplace=True)
logo_image = '/Volumes/LaCie/thought-society-content/ThoughtSociety/logos/tslogo-ai-three-heads.png'

options = []
for tic in nsdq.index:
    options.append({'label':'{} {}'.format(tic,nsdq.loc[tic]['Name']), 'value':tic})

'''
    This code block builds a set of divs that consist of :
        1. H1 and H3 labels
        2. Drop-down component to select the stock
        3. Date range picker component
        4. Button to initiate the selection
        5. Graph object within the div
'''

def get_logo():
    encoded_image = base64.b64encode(open(logo_image, "rb").read())
    logo = html.Div(
        html.Img(
            src="data:image/png;base64,{}".format(encoded_image.decode()), height="57"
        ),
        style={"marginTop": "0"},
        className="sept columns",
    )
    return logo


app.layout = html.Div([
html.Div([ get_logo() ]),
html.H1('Stock Ticker Dashboard',style={'color':'rgb(201,76,76'}),

html.Div([
    html.H3('Select stock symbols:', style={'paddingRight':'30px','color':'rgb(0, 138, 230)'}),
    dcc.Dropdown(
        id='my_ticker_symbol',
        options=options,
        value=['TSLA'],
        multi=True
    )
], style={'display':'inline-block', 'verticalAlign':'top', 'width':'30%','padding-bottom':'10'}),
html.Div([
    html.H3('Select start and end dates:'),
    dcc.DatePickerRange(
        id='my_date_picker',
        min_date_allowed=datetime(2015, 1, 1),
        max_date_allowed=datetime.today(),
        start_date=datetime(2018, 1, 1),
        end_date=datetime.today(),

    )
], style={'display':'inline-block','padding-bottom':'10px','padding-left':'10'}),
html.Div([
    html.Button(
        id='submit-button',
        n_clicks=0,
        children='Submit',
        style={'fontSize':24, 'marginLeft':'30px'}
    ),
], style={'display':'inline-block'}),
dcc.Graph(
    id='my_graph',
    figure={
        'data': [
            {'x': [1,2], 'y': [3,1]},

        ]
    }, style = {'border':'2px blue solid'}
    # 'border':'2px','border-style': 'solid','color':'rgb(0, 138, 230)'
)
] )

@app.callback(
    Output('my_graph', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('my_ticker_symbol', 'value'),
    State('my_date_picker', 'start_date'),
    State('my_date_picker', 'end_date')])
def update_graph(n_clicks, stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')
    traces = []
    for tic in stock_ticker:
        df = web.DataReader(tic,'iex',start,end)
        traces.append({'x':df.index, 'y': df.close, 'name':tic})
    fig = {
        'data': traces,
        'layout': {'title':', '.join(stock_ticker)+' Closing Prices'}
    }
    return fig

if __name__ == '__main__':
    #app.run_server(ssl_context='adhoc')
    app.run_server()
