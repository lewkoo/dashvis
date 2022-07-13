import ast
import pprint
import random

import dash_ace
from dash import State
from dash import dcc
from dashvis import DashNetwork
import dash
from dash.dependencies import Input, Output
from dash import html


def str_to_dict(str_data: str) -> dict:
    try:
        return ast.literal_eval(str_data)
    except Exception as e:
        print(e)
        return {}


app = dash.Dash(__name__, suppress_callback_exceptions=True)

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
    options=dict(
        autoResize=True,
        height='100%',
        width='100%',
        configure={
            'enabled': False,
            'showButton': False,
        },
        nodes={
            'shape': 'box',
            'margin': 10,
            'size': 25,
            'borderWidth': 2,
            'borderWidthSelected': 2,
            'font': {
                'multi': 'markdown',
                'align': 'center',
            },
            'labelHighlightBold': True,
            'widthConstraint': {
                'minimum': 30,
                'maximum': 100,
            }
        },
        edges={
            'color': {
                'inherit': 'both',
            },
            'arrows': {
                'to': {
                    'enabled': True,
                    'scaleFactor': 0.5
                }
            },
            'chosen': False,
            "arrowStrikethrough": False,
            'smooth': {
                'type': "dynamic",
                'roundness': 0.5,
            }
        },
        layout={
            'improvedLayout': True,
        },
        interaction={
            'hover': True,
            'hoverConnectedEdges': True,
            'multiselect': True,
            'keyboard': {
                'enabled': True,
                'bindToWindow': False,
                'autoFocus': True,
            },
            'navigationButtons': True,
        },
        manipulation={
            'enabled': True,
            'initiallyActive': True,
            'addNode': """function(nodeData,callback) {
      nodeData.label = 'hello world';
      callback(nodeData);
}""",
            'addEdge': True,
            'editNode': None,
            'editEdge': True,
            'deleteNode': True,
            'deleteEdge': True,
        },
        physics={
            'enabled': True,
        },
    ),
    enableHciEvents=True,
    enablePhysicsEvents=True,
    enableOtherEvents=True
)

app.layout = html.Div([
    network,
    html.Table([
        html.Tbody([
            html.Tr([
                html.Td([
                    html.H4("Generate new network data:"),
                    html.Button("Generate", id="generate-button"),
                    html.H4("Destroy network:"),
                    html.Button("Destroy", id="destroy-button"),
                    html.H4("Redraw network:"),
                    html.Button("Redraw", id="redraw-button"),
                    html.H4("Network seed:", id="seed-label"),
                    html.H4("Selection: ", id="selection-label"),
                    html.H4("Selected nodes: ", id='selected-nodes'),
                    html.H4("Selected edges: ", id='selected-edges'),
                ], style={'paddingRight': '3em'}),
            ], style={'verticalAlign': 'top'}),
            html.Tr([
                html.Td([
                    html.H4("Manipulation methods:"),
                    html.Button("Enabled Edit Mode", id="enableEditMode_button"),
                    html.Button("Disable Edit Mode", id="disableEditMode_button"),
                    html.Button("Add Mode Mode", id="addNodeMode_button"),
                    html.Button("Edit Node", id="editNode_button"),
                    html.Button("Add Edge Mode", id="addEdgeMode_button"),
                    html.Button("Edit Edge Mode", id="editEdgeMode_button"),
                    html.Button("Delete Selected", id="deleteSelected_button"),
                    dcc.Store(id='button_press_sink')
                ])
            ]),
            html.Tr([
                html.Td([
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
                html.Td([
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
                ], style={'maxWidth': '20em'})]),
            html.Td([
                html.H4("Clustering"),
                html.H4("Write your custom joinCondition(...) callback:"),
                dash_ace.DashAceEditor(
                    id='join-condition-input',
                    value='''function(nodeOptions) {
    return nodeOptions.cid === 1;
} 
// Note if using clusterByConnection then you need to provide a function which accepts two parameters (see vis.js docs)
  ''',
                    theme='github',
                    mode='javascript',
                    tabSize=4,
                    width='20em',
                    height='15em',
                    enableBasicAutocompletion=False,
                    enableLiveAutocompletion=False,
                    placeholder='Javascript code ...'
                ),
                html.H4("Write your custom processProperties(...) callback:"),
                dash_ace.DashAceEditor(
                    id='process-properties-input',
                    value='''function (clusterOptions, childNodes, childEdges) {
    return clusterOptions;
} 
''',
                    theme='github',
                    mode='javascript',
                    tabSize=4,
                    width='20em',
                    height='15em',
                    enableBasicAutocompletion=False,
                    enableLiveAutocompletion=False,
                    placeholder='Javascript code ...'
                ),
                html.H4("Write your custom clusterNodeProperties(...) dictionary:"),
                dash_ace.DashAceEditor(
                    id='cluster-node-properties-input',
                    value='''{
# Python dictionary with node properties
} 
''',
                    theme='github',
                    mode='python',
                    tabSize=4,
                    width='20em',
                    height='15em',
                    enableBasicAutocompletion=False,
                    enableLiveAutocompletion=False,
                    placeholder='Python code ...'
                ),
                html.H4("Write your custom clusterEdgeProperties(...) dictionary:"),
                dash_ace.DashAceEditor(
                    id='cluster-edge-properties-input',
                    value='''{
# Python dictionary with edge properties
} 
''',
                    theme='github',
                    mode='python',
                    tabSize=4,
                    width='20em',
                    height='15em',
                    enableBasicAutocompletion=False,
                    enableLiveAutocompletion=False,
                    placeholder='Python code ...'
                ),
                html.Div([
                    html.A("Node ID for cluster by connection: "),
                    dcc.Input(id='cluster_node_id', value=1, type='number', placeholder="Node ID"),
                ]),
                html.Div([
                    html.A("Hubsize for cluster by hubsize: "),
                    dcc.Input(id='hubsize', value=1, type='number', placeholder="Hubsize"),
                ]),
                html.Div(
                    [
                        html.Button("Cluster", id="cluster_button"),
                        html.Button("Cluster by connection", id="clusterByConnection_button"),
                        html.Button("Cluster by hubsize", id="clusterByHubsize_button"),
                        html.Button("Cluster outliers", id="clusterOutliers_button"),
                    ]
                ),
                dash_ace.DashAceEditor(
                    id='search_results',
                    value="",
                    theme='github',
                    mode='python',
                    tabSize=4,
                    width='20em',
                    height='15em',
                    enableBasicAutocompletion=False,
                    enableLiveAutocompletion=False,
                    placeholder='Python code ...'
                ),
                html.Button("Find node", id="findNode_button"),
            ], style={'maxWidth': '20em'}),
            html.Tr([

            ])
        ])
    ], id="actions-grid"),

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
    html.H4("Select Other type callback event type below: "),
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


@app.callback(Output('seed-label', 'children'), Input('network', 'getSeed'))
def print_network_seed(network_seed):
    return f"Network seed: {network_seed}"


@app.callback(Output('selection-label', 'children'), Input('network', 'getSelection'))
def print_selection(selection):
    return f"Current selection: {selection}"


@app.callback(Output('selected-nodes', 'children'), Input('network', 'getSelectedNodes'))
def print_selected_nodes(selected_nodes):
    return f"Currently selected nodes: {selected_nodes}"


@app.callback(Output('selected-edges', 'children'), Input('network', 'getSelectedEdges'))
def print_selected_edges(selected_edges):
    return f"Currently selected edges: {selected_edges}"


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

    print("Input CanvasToDom: ", canvasToDom)
    print("Input DomToCanvas: ", domToCanvas)
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
    print("Canvas to DOM result: ", canvasToDOM)
    print("DOM to Canvas result: ", DOMtoCanvas)
    if canvasToDOM['x'] and canvasToDOM['y']:
        result_obj = canvasToDOM
    elif DOMtoCanvas['x'] and DOMtoCanvas['y']:
        result_obj = DOMtoCanvas

    if not result_obj:
        raise dash.exceptions.PreventUpdate
    else:
        return result_obj['x'], result_obj['y']


@app.callback(
    Output('network', 'cluster'),
    Input('cluster_button', 'n_clicks'),
    State('join-condition-input', 'value'),
    State('process-properties-input', 'value'),
    State('cluster-node-properties-input', 'value'),
    State('cluster-edge-properties-input', 'value'),
    prevent_initial_callbacks=False
)
def cluster(n_clicks, joinCondition, processProperties, clusterNodeProperties, clusterEdgeProperties):
    clusterNodeProperties = str_to_dict(clusterNodeProperties)
    clusterEdgeProperties = str_to_dict(clusterEdgeProperties)

    if not n_clicks:
        raise dash.exceptions.PreventUpdate
    else:
        return {
            'options': {
                'joinCondition': joinCondition,
                'processProperties': processProperties,
                'clusterNodeProperties': clusterNodeProperties,
                'clusterEdgeProperties': clusterEdgeProperties
            }
        }


@app.callback(
    Output('network', 'clusterByConnection'),
    Input('clusterByConnection_button', 'n_clicks'),
    State('cluster_node_id', 'value'),
    State('join-condition-input', 'value'),
    State('process-properties-input', 'value'),
    State('cluster-node-properties-input', 'value'),
    State('cluster-edge-properties-input', 'value'),
    prevent_initial_callbacks=False
)
def clusterByConnection(n_clicks, cluster_node_id, joinCondition, processProperties, clusterNodeProperties,
                        clusterEdgeProperties):
    clusterNodeProperties = str_to_dict(clusterNodeProperties)
    clusterEdgeProperties = str_to_dict(clusterEdgeProperties)

    if not n_clicks:
        raise dash.exceptions.PreventUpdate
    else:
        return {
            'nodeId': str(cluster_node_id),
            'options': {
                'joinCondition': joinCondition,
                'processProperties': processProperties,
                'clusterNodeProperties': clusterNodeProperties,
                'clusterEdgeProperties': clusterEdgeProperties
            }
        }


@app.callback(
    Output('network', 'clusterByHubsize'),
    Input('clusterByHubsize_button', 'n_clicks'),
    State('hubsize', 'value'),
    State('join-condition-input', 'value'),
    State('process-properties-input', 'value'),
    State('cluster-node-properties-input', 'value'),
    State('cluster-edge-properties-input', 'value'),
    prevent_initial_callbacks=False
)
def clusterByHubsize(n_clicks, hubsize, joinCondition, processProperties, clusterNodeProperties,
                     clusterEdgeProperties):
    clusterNodeProperties = str_to_dict(clusterNodeProperties)
    clusterEdgeProperties = str_to_dict(clusterEdgeProperties)

    if not n_clicks:
        raise dash.exceptions.PreventUpdate
    else:
        return {
            'hubsize': int(hubsize),
            'options': {
                'joinCondition': joinCondition,
                'processProperties': processProperties,
                'clusterNodeProperties': clusterNodeProperties,
                'clusterEdgeProperties': clusterEdgeProperties
            }
        }


@app.callback(
    Output('network', 'clusterOutliers'),
    Input('clusterOutliers_button', 'n_clicks'),
    State('join-condition-input', 'value'),
    State('process-properties-input', 'value'),
    State('cluster-node-properties-input', 'value'),
    State('cluster-edge-properties-input', 'value'),
    prevent_initial_callbacks=False
)
def clusterOutliers(n_clicks, joinCondition, processProperties, clusterNodeProperties,
                    clusterEdgeProperties):
    clusterNodeProperties = str_to_dict(clusterNodeProperties)
    clusterEdgeProperties = str_to_dict(clusterEdgeProperties)

    if not n_clicks:
        raise dash.exceptions.PreventUpdate
    else:
        return {
            'options': {
                'joinCondition': joinCondition,
                'processProperties': processProperties,
                'clusterNodeProperties': clusterNodeProperties,
                'clusterEdgeProperties': clusterEdgeProperties
            }
        }


@app.callback(
    Output('network', 'findNode'),
    Input('findNode_button', 'n_clicks'),
    State('cluster_node_id', 'value'),
    prevent_initial_callbacks=True
)
def findNode(n_clicks, nodeId):
    if not n_clicks:
        raise dash.exceptions.PreventUpdate

    return {
        'nodeId': int(nodeId),
        'result': [''],
    }


@app.callback(
    Output('search_results', 'value'),
    Input('network', 'findNode'),
    prevent_initial_callbacks=True
)
def handleFindNodeOutput(results):
    return str(results['result'])


@app.callback(Output('network', 'data'), Input('generate-button', 'n_clicks'))
def generate_new_graph_data(n_clicks):
    if n_clicks is None:
        # PreventUpdate prevents ALL outputs updating
        raise dash.exceptions.PreventUpdate

    nodes = []
    edges = []
    # Generate random number of nodes
    num_nodes = random.randint(5, 100)
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


@app.callback(Output('network', 'destroy'), Input('destroy-button', 'n_clicks'))
def destroy_graph(n_clicks):
    if n_clicks is None:
        # PreventUpdate prevents ALL outputs updating
        raise dash.exceptions.PreventUpdate
    else:
        return True


@app.callback(Output('network', 'redraw'), Input('redraw-button', 'n_clicks'))
def redraw_graph(n_clicks):
    if n_clicks is None:
        # PreventUpdate prevents ALL outputs updating
        raise dash.exceptions.PreventUpdate
    else:
        return True


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


callback_ouputs = {
    'enableEditMode': Output('network', 'enableEditMode'),
    'disableEditMode': Output('network', 'disableEditMode'),
    'addNodeMode': Output('network', 'addNodeMode'),
    'editNode': Output('network', 'editNode'),
    'addEdgeMode': Output('network', 'addEdgeMode'),
    'editEdgeMode': Output('network', 'editEdgeMode'),
    'deleteSelected': Output('network', 'deleteSelected'),
}


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
            dcc.Markdown(id='deselect_node_output'),
            dcc.Markdown(id='deselect_edge_output')
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


# @app.callback(
#     Output('deselect_node_output', 'children'),
#     Input('network', 'deselectNode')
# )
# def capture_deselect_node_output(deselect_node):
#
#     if deselect_node is not None:
#         return '''
#         Deselect node event produced:
#         ```
#         {}
#         ```'''.format(pprint.pformat(deselect_node, indent=4, width=200, compact=False, sort_dicts=True))

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


# @app.callback(
#     Output('deselect_edge_output', 'children'),
#     Input('network', 'deselectEdge')
# )
# def capture_deselect_output(deselect_edge):
#
#     if deselect_edge is not None:
#         return '''
#         Deselect node event produced:
#         ```
#         {}
#         ```'''.format(pprint.pformat(deselect_edge, indent=4, width=200, compact=False, sort_dicts=True))

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
