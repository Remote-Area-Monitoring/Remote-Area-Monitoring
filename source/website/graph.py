import json

from source.util.settings import Settings
from source.util.database import Database
from source.util.timekeeper import Timestamps
from source.util.conversions import Convert
from dash import Dash, dcc, html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


class Graph:
    def __init__(self):
        self.ts = Timestamps()
        self.convert = Convert()
        self.config = Settings('general.config')
        self.nodes_db = Database(self.config.get_setting('databases', 'nodes_db_path'))
        self.sensors_db = Database(self.config.get_setting('databases', 'sensor_data_db_path'))

    def __get_sensor_data_by_node(self, node_id, timestamp=None):
        data = self.sensors_db.get_data_single_field('node_id', node_id, timestamp=timestamp)
        return data

    def __convert_timestamp_to_datetime(self, data):
        for record in data:
            record['timestamp'] = self.ts.date_obj_from_timestamp(record['timestamp'])
        return data

    def __get_single_value_dataframe(self, sensor_data, value_key):
        # date
        x_data = list()
        # temperature
        y_data = list()
        for record in sensor_data:
            timestamp = record['timestamp']
            degrees_c = record[value_key]
            if timestamp and degrees_c:
                x_data.append(timestamp)
                y_data.append(degrees_c)
        data_frame = pd.DataFrame(dict(
            x=x_data,
            y=y_data
        ))
        return data_frame

    def get_example_data(self):
        data = self.__get_sensor_data_by_node(222263147)
        data_frame = self.__get_single_value_dataframe(data, 'air_temperature_C')
        return data_frame

    def get_example_temperature_graph_div(self):
        data_frame = self.get_example_data()
        fig = None
        # fig.show()
        div = html.Div([
            dcc.Graph(figure=fig)
        ])
        return div

    def get_24h_temperature(self, node_id):
        # date
        x_data = list()
        # temperature
        y_data = list()
        data = self.__get_sensor_data_by_node(node_id, self.ts.get_24h_timestamp())
        data = self.__convert_timestamp_to_datetime(data)
        for record in data:
            x_data.append(record['timestamp'])
            try:
                y_data.append(self.convert.temperature(record['calibration_temperature']))
                # y_data.append(self.convert.temperature(record['air_temperature_C']))
            except KeyError:
                y_data.append(self.convert.temperature(record['air_temperature_C']))
        data_frame = pd.DataFrame(dict(
            x=x_data,
            y=y_data
        ))
        if self.config.get_setting('units', 'unit') == 'imperial':
            y_label = 'Temperature (F)'
        else:
            y_label = 'Temperature (C)'
        x_label = 'Datetime'
        title = str(node_id) + 'Temperature Over the Last 24 Hours'
        labels = {
            'x': x_label,
            'y': y_label
        }
        fig = px.line(data_frame, x='x', y='y', title=title, labels=labels)
        fig.show()

    def get_single_select_graph(self, graph_info: str):
        try:
            print('Graph Info: ' + graph_info)
            graph_info = graph_info.split(' -> ')
            node_id = int(graph_info[0])
            data_type = graph_info[1]
            # graph_info = json.loads(graph_info)
            # node_id = graph_info['node_id']
            # data_type = graph_info['graph'].lower()
        except Exception as e:
            print(e)
            return html.Div([])
        data_type = data_type.lower()
        # date
        x_data = list()
        # sensor data
        y_data = list()
        data = self.__get_sensor_data_by_node(node_id)
        data = self.__convert_timestamp_to_datetime(data)
        x_label = 'Datetime'
        if data_type == 'temperature':
            title = '(' + str(node_id) + ') Temperature Over Time'
            if self.config.get_setting('units', 'unit') == 'imperial':
                y_label = 'Temperature (F)'
            else:
                y_label = 'Temperature (C)'
            for record in data:
                x_data.append(record['timestamp'])
                try:
                    y_data.append(self.convert.temperature(record['calibration_temperature']))
                    # y_data.append(self.convert.temperature(record['air_temperature_C']))
                except KeyError:
                    y_data.append(self.convert.temperature(record['air_temperature_C']))
        elif data_type == 'humidity':
            title = '(' + str(node_id) + ') Humidity Over Time'
            y_label = 'Humidity (%)'
            for record in data:
                try:
                    x_data.append(record['timestamp'])
                    y_data.append(self.convert.humidity(record['humidity']))
                except IndexError:
                    continue
        elif data_type == 'pressure':
            title = '(' + str(node_id) + ') Atmospheric Pressure Over Time'
            y_label = 'Pressure (mbar)'
            for record in data:
                try:
                    x_data.append(record['timestamp'])
                    y_data.append(self.convert.pressure_mbar(record['air_pressure_Pa']))
                except IndexError:
                    continue
        elif data_type == 'co2':
            title = '(' + str(node_id) + ') Carbon Dioxide (CO2) Over Time'
            y_label = 'CO2 (PPM)'
            for record in data:
                try:
                    x_data.append(record['timestamp'])
                    y_data.append(record['co2_ppm'])
                except IndexError:
                    continue
        elif data_type == 'tvoc':
            title = '(' + str(node_id) + ') Total Volatile Organic Carbons (TVOC) Over Time'
            y_label = 'TVOC (PPB)'
            for record in data:
                try:
                    x_data.append(record['timestamp'])
                    y_data.append(record['tvoc_ppb'])
                except IndexError:
                    continue
        elif data_type == 'tvoc':
            title = '(' + str(node_id) + ') Total Volatile Organic Carbons (TVOC) Over Time'
            y_label = 'TVOC (PPB)'
            for record in data:
                try:
                    x_data.append(record['timestamp'])
                    y_data.append(record['tvoc_ppb'])
                except IndexError:
                    continue
        elif 'soil' in data_type:
            title = '(' + str(node_id) + ') Soil Moisture Content Over Time'
            y_label = 'Moisture Content (%)'
            for record in data:
                try:
                    x_data.append(record['timestamp'])
                    y_data.append(record['soil_moisture_adc'])
                except IndexError:
                    continue
        elif 'speed' in data_type:
            title = '(' + str(node_id) + ') Wind Speed Over Time'
            unit = '(m/s)'
            if self.config.get_setting('units', 'unit') == 'imperial':
                unit = '(mph)'
            y_label = 'Wind Speed ' + unit
            for record in data:
                try:
                    x_data.append(record['timestamp'])
                    y_data.append(self.convert.wind_speed(record['wind_speed_mph']))
                except IndexError:
                    continue
        elif 'direction' in data_type:
            title = '(' + str(node_id) + ') Wind Direction Over Time'
            y_label = 'Wind Direction (Degrees)'
            for record in data:
                try:
                    x_data.append(record['timestamp'])
                    y_data.append(record['wind_direction'])
                except IndexError:
                    continue
        elif 'current' in data_type:
            title = '(' + str(node_id) + ') Battery Current Over Time'
            y_label = 'Current (mA)'
            for record in data:
                try:
                    x_data.append(record['timestamp'])
                    y_data.append(record['current_mA'])
                except IndexError:
                    continue
        elif 'volt' in data_type:
            title = '(' + str(node_id) + ') Battery Voltage Over Time'
            y_label = 'Voltage (V)'
            for record in data:
                try:
                    x_data.append(record['timestamp'])
                    y_data.append(record['bus_voltage_V'])
                except IndexError:
                    continue
        elif 'power' in data_type:
            title = '(' + str(node_id) + ') Bus Power Over Time'
            y_label = 'Power (w)'
            for record in data:
                try:
                    x_data.append(record['timestamp'])
                    y_data.append(self.convert.power(record['power_mW']))
                except IndexError:
                    continue
        else:
            return html.Div([])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_data, y=y_data))
        fig.update_layout(
            title=title,
            xaxis_title=x_label,
            yaxis_title=y_label,
            margin=dict(l=0, r=0)
        )
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label="1h",
                             step="hour",
                             stepmode="backward"),
                        dict(count=1,
                             label="1d",
                             step="day",
                             stepmode="backward"),
                        dict(count=7,
                             label="1w",
                             step="day",
                             stepmode="backward"),
                        dict(count=1,
                             label="1m",
                             step="month",
                             stepmode="backward"),
                        dict(count=6,
                             label="6m",
                             step="month",
                             stepmode="backward"),
                        dict(count=1,
                             label="YTD",
                             step="year",
                             stepmode="todate"),
                        dict(count=1,
                             label="1y",
                             step="year",
                             stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            )
        )
        return html.Div([dcc.Graph(figure=fig, style={'height': '60vh'})])

    # def get_min_max_avg(self, node_id=None):
    #     for record in records:
    #         if timestamp < record['timestamp'] < timestamp + 3600:


def main():
    graph = Graph()
    graph.get_single_select_graph(4144723677, 'humidity')


if __name__ == '__main__':
    main()
