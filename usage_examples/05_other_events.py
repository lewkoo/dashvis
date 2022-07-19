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
    enablePhysicsEvents=False,
    enableOtherEvents=True
)

app.layout = html.Div([
    html.Header("This demo shows how one can process various other events from the network component."),
    network,
    html.Br(),
    html.Div([
        dcc.Tabs(id="other-event-listeners-tabs", value='other-event-listener-tabs', vertical=True, children=[
            dcc.Tab(label='Resize', value='resize-tab'),
            dcc.Tab(label='Init Redraw', value='init-redraw-tab'),
            dcc.Tab(label='Before Drawing', value='before-drawing-tab'),
            dcc.Tab(label='Animation Finished', value='animation-finished-tab'),
            dcc.Tab(label='Config Change', value='config-change-tab'),
        ]),
        html.Div(id='other-event-listeners-tabs-content')
    ], style={'width': '100%', 'display': 'flex'}),
])

@app.callback(Output('other-event-listeners-tabs-content', 'children'),
              Input('other-event-listeners-tabs', 'value'))
def render_other_content(tab):
    if tab == 'resize-tab':
        return dcc.Markdown(id='resize_output')
    elif tab == 'init-redraw-tab':
        return dcc.Markdown(id='init_redraw_output')
    elif tab == 'before-drawing-tab':
        return dcc.Markdown(id='before_drawing_output')
    elif tab == 'animation-finished-tab':
        return dcc.Markdown(id='animation_finished_output')
    elif tab == 'config-change-tab':
        return dcc.Markdown(id='config_change_output'),

@app.callback(
    Output('resize_output', 'children'),
    Input('network', 'resize')
)
def capture_resize_output(resize):
    return '''
    Resize event produced:
    ```
    {}
    ```'''.format(pprint.pformat(resize, indent=4, width=200, compact=False, sort_dicts=True))


@app.callback(
    Output('init_redraw_output', 'children'),
    Input('network', 'initRedraw')
)
def capture_init_redraw_output(init_redraw):
    return '''
    Init redraw event produced:
    ```
    {}
    ```'''.format(pprint.pformat(init_redraw, indent=4, width=200, compact=False, sort_dicts=True))


@app.callback(
    Output('before_drawing_output', 'children'),
    Input('network', 'beforeDrawing')
)
def capture_before_drawing_output(before_drawing):
    return '''
    Before drawing event produced:
    ```
    {}
    ```'''.format(pprint.pformat(before_drawing, indent=4, width=200, compact=False, sort_dicts=True))


@app.callback(
    Output('after_drawing_output', 'children'),
    Input('network', 'afterDrawing')
)
def capture_after_drawing_output(after_drawing):
    return '''
    After drawing event produced:
    ```
    {}
    ```'''.format(pprint.pformat(after_drawing, indent=4, width=200, compact=False, sort_dicts=True))


@app.callback(
    Output('animation_finished_output', 'children'),
    Input('network', 'animationFinished')
)
def capture_animation_finished_output(animation_finished):
    return '''
    Animation finished event produced:
    ```
    {}
    ```'''.format(pprint.pformat(animation_finished, indent=4, width=200, compact=False, sort_dicts=True))


@app.callback(
    Output('config_change_output', 'children'),
    Input('network', 'configChange')
)
def capture_config_change_output(config_change):
    return '''
    Config change event produced:
    ```
    {}
    ```'''.format(pprint.pformat(config_change, indent=4, width=200, compact=False, sort_dicts=True))


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
