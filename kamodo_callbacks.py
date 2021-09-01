import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc


def update_menubar_details(active_tab):
    if active_tab == "workflow_tab":
        return "WORKFLOW TAB"
    elif active_tab == "models_tab":
        return "MODELS TAB"
    elif active_tab == "datasets_tab":
        return "DATASETS TAB"
    elif active_tab == "editor_tab":
        return "EDITOR TAB"
    return html.P("This shouldn't ever be displayed...")