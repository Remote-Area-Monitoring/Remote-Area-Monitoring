from source.util.settings import Settings
from source.util.database import Database
from dash import Dash, dcc, html
import pandas as pd


class Graph:
    def __init__(self):
        self.config = Settings('general.config')
        self.nodes_db = Database(self.config.get_setting('databases', 'nodes_db_path'))
        self.sensors_db = Database(self.config.get_setting('databases', 'sensor_data_db_path'))

    def __get_sensor_data_by_node(self, node_id, timestamp=None):
        data = self.sensors_db.get_data_single_field('node_id', node_id, timestamp=timestamp)
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


def main():
    graph = Graph()
    print(graph.get_example_data())


if __name__ == '__main__':
    main()
