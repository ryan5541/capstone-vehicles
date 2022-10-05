
from dash import html, dcc 
from dash.dependencies import Input, Output

#connects to app.py file
from app import app

#connect to specific page designs
from pages import present1, past1, home, future

#connect to the components folder
from components import pageHeader

nav = pageHeader.pageHeader()

app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    nav,
    html.Div(id = 'page-content', children=[])
])


@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return home.layout
    if pathname == '/past1':
        return past1.layout
    if pathname == '/present1':
        return present1.layout
    if pathname == '/future':
        return future.layout
    else:
        return "404 Page Error!"


if __name__ == '__main__':
    app.run_server(debug=False)