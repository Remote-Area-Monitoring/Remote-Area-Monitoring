from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px


class Map:
    def get_map_div(self, latitude: float, longitude: float, size: float = 5.0, zoom=15):
        point = [{'lat': latitude, 'lon': longitude, 'point_size': size}]
        fig = px.scatter_mapbox(point, lat="lat", lon="lon", color_discrete_sequence=["blue"], zoom=zoom,
                                size='point_size', size_max=15.0)
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        div = html.Div([
            dcc.Graph(figure=fig)
        ])
        return div
