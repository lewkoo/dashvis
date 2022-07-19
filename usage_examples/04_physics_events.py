import pprint

import dash
import dashvis.stylesheets
from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from dashvis import DashNetwork

from usage_examples._common import default_options_

app = dash.Dash(__name__, external_stylesheets=[dashvis.stylesheets.VIS_NETWORK_STYLESHEET],
                suppress_callback_exceptions=True)

network = DashNetwork(
    id='network',
    style={'height': '400px'},
    options=default_options_,
    enableHciEvents=False,
    enablePhysicsEvents=True,
    enableOtherEvents=False
)

app.layout = html.Div([
    html.Header("This demo shows how one can process various physics events from the network component."),
    network,
    html.Br(),
    html.H4("Select Physics type callback event type below: "),
    html.Div([
        dcc.Tabs(id="physics-event-listeners-tabs", value='physics-event-listener-tabs', vertical=True, children=[
            dcc.Tab(label='Start Stabilizing', value='start-stabilizing-tab'),
            dcc.Tab(label='Stabilization Progress', value='stabilization-progress-tab'),
            dcc.Tab(label='Stabilization Iterations Done', value='stabilization-iterations-done-tab'),
            dcc.Tab(label='Stabilized', value='stabilized-tab'),
        ]),
        html.Div(id='physics-event-listeners-tabs-content')
    ], style={'width': '100%', 'display': 'flex'}),
])

@app.callback(Output('physics-event-listeners-tabs-content', 'children'),
              Input('physics-event-listeners-tabs', 'value'))
def render_physics_content(tab):
    if tab == 'start-stabilizing-tab':
        return dcc.Markdown(id='start_stabilizing_output')
    elif tab == 'stabilization-progress-tab':
        return dcc.Markdown(id='stabilization_progress_output')
    elif tab == 'stabilization-iterations-done-tab':
        return dcc.Markdown(id='stabilization_iterations_done_output')
    elif tab == 'stabilized-tab':
        return dcc.Markdown(id='stabilized_output'),

@app.callback(
    Output('start_stabilizing_output', 'children'),
    Input('network', 'startStabilizing')
)
def capture_start_stabilizing_output(startStabilizing):
    return '''
    Start Stabilizing event produced:
    ```
    {}
    ```'''.format(pprint.pformat(startStabilizing, indent=4, width=200, compact=False, sort_dicts=True))


@app.callback(
    Output('stabilization_progress_output', 'children'),
    Input('network', 'stabilizationProgress')
)
def capture_stabilization_progress_output(stabilizationProgress):
    return '''
    Stabilization Progress event produced:
    ```
    {}
    ```'''.format(pprint.pformat(stabilizationProgress, indent=4, width=200, compact=False, sort_dicts=True))


@app.callback(
    Output('stabilization_iterations_done_output', 'children'),
    Input('network', 'stabilizationIterationsDone')
)
def capture_stabilization_iterations_done_output(stabilizationIterationsDone):
    return '''
    Stabilization iterations done event produced:
    ```
    {}
    ```'''.format(pprint.pformat(stabilizationIterationsDone, indent=4, width=200, compact=False, sort_dicts=True))


@app.callback(
    Output('stabilized_output', 'children'),
    Input('network', 'stabilized')
)
def capture_stabilized_output(stabilized):
    return '''
    Stabilized event produced:
    ```
    {}
    ```'''.format(pprint.pformat(stabilized, indent=4, width=200, compact=False, sort_dicts=True))

if __name__ == '__main__':
    app.run_server(debug=True)
