import random

import dash
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

# Generate a large random network
def generate_network():
    nodes = []
    edges = []
    # Generate random number of nodes
    num_nodes = random.randint(100, 1000)
    for i in range(0, num_nodes):
        nodes.append({
            'id': i,
            'label': 'Node ' + str(i),
            'title': 'This is Node ' + str(i),
        })
    num_edges = random.sample(range(0, num_nodes), random.randint(5, num_nodes))
    for i in num_edges:
        edges.append({
            'id': i,
            'from': i,
            'to': random.randint(0, num_nodes - 1),
            'title': 'This is Edge ' + str(i),
        })

    return {
        'nodes': nodes,
        'edges': edges
    }

network_data = generate_network()
default_options_['layout']['improvedLayout'] = False

network = DashNetwork(
    id='network',
    data=network_data,
    style={'height': '400px'},
    options=default_options_,
    enableHciEvents=False,
    enablePhysicsEvents=False,
    enableOtherEvents=False
)

app.layout = html.Div([
    html.Header(
        "This demo shows how one can use the API to control network physics."),
    network,
    html.Br(),
    html.Button("Start Simulation", id="startSimulation_button"),
    html.Button("Stop Simulation", id="stopSimulation_button"),
    html.Div([
        html.A("Number of iterations: "),
        dcc.Input(id='num_iterations', value='600', type='number'),
        html.Button("Stabilise", id="stabilize_button"),
    ]),
])

callback_ouputs = {
    'startSimulation': Output('network', 'startSimulation'),
    'stopSimulation': Output('network', 'stopSimulation'),
    'stabilize': Output('network', 'stabilize'),
}


# noinspection PyUnusedLocal
@app.callback(
    output=callback_ouputs,
    inputs=dict(
        inputs={
            'startSimulation_button': Input('startSimulation_button', 'n_clicks'),
            'stopSimulation_button': Input('stopSimulation_button', 'n_clicks'),
            'stabilize_button': Input('stabilize_button', 'n_clicks'),
        },
        state={
            'num_iterations': State('num_iterations', 'value'),
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
    if button_id == 'stabilize_button':
        outputs[button_id.replace('_button', '')] = int(state['num_iterations'])
    else:
        outputs[button_id.replace('_button', '')] = True

    return outputs


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
