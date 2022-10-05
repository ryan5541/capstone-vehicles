
from dash import html, Input, Output, State, callback
import dash_bootstrap_components as dbc






def pageHeader():
    #created to replace initial pageHeader function, uses navbar
    dropdown = dbc.DropdownMenu(
        children = [
            dbc.DropdownMenuItem(dbc.NavLink("Home", href="/")),
            dbc.DropdownMenuItem(dbc.NavLink("Past", href="/past1")),
            dbc.DropdownMenuItem(dbc.NavLink("Present", href='/present1')),
            dbc.DropdownMenuItem(dbc.NavLink("Future", href="/future"))
        ],
        align_end = False,
        nav = True,
        in_navbar = True,
        label = "Menu",
    )

    layout = dbc.Navbar(
        dbc.Container(
            [
                dbc.NavbarToggler(id='navbar-toggler1'),
                dbc.Collapse(
                    dbc.Nav(
                        [dropdown], navbar = True
                    ),
                    id = "navbar-collapse1",
                    navbar = True,
                    className = 'mx-auto'
                ),
                dbc.Container(
                [
                dbc.NavbarBrand("Automotive Industry", className = 'ms-auto'),
                ]),
                dbc.Container([dbc.CardHeader("Dennis Kelly, Ryan-Arnold Gamilo, Robert Stewart",
                 className = 'me-auto'),]),
            ]
            
        ),
       className = 'mb-5',
    )
    return layout



def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# the same function (toggle_navbar_collapse) is used in all three callbacks

callback(
    Output(f"navbar-collapse1", "is_open"),
    [Input(f"navbar-toggler1", "n_clicks")],
    [State(f"navbar-collapse1", "is_open")],
)(toggle_navbar_collapse)