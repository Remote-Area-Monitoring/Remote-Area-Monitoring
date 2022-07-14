from source.util.database import Database
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_daq as daq
from source.util.settings import Settings
from source.util.conversions import Convert
from source.website.map import Map
from source.util.image import Image
from source.util.timekeeper import Timestamps


class Notification:
    def __init__(self):
        self.ts = Timestamps()
        self.config = Settings('general.config')
        self.db = Database(self.config.get_setting('databases', 'notify_users_db'))

    def __get_rows(self):
        rows = list()
        break_row = dbc.Row([dbc.Col([html.Br()], width='auto')], justify='center')
        rows.append(break_row)

        users = self.db.get_all()
        num_users = len(users)
        active = self.config.get_bool_setting('notify', 'active')
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
                            dbc.Badge(status_label, color="success", className="me-1")
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
                    html.P('Edit Personal Settings'),
                    dbc.Row([
                        dbc.FormFloating(
                            [
                                dbc.Input(type="email", id='user-notify-email-input',
                                          placeholder="example@internet.com"),
                                dbc.Label("Email address"),
                            ]),
                    ], justify='center'),
                    break_row,
                    dbc.Row([
                        dbc.Button('Edit User Settings', id='user-notify-settings-button', n_clicks=0),
                    ], justify='center')
                ], className="h-100 p-5 bg-light border rounded-3")
            ], width='auto')
        ], justify='center')
        rows.append(notification_manager)

        rows.append(break_row)
        return rows

    def get_layout(self):
        return html.Div(self.__get_rows())