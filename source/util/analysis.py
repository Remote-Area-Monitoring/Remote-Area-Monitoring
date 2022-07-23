from source.util.timekeeper import Timestamps
import numbers


class Analysis:
    def __init__(self, sensor_data):
        self.ts = Timestamps()
        self.sensor_data = sorted(sensor_data, key=lambda d: d['timestamp'])

    def get_gauge_data(self):
        if self.sensor_data is None:
            return None
        results = list()
        keys = self.sensor_data[-1].keys()
        for key in keys:
            if key not in self.sensor_data[-1]:
                continue
            if isinstance(self.sensor_data[-1][key], numbers.Number) is False:
                continue
            try:
                # seq = [x[key] for x in self.sensor_data]
                seq = list()
                for record in self.sensor_data:
                    if key in record:
                        seq.append(record[key])
                maximum = round(max(seq), 2)
                minimum = round(min(seq), 2)
                current = round(self.sensor_data[-1][key], 2)
                results.append({'name': key, 'current_value': current, 'max_value': maximum, 'min_value': minimum})
            except Exception as e:
                print('Error -> analysis.py: ', e)
        return results

    def get_last_update_string(self):
        seq = [x['timestamp'] for x in self.sensor_data]
        last_updated = max(seq)
        last_updated = self.ts.get_time_date_string(last_updated)
        return last_updated

    def get_node_graphs_list(self):
        graphs = ['Temperature', 'Humidity', 'Pressure', 'CO2', 'TVOC', 'Soil Moisture', 'Wind Speed', 'Wind Direction',
                  'Battery Voltage', 'Battery Current', 'Bus Power', 'Mesh Connection Strength']
        return graphs
