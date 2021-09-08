import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from kamodo import KamodoAPI
from plotly import graph_objs as go

from constants import PYSAT_URL

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


def make_item(i):
    if i == 3:
        return html.Div([
            dbc.Button(
                [
                    dbc.Card([
                        dbc.Row([
                            dbc.Col(
                                [
                                    html.H1("IRI", className="model-header")
                                ],
                                lg=6,
                            ),
                            dbc.Col(
                                [
                                    dbc.CardBody(
                                        [
                                            dbc.ListGroup(
                                                [
                                                    dbc.ListGroupItem("Lonosphere", className="model-type-name"),
                                                ], className="model-types iri-list-group")
                                        ]
                                    ),
                                ],
                                lg=6,
                            ),
                        ])
                    ], className="iri-card model-card", id="iri-card")
                ],
                id=f"group-3-toggle",
                className="iri-collapse-button",
                n_clicks=0,
            ),
            dbc.Collapse([
                ctipe_details
            ], id=f"collapse-3", className='container', is_open=False)
        ], className='model-accordion-card')

    elif i == 2:
        return html.Div([
            dbc.Button(
                [
                    dbc.Card([
                        dbc.Row([
                            dbc.Col(
                                [
                                    html.H1("GITM", className="model-header")
                                ],
                                lg=6,
                            ),
                            dbc.Col(
                                [
                                    dbc.CardBody(
                                        [
                                            dbc.ListGroup(
                                                [
                                                    dbc.ListGroupItem("Thermosphere", className="model-type-name"),
                                                    dbc.ListGroupItem("Lonosphere", className="model-type-name"),
                                                ], className="model-types gitm-list-group")
                                        ]
                                    ),
                                ],
                                lg=6,
                            ),
                        ])
                    ], className="gitm-card model-card", id="gitm-card"),
                ],
                id=f"group-2-toggle",
                className="gitm-collapse-button",
                n_clicks=0,
            ),
            dbc.Collapse([
                ctipe_details
            ], id=f"collapse-2", className='container', is_open=False)
        ], className='model-accordion-card')

    elif i == 1:
        return html.Div([dbc.Button(
            [
                dbc.Card([
                    dbc.Row([
                        dbc.Col(
                            [
                                html.H1("CTIPe", className="model-header")
                            ],
                            lg=6,
                        ),
                        dbc.Col(
                            [
                                dbc.CardBody(
                                    [
                                        dbc.ListGroup(
                                            [
                                                dbc.ListGroupItem("Couple", className="model-type-name"),
                                                dbc.ListGroupItem("Thermosphere", className="model-type-name"),
                                                dbc.ListGroupItem("Lonosphere", className="model-type-name"),
                                                dbc.ListGroupItem("Plasmasphere", className="model-type-name"),
                                            ], className="model-types ctipe-list-group")
                                    ]
                                ),
                            ],
                            lg=6,
                        ),
                    ]),
                ], className="ctipe-card model-card", id="ctipe-card"),
            ],
            id=f"group-1-toggle",
            className="ctipe-collapse-button",
            n_clicks=0,
        ),
            dbc.Collapse([
                ctipe_details
            ], id=f"collapse-1", className='container', is_open=False)
        ], className='model-accordion-card')


accordion = html.Div(
    [make_item(1), make_item(2), make_item(3)], className="accordion", id="accordion"
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


def expand_model_card(n, is_open):
    if n:
        return not is_open
    return is_open


def toggle_accordion(n1, n2, n3, is_open1, is_open2, is_open3):
    ctx = dash.callback_context

    if not ctx.triggered:
        return False, False, False
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "group-1-toggle" and n1:
        return not is_open1, False, False
    elif button_id == "group-2-toggle" and n2:
        return False, not is_open2, False
    elif button_id == "group-3-toggle" and n3:
        return False, False, not is_open3
    return False, False, False


def graph_function(n1, n2):
    ctx = dash.callback_context
    graph = dcc.Graph(
        id='my-graph',
        figure={}
    )

    if not ctx.triggered:
        return graph
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "plot-graph" and n1:
        print(f"PLOT GRAPH {n1}")
        k = KamodoAPI(PYSAT_URL)
        graph = dcc.Graph(
            id='my-graph',
            figure=k.plot('B_north'),
        )
        return graph
    elif button_id == "remove-graph" and n2:
        print(f"REMOVE GRAPH {n2}")
        new_graph = dcc.Graph(
            id='my-graph-empty',
            figure={},
        )
        return new_graph
