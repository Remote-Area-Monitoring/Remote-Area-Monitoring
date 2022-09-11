import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from source.util.settings import Settings
from source.util.timekeeper import Timestamps
from source.util.database import Database
from source.util.conversions import Convert
from statistics import mean


class Notify:
    def __init__(self):
        self.ts = Timestamps()
        self.convert = Convert()
        self.email_config = Settings('secret.config')
        self.general_config = Settings('general.config')
        self.nodes_db = Database(self.general_config.get_setting('databases', 'nodes_db_path'))
        self.sensor_db = Database(self.general_config.get_setting('databases', 'sensor_data_db_path'))
        self.alerts_db = Database(self.general_config.get_setting('databases', 'alerts_db_path'))
        server = self.email_config.get_setting('google', 'server')
        port = self.email_config.get_int_setting('google', 'port')
        self.server = smtplib.SMTP(server, port)
        self.email_username = self.email_config.get_setting('email_creds', 'user')
        self.email_password = self.email_config.get_setting('email_creds', 'pass')
        self.context = ssl.create_default_context()

    def __send_email(self, subject, message, users):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_username
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))
            self.server.starttls(context=self.context)
            self.server.login(self.email_username, self.email_password)
            self.server.sendmail(from_addr=self.email_username, to_addrs=users, msg=message)
            return True
        except Exception as e:
            print(e)
            return False

    def send_subscribe_notice(self, email: str):
        subject = 'Remote Area Monitoring: Subscribed'
        message = 'Subject: {}\n\n' \
                  'User Email: {}\n\n' \
                  'Subscribed on: {}'.format(subject, email, self.ts.get_day_timestring(self.ts.get_timestamp()))
        users = list()
        users.append(email)
        sent = self.__send_email(subject, message, users)
        if sent is False:
            self.__send_email(subject, message, users)

    def send_unsubscribe_notice(self, email: str):
        subject = 'Remote Area Monitoring: Unsubscribed'
        message = 'Subject: {}\n\n' \
                  'User Email: {}\n\n' \
                  'Unsubscribed on: {}'.format(subject, email, self.ts.get_day_timestring(self.ts.get_timestamp()))
        users = list()
        users.append(email)
        sent = self.__send_email(subject, message, users)
        if sent is False:
            self.__send_email(subject, message, users)

    def __send_node_error(self, last_connected_timestamp, node_config, last_entry):
        subject = 'Node Disconnected'
        message = 'Subject: {}\n\n' \
                  'Node ID: {}\n\n' \
                  'Last Connected Time: {} \n\n' \
                  'Node Config:\n'.format(subject,
                                          node_config['node_id'],
                                          self.ts.get_time_date_string(last_connected_timestamp))
        for key in node_config.keys():
            line = str(key) + ': ' + str(node_config[key]) + '\n'
            message += line

        message += '\nLast Data Package Reported:\n\n'
        if last_entry is None:
            message += 'No Data Available'
        else:
            message += 'Report Time: {}\n\n'.format(self.ts.get_time_date_string(last_entry['timestamp']))
            message += 'Report Contents:\n\n'
            for key in last_entry.keys():
                line = str(key) + ': ' + str(last_entry[key]) + '\n'
                message += line

        users = self.email_config.get_list_setting('notify', 'emails')
        sent = self.__send_email(subject, message, users)
        if sent is False:
            sent = self.__send_email(subject, message, users)
        return sent

    def monitor_nodes(self):
        if self.general_config.get_bool_setting('notify', 'active') is False:
            return None
        nodes = self.nodes_db.get_all()
        sensor_query_interval = self.general_config.get_int_setting('mesh_network', 'sensor_polling_interval')
        limit_multiplier = self.general_config.get_int_setting('notify', 'limit_multiplier')
        sensor_notify_limit = limit_multiplier * sensor_query_interval
        for node in nodes:
            if node['status'] == 'active':
                sensor_data = self.sensor_db.get_data_single_field('node_id', node['node_id'],
                                                                   self.ts.get_24h_timestamp())
                timestamps = list()
                for record in sensor_data:
                    timestamps.append(record['timestamp'])
                last_timestamp = max(timestamps)
                if last_timestamp < self.ts.get_timestamp() - sensor_notify_limit:
                    search_timestamp = self.ts.get_timestamp() - self.general_config.get_int_setting('notify',
                                                                                                     'cooldown')
                    previous_notifications = self.alerts_db.get_data_single_field('node_id', node['node_id'],
                                                                                  search_timestamp)
                    if len(previous_notifications) > 0:
                        continue
                    if len(sensor_data) > 0:
                        last_entry = sensor_data[-1]
                    else:
                        last_entry = None
                    dataobj = {
                        'timestamp': self.ts.get_timestamp(),
                        'node_id': node['node_id'],
                        'type': 'Node Error',
                        'last_entry': last_entry,
                        'users_notified': True
                    }
                    sent = self.__send_node_error(last_timestamp, node, last_entry)
                    if sent is False:
                        sent = self.__send_node_error(last_timestamp, node, last_entry)
                    dataobj['users_notified'] = sent
                    self.alerts_db.insert(dataobj)
                    print(dataobj)

    def daily_summary(self, force=False):
        if self.general_config.get_bool_setting('notify', 'active') is False and force is False:
            return None
        daily_update_sent = False
        daily_summary_hour = self.general_config.get_int_setting('notify', 'daily_summary_hour')
        if self.ts.hour_from_timestamp(self.ts.get_timestamp()) < daily_summary_hour and force is False:
            return None
        previous_notifications = self.alerts_db.get_records(self.ts.get_24h_timestamp())
        if previous_notifications is None:
            previous_notifications = []
        for record in previous_notifications:
            if 'type' in record:
                if record['type'] == 'Daily Summary':
                    daily_update_sent = True
                    break
        if daily_update_sent is True and force is False:
            return None

        data = self.sensor_db.get_records(self.ts.get_24h_timestamp())
        temperature_data = list()
        humidity_data = list()
        pressure_data = list()
        soil_moisture_data = list()
        wind_speed_data = list()
        co2_data = list()
        tvoc_data = list()
        for record in data:
            if 'calibration_temperature' in record:
                temperature_data.append(record['calibration_temperature'])
            elif 'air_temperature_C' in record:
                temperature_data.append(record['air_temperature_C'])
            if 'humidity' in record:
                humidity_data.append(record['humidity'])
            if 'air_pressure_Pa' in record:
                pressure_data.append(record['air_pressure_Pa'])
            if 'soil_moisture_adc' in record:
                soil_moisture_data.append(self.convert.soil_moisture(record['soil_moisture_adc']))
            if 'wind_speed_mph' in record:
                wind_speed_data.append(self.convert.wind_speed(record['wind_speed_mph']))
            if 'co2_ppm' in record:
                co2_data.append(record['co2_ppm'])
            if 'tvoc_ppb' in record:
                tvoc_data.append(record['tvoc_ppb'])

        max_temperature = self.convert.temperature(max(temperature_data))
        max_humidity = self.convert.humidity(max(humidity_data))
        max_pressure_mbar = self.convert.pressure_mbar(max(pressure_data))
        max_soil_sat = max(soil_moisture_data)
        max_wind_speed = max(wind_speed_data)
        max_co2 = max(co2_data)
        max_tvoc = max(tvoc_data)

        min_temperature = self.convert.temperature(min(temperature_data))
        min_humidity = self.convert.humidity(min(humidity_data))
        min_pressure_mbar = self.convert.pressure_mbar(min(pressure_data))
        min_soil_sat = min(soil_moisture_data)
        if min_soil_sat < 0:
            min_soil_sat = 0
        min_wind_speed = min(wind_speed_data)
        min_co2 = min(co2_data)
        if min_co2 < 400:
            min_co2 = 400
        min_tvoc = min(tvoc_data)

        avg_temperature = self.convert.temperature(mean(temperature_data))
        avg_humidity = self.convert.humidity(mean(humidity_data))
        avg_pressure_mbar = self.convert.pressure_mbar(mean(pressure_data))
        avg_soil_sat = round(mean(soil_moisture_data), 2)
        avg_wind_speed = round((mean(wind_speed_data)), 2)
        avg_co2 = round(mean(co2_data), 2)
        avg_tvoc = round(mean(tvoc_data), 2)

        unit_system = self.general_config.get_setting('units', 'unit')
        if unit_system == 'imperial':
            date = self.ts.get_imperial_date_string()
            temperature_units = 'F'
            speed_units = 'MPH'
        else:
            date = self.ts.get_metric_date_string()
            temperature_units = 'C'
            speed_units = 'm/s'

        subject = 'Daily Summary {}'.format(date)
        message = 'Subject: {}\n\n' \
                  'Environment Overview:\n\n'.format(subject)
        message += 'Min Temperature: {} {}\n' \
                   'Average Temperature: {} {}\n' \
                   'Max Temperature: {} {}\n'.format(min_temperature, temperature_units,
                                                     avg_temperature, temperature_units,
                                                     max_temperature, temperature_units)
        message += '\n'
        message += 'Min Humidity: {}%\n' \
                   'Average Humidity: {}%\n' \
                   'Max Humidity: {}%\n'.format(min_humidity, avg_humidity, max_humidity)
        message += '\n'
        message += 'Min Pressure: {} mbar\n' \
                   'Average Pressure: {} mbar\n' \
                   'Max Pressure: {} mbar\n'.format(min_pressure_mbar, avg_pressure_mbar, max_pressure_mbar)
        message += '\n'
        message += 'Min Soil Saturation: {}%\n' \
                   'Average Soil Saturation: {}%\n' \
                   'Max Soil Saturation: {}%\n'.format(min_soil_sat, avg_soil_sat, max_soil_sat)
        message += '\n'
        message += 'Min Wind Speed: {} {}\n' \
                   'Average Wind Speed: {} {}\n' \
                   'Max Wind Speed: {} {}\n'.format(min_wind_speed, speed_units,
                                                    avg_wind_speed, speed_units,
                                                    max_wind_speed, speed_units)
        message += '\n'
        message += 'Min CO2: {} PPM\n' \
                   'Average CO2: {} PPM\n' \
                   'Max CO2: {} PPM\n'.format(min_co2, avg_co2, max_co2)
        message += '\n'
        message += 'Min TVOC: {} PPB\n' \
                   'Average TVOC: {} PPB\n' \
                   'Max TVOC: {} PPB\n'.format(min_tvoc, avg_tvoc, max_tvoc)
        dataobj = {
            'timestamp': self.ts.get_timestamp(),
            'type': 'Daily Summary',
            'users_notified': True
        }
        users = self.email_config.get_list_setting('notify', 'emails')
        sent = self.__send_email(subject, message, users)
        if sent is False:
            sent = self.__send_email(subject, message, users)
        dataobj['users_notified'] = sent
        self.alerts_db.insert(dataobj)
        print(dataobj)


def main():
    notify = Notify()
    # notify.daily_summary(force=True)
    ts = Timestamps()
    config = Settings('general.config')
    monitor_interval = config.get_int_setting('notify', 'monitor_interval')
    monitor_start = 0
    try:
        while True:
            if ts.get_timestamp() - monitor_start > monitor_interval:
                notify.monitor_nodes()
                notify.daily_summary()
                monitor_start = ts.get_timestamp()
    except KeyboardInterrupt:
        exit(0)


if __name__ == '__main__':
    main()
