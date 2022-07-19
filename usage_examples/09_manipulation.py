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
        "This demo shows how one can control network manipulation using Dash callbacks."),
    network,
    html.Br(),
    html.Div([
        html.H4("Manipulation methods:"),
        html.Button("Enabled Edit Mode", id="enableEditMode_button"),
        html.Button("Disable Edit Mode", id="disableEditMode_button"),
        html.Button("Add Mode Mode", id="addNodeMode_button"),
        html.Button("Edit Node", id="editNode_button"),
        html.Button("Add Edge Mode", id="addEdgeMode_button"),
        html.Button("Edit Edge Mode", id="editEdgeMode_button"),
        html.Button("Delete Selected", id="deleteSelected_button")
    ])
])

callback_ouputs = {
    'enableEditMode': Output('network', 'enableEditMode'),
    'disableEditMode': Output('network', 'disableEditMode'),
    'addNodeMode': Output('network', 'addNodeMode'),
    'editNode': Output('network', 'editNode'),
    'addEdgeMode': Output('network', 'addEdgeMode'),
    'editEdgeMode': Output('network', 'editEdgeMode'),
    'deleteSelected': Output('network', 'deleteSelected'),
}

# noinspection PyUnusedLocal
@app.callback(
    output=callback_ouputs,
    inputs=dict(
        inputs={
            'enableEditMode_button': Input('enableEditMode_button', 'n_clicks'),
            'disableEditMode_button': Input('disableEditMode_button', 'n_clicks'),
            'addNodeMode_button': Input('addNodeMode_button', 'n_clicks'),
            'editNode_button': Input('editNode_button', 'n_clicks'),
            'addEdgeMode_button': Input('addEdgeMode_button', 'n_clicks'),
            'editEdgeMode_button': Input('editEdgeMode_button', 'n_clicks'),
            'deleteSelected_button': Input('deleteSelected_button', 'n_clicks'),
        }
    ),
    prevent_initial_callbacks=True
)
def handle_manipulation_methods(inputs):
    # Get the button id
    ctx = dash.callback_context
    button_id = None
    if not ctx.triggered_id:
        raise dash.exceptions.PreventUpdate
    else:
        button_id = ctx.triggered_id

    outputs = {key: False for key in callback_ouputs.keys()}
    outputs[button_id.replace('_button', '')] = True

    return outputs

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
