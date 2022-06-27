from source.util.settings import Settings


class Convert:
    def __init__(self):
        self.config = Settings('general.config')
        self.system = self.config.get_setting('units', 'unit')

    def temperature(self, value, get_string=False):
        if self.system == 'imperial':
            value = (value * (9.0 / 5.0)) + 32
            value = round(value, 2)
        if get_string:
            return '{}\xb0F'.format(value)
        return value

    def pressure_mbar(self, value):
        mbar = value / 100
        mbar = round(mbar, 2)
        return mbar

    def soil_moisture(self, value):
        value -= 900
        if value < 0:
            return 100
        value /= 2000
        value = (1 - value) * 100
        return round(value, 2)

    def wind_speed(self, value):
        if self.system == 'imperial':
            return value
        value /= 2.237
        return round(value, 2)

    def humidity(self, value):
        humidity = value + 10
        if humidity > 100:
            humidity = 100
        return round(humidity, 2)

    def power(self, value):
        return round(value / 1000, 2)

