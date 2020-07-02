# -*- coding: utf-8 -*-
import os
import pathlib
import statistics
import numpy as np
from collections import OrderedDict

import pathlib as pl
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State

import qa_utils

import pandas as pd

APP_PATH = str(pl.Path(__file__).parent.resolve())

df = pd.read_csv(os.path.join(APP_PATH, os.path.join("data", "material.csv")))

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(
    className="",
    children=[
        html.Div(
            className="pkcalc-banner",
            children=[
                html.A(
                    id="dash-logo",
                    children=[html.Img(src=app.get_asset_url("dash-bio-logo.png"))],
                    href="/Portal",
                ),
                html.H2("Titulaciones Acido - Base"),
                html.A(
                    id="gh-link",
                    children=["View on GitHub"],
                    href="https://github.com/estebangadea/QA",
                    style={"color": "black", "border": "solid 1px black"},
                ),
                html.Img(src=app.get_asset_url("GitHub-Mark-64px.png")),
            ],
        ),
        html.Div(
            className="container",
            children=[
                html.Img(src=app.get_asset_url("dilution.jpg"),
                    style={'widht': '300', 'float': 'right', 'margin-top':'50px'}),
                dcc.Graph(id='graph-with-slider',
                    figure = {'layout' :{ 'float': 'right', 'height': '400', 'width': '600'}}),

                html.Label(
                    [
                        html.Div(["Volumen de la pipeta"]),
                        dcc.Slider(
                            id='pipeta-slider',
                            min=df['pipeta'].min(),
                            max=df['pipeta'].max(),
                            value=df['pipeta'].min(),
                            marks={str(pipeta): str(pipeta) for pipeta in df['pipeta'].unique()},
                            step=None
                            ),
                        ], style={'width': '40%', 'display': 'inline-block'},
                    ),
                html.Label(
                    [
                        html.Div(["Volumen del matraz"]),
                        dcc.Slider(
                            id='matraz-slider',
                            min=df['matraz'].min(),
                            max=df['matraz'].max(),
                            value=df['matraz'].min(),
                            marks={str(matraz): str(matraz) for matraz in df['matraz'].unique()},
                            step=None
                            ),
                        ], style={'width': '40%', 'display': 'inline-block', 'float':'right'},
                    ),
                ],
            ),
        ],
    )


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('pipeta-slider', 'value'),
    Input('matraz-slider', 'value')])
def update_figure(selected_pipeta, selected_matraz):

    f_vol = np.arange(1,25,0.2)
    f_ph = qa_utils.construct_curve(4.76, 0.8326394*selected_pipeta/selected_matraz)
    fig = px.line(y=f_ph, x=f_vol)

    fig.update_layout(transition_duration=500,
                        xaxis_title = "Volumen de base",
                        yaxis_title = "pH")

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
