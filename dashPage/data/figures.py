from data import config
#from config import *
import pymssql
import plotly.express as px
import pandas as pd

try:
    conn = pymssql.connect(server=config.server, user=f'{config.user}@{config.server}', 
        password=config.password, database=config.database)
    cursor = conn.cursor()
except Exception as e:
    print(e)


cars_sold = pd.read_sql('SELECT * FROM CarsSold2021',conn)
car_category = pd.read_sql('SELECT * FROM carCategory', conn)
car_subtype = pd.read_sql('SELECT * FROM carSubtype', conn)
car_features = pd.read_sql('SELECT * from carFeatures', conn)

merged = cars_sold.merge(car_features, 'inner', 'carFeaturesID')
merged = merged.merge(car_category, 'inner', 'carCategoryID')
merged = merged.merge(car_subtype, 'inner', 'carSubtypeID')
merged = merged.drop(columns = ['CarsSold2021ID', 'carCategoryID', 'carSubtypeID', 'carFeaturesID'])

category_sales = merged.groupby('category').sum()[['sales2021', 'sales2020']]
#category_sales


carSalesCat = px.bar(category_sales, x = category_sales.index, y = ['sales2020', 'sales2021'], 
    title='Car Sales by Car Category', labels={'value': 'Sales in Millions', 'category': 'Car Category'}, 
    barmode='group')

#figure 2 present
subtype_sales = merged.groupby('subtypeName').sum()[['sales2021', 'sales2020']].sort_values('sales2021')
carSalesSub = px.bar(subtype_sales, y = subtype_sales.index, x = ['sales2020', 'sales2021'], 
    labels={'value': 'Sales in Millions', 'subtypeName': 'Car Subtype'},
    title = 'Car Sales in Millions Split by Subtype', barmode='group', orientation = 'h')

#figure 3 present
largest = merged.nlargest(10, ['sales2021', 'sales2020'], 'all')
topTenCarSales = px.bar(largest, x = ['sales2020', 'sales2021'], y = 'carName',
    labels={'carName': 'Type of Car', 'value': 'Number of Sales'},
    title = 'Top Ten Total Car Sales by Type of Car', barmode='group', orientation='h')

#figure 4 present
brand_sales = merged.groupby('brand').sum()[['sales2021','sales2020']].nlargest(7, ['sales2020', 'sales2021'], 'all')
topFiveBrandSales = px.bar(brand_sales, x = brand_sales.index, y= ['sales2020', 'sales2021'],
    labels={'brand': 'Car Brand', 'value': 'Number of Sales'}, title = 'Car Sales Grouped by Brand',
    barmode = 'group')

#figure 5 present
subtype_mpg = merged.groupby('subtypeName').median()[['mpg']].sort_values('mpg')
mpgSubType = px.bar(subtype_mpg, x = 'mpg', y= subtype_mpg.index, barmode='group',
    labels={'subtypeName': 'Car Subtype', 'mpg': 'MPG'}, title='Miles per Gallon by Car Subtype', orientation='h')

#figure 6 present 
category_height = merged.groupby('category').mean()[['height']]
heightCar = px.bar(category_height, x = category_height.index, y = 'height',
labels={'height': 'Car Height in Inches', 'category': 'Car Category'}, title='Average Car Height')

#figure 7 present
engineDrive_count = merged.groupby(['engineDrive']).count()[['carName']].sort_values('carName')
engineDrive = px.bar(engineDrive_count, x = 'carName', y = engineDrive_count.index, orientation = 'h',
labels={'engineDrive': 'Car Engine Drive', 'carName': 'Number of Cars'}, title='Cars with Different Steering Types')

#engineDrive table
engineDriveTable_subtype = merged.groupby(['subtypeName', 'engineDrive']).count()[['carName']]

#engineDrive table 2
engineDriveTable_brand = merged.groupby(['brand', 'engineDrive']).count()[['carName']]

#correlation Matrix
cars = pd.get_dummies(merged, columns = ['engineDrive', 'brand', 'category', 'subtypeName'])
cars.drop(columns = ['carName', 'model', 'sub_segment'], inplace = True)
corr = cars.corr()
corr = corr[['sales2021']]
corr = corr.loc[abs(corr['sales2021']) > 0.15][1:]
corr = corr.to_dict()['sales2021']
corr2 = []

for key in corr.keys():
    corr2.append({key:corr[key]})

#dcc markdown.

#TimeSeries figures START!
query = """
SELECT *
FROM dbo.TimeSeries
"""

series_df = pd.read_sql(query, con=conn, index_col="date")
series_df = series_df.apply(pd.to_numeric)
sales_df = series_df.drop(columns="Gas Price")
sales_df.index = pd.to_datetime(sales_df.index)

salesOverTime = px.line(sales_df, x = sales_df.index, y = ['Domestic Autos', 'Domestic Light Trucks', 'Foreign Autos', 'Foreign Light Trucks', 'Heavy Trucks'],
title = 'Monthly Vehicle Sales Over Time')



category_sales = pd.DataFrame({})
category_sales['Autos'] = series_df['Domestic Autos'].copy() + series_df['Foreign Autos'].copy()
category_sales['Light Trucks'] = series_df['Domestic Light Trucks'].copy() + series_df['Foreign Light Trucks'].copy()
category_sales['Heavy Trucks'] = series_df['Heavy Trucks'].copy()
total_sales = category_sales.apply(sum, axis=1)

sales_delta = category_sales.pct_change()
total_sales_delta = total_sales.pct_change()
gas_price_delta = series_df['Gas Price'].pct_change().dropna().copy()
#print(gas_price_delta)
# Line these 3 up on the same set of indices
sales_delta = sales_delta.loc[gas_price_delta.index]
total_sales_delta = total_sales_delta.loc[gas_price_delta.index]

import statsmodels.api as sm
model = sm.OLS(total_sales_delta, sm.add_constant(gas_price_delta))
res = model.fit()
statsSummary = res.summary()


# Remaking above graph in plotly
omnibus_delta = pd.concat([gas_price_delta, sales_delta, res.fittedvalues], axis=1)
omnibus_delta.rename(columns={0:"Predicted"}, inplace=True)

import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Make scatterplot
fig2 = go.Figure()
for col in omnibus_delta.columns[1:-1]:
  X = 100*omnibus_delta['Gas Price'].values
  Y = 100*omnibus_delta[col].values
  fig2.add_trace(go.Scatter(x=X, y=Y, mode='markers', opacity=0.5, name=col))

# Add trendline
fig2 = fig2.add_trace(go.Scatter(x=100*omnibus_delta['Gas Price'], y=100*omnibus_delta['Predicted'], name="Predicted Change in Total Sales", mode='lines', line_color='#000000'))

fig2 = fig2.update_layout(
    title="Month-to-Month Percent Change in Vehicle Sales vs. Change in Gasoline Price",
    xaxis_title="Change in Gasoline Price (%)",
    yaxis_title="Percent Change in Vehicles Sold (%)"
    )

def getUpdatedData():
    streamData = pd.read_sql('SELECT * FROM DJUSAU ORDER BY time ASC', conn)
    streamData['time'] = pd.to_datetime(streamData['time'])
    newestPoint = streamData.tail(1)
    return newestPoint['price']

#Adding in commute time graphics.
car_query = """
SELECT [State], Vehicle, category
FROM dbo.State
LEFT JOIN dbo.CarsSold2021 sold ON Vehicle=carName
LEFT JOIN dbo.carCategory cat ON sold.carCategoryID=cat.carCategoryID
"""

state_best_sellers = pd.read_sql(car_query, con=conn)
# Need to clean this, for some reason
state_best_sellers.loc[state_best_sellers['Vehicle']=='Ford F-Series', 'category'] = 'Misc'
state_best_sellers.loc[state_best_sellers['Vehicle']=='Dodge Ram', 'category'] = 'Misc'
state_best_sellers.loc[state_best_sellers['Vehicle']=='Honda CR-V', 'category'] = 'SUV'

# Replace 'Misc' with 'Pickup'
state_best_sellers.loc[state_best_sellers['category']=='Misc', 'category'] = 'Pickup'

state_best_sellers['category'].value_counts()


# Get data on state commutes
commute_query = """
SELECT [State], NumWorkers, MeanTravelTime 
FROM dbo.StateCommutes sc
INNER JOIN dbo.State s ON sc.StateID=s.StateID
INNER JOIN dbo.CommuteMethod cm ON sc.CommuteMethodID=cm.CommuteMethodID
WHERE CommuteMethod='All Commuters'
"""

state_commutes = pd.read_sql(commute_query, conn)

# Will want to weight states by population in taking avg later, add CumulativeCommute column
state_commutes['Cumulative'] = state_commutes['NumWorkers']*state_commutes["MeanTravelTime"]

# Merge queries
merged_df = state_commutes.merge(state_best_sellers, how='inner', left_on='State', right_on='State')
visual_df = merged_df[['NumWorkers', 'Cumulative', 'category']].groupby(by='category').sum()


# Get population-weighted mean transit times
visual_df['Test'] = visual_df['Cumulative']/visual_df['NumWorkers']
visual_df.drop(columns=['NumWorkers', 'Cumulative'], inplace=True)

visual_df

#Visualize with Bar Graph
commuteTimes = px.bar(visual_df)
commuteTimes.update_layout(
    title='Grand Average of State Commute Times by Type of Best-Selling Car',
    xaxis_title="Type of Best-Selling Vehicle",
    yaxis_title='Avg. Commute Time',
    showlegend=False
)