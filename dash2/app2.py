#######
# Objective: build a dashboard that imports OldFaithful.csv
# from the data directory, and displays a scatterplot.
# The field names are:
# 'D' = date of recordings in month (in August),
# 'X' = duration of the current eruption in minutes (to nearest 0.1 minute),
# 'Y' = waiting time until the next eruption in minutes (to nearest minute).
######

# Perform imports here:
from flask import Flask
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

# Launch the application:
server = Flask(__name__)

app2 = dash.Dash(name='Bootstrap_docker_app',
                 server=server,
                url_base_pathname='/dash2/',
                csrf_protect=False)

# Create a DataFrame from the .csv file:
df = pd.read_csv('/tmp/data/OldFaithful.csv')

# Create a Dash layout that contains a Graph component:
app2.layout = html.Div([
    dcc.Graph(
    id='old_faithful',
    figure={
        'data': [
            go.Scatter(
                x = df['X'],
                y = df['Y'],
                mode = 'markers'
            )
        ],
        'layout': go.Layout(
            title = 'Old Faithful Eruption Intervals v Durations',
            xaxis = {'title': 'Duration of eruption (minutes)'},
            yaxis = {'title': 'Interval to next eruption (minutes)'},
            hovermode='closest'
        )
    } # close figure {}
    ),

    # add another graph
html.Div([
    dcc.Graph(
        id='old_faithful1',
        figure={
            'data': [
                go.Scatter(
                    x = df['X'],
                    y = df['Y'],
                    mode = 'markers'
                )
            ],
            'layout': go.Layout(
                title = 'Old Faithful Eruption Intervals v Durations',
                xaxis = {'title': 'Duration of eruption (minutes)'},
                yaxis = {'title': 'Interval to next eruption (minutes)'},
                hovermode='closest'
            ) # close layout ()
        } # close figure {}
    )
    ])
])

# Close Div ([ ])

# Add the server clause:
if __name__ == '__main__':
    app2.run_server()
