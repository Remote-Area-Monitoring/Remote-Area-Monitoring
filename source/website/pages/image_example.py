from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from source.util.image import Image


class ImageExample:
    def get_layout(self):
        layout = html.Div([
            html.Br(),
            Image().get_test_image_div()
        ])
        return layout
