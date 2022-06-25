from source.util.analysis import Analysis
from source.network.mesh import Mesh
from source.util.database import Database
from dash import html
import dash_bootstrap_components as dbc
import dash_daq as daq
from source.util.settings import Settings
from source.util.conversions import Convert
from source.website.map import Map


class NodeDetails:
    def __init__(self, pathname: str, mesh: Mesh, nodes_db: Database, sensors_db: Database):
        self.mesh = mesh
        self.nodes_db = nodes_db
        self.map = Map()
        self.config = Settings('general.config')
        self.convert = Convert()
        self.sensors_db = sensors_db
        self.node_id = self.__get_node_id(pathname)
        self.node_config = self.__get_node_config()
        self.sensor_data = self.__get_node_sensor_data()
        self.analysis = Analysis(self.sensor_data)
        self.analyzed_data = self.analysis.get_gauge_data()

    def __get_node_id(self, pathname: str):
        try:
            # example pathname: /node_details-123456789
            node_id = int(pathname.split('-')[1])
            return node_id
        except Exception as e:
            print(e)
            return None

    def __get_node_config(self):
        if self.node_id is None:
            return None
        data = self.nodes_db.get_data_single_field('node_id', self.node_id)
        if len(data) > 0:
            data = data[0]
        return data

    def __get_node_sensor_data(self, end_timestamp=None):
        if self.node_id is None:
            return None
        data = self.sensors_db.get_data_single_field('node_id', self.node_id, timestamp=end_timestamp)
        return data

    def __get_rows(self):
        rows = list()
        row_1 = dbc.Row([dbc.Col([html.H2('Environmental Data')], width='auto')], justify='center')
        rows.append(row_1)
        row_2 = dbc.Row([dbc.Col([html.P('Date Last Updated: ' + self.analysis.get_last_update_string())],
                                 width='auto')],
                        justify='center')
        rows.append(row_2)

        temperature_data = next(record for record in self.analyzed_data if record['name'] == 'air_temperature_C')
        temperature_data['current_value'] = self.convert.temperature(temperature_data['current_value'])

        if self.config.get_setting('units', 'unit') == 'imperial':
            maximum_temp = self.config.get_int_setting('units', 'max_temperature_f')
            minimum_temp = self.config.get_int_setting('units', 'min_temperature_f')
            units = '\xb0F'
        else:
            maximum_temp = self.config.get_int_setting('units', 'max_temperature_c')
            minimum_temp = self.config.get_int_setting('units', 'min_temperature_c')
            units = '\xb0C'

        humidity_data = next(record for record in self.analyzed_data if record['name'] == 'humidity')

        pressure_data = next(record for record in self.analyzed_data if record['name'] == 'air_pressure_Pa')
        pressure_mbar = self.convert.pressure_mbar(pressure_data['current_value'])
        max_mbar = self.config.get_int_setting('units', 'max_mbar')
        min_mbar = self.config.get_int_setting('units', 'min_mbar')

        soil_data = next(record for record in self.analyzed_data if record['name'] == 'soil_moisture_adc')
        soil_sat = self.convert.soil_moisture(soil_data['current_value'])

        row_3 = dbc.Row([
            dbc.Col([
                html.Div([
                    daq.Gauge(
                        showCurrentValue=True,
                        color='#0d6dfd',
                        label='Temperature',
                        units=units,
                        value=temperature_data['current_value'],
                        max=maximum_temp,
                        min=minimum_temp,
                    )
                ])
            ], width='auto'),
            dbc.Col([
                html.Div([
                    daq.Gauge(
                        # scale={'start': 973, 'interval': 10, 'labelInterval': 1},
                        showCurrentValue=True,
                        color='#0d6dfd',
                        label='Pressure',
                        units='mbar',
                        value=pressure_mbar,
                        max=max_mbar,
                        min=min_mbar,
                    )
                ])
            ], width='auto'),
            dbc.Col([
                html.Div([
                    daq.Gauge(
                        showCurrentValue=True,
                        color='#0d6dfd',
                        label='Humidity',
                        units='%',
                        value=humidity_data['current_value'],
                        max=100,
                        min=0,
                    )
                ])
            ], width='auto'),
            dbc.Col([
                html.Div([
                    daq.Gauge(
                        showCurrentValue=True,
                        color={"gradient": True, "ranges": {"red": [0, 60], "yellow": [60, 80], "green": [80, 100]}},
                        label='Soil Moisture Saturation',
                        units='%',
                        value=soil_sat,
                        max=100,
                        min=0,
                    )
                ])
            ], width='auto')
        ], justify='center')

        rows.append(row_3)

        wind_speed_data = next(record for record in self.analyzed_data if record['name'] == 'wind_speed_mph')
        wind_speed = wind_speed_data['current_value']
        if self.config.get_setting('units', 'unit') == 'imperial':
            max_wind_speed = self.config.get_int_setting('units', 'max_wind_speed_mph')
            min_wind_speed = self.config.get_int_setting('units', 'min_wind_speed_mph')
            wind_speed_units = 'MPH'
        else:
            max_wind_speed = self.config.get_int_setting('units', 'max_wind_speed_ms')
            min_wind_speed = self.config.get_int_setting('units', 'min_wind_speed_ms')
            wind_speed_units = 'm/s'

        wind_direction_data = next(record for record in self.analyzed_data if record['name'] == 'wind_direction')
        wind_direction_string = str(round(wind_direction_data['current_value']))

        co2_data = next(record for record in self.analyzed_data if record['name'] == 'co2_ppm')
        co2 = co2_data['current_value']
        co2_unit = 'PPM'
        min_co2 = self.config.get_int_setting('units', 'min_co2')
        max_co2 = self.config.get_int_setting('units', 'max_co2')
        if co2 > max_co2:
            max_co2 = co2

        tvoc_data = next(record for record in self.analyzed_data if record['name'] == 'tvoc_ppb')
        tvoc = tvoc_data['current_value']
        tvoc_unit = 'PPB'
        min_tvoc = self.config.get_int_setting('units', 'min_tvoc')
        max_tvoc = self.config.get_int_setting('units', 'max_tvoc')
        if tvoc > max_tvoc:
            max_tvoc = tvoc

        row_4 = dbc.Row([
            dbc.Col([
                html.Div([
                    daq.LEDDisplay(
                        color='#0d6dfd',
                        label='Wind Direction Degrees',
                        value=wind_direction_string,
                        # size=64
                    )
                ])
            ], width='auto', align='center'),
            dbc.Col([
                html.Div([
                    daq.Gauge(
                        showCurrentValue=True,
                        color='#0d6dfd',
                        label='Wind Speed',
                        units=wind_speed_units,
                        value=wind_speed,
                        max=max_wind_speed,
                        min=min_wind_speed,
                    )
                ])
            ], width='auto'),
            dbc.Col([
                html.Div([
                    daq.Gauge(
                        scale={'start': 0, 'interval': 100, 'labelInterval': 2},
                        showCurrentValue=True,
                        color='#0d6dfd',
                        label='CO2',
                        units=co2_unit,
                        value=co2,
                        max=max_co2,
                        min=min_co2,
                    )
                ])
            ], width='auto'),
            dbc.Col([
                html.Div([
                    daq.Gauge(
                        showCurrentValue=True,
                        color='#0d6dfd',
                        label='TVOC',
                        units=tvoc_unit,
                        value=tvoc,
                        max=max_tvoc,
                        min=min_tvoc,
                    )
                ])
            ], width='auto'),
        ], justify='center')

        rows.append(row_4)

        location_title_row = dbc.Row([
            dbc.Col([
                html.H3('Location')
            ], width='auto')
        ], justify='center')
        rows.append(location_title_row)

        location_info_row = dbc.Row([
            dbc.Col([
                html.P('Latitude: ' + str(self.node_config['lat']))
            ], width='auto'),
            dbc.Col([
                html.P('Longitude: ' + str(self.node_config['lon']))
            ], width='auto'),
        ], justify='center')
        rows.append(location_info_row)

        map_row = dbc.Row([
            dbc.Col([
                self.map.get_single_point_map_div(latitude=self.node_config['lat'], longitude=self.node_config['lon'],
                                                  zoom=15, style='stamen-terrain')
            ], width='auto')
        ], justify='center')
        rows.append(map_row)

        row_5 = dbc.Row([dbc.Col([html.Hr()], width='auto')], justify='center')
        rows.append(row_5)

        row_6 = dbc.Row([dbc.Col([html.H2('Node Health')], width='auto')], justify='center')
        rows.append(row_6)
        rows.append(row_2)

        # TODO: give the user a way to edit node config
        # TODO: Actually detect connection status
        connection_status = 'connected'
        connection_color = 'green'
        connection_status_row = dbc.Row([
            dbc.Col([
                html.H3('Status: ' + connection_status, style={'color': connection_color})
            ], width='auto')
        ], justify='center')
        rows.append(connection_status_row)

        return rows

    def get_layout(self):
        default_layout = html.Div([
            html.Br(),
            html.H1('Node Data Unavailable')
        ])
        if self.node_id is None or self.sensor_data is None:
            return default_layout
        return html.Div(self.__get_rows())
