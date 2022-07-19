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
    options=default_options_,
    enableHciEvents=False,
    enablePhysicsEvents=False,
    enableOtherEvents=False
)

app.layout = html.Div([
    html.Header(
        "This demo shows how one can use the API to control network viewport."),
    network,
    html.Br(),
    html.Div([
        html.Button("Get Scale", id="getScale_button"),
        html.Button("Get View Position", id="getViewPosition_button"),
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
        html.H5("Focus Node ID: "),
        dcc.Input(id='focus_node_id_input', value="", type='text', placeholder="Focus Node ID"),
        html.H5("Focus options:"),
        html.Div([
            html.A("Scale:"),
            dcc.Input(id='focus_scale', value=5, type='number'),
        ]),
        html.Div([
            html.A("Offset:"),
            html.A("X:"),
            dcc.Input(id='x_offset', value=0, type='number'),
            html.A("Y:"),
            dcc.Input(id='y_offset', value=0, type='number'),
        ]),
        html.Div([
            dcc.Checklist(
                options=[{'label': 'Locked', 'value': 'locked'}],
                value=[],
                id='focus_locked'
            ),
        ]),
        html.Div([
            dcc.Checklist(
                options=[
                    {'label': 'Animation enabled', 'value': 'enabled'},
                ],
                value=[],
                id='animation_enabled'
            ),
            html.A("Duration:"),
            dcc.Input(id='animation_duration', value=0, type='number'),
            html.A("Easing function:"),
            dcc.Dropdown(id='easing_function', options=['linear', 'easeInQuad', 'easeOutQuad', 'easeInOutQuad',
                                                        'easeInCubic', 'easeOutCubic', 'easeInOutCubic', 'easeInQuart',
                                                        'easeOutQuart', 'easeInOutQuart', 'easeInQuint', 'easeOutQuint',
                                                        'easeInOutQuint'], value='linear'),
        ]),
        html.Button("Focus", id="focus_button"),

    ]),
    html.Div([
        html.H5("Move To Options: "),
        html.Div([
            html.A("Scale:"),
            dcc.Input(id='move_to_scale', value=5, type='number'),
        ]),
        html.Div([
            html.A("Position:"),
            html.A("X:"),
            dcc.Input(id='x_position', value=0, type='number'),
            html.A("Y:"),
            dcc.Input(id='y_position', value=0, type='number'),
        ]),
        html.Div([
            html.A("Offset:"),
            html.A("X:"),
            dcc.Input(id='move_to_x_offset', value=0, type='number'),
            html.A("Y:"),
            dcc.Input(id='move_to_y_offset', value=0, type='number'),
        ]),
        html.Div([
            dcc.Checklist(
                options=[{'label': 'Locked', 'value': 'locked'}],
                value=[],
                id='move_to_locked'
            ),
        ]),
        html.Div([
            dcc.Checklist(
                options=[
                    {'label': 'Animation enabled', 'value': 'enabled'},
                ],
                value=[],
                id='move_to_animation_enabled'
            ),
            html.A("Duration:"),
            dcc.Input(id='move_to_animation_duration', value=0, type='number'),
            html.A("Easing function:"),
            dcc.Dropdown(id='move_to_easing_function', options=['linear', 'easeInQuad', 'easeOutQuad', 'easeInOutQuad',
                                                                'easeInCubic', 'easeOutCubic', 'easeInOutCubic',
                                                                'easeInQuart',
                                                                'easeOutQuart', 'easeInOutQuart', 'easeInQuint',
                                                                'easeOutQuint',
                                                                'easeInOutQuint'], value='linear'),
        ]),
        html.Button("Move To", id="moveTo_button"),

    ])
])

callback_ouputs = {
    'getScale': Output('network', 'getScale'),
    'getViewPosition': Output('network', 'getViewPosition'),
}


# # noinspection PyUnusedLocal
@app.callback(
    output=callback_ouputs,
    inputs=dict(
        inputs={
            'getScale_button': Input('getScale_button', 'n_clicks'),
            'getViewPosition_button': Input('getViewPosition_button', 'n_clicks'),
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
    if button_id == 'getScale_button':
        outputs[button_id.replace('_button', '')] = 0
    else:
        outputs[button_id.replace('_button', '')] = {}

    return outputs


@app.callback(
    output=Output('data-output', 'value'),
    inputs=dict(
        inputs={
            'getScale': Input('network', 'getScale'),
            'getViewPosition': Input('network', 'getViewPosition'),
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


@app.callback(
    Output('network', 'focus'),
    Input('focus_button', 'n_clicks'),
    State('focus_node_id_input', 'value'),
    State('focus_scale', 'value'),
    State('x_offset', 'value'),
    State('y_offset', 'value'),
    State('focus_locked', 'value'),
    State('animation_enabled', 'value'),
    State('animation_duration', 'value'),
    State('easing_function', 'value'),
    prevent_initial_callbacks=True
)
def handle_focus(n_clicks, node_id, scale, x_offset, y_offset, locked, animation_enabled,
                 animation_duration, easing_function):
    if not n_clicks:
        raise dash.exceptions.PreventUpdate

    return {
        'nodeId': node_id,
        'options': {
            'scale': scale,
            'offset': {
                'x': x_offset,
                'y': y_offset
            },
            'locked': False if not locked else True,
            'animation': False if not animation_enabled else {
                'duration': animation_duration,
                'easingFunction': easing_function
            }
        }
    }


@app.callback(
    Output('network', 'moveTo'),
    Input('moveTo_button', 'n_clicks'),
    State('move_to_scale', 'value'),
    State('x_position', 'value'),
    State('y_position', 'value'),
    State('move_to_x_offset', 'value'),
    State('move_to_y_offset', 'value'),
    State('move_to_locked', 'value'),
    State('move_to_animation_enabled', 'value'),
    State('move_to_animation_duration', 'value'),
    State('move_to_easing_function', 'value'),
    prevent_initial_callbacks=True
)
def handle_move_to(n_clicks, scale, x_position, y_position, x_offset, y_offset, locked, animation_enabled,
                   animation_duration, easing_function):
    if not n_clicks:
        raise dash.exceptions.PreventUpdate

    return {
        'options': {
            'position': {
                'x': x_position,
                'y': y_position
            },
            'scale': scale,
            'offset': {
                'x': x_offset,
                'y': y_offset
            },
            'locked': False if not locked else True,
            'animation': False if not animation_enabled else {
                'duration': animation_duration,
                'easingFunction': easing_function
            }
        }
    }


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
