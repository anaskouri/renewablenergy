from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output,State

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import renewable_statistics,hydro,wind,solar,electricity


# building the navigation bar
# https://github.com/facultyai/dash-bootstrap-components/blob/master/examples/advanced-component-usage/Navbars.py
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Renewable Energy", href="/apps/renewable_statistics"),
        dbc.DropdownMenuItem("Hydropower", href="/apps/hydro"),
        dbc.DropdownMenuItem("Wind Energy", href="/apps/wind"),
        dbc.DropdownMenuItem("Solar Energy", href="/apps/solar"),
        dbc.DropdownMenuItem("Electricity", href="/apps/electricity")



    ],
    nav = True,
    in_navbar = True,
    label = "Explore",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="/assets/renewable_energy.png", height="30px")),
                        dbc.Col(dbc.NavbarBrand("RENEWABLE ENERGY DASH", className="ml-2")),
                    ],
                    align="center",
                    #No_gutters=True,
                ),
                #href="/home",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    # right align dropdown menu with ml-auto className
                    [dropdown], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    className="mb-4",
)

def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

# embedding the navigation bar
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/renewable_statistics':
        return renewable_statistics.layout
    elif pathname == '/apps/hydro':
        return hydro.layout
    elif pathname == '/apps/wind':
        return wind.layout
    elif pathname == '/apps/solar':
        return solar.layout
    elif pathname == '/apps/electricity':
        return electricity.layout
    else:
        return renewable_statistics.layout



if __name__ == "__main__":
    app.run_server(debug=True)

