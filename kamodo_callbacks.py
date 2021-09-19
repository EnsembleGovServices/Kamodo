import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from kamodo import KamodoAPI, Kamodo
from plotly import graph_objs as go

from constants import PYSAT_URL

import logging
from dash.exceptions import PreventUpdate

logger = logging.getLogger(__name__)



# WORKFLOW CARDS START
workflow_cards = html.Div(
    [
        html.Div([
            html.H2("Select a Workflow", className="workflow-title"),
        ], className="row justify-content-center"),
        html.Div([
            dbc.Card([
                dbc.Row([
                    dbc.Col(
                        [
                            dbc.CardImg(className="card-img-left workflow-card-img", src="assets/images/workflow1.png"),
                        ],
                        lg=6,
                    ),
                    dbc.Col(
                        [
                            dbc.CardBody(
                                [
                                    html.H3("Satellite Fly Through", className="workflow-header"),
                                ]
                            ),
                        ],
                        lg=6,
                    ),
                ])
            ], className="workflow-card"),
            dbc.Card([
                dbc.Row([
                    dbc.Col(
                        [
                            dbc.CardImg(className="card-img-left workflow-card-img", src="assets/images/workflow2.png"),
                        ],
                        lg=6,
                    ),
                    dbc.Col(
                        [
                            dbc.CardBody(
                                [
                                    html.H3("Model Coupling", className="workflow-header"),
                                ]
                            ),
                        ],
                        lg=6,
                    ),
                ])
            ], className="workflow-card"),

            dbc.Card([
                dbc.Row([
                    dbc.Col(
                        [
                            dbc.CardImg(className="card-img-left workflow-card-img", src="assets/images/workflow3.png"),
                        ],
                        lg=6,
                    ),
                    dbc.Col(
                        [
                            dbc.CardBody(
                                [
                                    html.H3("Data / Model Comparison", className="workflow-header"),
                                ]
                            ),
                        ],
                        lg=6,
                    ),
                ])
            ], className="workflow-card")
        ], className="row justify-content-center"),
    ],
    className="container workflow-section"

)

# WORKFLOW CARDS ENDS

# MODEL CARDS START


ctipe_details = html.Div([
    dbc.Row([
        html.P(
            'The Coupled Thermosphere Ionosphere Plasmasphere Electrodynamics Model (CTIPe) model consists of four distinct components:'),
        html.P(
            'A high-latitude ionosphere model; A mid and low-latitude ionosphere/plasmasphere model; An electrodynamical calculation of the global dynamo electric field.')
    ], className="justify-content-center"),
    dbc.Row([
        html.P('Model Developer(s) Timothy Fuller-Rowell, Mihail Codrescu, et al. NOAA Space Weather Prediction Center')
    ], className="justify-content-center"),
    dbc.Row([
        dbc.Input(id="ctipe-input-one", placeholder="Type something...", type="text", style={'margin': '3% 0'}),
    ], className="justify-content-center"),
    dbc.Row([
        dbc.Input(id="ctipe-input-two", placeholder="Type something...", type="text", style={'margin': '3% 0'}),
    ], className="justify-content-center")
], className="ctipe-details")


def get_model_types(model_name):
    if model_name == "CTIPe":
        return dbc.ListGroup(
            [
                dbc.ListGroupItem("Couple", className="model-type-name"),
                dbc.ListGroupItem("Thermosphere", className="model-type-name"),
                dbc.ListGroupItem("Lonosphere", className="model-type-name"),
                dbc.ListGroupItem("Plasmasphere", className="model-type-name"),
            ], className=f"model-types {model_name}-list-group")
    elif model_name == "GITM":
        return dbc.ListGroup(
            [
                dbc.ListGroupItem("Thermosphere", className="model-type-name"),
                dbc.ListGroupItem("Lonosphere", className="model-type-name"),
            ], className=f"model-types {model_name}-list-group")
    else:
        return dbc.ListGroup(
            [
                dbc.ListGroupItem("Lonosphere", className="model-type-name"),
            ], className=f"model-types {model_name}-list-group")


def make_model_card(model_name):
    return html.Div([dbc.Button(
        [
            dbc.Card([
                dbc.Row([
                    dbc.Col(
                        [
                            html.H1(f"{model_name}", className="model-header")
                        ],
                        lg=6,
                    ),
                    dbc.Col(
                        [
                            dbc.CardBody(
                                [
                                    get_model_types(model_name)
                                ]
                            ),
                        ],
                        lg=6,
                    ),
                ]),
            ], className=f"{model_name}-card model-card", id=f"{model_name}-card"),
        ],
        id=f"{model_name}-toggle",
        className=f"{model_name}-collapse-button",
        n_clicks=0,
    ),
        dbc.Collapse([
            ctipe_details
        ], id=f"collapse-{model_name}", className='container', is_open=False)
    ], className='model-accordion-card')


accordion = html.Div(
    [make_model_card('CTIPe'), make_model_card('GITM'), make_model_card('IRI')], className="accordion", id="accordion"
)

model_cards = html.Div(
    [
        html.Div([
            html.H2("Select a Model", className="model-title"),
        ], className="row justify-content-center"),
        html.Div([
            accordion
        ], className="row justify-content-center"),
    ], className="container model-section"
)


# MODEL CARDS END


# TESTING  START

# TESTING END


def update_menubar_details(active_tab):
    if active_tab == "workflow_tab":
        return workflow_cards
    elif active_tab == "models_tab":
        return model_cards
    elif active_tab == "datasets_tab":
        return "DATASETS TAB"
    elif active_tab == "editor_tab":
        return "EDITOR TAB"
    return html.P("This shouldn't ever be displayed...")


def toggle_model_cards_accordion(n1, n2, n3, is_open1, is_open2, is_open3):
    ctx = dash.callback_context

    if not ctx.triggered:
        return False, False, False
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "CTIPe-toggle" and n1:
        return not is_open1, False, False
    elif button_id == "GITM-toggle" and n2:
        return False, not is_open2, False
    elif button_id == "IRI-toggle" and n3:
        return False, False, not is_open3
    return False, False, False


# PLOT DYNAMICALLY START #

def make_graph(button_id):
    plot_function_name = button_id.split('-')[0]
    k = KamodoAPI(PYSAT_URL)
    graph = dcc.Graph(
        id='my-graph',
        className= plot_function_name + '-my-graph',
        figure=k.plot(plot_function_name),
    )
    return graph


def graph_function(input_value, data_value, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, remove):
    ctx = dash.callback_context
    new_graph = dcc.Graph(
        id='my-graph-empty',
        figure={}
    )
    if not ctx.triggered:
        return new_graph
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        print(f"PLOT GRAPH")

    if input_value:
        plot_custom_function(input_value, data_value)

    if button_id == "B_north-button" and n1:
        return make_graph(button_id)
    elif button_id == "B_up-button" and n2:
        return make_graph(button_id)
    elif button_id == "B_west-button" and n3:
        return make_graph(button_id)
    elif button_id == "B_IGRF_north-button" and n4:
        return make_graph(button_id)
    elif button_id == "B_IGRF_up-button" and n5:
        return make_graph(button_id)
    elif button_id == "B_IGRF_west-button" and n6:
        return make_graph(button_id)
    elif button_id == "latitude-button" and n7:
        return make_graph(button_id)
    elif button_id == "longitude-button" and n8:
        return make_graph(button_id)
    elif button_id == "altitude-button" and n9:
        return make_graph(button_id)
    elif button_id == "dB_zon-button" and n10:
        return make_graph(button_id)
    elif button_id == "dB_mer-button" and n11:
        return make_graph(button_id)
    elif button_id == "bB_par-button" and n12:
        return make_graph(button_id)
    elif button_id == "year-button" and n13:
        return make_graph(button_id)
    elif button_id == "dayofyear-button" and n14:
        return make_graph(button_id)
    elif button_id == "B_flag-button" and n15:
        return make_graph(button_id)
    elif button_id == "remove-graph" and remove:
        print(f"REMOVE GRAPH {n2}")
        return new_graph
    else:
        return new_graph

# PLOT DYNAMICALLY END #

# MODEL NAME LIST START #

import numpy as np

k = Kamodo(
    f=lambda x=np.linspace(-5, 5, 30): x**2,
    g=lambda y=np.linspace(-1,1, 30): y**3)

def get_selected_model_names(n_clicks):
    if n_clicks not in [0, None]:
        # k = KamodoAPI(PYSAT_URL)

        model_list = []
        i = 0 # only increment when there's a symbol without parenthesis
        for index in k:
            if '(' not in str(index):
                symbolic_fname = str(k.signatures[str(index)]['symbol'])
                fname = str(index)
                model_list.append(
                    dbc.ListGroupItem(
                        # symbolic_fname,
                        fname,
                        id={'type': 'model-plot-button', 'index':i},
                        n_clicks=0,
                        action=True
                    ),
                )
                i += 1

        return dbc.ListGroup(model_list, className="model-type-list")

def init_kamodo_graphs(children):
    if children is None:
        raise PreventUpdate
    graph_list = []
    print(children)
    for index, _ in enumerate(children['props']['children']):
        fname = _['props']['children']
        print(index, fname)
        graph_list.append(
            dbc.ListGroupItem(
                dcc.Graph(
                    id={'type': 'kamodo-plot', 'index': index},
                    # figure=k.plot(fname),
                    )))
    print('initialized graphs')
    return graph_list

# MODEL NAME LIST END #

# CUSTOM FUNCTION PLOTTING START #

def plot_custom_function(input_value, data_value):
    return f" INPUT: {input_value} DATA: {data_value}"

# CUSTOM FUNCTION PLOTTING END #

# TESTING GRAPH FUNCTION START #

# def graph_function_testing(n_clicks, id):
def graph_function_testing(n_clicks, id):
    print('button clicked {}'.format(n_clicks))
    if n_clicks is None:
        raise PreventUpdate
    print('hello')
    logger.debug("HELLO")
    logger.debug(f"INPUT : {n_clicks} id: {id['index']}")
    fsymbol = list(k.signatures.keys())[id['index']]
    print(fsymbol)
    return k.plot(fsymbol)

# TESTING GRAPH FUNCTION END #