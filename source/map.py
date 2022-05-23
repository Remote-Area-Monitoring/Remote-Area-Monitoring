from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px


class Map:
    def get_map_div(self, latitude: float, longitude: float, size=10, zoom=15):
        point = [{'lat': latitude, 'lon': longitude, 'size': size}]
        fig = px.scatter_mapbox(point, lat="lat", lon="lon", color_discrete_sequence=["blue"], size='size', zoom=zoom)
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        div = html.Div([
            dcc.Graph(figure=fig)
        ])
        return div
