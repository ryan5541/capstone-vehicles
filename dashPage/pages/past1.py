from dash import html, callback, Output, Input
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from data import figures


layout = dbc.Container([
    dbc.Row(html.Center(dcc.Markdown('''### Past'''))),
    dbc.Row(dcc.Markdown('''History repeats itself.  The past is a wealth of information
    that can allow us to gather insight on the present and the future.  Here we inspect some
    of the trends of the past.''')),
    dcc.Graph(id = 'PastItem', figure = figures.salesOverTime),
    dbc.Row(dcc.Markdown('''There are a couple of interesting things to note here in this graph.  Firstly,
    Domestic Autos have a structural decline throughout the years and Light Trucks are having a structural increase.
    This is true throughout out all three key time periods, before the 2008 recession, between the recession and the pandemic
    , and after the pandemic.''')),
    dcc.Graph(id = 'Panic', figure = figures.fig2),
    dbc.Row(dcc.Markdown('''Unexpectedly, we found a positive association between vehicle sales and gas price. We expect that
    this is a cause of confounding variables.  Even if it wasn't, the relation is realistically impractical since the one
    percent increase in gas price corresponds to a point one percent increase in total car sales.'''))
])  