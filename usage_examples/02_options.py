import json
from datetime import datetime

import dash
import dash_ace
import dashvis.stylesheets
from dash import html
from dash.dependencies import Input, Output
from dashvis import DashNetwork
from usage_examples._common import default_options_

app = dash.Dash(__name__, external_stylesheets=[dashvis.stylesheets.VIS_NETWORK_STYLESHEET])

# Enable vis.js network built-it configurator UI
network_options = default_options_
network_options['configure']['enabled'] = True

network = DashNetwork(
    id='network',
    style={'height': '400px'},
    options=network_options,
    enableHciEvents=False,
    enablePhysicsEvents=False,
    enableOtherEvents=['configChange']
)

app.layout = html.Div([
    html.Header("This demo enables vis-network built-in configurator UI and shows how one can subscribe "
                "to configuration changed events to get notified whenever network configuration is altered."),
    network,
    html.Br(),
    html.Table([
        html.Tbody([
            html.Tr([
                html.Td([
                    html.Label("Configuration changed event output:"),
                    dash_ace.DashAceEditor(
                        id='configuration-changed-event-output',
                        value="",
                        theme='github',
                        mode='python',
                        readOnly=True,
                        tabSize=4,
                        height='400px',
                        enableBasicAutocompletion=False,
                        enableLiveAutocompletion=False,
                        placeholder='Python code ...'
                    )
                ]),
                html.Td([
                    html.Label("Get options from configurator output:"),
                    dash_ace.DashAceEditor(
                        id='get-options-from-configurator-output',
                        value="",
                        theme='github',
                        mode='python',
                        readOnly=True,
                        tabSize=4,
                        height='400px',
                        enableBasicAutocompletion=False,
                        enableLiveAutocompletion=False,
                        placeholder='Python code ...'
                    )
                ])
            ])
        ])
    ]),
])

server = app.server


@app.callback(
    Output('configuration-changed-event-output', 'value'),
    Input('network', 'configChange'),
)
def from_input_to_network(data):
    return json.dumps(data, sort_keys=False, indent=2)


@app.callback(
    Output('get-options-from-configurator-output', 'value'),
    Input('network', 'getOptionsFromConfigurator'),
)
def from_input_to_network(data):
    return json.dumps(data, sort_keys=False, indent=2)


if __name__ == '__main__':
    app.run_server(debug=True)
