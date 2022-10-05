from dash import html, callback, Output, Input
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from data import figures
from skimage import io
import plotly.express as px

img = io.imread('./components/ML.png')
fig = px.imshow(img)
fig.update_layout(coloraxis_showscale = False)
fig.update_xaxes(showticklabels=False)
fig.update_yaxes(showticklabels=False)

layout = dbc.Container([
    dbc.Row(html.Center(dcc.Markdown("### Future"))),
    dbc.Row(dcc.Markdown('''Upon inspecting the past and the present, all that remains is to
    inspect the future.  We examine our machine learning model to see how well it functions with
    the time series data as it could become a potential path to predicting the state of the
    automotive market.  ''')),
    dbc.Row(dcc.Markdown("The current US Dow Jones value for the autmotive industry is: ")),  
    html.Div(id= 'LiveUpdate', children=[]),
    html.Br(),
    html.Br(),
    dbc.Row(dcc.Markdown('''#### Machine Learning, Sales Forecast: ''')),
    dcc.Interval(id = 'interval-component', interval = 60000, n_intervals=0),
    html.Div([dcc.Graph(figure=fig)]),
    dbc.Row(dcc.Markdown('''From what we see in the neural network modeling above, the model works very
    well before the recession, starts to waver between the recession and the pandemic,  and then starts to lose trakc of
    the story after the pandemic.  This was similar with the the other model we don't show.
    The pandemic completely threw off predictions and forced the market into such a wild state.  We think
    that after a bit more time, the market will steady out and go back to it's before pandemic pattern.'''))
])

@callback(Output('LiveUpdate', 'children'), Input('interval-component', 'n_intervals'))
def update_text(n):
    newValue = figures.getUpdatedData()
    return html.Center(html.H3(newValue))