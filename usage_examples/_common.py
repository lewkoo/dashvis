import ast

height_ = '100%'
width_ = '100%'

nodes_ = {
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
}

edges_ = {
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
}

physics_ = {
    'enabled': True,
}

manipulation_ = {
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
}

interaction_ = {
    'hover': True,
    'hoverConnectedEdges': True,
    'multiselect': True,
    'keyboard': {
        'enabled': True,
        'bindToWindow': False,
        'autoFocus': True,
    },
    'navigationButtons': True,
}

layout_ = {
    'improvedLayout': True,
}

configure_ = {
    'enabled': False,
    'showButton': False,
}

default_options_ = dict(autoResize=True, height=height_, width=width_, configure=configure_, nodes=nodes_, edges=edges_,
                        layout=layout_, interaction=interaction_, manipulation=manipulation_, physics=physics_, )


def str_to_dict(str_data: str) -> dict:
    try:
        return ast.literal_eval(str_data)
    except Exception as e:
        print(e)
        return {}

def dict_to_str(dict_data: dict) -> str:
    try:
        return ast.literal_eval(dict_data)
    except Exception as e:
        print(e)
        return {}
