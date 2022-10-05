from dash import html, dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from data import figures



layout = dbc.Container([
    dbc.Row([
        html.Center(dcc.Markdown("### Present"))
    ]),
    dbc.Row([dcc.Markdown('''As the autmotive industry continues to change, we took the
    time time to look at what is the current landscape of the market.  What features are
    most prevalent?  ''')]),
    dbc.Row([dcc.Markdown('''In the first three graphs below we examined the popularity of
    different types of cars in 2020 and 2021 judged by their number of sales.''')]),
    dcc.Graph(id = 'CarsBarGraph', figure = figures.carSalesCat),
    dbc.Row([dcc.Markdown('''We note that despite the covid-19 pandemic occuring in early 2020
    , the car sales decreased in 2021.''')]),
    dcc.Graph(id = 'SubtypeCarSales', figure = figures.carSalesSub),
    dbc.Row([dcc.Markdown('''Drilling down into the data a little, we see that the 
    large pickups and the midsized cars are the only two categories in which there
    is an increase in sales in 2021.''')]),
    dcc.Graph(id = 'TopTenCarsSold', figure= figures.topTenCarSales),
    dbc.Row([dcc.Markdown('''Here, we drill down one last time to inspect specifically which car
    sold the best in 2021.  We can see things that we would expect, like the Chevrolet Silerado
    and the Ford F Series indicating the increase in large pickups we saw in the previous graph.
    We also find the Chevrolet Equinox demonstrating a large increase in sales in 2021.  This
    is particuarly seperate from the data before since the Equinox is a type of SUV.  Since it is 
    showing such a large increase in sales despite the overall drop in sales, if you are looking for
    a SUV of some sort, the Equinox may be a good place to start looking.  We do note that as the
    graphic's title implies, this is only the top 10 cars in terms of overall sales.''')]),
    dcc.Graph(id = 'BrandCarsSold', figure = figures.topFiveBrandSales),
    dbc.Row([dcc.Markdown('''We also took a quick look at the number of sales divided up by the top seven
    car brands. Where we can see that as we've seen so far, Ford and Chevrolet are on an upwards trend.''')]),
    dcc.Graph(id = 'SubtypeMPG', figure = figures.mpgSubType),
    dcc.Graph(id = 'CarHeight', figure = figures.heightCar),
    dcc.Graph(id = 'EngineDrive', figure = figures.engineDrive),
    dbc.Row(dcc.Markdown('''Finally, we show some distribution of common car freatures.  Knowing this, it 
    is natural to wonder if we can try and learn what features may correlate with sales of cars in 2021. 
    When we examined a correlation matrix, we looked at all values with an absolute value greater than .15.
    We found that length (.15575), height (.224801), brand_ford (.165703), brand_ram (.185817), and large pickups
    (.505166) indicated a correlation.  The most insightful correlation here was that there was a correlation
    between the length and height of the car sales in 2021. Some notable ones slightly below our .15 cut off
    were, mpg at .117514.''')),
    html.Br(),
    dcc.Graph(id = 'CommuteTimes', figure = figures.commuteTimes),
    dbc.Row(dcc.Markdown('''We take a second to consider another cause of the change in car sales.
    This graph seems to imply that those who have a lower average commute time own a truck of some sort, and that
    cars and SUVs have significantly higher commute times than pickup trucks.  We think that this line of thought
    could be a useful avenue of future research.'''))
])
