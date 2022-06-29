from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
from source.util.database import Database
from source.util.settings import Settings
import pandas as pd
from source.util.timekeeper import Timestamps
import json
import plotly.graph_objects as go


class Map:
    def __init__(self):
        self.ts = Timestamps()
        self.config = Settings('general.config')
        self.nodes_config = Settings('nodes.config')
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

    def get_connection_tree(self, subs, lats, lons):
        # print(subs)
        for sub in subs:
            node_id = sub['nodeId']
            node_data = self.nodes_db.get_data_single_field('node_id', node_id)
            if len(node_data) > 0:
                node_data = node_data[0]
                lats.append(node_data['lat'])
                lons.append(node_data['lon'])
            if 'subs' in sub:
                self.get_connection_tree(sub['subs'], lats, lons)
        location_data = {
            'lats': lats,
            'lons': lons
        }
        return location_data

    def network_map(self):
        lats = list()
        lons = list()
        topology = self.nodes_config.get_setting('connected_nodes', 'topology')
        if topology is None:
            return html.Div([])
        topology = json.loads(topology)
        # Example topology
        # topology = {'nodeId': 2222635529, 'root': True, 'subs': [{'nodeId': 4144717489,
        #                                                           'subs': [{'nodeId': 4146216805},
        #                                                                    {'nodeId': 4144723677,
        #                                                                     'subs': [{'nodeId': 2222631473}]}]}]}
        root = topology['nodeId']
        if self.config.get_int_setting('mesh_network', 'root_id') != root:
            return html.Div([html.P('No data available for root node')])
        root_lat = self.config.get_float_setting('mesh_network', 'root_lat')
        lats.append(root_lat)
        root_lon = self.config.get_float_setting('mesh_network', 'root_lon')
        lons.append(self.config.get_float_setting('mesh_network', 'root_lon'))
        if 'subs' in topology:
            subs = topology['subs']
        else:
            subs = []
        location_data = self.get_connection_tree(subs, lats, lons)

        fig = go.Figure(go.Scattermapbox(
            mode='markers+lines',
            lon=location_data['lons'],
            lat=location_data['lats'],
            line={'width': 5},
            marker={'size': 15}
        ))
        fig.update_layout(
            mapbox={
                'style': 'stamen-terrain',
                'center': {'lon': root_lon, 'lat': root_lat},
                'zoom': 15
            }
        )
        fig.show()


def main():
    map = Map()
    map.test_multi_point_map()


if __name__ == '__main__':
    main()
