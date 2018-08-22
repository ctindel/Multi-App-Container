from flask import Flask
import dash
import dash_core_components as dcc
import dash_html_components as html

server = Flask(__name__)

app1 = dash.Dash(name='Bootstrap_docker_app',
                server=server,
                url_base_pathname='/dash2/', # Reference to the app for creating a path to it
                csrf_protect=False)

colors = {
    'background': '#444547',
    'text': '#ffffff'
}

app1.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Test 1',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Dash: A Dashboard Visualization Framework for Python', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='example-graph-2',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                {'x': [1, 2, 3], 'y': [5, 3, 1], 'type': 'bar', 'name': u'New York'},
                {'x': [1, 2, 3], 'y': [5, 4, 3], 'type': 'bar', 'name': u'Portland'},
            ],
            'layout': {

                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    )
])

if __name__ == '__main__':
    app1.run_server(debug=True)
