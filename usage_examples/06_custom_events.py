import dash
import dash_ace
import dashvis.stylesheets
from dash import State
from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from dashvis import DashNetwork

from usage_examples._common import default_options_

app = dash.Dash(__name__, external_stylesheets=[dashvis.stylesheets.VIS_NETWORK_STYLESHEET],
                suppress_callback_exceptions=True)

network_events = [
    'click',
    'doubleClick',
    'oncontext',
    'hold',
    'release',
    'select',
    'selectNode',
    'selectEdge',
    'deselectNode',
    'deselectEdge',
    'dragStart',
    'dragging',
    'dragEnd',
    'controlNodeDragging',
    'controlNodeDragEnd',
    'hoverNode',
    'blurNode',
    'hoverEdge',
    'blurEdge',
    'zoom',
    'showPopup',
    'hidePopup',
    'startStabilizing',
    'stabilizationProgress',
    'stabilizationIterationsDone',
    'stabilized',
    'resize',
    'initRedraw',
    'beforeDrawing',
    'afterDrawing',
    'animationFinished',
    'configChange'
]

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
        "This demo shows how one can define custom front end function handlers for all events happening with the "
        "network component."),
    network,
    html.Br(),
    html.Div([
        html.H4("Select event name:"),
        dcc.Dropdown(id='event-name-selection', options=network_events),
        html.H4("Write your custom JavaScript callback:"),
        dash_ace.DashAceEditor(
            id='callback-input',
            value='''function log() {
// Write your code below
}''',
            theme='github',
            mode='javascript',
            tabSize=4,
            width='20em',
            height='15em',
            enableBasicAutocompletion=False,
            enableLiveAutocompletion=False,
            placeholder='Javascript code ...'
        ),
        html.Button("Register custom callback", id="register-on-event"),
        html.Button("De-register custom callback", id="register-off-event"),
        html.Button("Execute callback once", id="register-once-event"),
    ], style={'maxWidth': '20em'})
])


# noinspection PyUnusedLocal
@app.callback(Output('network', 'on'), Input('register-on-event', 'n_clicks'),
              State('event-name-selection', 'value'), State('callback-input', 'value'), prevent_initial_callbacks=False)
def register_single_on_function(n_clicks, selected_event, code_input):
    if not selected_event:
        return None
    else:
        return {
            'event_name': selected_event,
            'callback': code_input
        }


# noinspection PyUnusedLocal
@app.callback(Output('network', 'off'), Input('register-off-event', 'n_clicks'),
              State('event-name-selection', 'value'), State('callback-input', 'value'), prevent_initial_callbacks=False)
def register_single_off_function(n_clicks, selected_event, code_input):
    if not selected_event:
        return None
    else:
        return {
            'event_name': selected_event,
            'callback': code_input
        }


# noinspection PyUnusedLocal
@app.callback(Output('network', 'once'), Input('register-once-event', 'n_clicks'),
              State('event-name-selection', 'value'), State('callback-input', 'value'), prevent_initial_callbacks=False)
def register_single_once_function(n_clicks, selected_event, code_input):
    if not selected_event:
        return None
    else:
        return {
            'event_name': selected_event,
            'callback': code_input
        }


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
