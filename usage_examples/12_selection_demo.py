import json
import random

import dash
import dash_ace
import dashvis.stylesheets
from dash import Input
from dash import Output
from dash import State
from dash import dcc
from dash import html
from dashvis import DashNetwork

from usage_examples._common import default_options_

app = dash.Dash(__name__, external_stylesheets=[dashvis.stylesheets.VIS_NETWORK_STYLESHEET],
                suppress_callback_exceptions=True)

network = DashNetwork(
    id='network',
    style={'height': '400px'},
    enableHciEvents=['select'],
    options=default_options_,
    enablePhysicsEvents=False,
    enableOtherEvents=False
)

app.layout = html.Div([
    html.Header(
        "This demo shows how one can use the API to control node/edge selection."),
    network,
    html.Br(),
    html.Div([
        html.Button("Get Selection", id="getSelection_button"),
        html.Button("Get Selected Nodes", id="getSelectedNodes_button"),
        html.Button("Get Selected Edges", id="getSelectedEdges_button"),
        dash_ace.DashAceEditor(
            id='data-output',
            value='''{
# Here you'll see the output of the operations triggered by the buttons above.
} 
''',
            theme='github',
            mode='python',
            tabSize=4,
            # width='20em',
            height='25em',
            enableBasicAutocompletion=False,
            enableLiveAutocompletion=False,
            placeholder='Python code ...'
        ),
    ]),
    html.Div([
        html.H5("X and Y coordinates must be in canvas space"),
        html.Div([
            html.A("X: "),
            dcc.Input(id='x_input', value=100, type='number', placeholder="X"),
        ]),
        html.Div([
            html.A("Y: "),
            dcc.Input(id='y_input', value=100, type='number', placeholder="Y"),
        ]),
        html.Button("Get Node At", id="getNodeAt_button"),
        html.Button("Get Edge At", id="getEdgeAt_button"),
        dash_ace.DashAceEditor(
            id='get-output',
            value='''{
# Here you'll see the output of the operations triggered by the buttons above.
} 
''',
            theme='github',
            mode='python',
            tabSize=4,
            # width='20em',
            height='25em',
            enableBasicAutocompletion=False,
            enableLiveAutocompletion=False,
            placeholder='Python code ...'
        ),
    ]),
    html.Div([
        html.Div([
            html.A("Node IDs:"),
            dcc.Input(id='node_ids_input', value='', type='text'),
        ]),
        html.Div([
            html.A("Edge IDs:"),
            dcc.Input(id='edge_ids_input', value='', type='text'),
        ]),
        dcc.Checklist(
            options=[
                {'label': 'Unselect All', 'value': 'unselectAll'},
                {'label': 'Highlight Edges', 'value': 'highlightEdges'},
            ],
            value=['highlightEdges'],
            id='extra_options'
        ),
        html.Button("Select Nodes", id="selectNodes_button"),
        html.Button("Select Edges", id="selectEdges_button"),
        html.Button("Set Selection", id="setSelection_button"),
        html.Button("Unselect All", id="unselectAll_button"),
    ]),
])

callback_ouputs = {
    'getSelection': Output('network', 'getSelection'),
    'getSelectedNodes': Output('network', 'getSelectedNodes'),
    'getSelectedEdges': Output('network', 'getSelectedEdges'),
}


# # noinspection PyUnusedLocal
@app.callback(
    output=callback_ouputs,
    inputs=dict(
        inputs={
            'getSelection_button': Input('getSelection_button', 'n_clicks'),
            'getSelectedNodes_button': Input('getSelectedNodes_button', 'n_clicks'),
            'getSelectedEdges_button': Input('getSelectedEdges_button', 'n_clicks'),
        }
    ),
    prevent_initial_callbacks=True
)
def handle_button_press(inputs):
    # Get the button id
    ctx = dash.callback_context
    button_id = None
    if not ctx.triggered_id:
        raise dash.exceptions.PreventUpdate
    else:
        button_id = ctx.triggered_id

    outputs = {key: None for key in callback_ouputs.keys()}
    if button_id == 'getSelection_button':
        outputs[button_id.replace('_button', '')] = {}
    else:
        outputs[button_id.replace('_button', '')] = []

    return outputs


@app.callback(
    output=Output('data-output', 'value'),
    inputs=dict(
        inputs={
            'getSelection': Input('network', 'getSelection'),
            'getSelectedNodes': Input('network', 'getSelectedNodes'),
            'getSelectedEdges': Input('network', 'getSelectedEdges'),
        }
    ),
    prevent_initial_callbacks=True
)
def handle_result_generation(inputs):
    # Get the result
    ctx = dash.callback_context

    output_data = ""
    for prop in ctx.triggered:
        output_data += json.dumps(prop, sort_keys=False, indent=2)

    return output_data


# # noinspection PyUnusedLocal
get_callback_ouputs = {
        'getNodeAt': Output('network', 'getNodeAt'),
        'getEdgeAt': Output('network', 'getEdgeAt'),
    }
@app.callback(
    output=get_callback_ouputs,
    inputs=dict(
        inputs={
            'getNodeAt_button': Input('getNodeAt_button', 'n_clicks'),
            'getEdgeAt_button': Input('getEdgeAt_button', 'n_clicks'),
        },
        state={
            'x_input': State('x_input', 'value'),
            'y_input': State('y_input', 'value'),
        }
    ),
    prevent_initial_callbacks=True
)
def handle_get_button_press(inputs, state):
    # Get the button id
    ctx = dash.callback_context
    button_id = None
    if not ctx.triggered_id:
        raise dash.exceptions.PreventUpdate
    else:
        button_id = ctx.triggered_id

    outputs = {key: None for key in get_callback_ouputs.keys()}

    outputs[button_id.replace('_button', '')] = {
        'position': {
            'x': state['x_input'],
            'y': state['y_input'],
        },
        'result': []
    }

    return outputs


@app.callback(
    output=Output('get-output', 'value'),
    inputs=dict(
        inputs={
            'getNodeAt': Input('network', 'getNodeAt'),
            'getEdgeAt': Input('network', 'getEdgeAt'),
        }
    ),
    prevent_initial_callbacks=True
)
def handle_get_results(inputs):
    # Get the result
    ctx = dash.callback_context

    output_data = ""
    for prop in ctx.triggered:
        output_data += json.dumps(prop, sort_keys=False, indent=2)

    return output_data

select_ouputs = {
    'selectNodes': Output('network', 'selectNodes'),
    'selectEdges': Output('network', 'selectEdges'),
    'setSelection': Output('network', 'setSelection'),
    'unselectAll': Output('network', 'unselectAll'),
}

# noinspection PyUnusedLocal
@app.callback(
    output=select_ouputs,
    inputs=dict(
        inputs={
            'selectNodes_button': Input('selectNodes_button', 'n_clicks'),
            'selectEdges_button': Input('selectEdges_button', 'n_clicks'),
            'setSelection_button': Input('setSelection_button', 'n_clicks'),
            'unselectAll_button': Input('unselectAll_button', 'n_clicks'),
        },
        state={
            'node_ids_input': State('node_ids_input', 'value'),
            'edge_ids_input': State('edge_ids_input', 'value'),
            'extra_options': State('extra_options', 'value'),
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

    outputs = {key: None for key in select_ouputs.keys()}
    outputs['unselectAll'] = False

    node_ids = state['node_ids_input'].replace(' ', '').split(',') if len(state['node_ids_input']) > 0 else []
    edge_ids = state['edge_ids_input'].replace(' ', '').split(',') if len(state['edge_ids_input']) > 0 else []
    unselectAll = 'unselectAll' in state['extra_options']
    highlightEdges = 'highlightEdges' in state['extra_options']

    if button_id == 'selectNodes_button':
        outputs['selectNodes'] = {
            'nodeIds': node_ids,
            'highlightEdges': highlightEdges
        }
    elif button_id == 'selectEdges_button':
        outputs['selectEdges'] = {
            'edgeIds': edge_ids,
        }
    elif button_id == 'setSelection_button':
        outputs['setSelection'] = {
            'selection': {
                'nodes': node_ids if len(node_ids) > 0 else None,
                'edges': edge_ids if len(edge_ids) > 0 else None,
            },
            'options': {
                'unselectAll': unselectAll,
                'highlightEdges': highlightEdges,
            }
        }
    elif button_id == 'unselectAll_button':
        outputs['unselectAll'] = True

    return outputs

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
