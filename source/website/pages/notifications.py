from source.util.database import Database
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_daq as daq
from source.util.settings import Settings
from source.util.conversions import Convert
from source.website.map import Map
from source.util.image import Image
from source.util.timekeeper import Timestamps
import plotly.graph_objects as go


class Notification:
    def __init__(self):
        self.ts = Timestamps()
        self.config = Settings('secret.config')
        self.general_config = Settings('general.config')
        self.notify_db = Database(self.general_config.get_setting('databases', 'alerts_db_path'))

    def __get_rows(self):
        rows = list()
        break_row = dbc.Row([dbc.Col([html.Br()], width='auto')], justify='center')
        rows.append(break_row)

        user_emails = self.config.get_list_setting('notify', 'emails')
        if user_emails is not None:
            num_users = len(user_emails)
        else:
            num_users = 0
        active = self.general_config.get_bool_setting('notify', 'active')
        if active:
            status_label = 'Ready: '
            status_color = 'success'
            if num_users < 1:
                status_label += 'No Users'
            else:
                status_label += '{} Users'.format(num_users)
        else:
            status_label = 'Inactive'
            status_color = 'secondary'

        notification_manager = dbc.Row([
            dbc.Col([
                html.Div([
                    html.H5("Notifications", className="display-3"),
                    html.Hr(className="my-2"),
                    html.P('Notify Status'),
                    dbc.Row([
                        dbc.Col([
                            dbc.Badge(status_label, color=status_color, className="me-1")
                        ], width='auto'),
                    ], justify='center'),
                    break_row,
                    html.Hr(className="my-2"),
                    html.P('Quick Controls'),
                    dbc.Row([
                        dbc.Col([
                            dbc.Switch(
                                id='notify-enable-switch',
                                label='Notifications',
                                value=active,
                            )
                        ], width='auto'),
                    ], justify='center'),
                    html.Hr(className="my-2"),
                    html.P('Add or Remove Email'),
                    dbc.Row([
                        dbc.FormFloating(
                            [
                                dbc.Input(type="email", id='notify-email-input',
                                          placeholder="example@internet.com"),
                                dbc.Label("Email address"),
                            ]),
                    ], justify='center'),
                    break_row,
                    dbc.Row([
                        html.Div([
                            dbc.Button('Add Email', id='notify-add-email-button', n_clicks=0),
                            dbc.Button('Remove Email', id='notify-remove-email-button', n_clicks=0, color='secondary'),
                        ], className="d-grid gap-2 col-6 mx-auto",)

                    ], justify='center'),
                    break_row,
                    dbc.Row([
                        html.Div([], id='notify-email-status-label')
                    ], justify='center'),
                ], className="h-100 p-5 bg-light border rounded-3")
            ], width='auto')
        ], justify='center')
        rows.append(notification_manager)

        rows.append(break_row)

        table_title_row = dbc.Row([dbc.Col([html.H2('Notifications Over the Last 24 Hours')], width='auto')],
                                  justify='center')
        rows.append(table_title_row)
        rows.append(break_row)

        notifications = self.notify_db.get_records(self.ts.get_24h_timestamp())
        if notifications is None or len(notifications) < 1:
            headers = ['Notifications']
            values = [['No Notifications Sent']]
        else:
            notifications = sorted(notifications, key=lambda d: d['timestamp'])
            headers = ['Date', 'Type', 'Users Notified', 'Notes']
            # keys = ['timestamp', 'type', 'users_notified']
            values = list()
            timestamps = list()
            types = list()
            users_notified = list()
            notes = list()
            for record in notifications:
                if 'timestamp' in record and 'type' in record and 'users_notified' in record:
                    timestamps.append(self.ts.get_day_timestring(record['timestamp']))
                    types.append(record['type'])
                    users_notified.append(record['users_notified'])
                    if 'node_id' in record:
                        notes.append('Node ID: {}'.format(record['node_id']))
                    else:
                        notes.append('None')
            values.append(timestamps)
            values.append(types)
            values.append(users_notified)
            values.append(notes)
        fig = go.Figure(
            data=[
                go.Table(
                    header={'values': headers},
                    cells={'values': values}
                )
            ]
        )
        fig.update_layout(
            margin=dict(l=15, r=15, t=0, b=15),
        )

        notify_table = dbc.Row([
            dbc.Col([
                html.Div([dcc.Graph(figure=fig)])
            ], width='auto'),
        ], justify='center')
        rows.append(notify_table)
        rows.append(break_row)
        return rows

    def get_layout(self):
        return html.Div(self.__get_rows())