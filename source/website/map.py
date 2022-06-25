from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
from source.util.database import Database
from source.util.settings import Settings
import pandas as pd
from source.util.timekeeper import Timestamps


class Map:
    def __init__(self):
        self.ts = Timestamps()
        self.config = Settings('general.config')
        self.nodes_db = Database(self.config.get_setting('databases', 'nodes_db_path'))
        self.sensors_db = Database(self.config.get_setting('databases', 'sensor_data_db_path'))

    def __get_node_location_dataframe(self):
        data = self.nodes_db.get_all()
        for record in data:
            record.pop('node_config')
            record['date_created'] = self.ts.get_time_date_string(record['date_created'])
            record['date_last_modified'] = self.ts.get_time_date_string(record['date_last_modified'])
            record['size'] = 5
        print(data)
        return pd.DataFrame(data)

    def get_all_nodes_map_div(self, zoom=12):
        data = self.__get_node_location_dataframe()
        fig = px.scatter_mapbox(data, lat="lat", lon="lon", color_discrete_sequence=["blue"], zoom=zoom, size='size',
                                size_max=15.0)
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        # fig.show()
        div = html.Div([
            dcc.Graph(figure=fig)
            ],
            style={'display': 'flex', 'justifyContent': 'center'}
        )
        return div

    def get_single_point_map_div(self, latitude: float, longitude: float, size: float = 5.0, zoom=15,
                                 style='open-street-map'):
        point = [{'lat': latitude, 'lon': longitude, 'point_size': size}]
        fig = px.scatter_mapbox(point, lat="lat", lon="lon", color_discrete_sequence=["blue"], zoom=zoom,
                                size='point_size', size_max=15.0)
        fig.update_layout(mapbox_style=style)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        div = html.Div([
            dcc.Graph(figure=fig)
        ])
        return div

    def get_node_point(self, node_id):
        data = self.nodes_db.get_data_single_field('node_id', node_id)
        if len(data) > 0:
            node = data[0]
            return self.get_single_point_map_div(node['lat'], node['lon'], zoom=15, style='stamen-terrain')
        return html.Div([])

    def test_multi_point_map(self):
        df = self.__get_node_location_dataframe()
        pd.set_option("display.max_rows", None, "display.max_columns", None)
        print(df)
        fig = px.scatter_mapbox(df,
                                lat='lat',
                                lon='lon',
                                hover_name='node_id',
                                zoom=1)

        fig.show()


def main():
    map = Map()
    map.test_multi_point_map()


if __name__ == '__main__':
    main()
