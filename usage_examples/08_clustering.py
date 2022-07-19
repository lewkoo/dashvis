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
        "This demo shows how one can control network clustering using Dash callbacks."),
    network,
    html.Br(),
    html.Div([
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
            # width='20em',
            # height='15em',
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
            # width='20em',
            # height='15em',
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
            # width='20em',
            # height='15em',
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
            # width='20em',
            # height='15em',
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
            # width='20em',
            # height='15em',
            enableBasicAutocompletion=False,
            enableLiveAutocompletion=False,
            placeholder='Python code ...'
        ),
        html.Button("Find node", id="findNode_button"),
    ])
])

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

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
