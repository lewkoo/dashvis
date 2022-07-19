import dash
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
        "This demo shows how one can resize the network and "
        "convert coordinates between its internal coordinate system and the DOM."),
    network,
    html.Br(),
    html.Div([
        html.H4("Resize network:"),
        html.Div([
            html.A("Width: "),
            dcc.Input(id='width-input', value=500, type='number', placeholder="Width"),
        ]),
        html.Div([
            html.A("Height: "),
            dcc.Input(id='height-input', value=500, type='number', placeholder="Height"),
        ]),
        html.Button("Resize", id="resize-button"),
        html.H4("Coordinate conversion:"),
        html.H5("Inputs:"),
        html.Div([
            html.A("X: "),
            dcc.Input(id='x_input', value=100, type='number', placeholder="X"),
        ]),
        html.Div([
            html.A("Y: "),
            dcc.Input(id='y_input', value=100, type='number', placeholder="Y"),
        ]),
        html.Button("Canvas to DOM", id="canvasToDom_button"),
        html.Button("DOM to Canvas", id="domToCanvas_button"),
        html.H5("Latest results:"),
        html.Div([
            html.A("X: "),
            html.A(id='x_output')
        ]),
        html.Div([
            html.A("Y: "),
            html.A(id='y_output')
        ]),
    ]),
])


# noinspection PyUnusedLocal
@app.callback(
    [Output('network', 'canvasToDOM'),
     Output('network', 'DOMtoCanvas')],
    [Input('canvasToDom_button', 'n_clicks'),
     Input('domToCanvas_button', 'n_clicks')],
    [State('x_input', 'value'),
     State('y_input', 'value')],
    prevent_initial_callback=True
)
def initiate_coordinate_conversion(ctd_n_clicks, dtc_n_clicks, x_input, y_input):
    ctx = dash.callback_context
    button_id = None
    if not ctx.triggered_id:
        raise dash.exceptions.PreventUpdate
    else:
        button_id = ctx.triggered_id

    canvasToDom = {}
    domToCanvas = {}

    if "canvasToDom" in button_id:
        canvasToDom = {'x': x_input, 'y': y_input}

    else:
        domToCanvas = {'x': x_input, 'y': y_input}

    return canvasToDom, domToCanvas


@app.callback(Output('x_output', 'children'),
              Output('y_output', 'children'),
              Input('network', 'canvasToDOM'),
              Input('network', 'DOMtoCanvas'),
              prevent_initial_callbacks=True)
def process_coordinate_conversion(canvasToDOM, DOMtoCanvas):
    if canvasToDOM is None and DOMtoCanvas is None:
        raise dash.exceptions.PreventUpdate

    result_obj = None
    if canvasToDOM['x'] and canvasToDOM['y']:
        result_obj = canvasToDOM
    elif DOMtoCanvas['x'] and DOMtoCanvas['y']:
        result_obj = DOMtoCanvas

    if not result_obj:
        raise dash.exceptions.PreventUpdate
    else:
        return result_obj['x'], result_obj['y']


@app.callback(Output('network', 'setSize'), [
    Input('resize-button', 'n_clicks'),
    State('width-input', 'value'),
    State('height-input', 'value')
])
def resize_graph(n_clicks, cur_width, cur_height):
    if n_clicks is None:
        # PreventUpdate prevents ALL outputs updating
        raise dash.exceptions.PreventUpdate
    else:
        return {'width': str(cur_width), 'height': str(cur_height)}


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
