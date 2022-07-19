import json

import dash
import dash_ace
from dash import html
from dash.dependencies import Input, Output
from dashvis import DashNetwork
from usage_examples._common import *

app = dash.Dash(__name__)

network = DashNetwork(
    id='network',
    style={'height': '400px'},
    options=default_options_,
    enableHciEvents=False,
    enablePhysicsEvents=False,
    enableOtherEvents=False
)

data = {
    'nodes': [
        {'id': 1, 'cid': 1, 'label': 'Node 1', 'title': 'This is Node 1'},
        {'id': 2, 'cid': 1, 'label': 'Node 2', 'title': 'This is Node 2'},
        {'id': 3, 'cid': 1, 'label': 'Node 3', 'title': 'This is Node 3'},
        {'id': 4, 'label': 'Node 4', 'title': 'This is Node 4'},
        {'id': 5, 'label': 'Node 5', 'title': 'This is Node 5'}
    ],
    'edges': [
        {'from': 1, 'to': 3},
        {'from': 1, 'to': 2},
        {'from': 2, 'to': 4},
        {'from': 2, 'to': 5}
    ]
}

app.layout = html.Div([
    html.Header("This demo demonstrates how to inject network data into the Dash network component. \n"
                "Feel free to change the data structure in the editor below and see it being updated live in the graph"),
    network,
    html.Br(),
    html.Table([
        html.Tbody([
            html.Tr([
                html.Td([
                    html.Label("Network data input"),
                    dash_ace.DashAceEditor(
                        id='network-data-input',
                        value='''{
  "nodes": [
    {
      "id": 1,
      "cid": 1,
      "label": "Node 1",
      "title": "This is Node 1"
    },
    {
      "id": 2,
      "cid": 1,
      "label": "Node 2",
      "title": "This is Node 2"
    },
    {
      "id": 3,
      "cid": 1,
      "label": "Node 3",
      "title": "This is Node 3"
    },
    {
      "id": 4,
      "label": "Node 4",
      "title": "This is Node 4"
    },
    {
      "id": 5,
      "label": "Node 5",
      "title": "This is Node 5"
    }
  ],
  "edges": [
    {
      "from": 1,
      "to": 3
    },
    {
      "from": 1,
      "to": 2
    },
    {
      "from": 2,
      "to": 4
    },
    {
      "from": 2,
      "to": 5
    }
  ]
}
''',
                        theme='github',
                        mode='python',
                        tabSize=4,
                        height='400px',
                        enableBasicAutocompletion=False,
                        enableLiveAutocompletion=False,
                        placeholder='Python code ...'
                    )
                ]),
                html.Td([
                    html.Label("Network data output"),
                    dash_ace.DashAceEditor(
                        id='network-data-output',
                        value="",
                        theme='github',
                        mode='python',
                        readOnly=True,
                        tabSize=4,
                        height='400px',
                        enableBasicAutocompletion=False,
                        enableLiveAutocompletion=False,
                        placeholder='Python code ...'
                    )
                ])
            ])
        ])
    ]),
])

server = app.server


@app.callback(Output('network-data-output', 'value'),
              Input('network', 'data'))
def from_network_to_output(data):
    return json.dumps(data, sort_keys=False, indent=2)


@app.callback(
    Output('network', 'data'),
    Input('network-data-input', 'value'),
)
def from_input_to_network(data):
    if str_to_dict(data) != {}:
        return str_to_dict(data)
    else:
        raise dash.exceptions.PreventUpdate()


if __name__ == '__main__':
    app.run_server(debug=True)
