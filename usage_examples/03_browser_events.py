import json
import pprint
from datetime import datetime

import dash
import dash_ace
import dashvis.stylesheets
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dashvis import DashNetwork
from usage_examples._common import default_options_

app = dash.Dash(__name__, external_stylesheets=[dashvis.stylesheets.VIS_NETWORK_STYLESHEET],
                suppress_callback_exceptions=True)

network = DashNetwork(
    id='network',
    style={'height': '400px'},
    options=default_options_,
    enableHciEvents=True,
    enablePhysicsEvents=False,
    enableOtherEvents=False
)

app.layout = html.Div([
    html.Header("This demo shows how one can process various user-driven events from the network component."),
    network,
    html.Br(),
    html.H4("Select HCI type callback event type below: "),
    html.Div([
        dcc.Tabs(id="hci-event-listeners-tabs", value='hci-event-listener-tabs', vertical=True, children=[
            dcc.Tab(label='Click', value='click-tab'),
            dcc.Tab(label='Double Click', value='double-click-tab'),
            dcc.Tab(label='On Context', value='on-context-tab'),
            dcc.Tab(label='Hold and Release', value='hold-release-tab'),
            dcc.Tab(label='Select', value='select-tab'),
            dcc.Tab(label='Select - Deselect Node and Edge', value='select-deselect-tab'),
            dcc.Tab(label='Dragging', value='dragging-tab'),
            dcc.Tab(label='Control node dragging', value='control-node-dragging-tab'),
            dcc.Tab(label='Hover - Blur Node and Edge', value='hover-blur-tab'),
            dcc.Tab(label='Zoom', value='zoom-tab'),
            dcc.Tab(label='Popup', value='popup-tab'),
        ]),
        html.Div(id='hci-event-listeners-tabs-content')
    ], style={'width': '100%', 'display': 'flex'}),
])


@app.callback(Output('hci-event-listeners-tabs-content', 'children'),
              Input('hci-event-listeners-tabs', 'value'))
def render_hci_content(tab):
    if tab == 'click-tab':
        return dcc.Markdown(id='click_output')
    elif tab == 'double-click-tab':
        return dcc.Markdown(id='double_click_output')
    elif tab == 'on-context-tab':
        return dcc.Markdown(id='on_context_output')
    elif tab == 'hold-release-tab':
        return html.Div([
            dcc.Markdown(id='hold_output'),
            dcc.Markdown(id='release_output')
        ])
    elif tab == 'select-tab':
        return dcc.Markdown(id='select_output')
    elif tab == 'select-deselect-tab':
        return html.Div([
            dcc.Markdown(id='select_node_output'),
            dcc.Markdown(id='select_edge_output'),
            dash_ace.DashAceEditor(
                id='deselect_node_output',
                value="",
                theme='github',
                mode='python',
                readOnly=True,
                tabSize=4,
                height='400px',
                enableBasicAutocompletion=False,
                enableLiveAutocompletion=False,
                placeholder='Python code ...'
            ),
            dash_ace.DashAceEditor(
                id='deselect_edge_output',
                value="",
                theme='github',
                mode='python',
                readOnly=True,
                tabSize=4,
                height='400px',
                enableBasicAutocompletion=False,
                enableLiveAutocompletion=False,
                placeholder='Python code ...'
            ),
        ])
    elif tab == 'dragging-tab':
        return html.Div([
            dcc.Markdown(id='drag_start_output'),
            dcc.Markdown(id='dragging_output'),
            dcc.Markdown(id='drag_end_output')
        ])
    elif tab == 'control-node-dragging-tab':
        return html.Div([
            dcc.Markdown(id='control_node_dragging_output'),
            dcc.Markdown(id='control_node_drag_end_output')
        ])
    elif tab == 'hover-blur-tab':
        return html.Div([
            dcc.Markdown(id='hover_node_output'),
            dcc.Markdown(id='blur_node_output'),
            dcc.Markdown(id='hover_edge_output'),
            dcc.Markdown(id='blur_edge_output')
        ])
    elif tab == 'zoom-tab':
        return html.Div([
            dcc.Markdown(id='zoom_output')
        ])
    elif tab == 'popup-tab':
        return html.Div([
            dcc.Markdown(id='show_popup_output'),
            dcc.Markdown(id='hide_popup_output')
        ])


@app.callback(
    Output('click_output', 'children'),
    Input('network', 'click')
)
def capture_click_output(click):
    return '''
    Click event produced:
    ```
    {}
    ```'''.format(pprint.pformat(click, indent=4, width=200, compact=False, sort_dicts=True))


@app.callback(
    Output('double_click_output', 'children'),
    Input('network', 'doubleClick')
)
def capture_double_click_output(double_click):
    return '''
    Double click event produced:
    ```
    {}
    ```'''.format(pprint.pformat(double_click, indent=4, width=200, compact=False, sort_dicts=True))


@app.callback(
    Output('on_context_output', 'children'),
    Input('network', 'oncontext')
)
def capture_on_context_output(oncontext):
    return '''
    On context event produced:
    ```
    {}
    ```'''.format(pprint.pformat(oncontext, indent=4, width=200, compact=False, sort_dicts=True))


@app.callback(
    Output('hold_output', 'children'),
    [Input('network', 'hold')]
)
def capture_hold_output(hold):
    return '''
    Hold event produced:
    ```
    {}
    ```'''.format(pprint.pformat(hold, indent=4, width=200, compact=False, sort_dicts=True))


@app.callback(
    Output('release_output', 'children'),
    [Input('network', 'release')]
)
def capture_release_output(release):
    return '''
    Release event produced:
    ```
    {}
    ```'''.format(pprint.pformat(release, indent=4, width=200, compact=False, sort_dicts=True))


@app.callback(
    Output('select_output', 'children'),
    Input('network', 'select')
)
def capture_select_output(select):
    return '''
    Selection event produced:
    ```
    {}
    ```'''.format(pprint.pformat(select, indent=4, width=200, compact=False, sort_dicts=True))


@app.callback(
    Output('select_node_output', 'children'),
    Input('network', 'selectNode')
)
def capture_select_node_output(select_node):
    return '''
    Select node event produced:
    ```
    {}
    ```'''.format(pprint.pformat(select_node, indent=4, width=200, compact=False, sort_dicts=True))


@app.callback(
    Output('deselect_node_output', 'value'),
    Input('network', 'deselectNode')
)
def capture_deselect_node_output(deselect_node):

    if deselect_node is not None:
        return json.dumps(deselect_node, sort_keys=False, indent=4)
    else:
        raise dash.exceptions.PreventUpdate

@app.callback(
    Output('select_edge_output', 'children'),
    Input('network', 'selectEdge')
)
def capture_select_edge_output(select_edge):
    return '''
    Select edge event produced:
    ```
    {}
    ```'''.format(pprint.pformat(select_edge, indent=4, width=200, compact=False, sort_dicts=True))


@app.callback(
    Output('deselect_edge_output', 'value'),
    Input('network', 'deselectEdge')
)
def capture_deselect_output(deselect_edge):

    if deselect_edge is not None:
        return json.dumps(deselect_edge, sort_keys=False, indent=4)
    else:
        raise dash.exceptions.PreventUpdate
    
@app.callback(
    Output('drag_start_output', 'children'),
    Input('network', 'dragStart')
)
def capture_drag_start_output(drag_start):
    return '''
    Drag start event produced:
    ```
    {}
    ```'''.format(pprint.pformat(drag_start, indent=4, width=200, compact=False, sort_dicts=True))


@app.callback(
    Output('dragging_output', 'children'),
    Input('network', 'dragging')
)
def capture_dragging_output(dragging):
    return '''
    Dragging event produced:
    ```
    {}
    ```'''.format(pprint.pformat(dragging, indent=4, width=200, compact=False, sort_dicts=True))


@app.callback(
    Output('drag_end_output', 'children'),
    Input('network', 'dragEnd')
)
def capture_drag_end_output(drag_end):
    return '''
    Drag end event produced:
    ```
    {}
    ```'''.format(pprint.pformat(drag_end, indent=4, width=200, compact=False, sort_dicts=True))


@app.callback(
    Output('control_node_dragging_output', 'children'),
    Input('network', 'controlNodeDragging')
)
def capture_control_node_dragging_output(control_node_dragging):
    return '''
    Control node dragging event produced:
    ```
    {}
    ```'''.format(pprint.pformat(control_node_dragging, indent=4, width=200, compact=False, sort_dicts=True))


@app.callback(
    Output('control_node_drag_end_output', 'children'),
    Input('network', 'controlNodeDragEnd')
)
def capture_control_node_drag_end_output(drag_end):
    return '''
    Control node drag end event produced:
    ```
    {}
    ```'''.format(pprint.pformat(drag_end, indent=4, width=200, compact=False, sort_dicts=True))


@app.callback(
    Output('hover_node_output', 'children'),
    Input('network', 'hoverNode')
)
def capture_hover_node_output(hover_node):
    return '''
    Hover node event produced:
    ```
    {}
    ```'''.format(pprint.pformat(hover_node, indent=4, width=200, compact=False, sort_dicts=True))


@app.callback(
    Output('blur_node_output', 'children'),
    Input('network', 'blurNode')
)
def capture_blur_node_output(blur_node):
    if blur_node is not None:
        return '''
        Blur node event produced:
        ```
        {}
        ```'''.format(pprint.pformat(blur_node, indent=4, width=200, compact=False, sort_dicts=True))


@app.callback(
    Output('hover_edge_output', 'children'),
    Input('network', 'hoverEdge')
)
def capture_hover_edge_output(hover_edge):
    return '''
    Hover edge event produced:
    ```
    {}
    ```'''.format(pprint.pformat(hover_edge, indent=4, width=200, compact=False, sort_dicts=True))


@app.callback(
    Output('blur_edge_output', 'children'),
    Input('network', 'blurEdge')
)
def capture_deselect_output(blur_edge):
    if blur_edge is not None:
        return '''
        Blur edge event produced:
        ```
        {}
        ```'''.format(pprint.pformat(blur_edge, indent=4, width=200, compact=False, sort_dicts=True))


@app.callback(
    Output('zoom_output', 'children'),
    Input('network', 'zoom')
)
def capture_deselect_output(zoom):
    if zoom is not None:
        return '''
        Zoom event produced:
        ```
        {}
        ```'''.format(pprint.pformat(zoom, indent=4, width=200, compact=False, sort_dicts=True))


@app.callback(
    Output('show_popup_output', 'children'),
    Input('network', 'showPopup')
)
def capture_show_popup_output(show_popup):
    if show_popup is not None:
        return '''
        Show popup event produced:
        ```
        {}
        ```'''.format(pprint.pformat(show_popup, indent=4, width=200, compact=False, sort_dicts=True))


@app.callback(
    Output('hide_popup_output', 'children'),
    Input('network', 'hidePopup')
)
def capture_hide_popup_output(hide_popup):
    return '''
    Hide popup event produced:
    ```
    {}
    ```'''.format(pprint.pformat(hide_popup, indent=4, width=200, compact=False, sort_dicts=True))


if __name__ == '__main__':
    app.run_server(debug=True)
