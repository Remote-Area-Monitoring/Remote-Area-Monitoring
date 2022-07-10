import statistics

from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
from source.util.database import Database
from source.util.settings import Settings
import pandas as pd
from source.util.timekeeper import Timestamps
import json
import plotly.graph_objects as go
from statistics import mean
from source.util.conversions import Convert


class Map:
    def __init__(self):
        self.ts = Timestamps()
        self.convert = Convert()
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

    def __get_node_status_map_dataframe(self):
        data = list()
        nodes = self.nodes_db.get_all()
        connected_nodes = self.nodes_config.get_list_setting('connected_nodes', 'node_ids')
        if len(connected_nodes) == 0:
            root_connection_status = 'Disconnected'
            root_signal_strength = 'None'
            root_polling_status = 'Inactive'
        else:
            root_connection_status = 'Connected'
            root_signal_strength = self.nodes_config.get_int_setting('connected_nodes', 'root_signal_strength')
            polling = self.config.get_bool_setting('mesh_network', 'polling')
            if polling is True:
                root_polling_status = 'Active'
            else:
                root_polling_status = 'Inactive'
        root_id = self.config.get_int_setting('mesh_network', 'root_id')
        root_lat = self.config.get_float_setting('mesh_network', 'root_lat')
        root_lon = self.config.get_float_setting('mesh_network', 'root_lon')
        dataobj = {
            'node_id': root_id,
            'lat': root_lat,
            'lon': root_lon,
            'connection_status': root_connection_status,
            'signal_strength(dB)': root_signal_strength,
            'polling_status': root_polling_status,
            'notes': 'Root Node',
            'size': 5
        }
        data.append(dataobj)

        for node in nodes:
            sensor_data = self.sensors_db.get_data_single_field('node_id', node['node_id'],
                                                                self.ts.get_1week_timestamp())
            if len(sensor_data) < 1:
                sensor_data = self.sensors_db.get_data_single_field('node_id', node['node_id'])
            try:
                sensor_data = sensor_data[-1]
            except IndexError:
                return None
            connection_status = 'Disconnected'
            signal_strength = 'None'
            if node['node_id'] in connected_nodes:
                connection_status = 'Connected'
                signal_strength = sensor_data['connection_strength']
            dataobj = {
                'node_id': node['node_id'],
                'lat': node['lat'],
                'lon': node['lon'],
                'connection_status': connection_status,
                'signal_strength(dB)': signal_strength,
                'polling_status': node['status'],
                'notes': node['notes'],
                'size': 5
            }
            data.append(dataobj)
        #     node_ids.append(node['node_id'])
        #     lats.append(node['lat'])
        #     lons.append(node['lon'])
        #     con_status.append(connection_status)
        #     sig_strength.append(signal_strength)
        #     poll_status.append(node['status'])
        #     notes.append(node['notes'])
        # dataobj = {
        #     'node_id': node_ids,
        #     'lat': lats,
        #     'lon': lons,
        #     'connection_status': con_status,
        #     'signal_strength(dB)': sig_strength,
        #     'polling_status': poll_status,
        #     'notes': notes
        # }
        return pd.DataFrame(data)

    def get_node_status_map(self):
        data = self.__get_node_status_map_dataframe()
        if data is None:
            return html.P('Network Status Map Unavailable')
        fig = px.scatter_mapbox(data, lat="lat", lon="lon", color='connection_status',
                                color_discrete_sequence=['green', 'red'], zoom=13, hover_name='node_id',
                                size='size', hover_data=['lat', 'lon', 'connection_status', 'signal_strength(dB)',
                                                         'polling_status', 'notes'])
        fig.update_layout(mapbox_style="stamen-terrain")
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.update_layout(legend_x=0.01, legend_y=0.99)
        div = html.Div([
            dcc.Graph(figure=fig)
        ])
        return div

    def get_heatmap(self):
        lats = list()
        lons = list()
        mags = list()
        nodes = self.nodes_db.get_all()
        for node in nodes:
            lats. append(node['lat'])
            lons.append(node['lon'])
            data = self.sensors_db.get_data_single_field('node_id', node['node_id'], self.ts.get_24h_timestamp())
            temperature_data = list()
            for record in data:
                if 'calibration_temperature' in record:
                    temperature_data.append(record['calibration_temperature'])
                elif 'air_temperature_C' in record:
                    temperature_data.append(record['air_temperature_C'])
            mags.append(mean(temperature_data))
        root_lat = self.config.get_float_setting('mesh_network', 'root_lat')
        root_lon = self.config.get_float_setting('mesh_network', 'root_lon')
        lats.append(root_lat)
        lons.append(root_lon)
        mags.append(0)
        dataobj = {
            'lats': lats,
            'lons': lons,
            'mags': mags
        }
        print(dataobj)

        df = pd.DataFrame(dataobj)
        print(df)
        fig = px.density_mapbox(df, lat='lats', lon='lons', z='mags', radius=100,
                                center=dict(lat=root_lat, lon=root_lon), zoom=12,
                                mapbox_style="stamen-terrain")
        fig.show()

    def get_animated_heatmap(self):
        data = list()
        hours = range(0, 24)
        nodes = self.nodes_db.get_all()
        root_lat = self.config.get_float_setting('mesh_network', 'root_lat')
        root_lon = self.config.get_float_setting('mesh_network', 'root_lon')
        root_node_id = self.config.get_float_setting('mesh_network', 'root_id')
        for node in nodes:
            sensor_data = self.sensors_db.get_data_single_field('node_id', node['node_id'], self.ts.get_24h_timestamp())
            timestamp = self.ts.get_24h_timestamp()
            for hour in hours:
                temperature_data = list()
                for record in sensor_data:
                    if self.ts.hour_from_timestamp(record['timestamp']) == hour:
                        timestamp = record['timestamp']
                        if 'calibration_temperature' in record:
                            temperature_data.append(self.convert.temperature(record['calibration_temperature']))
                        elif 'air_temperature_C' in record:
                            temperature_data.append(self.convert.temperature(record['air_temperature_C']))
                try:
                    mag = mean(temperature_data)
                except statistics.StatisticsError:
                    mag = 0
                dataobj = {
                    'timestamp': timestamp,
                    'node_id': node['node_id'],
                    'lat': node['lat'],
                    'lon': node['lon'],
                    'mag': mag,
                    'hour': hour
                }
                data.append(dataobj)
        # for hour in hours:
        #     hourly_data = list()
        #     for record in data:
        #         if record['hour'] == hour:
        #             hourly_data.append(record)
        #     mags = [x['mag'] for x in hourly_data]
        #     try:
        #         mag = mean(mags)
        #     except statistics.StatisticsError:
        #         mag = 0
        #     dataobj = {
        #         'node_id': root_node_id,
        #         'lat': root_lat,
        #         'lon': root_lon,
        #         'mag': mag,
        #         'hour': hour
        #     }
        #     data.append(dataobj)
        # data.reverse()
        data = sorted(data, key=lambda d: d['timestamp'])
        mags = [x['mag'] for x in data]
        max_mag = max(mags)
        min_mag = min(mags)
        for record in data:
            print(record)
        df = pd.DataFrame(data)
        print(df)
        fig = px.density_mapbox(df, lat='lat', lon='lon', z='mag', radius=100, center=dict(lat=root_lat, lon=root_lon),
                                zoom=12, mapbox_style="stamen-terrain", animation_frame='hour', hover_name='node_id',
                                range_color=[min_mag, max_mag])
        fig.show()




def main():
    map = Map()
    map.get_animated_heatmap()


if __name__ == '__main__':
    main()
