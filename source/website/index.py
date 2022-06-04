from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from app import app
from map import Map
from subprocess import check_output
import socket
from flask import request
from source.util.database import Database
from source.network.mesh import Mesh
from source.util.settings import Settings
from source.util.timekeeper import Timestamps
from source.website.pages import home, map_example, node_table, updater

config = Settings('general.config')
nodes_db = Database(config.get_setting('databases', 'nodes_db_path'))
mesh = Mesh()


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home Page", href="/home")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Dev Tools", header=True),
                dbc.DropdownMenuItem("Map Test", href="/map-example"),
                dbc.DropdownMenuItem("Nodes List Table", href="/nodes-table"),
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
    return Map().get_single_point_map_div(lat, lon, size=size, zoom=zoom)


# Navigate pages
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/map-example':
        return map_example.MapExample().get_layout()
    elif pathname == '/nodes-table':
        return node_table.NodeTable(mesh).get_layout()
    elif 'update' in pathname:
        return updater.Updater(mesh).get_layout()
    else:
        return home.Home().get_layout()


if __name__ == '__main__':
    try:
        ip_address = socket.gethostbyname(socket.gethostname())
    except:
        ip_address = check_output(["hostname", "-I"]).decode("utf-8").split(" ")[0]
    print("IP Address: ", ip_address)
    port = 8050
    print("Port: ", port)
    config.set_setting('website', 'ip_address', str(ip_address))
    config.set_setting('website', 'port', str(port))
    app.run_server(debug=False, host=ip_address, port=port)
