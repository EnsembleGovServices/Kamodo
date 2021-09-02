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
                            dbc.CardImg(className="card-img-left", src="assets/images/satelite.png"),
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
            ]),

            dbc.Card([
                dbc.Row([
                    dbc.Col(
                        [
                            dbc.CardImg(className="card-img-left", src="assets/images/satelite.png"),
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
            ]),

            dbc.Card([
                dbc.Row([
                    dbc.Col(
                        [
                            dbc.CardImg(className="card-img-left", src="assets/images/satelite.png"),
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
            ])
        ], className="row justify-content-center"),
    ],
    className="container workflow-section"

)

card = dbc.Card([
    dbc.Row([
        dbc.Col(
            [
                dbc.CardImg(className="card-img-left", src="assets/images/satelite.png"),
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
])


# WORKFLOW CARD ENDS


def update_menubar_details(active_tab):
    if active_tab == "workflow_tab":
        return workflow_cards
    elif active_tab == "models_tab":
        return "MODELS TAB"
    elif active_tab == "datasets_tab":
        return "DATASETS TAB"
    elif active_tab == "editor_tab":
        return "EDITOR TAB"
    return html.P("This shouldn't ever be displayed...")
