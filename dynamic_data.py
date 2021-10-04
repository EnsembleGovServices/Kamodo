from dash.dependencies import Input, Output, ClientsideFunction
from psidash import load_conf, load_dash, load_components, get_callbacks, assign_callbacks
import flask

import numpy as np

# +
conf = load_conf('dynamic_data.yaml')

# app = dash.Dash(__name__, server=server) # call flask server

import dash

server = flask.Flask(__name__) # define flask app.server

conf['app']['server'] = server

app = load_dash(__name__, conf['app'], conf.get('import'))

app.layout = load_components(conf['layout'], conf.get('import'))

if 'callbacks' in conf:
    callbacks = get_callbacks(app, conf['callbacks'])
    assign_callbacks(callbacks, conf['callbacks'])

psidash_reserved = [
    'layout',
    'import',
    'external_stylesheets',
    'external_scripts',
    'app',
    'run_server',
    'layout',
    'callbacks'
    ]


@callbacks.update_dropdown
def update_dropdown(url):
    options = []
    value = ''
    for _ in conf:
        if _ not in psidash_reserved:
            options.append(dict(label=_, value=_))
            value = _
    return options, value


@callbacks.update_content
def update_content(value):
    return load_components(conf[value], conf.get('import'))

def pass_through(value):
    return value

server = app.server

if __name__ == '__main__':
    app.run_server(
        host=conf['run_server']['host'],
        port=conf['run_server']['port'],
        debug=True,
        dev_tools_hot_reload=False,
        extra_files=['dynamic_data.yaml']
        )

