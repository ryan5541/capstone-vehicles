from dash import html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from skimage import io
import plotly.express as px

img = io.imread('./components/car.jpg')
fig = px.imshow(img)
fig.update_layout(coloraxis_showscale = False)
fig.update_xaxes(showticklabels=False)
fig.update_yaxes(showticklabels=False)


layout = dbc.Container([
    dcc.Markdown('''As it did in many other industries, the COVID-19 Pandemic caused immense disruption in the automotive industry: reducing sales, straining supply-chains, and casting great uncertainty over almost every facet of the business. Even so, automotive manufacturers must still make decisions about the kinds of vehicles to sell, and produce forecasts of future sales for the purpose of managing supply-chains. Moreover, if these decisions and forecasts are going to be reliable, they have to be reached in a principled and quantitatively rigorous way.

Our group adopts a data-driven approach to these questions. We examine historical data to discern the presence of any long-term trends in vehicle sales, as well as any possible associations between sales and external factors such as the price of gasoline. We then look at sales data from 2020 and 2021, to see which car types and which features are most strongly associated with present sales. Taking note of variability between U.S. states in the type of best-selling car, we investigate if this variability is related to differences in the average commute between states. Finally, we look toward the future, assessing the feasibility of using machine learning to produce monthly sales forecasts.
'''),
    dcc.Markdown("Use the menu in the top left to navigate the site and examine the various aspects of the Automotive Industry."),
    html.Div([dcc.Graph(figure=fig)])
    ]
)