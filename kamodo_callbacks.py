import ast

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from kamodo import KamodoAPI

from constants import PYSAT_URL

from utils.generate_2d_graph import create_2d_graph, update_2d_graph

# WORKFLOW CARDS START
from utils.generate_3d_graph import create_3d_graph

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


def graph_function(n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, remove):
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

def get_selected_model_names(n_clicks):
    if n_clicks not in [0, None]:
        k = KamodoAPI(PYSAT_URL)
        model_list = []
        for index, i in enumerate(k):
            if '(' not in str(i):
                model_list.append(
                    dbc.ListGroup(
                        [
                            # dbc.ListGroupItem(
                            #     f"{i}", id={'type': 'model-plot-button', 'index': index//2}, n_clicks=0,
                            #     action=True
                            # ),
                            dbc.ListGroupItem(
                                f"{i}", className=f"model-type-button {i}-plot", id= f'{i}-button', n_clicks=0,
                                action=True
                            ),
                        ]
                    )
                )
        return dbc.ListGroup(model_list, className="model-type-list")

# MODEL NAME LIST END #

# CUSTOM FUNCTION PLOTTING START #

def plot_custom_function(function_value, min_value, max_value):

    if not min_value:
        min_value = -10
    if not max_value:
        max_value = 10

    if function_value and min_value and max_value:
        function = function_value.split('=')[1]
        if (function.__contains__('x') or function.__contains__('X')) and (function.__contains__('y') or function.__contains__('Y')):
            figure = create_3d_graph(function)
        else:
            figure = create_2d_graph(function)

        if figure:
            new_graph = dcc.Graph(
                id='my-graph-custom',
                figure = figure,
            )
            range_slider =  dcc.RangeSlider(
                    id='my-range-slider',
                    min=int(min_value),
                    max=int(max_value),
                    step=0.5,
                    value=[-5, 5],
                    # marks={
                    #     0: int(min_value),
                    #     100: int(max_value)
                    # }
                )
            new_graph_area = html.Div([
                new_graph,
                html.Div([
                    dbc.Row(
                        [
                            # dbc.Col([
                            #     html.H5('X : ')
                            # ], width=1),
                            dbc.Col([
                                range_slider
                            ], width=12)
                        ]
                    ),
                ], id='my-range-slider-area', className='my-range-slider-area')
            ], id='my-graph-custom-area', className='my-graph-custom-area')

            return new_graph_area
        else:
            return dbc.Alert("Input valid function only...", color="danger")
    return False

# CUSTOM FUNCTION PLOTTING END #

# UPDATE CUSTOM FUNCTION GRAPH START #

def update_custom_function_graph(range_value, function_value):
    print(f"RANGE : {range_value}")
    function = function_value.split('=')[1]
    new_figure = update_2d_graph(range_value, function)
    return new_figure

# UPDATE CUSTOM FUNCTION GRAPH END #
