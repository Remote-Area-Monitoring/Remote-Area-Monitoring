import plotly.graph_objects as go
from plotly.subplots import make_subplots
from database import Database
from timekeeper import Timestamps


def basic_fig_example():
    db = Database('solar_log.json')
    ts = Timestamps()
    data = db.get_records()  # start_date=ts.get_custom_timestamp(2022, )
    count = 0
    x_data = list()
    y_data = list()
    for record in data:
        x_data.append(count)
        y_data.append(record['current'])
        count += 1
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines+markers', name='Current (mA)'))
    fig.update_layout(title='Solar Statistics over Time')
    fig.show()


def two_axis_example():
    db = Database('solar_log.json')
    ts = Timestamps()
    data = db.get_records()  # start_date=ts.get_custom_timestamp(2022, )
    count = 0
    x_data = list()
    y_data = list()
    for record in data:
        if record['current'] < -1000:
            continue
        x_data.append(count)
        y_data.append(record['current'])
        count += 1
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace((go.Scatter(x=x_data, y=y_data, mode='lines+markers', name='Current (mA)')),
                  secondary_y=False)
    count = 0
    x_data = list()
    y_data = list()
    for record in data:
        if record['bus_voltage'] > 15:
            continue
        x_data.append(count)
        y_data.append(record['bus_voltage'])
        count += 1
    fig.add_trace((go.Scatter(x=x_data, y=y_data, mode='lines+markers', name='Voltage (V)')),
                  secondary_y=True)
    # Add figure title
    fig.update_layout(
        title_text="Battery Current and Voltage"
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Minutes")

    # Set y-axes titles
    fig.update_yaxes(title_text="Current (mA)", secondary_y=False)
    fig.update_yaxes(title_text="Voltage (V)", secondary_y=True)

    fig.show()

def main():
    two_axis_example()


if __name__ == '__main__':
    main()