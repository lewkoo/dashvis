import json

import dash
import dash_ace
import dashvis.stylesheets
from dash import State
from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from dashvis import DashNetwork
from _common import str_to_dict, dict_to_str

from usage_examples._common import default_options_

app = dash.Dash(__name__, external_stylesheets=[dashvis.stylesheets.VIS_NETWORK_STYLESHEET],
                suppress_callback_exceptions=True)

network = DashNetwork(
    id='network',
    style={'height': '400px'},
    options=default_options_,
    enableHciEvents=False,
    enablePhysicsEvents=False,
    enableOtherEvents=False
)

app.layout = html.Div([
    html.Header(
        "This demo shows how one can use the API to get information on nodes and edges."),
    network,
    html.Br(),
    html.Div([
        html.Div([
            html.A("Comma-separated list of Node IDs: "),
            dcc.Input(id='node_ids_input', value='', type='text'),
        ]),
        html.Div([
            html.A("Direction (for get connected nodes call): "),
            dcc.Dropdown(id='direction_dropdown', options=['from', 'to'], value='from'),
        ]),
        html.Button("Get Positions", id="getPositions_button"),
        html.Button("Get Position", id="getPosition_button"),
        html.Button("Get Bounding Box", id="getBoundingBox_button"),
        html.Button("Get Connected Nodes", id="getConnectedNodes_button"),
        html.Button("Get Connected Edges", id="getConnectedEdges_button"),
        dash_ace.DashAceEditor(
            id='results',
            value="",
            theme='github',
            mode='python',
            tabSize=4,
            # width='20em',
            height='15em',
            enableBasicAutocompletion=False,
            enableLiveAutocompletion=False,
            placeholder='Query results will be displayed here ...'
        ),
        html.H4("Move node:"),
        html.Div([
            html.A("Node ID to move:"),
            dcc.Input(id='move_node_ids_input', value='', type='text'),
        ]),
        html.H5("X and Y coordinates must be in canvas space"),
        html.Div([
            html.A("X: "),
            dcc.Input(id='x_input', value=100, type='number', placeholder="X"),
        ]),
        html.Div([
            html.A("Y: "),
            dcc.Input(id='y_input', value=100, type='number', placeholder="Y"),
        ]),
        html.Button("Move node", id="moveNode_button"),
    ])
])

callback_ouputs = {
    'getPositions': Output('network', 'getPositions'),
    'getPosition': Output('network', 'getPosition'),
    'getBoundingBox': Output('network', 'getBoundingBox'),
    'getConnectedNodes': Output('network', 'getConnectedNodes'),
    'getConnectedEdges': Output('network', 'getConnectedEdges'),
    'moveNode': Output('network', 'moveNode'),
}


# noinspection PyUnusedLocal
@app.callback(
    output=callback_ouputs,
    inputs=dict(
        inputs={
            'getPositions_button': Input('getPositions_button', 'n_clicks'),
            'getPosition_button': Input('getPosition_button', 'n_clicks'),
            'getBoundingBox_button': Input('getBoundingBox_button', 'n_clicks'),
            'getConnectedNodes_button': Input('getConnectedNodes_button', 'n_clicks'),
            'getConnectedEdges_button': Input('getConnectedEdges_button', 'n_clicks'),
            'moveNode_button': Input('moveNode_button', 'n_clicks'),
        },
        state={
            'node_ids_input': State('node_ids_input', 'value'),
            'direction_dropdown': State('direction_dropdown', 'value'),
            'x_input': State('x_input', 'value'),
            'y_input': State('y_input', 'value'),
        }
    ),
    prevent_initial_callbacks=True
)
def handle_button_press(inputs, state):
    # Get the button id
    ctx = dash.callback_context
    button_id = None
    if not ctx.triggered_id:
        raise dash.exceptions.PreventUpdate
    else:
        button_id = ctx.triggered_id

    outputs = {key: None for key in callback_ouputs.keys()}

    node_ids = state['node_ids_input'].replace(' ', '').split(',')

    node_ids = node_ids if button_id == 'getPositions_button' else node_ids[0]

    if button_id == 'getPositions_button':
        outputs['getPositions'] = {
            'nodeIds': node_ids,
            'result': None
        }
    elif button_id == 'getConnectedNodes_button':
        outputs['getConnectedNodes'] = {
            'nodeId': node_ids,
            'direction': state['direction_dropdown'],
            'result': ['']
        }
    elif button_id == 'moveNode_button':
        outputs['moveNode'] = {
            'nodeId': node_ids,
            'x': state['x_input'],
            'y': state['y_input']
        }
    else:
        outputs[button_id.replace('_button', '')] = {
            'nodeId': node_ids,
            'result': None
        }

    return outputs


@app.callback(
    output=Output('results', 'value'),
    inputs=dict(
        inputs={
            'getPositions': Input('network', 'getPositions'),
            'getPosition': Input('network', 'getPosition'),
            'getBoundingBox': Input('network', 'getBoundingBox'),
            'getConnectedNodes': Input('network', 'getConnectedNodes'),
            'getConnectedEdges': Input('network', 'getConnectedEdges'),
        }
    ),
    prevent_initial_callbacks=True
)
def handle_result_generation(inputs):
    # Get the result
    ctx = dash.callback_context

    output_data = ""
    for prop in ctx.triggered:
        if prop['value'] and any(key in prop['value'] for key in ['nodeId', 'nodeIds'] ):
            output_data += json.dumps(prop['value'], sort_keys=False, indent=2)

    return output_data


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
