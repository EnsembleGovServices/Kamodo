from dash.dependencies import Input, Output, ClientsideFunction
from psidash import load_conf, load_dash, load_components, get_callbacks, assign_callbacks
import flask
from omegaconf import OmegaConf
import numpy as np
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

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


@callbacks.update_dropdown
def update_dropdown(url):
    options = []
    value = ''
    for _ in conf:
        if _ in conf['workflows']:
            options.append(dict(label=_, value=_))
            value = _
    return options, value


@callbacks.update_content
def update_content(value, data):
    # this needs to initialize content or load current state of buttons (e.g. n_clicks)
    if value is None:
        raise PreventUpdate
    if data is None:
        data = dict(workflow=value)
        data[value] = conf[value] # store initial params
    else:
        params = data[value]['params'] # get current parameters

    params = conf[value]

    return load_components(conf[value], imports), data

@callbacks.update_save_state
def update_save_state(n_clicks, data):
    if n_clicks is None:
        raise PreventUpdate

    if data is None:
        data = {'children': [], 'n_clicks': 0}
    else:
        previous_clicks = data['n_clicks']

    for i in range(n_clicks):
        if i >= previous_clicks:
            data['children'].append(dict(
                id='my-graph-{}'.format(i),
                children='Graph {}'.format(i),
                ))
    print(data['n_clicks'])
    for _ in data['children']:
        print(' {}'.format(_))

    data['n_clicks'] = n_clicks
    return data

@callbacks.render_click_content
def render_click_content(ts, data):
    if ts is None:
        raise PreventUpdate
    children = []
    for params in data['children']:
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

