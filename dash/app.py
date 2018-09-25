

# simple stock comparitor
from flask import Flask
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

from datetime import datetime
import pandas as pd
import numpy as np
pd.core.common.is_list_like = pd.api.types.is_list_like
# import pandas_datareader.data as web # requires v0.6.0 or later


server = Flask(__name__)

app = dash.Dash(name='Bootstrap_docker_app',
                 server=server,
                url_base_pathname='/dash/',
                csrf_protect=False)

text_color = 'rgb(36,36,36)'
bg_color = 'rgb(255,255,255)'
grid_color = '#666666'
black_text = '#000000'

# Get Chryddyp's CSS for Dash from Codepen

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
#app.css.append_css({'/Users/salvideoguy/static/reset.css'})

# get four excel datafiles - 1 for DJIA and the other for Nasdaq Tech Sector

djia = pd.read_excel('../data/djia.xls')
ndxt = pd.read_excel('../data/ndxt.xls')
ixic = pd.read_csv('../data/ixic.csv')
gspc = pd.read_csv('../data/gspc.csv')

last_year = 2018
first_year = 2006

# Prepare a clean list of integer years from mkt_Index
# Return the list

def clean_mkt_index(mkt_Index):
    yrstr = []
    year_list = []  # holding unique year strings
    nyear = []

    for rawdatestr in mkt_Index['Date']:
        yrstr.append(rawdatestr[0:4]) # extract date info for all dates
    for years in np.unique(yrstr): # get unique date info by year
        year_list.append(years)
    del year_list[-1] # strip the last string which is invalid
    for nyr in year_list:
        nyear.append(int(nyr))
    return nyear

year_index = clean_mkt_index(djia) # integer years
year_index_strings = [str(item) for item in year_index] # year strings

options = []
i = 0

for year in year_index_strings:
    options.append({'label':'{}'.format(year),'value':year_index[i]})
    i+=1

#for tic in nsdq.index:
#    options.append({'label':'{} {}'.format(tic,nsdq.loc[tic]['Name']), 'value':tic})


app.layout=html.Div([   # top,rt,bot,lft

    html.H2('Market Trends Over a Dozen Years',style={'width':'99.999%','color':'black',
        'text-align':'center','background-color':bg_color ,
            'margin-bottom': '0px','padding':'10px 0px 0px 0px'}
                                                         # 'padding':'10px 0px 100px 0px'})
            ),

    # combi-plots with dropdown

    html.Div([

    dcc.Graph(id='djia_id'), # djia graph

    #dcc.Dropdown(
    #            id='yr_selector_dd',
    #            options=options,
    #            value='2006'
    #            ),


    dcc.Graph(id='ndxt_id'), # ndxt graph
    ],style={'display':'inline-block','width':'33.333%'},
    ),

    html.Div ([
    dcc.Graph(id='djiaII_id'), # djia graph
    dcc.Graph(id='gspc_id'), # ndxt graph
    ],style={'display':'inline-block','width':'33.333%'}
    ),

    html.Div ([
    dcc.Graph(id='ixic2_id'), # djia graph
    dcc.Graph(id='gspc2_id'), # ndxt graph
    ],style={'display':'inline-block','width':'33.333%'}
    ),

    html.Div(dcc.Slider(  # The years range slider
                id='years-range-slider',
                min=2006,
                max=2018,
                value=2018,
                step=2,
                marks= {i: '{}'.format(i) for i in year_index},

            ), style={'color':'red','width': '95%', 'margin-top': '0px',
                      'padding':'30px 38px 30px 30px', # top,rt,bot,lft
                      'background-color':bg_color}
        )

], style={'width': '99.999%','display': 'inline','font': {'color':text_color},
          'padding':'0px 0px 60px 0px','background-color':bg_color,
          'margin-bottom': '0px'}

)

#### Callbacks

# trace all the closing values from year.min to selected max.year using the 'value' (highest year)
# reshape the array in a temporary array and run it to the end.

@app.callback( # Stock # 1 - DJIA
    Output('djia_id', 'figure'),
    [Input('years-range-slider', 'value')])
def update_stock_graph(value):

    # print (value)

    # original cutoff for the slider
    # cutoff = (value - first_year) * 12

    '''
    To use the dropdown, produce a slice range that grabs just the rows 
    from the selected year and copies it into the f_djia df
    each date has 12 rows of data - 1 for each month
    To set a lower and upper mask to slice the df, it is the first row of the chosen date +12
    
    value = integer year.  years go from 2006 - 2018 or 6-18.  This is essentially a range of 12 years.
    For 12 months.  So the index range is 0-143.  If the selected year is 2010
    
    
    '''

    #year_val = (int(value) - 2005) - 1
    #year_end = year_val + 12


    traces = []
    cutoff = (value - first_year) * 12

    f_djia = djia[0:cutoff]
    f_ndxt = ndxt[0:cutoff]
    f_ixic = ixic[0:cutoff]
    f_gspc = gspc[0:cutoff]

    #f_djia = djia[year_val:year_end]
    #f_ndxt = ndxt[year_val:year_end]
    #f_ixic = ixic[year_val:year_end]
    #f_gspc = gspc[year_val:year_end]



    traces.append({'x': f_djia['Date'], 'y': f_djia['Close'], 'name': 'djia'}),
    traces.append({'x': f_ndxt['Date'], 'y': f_ndxt['Close'], 'name': 'ndxt'}),
    traces.append({'x': f_ixic['Date'], 'y': f_ixic['Close'], 'name': 'ixic'}),
    traces.append({'x': f_gspc['Date'], 'y': f_gspc['Close'], 'name':'gspc'}),

    fig = {
        'data': traces,
        'layout': {'title':'DJIA, NDXT, NASDAQ, S&P Closings',
                   'paper_bgcolor':bg_color,'plot_bgcolor':bg_color,
                   'font': {'color':text_color},
                   'xaxis':{'gridcolor':grid_color,'range':[cutoff-first_year],'step':1},
                   'yaxis': {'gridcolor': grid_color}

    }
    }
    return fig


@app.callback( # Stock #2 NDXT
    Output('ndxt_id', 'figure'),
    [Input('years-range-slider', 'value')])
def update_stock_graph(value):

    traces = []
    cutoff = (value - first_year) * 12
    f_ndxt = ndxt[0:cutoff]

    traces.append({'x': f_ndxt['Date'], 'y': f_ndxt['Close'], 'name': 'ndxt'}),

    fig = {
        'data': traces,
        'layout': {'title':'Nasdaq Tech Sector Closing Price',
                   'paper_bgcolor':bg_color,'plot_bgcolor':bg_color,'font': {'color':text_color},
                   'xaxis': {'gridcolor': grid_color},
                   'yaxis': {'gridcolor': grid_color}
                   }
    }
    return fig

@app.callback( # Stock #3 IXIC
    Output('djiaII_id', 'figure'),
    [Input('years-range-slider', 'value')])
def update_stock_graph(value):

    traces = []
    cutoff = (value - first_year) * 12
    f_djia = djia[0:cutoff]

    traces.append({'x': f_djia['Date'], 'y': f_djia['Close'], 'name': 'djia'}),

    fig = {
        'data': traces,
        'layout': {'title':'Djia Closing Price',
                   'paper_bgcolor':bg_color,'plot_bgcolor':bg_color,'font': {'color':text_color},
                   'xaxis': {'gridcolor': grid_color},
                   'yaxis': {'gridcolor': grid_color}
                   }
    }
    return fig

@app.callback( # Stock #4 GSPC
    Output('gspc_id', 'figure'),
    [Input('years-range-slider', 'value')])
def update_stock_graph(value):

    traces = []
    cutoff = (value - first_year) * 12
    f_gspc = gspc[0:cutoff]

    traces.append({'x': f_gspc['Date'], 'y': f_gspc['Close'], 'name': 'gspc'})
    fig = {
        'data': traces,
        'layout': {'title':'S&P 500 Closing Price',
                   'paper_bgcolor':bg_color,'plot_bgcolor':bg_color,'font': {'color':text_color},
                   'xaxis': {'gridcolor': grid_color},
                   'yaxis': {'gridcolor': grid_color}
                   }
    }
    return fig

@app.callback( # Stock #3 IXIC
    Output('ixic2_id', 'figure'),
    [Input('years-range-slider', 'value')])
def update_stock_graph(value):

    traces = []
    cutoff = (value - first_year) * 12
    f_ixic = ixic[0:cutoff]

    traces.append({'x': f_ixic['Date'], 'y': f_ixic['Close'], 'name': 'ixic2'}),

    fig = {
        'data': traces,
        'layout': {'title':'Nasdaq-100 Closing Price',
                   'paper_bgcolor':bg_color,'plot_bgcolor':bg_color,'font': {'color':text_color},
                   'xaxis': {'gridcolor': grid_color},
                   'yaxis': {'gridcolor': grid_color}
                   }
    }
    return fig

@app.callback( # Stock #4 GSPC
    Output('gspc2_id', 'figure'),
    [Input('years-range-slider', 'value')])
def update_stock_graph(value):

    traces = []
    cutoff = (value - first_year) * 12
    f_gspc = gspc[0:cutoff]

    traces.append({'x': f_gspc['Date'], 'y': f_gspc['Close'], 'name': 'gspc2'})
    fig = {
        'data': traces,
        'layout': {'title':'S&P 500 Closing Price',
                   'paper_bgcolor':bg_color,'plot_bgcolor':bg_color,'font': {'color':text_color},
                   'xaxis': {'gridcolor': grid_color},
                   'yaxis': {'gridcolor': grid_color}
                   }
    }
    return fig


if __name__ == '__main__':
    #app.run_server(ssl_context='adhoc')
    app.run_server()
