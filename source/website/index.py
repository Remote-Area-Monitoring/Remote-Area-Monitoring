from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from app import app
from map import Map
from subprocess import check_output
import socket
from flask import request
from source.util.database import Database
from source.util.timekeeper import Timestamps
from source.website.pages import home, map_example


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home Page", href="/home")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Dev Tools", header=True),
                dbc.DropdownMenuItem("Map Test", href="/map-example"),
            ],
            nav=True,
            in_navbar=True,
            label="Developer",
        ),
        dbc.NavItem(dbc.NavLink("Login", href="/login")),
    ],
    brand="Remote Area Monitoring",
    brand_href="/home",
    color="primary",
    dark=True,
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])


@app.callback(Output('map-example-view', 'children'),
              Input('map-example-button', 'n_clicks'),
              State('map-example-lat', 'value'),
              State('map-example-lon', 'value'),
              State('map-example-size', 'value'),
              State('map-example-zoom', 'value'))
def update_example_map(n_clicks, lat, lon, size, zoom):
    try:
        lat = float(lat)
        lon = float(lon)
        size = float(size)
        zoom = int(zoom)
    except TypeError:
        print('map example type exception')
        lat = 28.602374
        lon = -81.200164
        size = 8.0
        zoom = 8
    return Map().get_map_div(lat, lon, size=size, zoom=zoom)


# Navigate pages
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/map-example':
        return map_example.MapExample().get_layout()
    else:
        return home.Home().get_layout()


if __name__ == '__main__':
    try:
        ip_address = check_output(["hostname", "-I"]).decode("utf-8").split(" ")[0]
    except:
        ip_address = socket.gethostbyname(socket.gethostname())
    print("IP Address: ", ip_address)
    port = 8050
    print("Port: ", port)
    app.run_server(debug=True, host=ip_address, port=port)
