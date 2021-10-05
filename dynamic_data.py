from dash.dependencies import Input, Output, ClientsideFunction
from psidash import load_conf, load_dash, load_components, get_callbacks, assign_callbacks
import flask
from omegaconf import OmegaConf
import numpy as np
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import hydra
import dash_html_components as html
from dash_katex import DashKatex

import re

# +
conf = load_conf('dynamic_data.yaml')

# app = dash.Dash(__name__, server=server) # call flask server

import dash

server = flask.Flask(__name__) # define flask app.server

conf['app']['server'] = server
imports = conf.get('import')

app = load_dash(__name__, conf['app'], imports)

app.layout = load_components(conf['layout'], imports)

if 'callbacks' in conf:
    callbacks = get_callbacks(app, conf['callbacks'])
    assign_callbacks(callbacks, conf['callbacks'])

def load_models(conf):
    models = {}
    if 'models' in conf:
        for _ in conf['models']:
            model_confs = OmegaConf.load(_)
            for model_name in model_confs:
                model_conf = model_confs[model_name]
                models[model_name] = hydra.utils.instantiate(model_conf)
        return models

# models = load_models(conf)
workflow_models = {}
for workflow_name in conf['workflows']:
    workflow = conf['workflows'][workflow_name]
    if workflow is None:
        continue
    workflow_models[workflow_name] = load_models(workflow)



@callbacks.update_models
def update_models(workflow):
    if workflow not in workflow_models:
        raise PreventUpdate
    children = []
    models = workflow_models[workflow]
    for _ in models:
        model = models[_]
        model_children = [html.H2(_)]

        for _ in model.signatures:
            latex_str = model.to_latex(_, mode='inline').replace('$','')
            latex_str = re.sub(r"\\\\",r"\\", latex_str)
            model_children.append(DashKatex(expression=latex_str))
        model_children.append(html.Details([html.Summary('model docstring'), model.__doc__]))
        children.append(html.Div(model_children))
    return children

@callbacks.update_dropdown
def update_dropdown(url):
    """get available workflow options from the conf"""
    options = []
    value = ''
    for _ in conf:
        if _ in conf['workflows']:
            options.append(dict(label=_, value=_))
            value = _
    return options, value


@callbacks.update_content
def update_content(workflow):
    """load the workflow from the configuration"""
    if workflow is None:
        raise PreventUpdate

    workflow_components = load_components(conf[workflow], imports)
    return workflow_components

@callbacks.update_click_store
def update_click_store(n_clicks, data):
    if n_clicks is None:
        print('n_clicks not initialized')
        raise PreventUpdate
    if n_clicks == 0:
        raise PreventUpdate

    if data is None:
        data = dict(rows={}, n_clicks=0)

    rows = data.get('rows', dict())
    row_number = len(rows)

    print('new row_number: {}'.format(row_number))
    data['rows'][row_number] = dict(
        id='my-graph-{}'.format(row_number),
        children='Graph {}'.format(row_number),
        )

    print('updated rows: {}'.format(len(data['rows'])))
    for _, row in data['rows'].items():
        print(' {}: {}'.format(_, row))

    return data

@callbacks.render_click_content
def render_click_content(ts, data):
    """whenever timestamp changes, render the current list of clicks"""
    if ts is None:
        raise PreventUpdate
    children = []
    for _, params in data['rows'].items():
        children.append(dbc.ListGroupItem(
            dbc.Button(color='primary',**params)))
    return dbc.ListGroup(children)

server = app.server

if __name__ == '__main__':
    app.run_server(
        host=conf['run_server']['host'],
        port=conf['run_server']['port'],
        debug=True,
        dev_tools_hot_reload=False,
        extra_files=['dynamic_data.yaml']
        )

