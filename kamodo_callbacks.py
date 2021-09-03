import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

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


def make_item(i):

    if i == 3:
        return dbc.Button(
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
                    ]),
                    dbc.Row([dbc.Collapse(
                        dbc.CardBody(f"This is the content of group {i}..."),
                        id=f"collapse-3",
                        is_open=False,
                    )], className="justify-content-center")
                ], className="iri-card model-card", id="iri-card")
            ],
            id=f"group-3-toggle",
            className="iri-collapse-button",
            n_clicks=0,
        )

    elif i == 2:
        return dbc.Button(
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
                    ]),
                    dbc.Row([dbc.Collapse(
                        dbc.CardBody(f"This is the content of group {i}..."),
                        id=f"collapse-2",
                        is_open=False,
                    )], className="justify-content-center")

                ], className="gitm-card model-card", id="gitm-card"),
            ],
            id=f"group-2-toggle",
            className="gitm-collapse-button",
            n_clicks=0,
        )

    elif i == 1:
        return dbc.Button(
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
                    dbc.Row([dbc.Collapse(
                        dbc.CardBody(f"This is the content of group {i}..."),
                        id=f"collapse-1",
                        is_open=False,
                    )], className="justify-content-center")
                ], className="ctipe-card model-card", id="ctipe-card"),
            ],
            id=f"group-1-toggle",
            className="ctipe-collapse-button",
            n_clicks=0,
        )


accordion = html.Div(
    [make_item(1), make_item(2), make_item(3)], className="accordion"
)


model_cards = html.Div(
    [
        html.Div([
            html.H2("Select a Model", className="model-title"),
        ], className="row justify-content-center"),
        html.Div([
            accordion
        ], className="row justify-content-center"),
    ], className= "container model-section"
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
