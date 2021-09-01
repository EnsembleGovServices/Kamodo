import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc


def update_menubar_details(active_tab):
    if active_tab == "tab-1":
        return "tab1_content"
    elif active_tab == "tab-2":
        return "tab2_content"
    elif active_tab == "tab-3":
        return "tab3_content"
    elif active_tab == "tab-4":
        return "tab4_content"
    return html.P("This shouldn't ever be displayed...")