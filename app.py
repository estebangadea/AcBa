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
indicador_dict={"FF":[8.2,10],
                    "HT":[3.1,4.2],
                    "VBC":[3.8,5.4],
                    "RM":[4.2,6.3],
                    "ABT":[6.0,7.6]}
indcolor_dict={"FF":["white","#fcccfa","#f734ef"],
                    "HT":["#ed0000","#ed6f00","#eddd00"],
                    "VBC":["#edce02","#03a843","#0476c7"],
                    "RM":["#f5225a","#f58f22","#f5ee22"],
                    "ABT":["#e8d900","#029e0c","#0032fa"]}

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(
    className="",
    children=[
        html.Div(
            className="unlp-banner",
            children=[
                html.A(
                    id="unlp-logo",
                    children=[html.Img(src=app.get_asset_url("unlp-logo.png"))],
                    href="/Portal",
                ),
                html.H2("Titulación de una muestra de vinagre"),
                html.A(
                    id="gh-link",
                    children=["View on GitHub"],
                    href="https://github.com/estebangadea/AcBa",
                    style={"color": "black", "border": "solid 1px black"},
                ),
                html.Img(src=app.get_asset_url("GitHub-Mark-64px.png")),
            ],
        ),
        html.Div(
            className="container",
            children=[
                html.Img(src=app.get_asset_url("image933.png")),
                html.Div(
                    className="text-block",
                    children=[
                        html.H6("Seleccione volúmenes adecuados"),
                        html.H6("para realizar la dilución y"),
                        html.H6("minimizar el error de la bureta.")
                        ],
                    ),
                html.Div(
                    className="tit-graph",
                    children=[
                        dcc.Graph(id='graph-with-slider'),
                        ],
                    ),


                html.Label(
                    [
                        html.Div(["Volumen de la pipeta (ml)"]),
                        dcc.Slider(
                            id='pipeta-slider',
                            min=df['pipeta'].min(),
                            max=df['pipeta'].max(),
                            value=df['pipeta'].min(),
                            marks={str(pipeta): str(pipeta) for pipeta in df['pipeta'].unique()},
                            step=None
                            ),
                        ], style={'width': '300px', 'display': 'inline-block', 'margin-left':'30px'},
                    ),
                html.Label(
                    [
                        html.Div(["Volumen del matraz aforado (ml)"]),
                        dcc.Slider(
                            id='matraz-slider',
                            min=df['matraz'].min(),
                            max=df['matraz'].max(),
                            value=df['matraz'].min(),
                            marks={str(matraz): str(matraz) for matraz in df['matraz'].unique()},
                            step=None
                            ),
                        ], style={'width': '300px', 'display': 'inline-block', 'margin-left':'50px' },
                    ),
                html.Div(
                    [
                        html.Div(["Indicador"]),
                        dcc.Dropdown(
                            id='ind-dropdown',
                            options=[
                                {'label': 'Fenolftaleina', 'value': 'FF'},
                                {'label': 'Heliantina', 'value': 'HT'},
                                {'label': 'Verde de Bromocresol', 'value': 'VBC'},
                                {'label': 'Rojo de Metilo', 'value': 'RM'},
                                {'label': 'Azul de Bromotimol', 'value': 'ABT'}
                            ],
                            value='FF'
                            ),
                        ], style={'width': '200px', 'display': 'inline-block', 'margin-left':'50px' },
                    ),
                ],
            ),
        ],
    )


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('pipeta-slider', 'value'),
    Input('matraz-slider', 'value'),
    Input('ind-dropdown', 'value')])
def update_figure(selected_pipeta, selected_matraz, selected_value):

    f_vol = np.arange(1,25,0.2)
    f_ph = qa_utils.construct_curve(4.76, 0.8326394*selected_pipeta/selected_matraz)
    fig = go.Figure(data=go.Scatter(y=f_ph, x=f_vol,line_color='black'))
    fig.add_shape(go.layout.Shape(
        # filled Rectangle
            name='lower',
            type="rect",
            x0=1,
            y0=2,
            x1=24.8,
            y1=8.2,
            fillcolor="white",
            layer='below',
            line_width=0
        )
        )

    fig.add_shape(go.layout.Shape(
            # filled Rectangle
            name='middle',
            type="rect",
            x0=1,
            y0=8.2,
            x1=24.8,
            y1=10,
            fillcolor="#fcccfa",
            layer='below',
            line_width=0
            )
            )
    fig.add_shape(go.layout.Shape(
            # filled Rectangle
            name='higher',
            type="rect",
            x0=1,
            y0=10,
            x1=24.8,
            y1=13.5,
            fillcolor="#f734ef",
            layer='below',
            line_width=0
            )
            )
    fig.update_shapes(dict(y1=indicador_dict[selected_value][0],
                            fillcolor=indcolor_dict[selected_value][0]),
                        selector=dict(y0=2))
    fig.update_shapes(patch=dict(y0=indicador_dict[selected_value][0],
                                y1=indicador_dict[selected_value][1],
                                fillcolor=indcolor_dict[selected_value][1]),
                            selector=dict(name='middle'))
    fig.update_shapes(patch=dict(y0=indicador_dict[selected_value][1],
                                fillcolor=indcolor_dict[selected_value][2]),
                            selector=dict(name='higher'))
    fig.update_xaxes(showline=True,
                    linewidth=2,
                    linecolor='black')
    fig.update_yaxes(showline=True,
                    linewidth=2,
                    linecolor='black')
    fig.update_layout(
                        xaxis_title = "Volumen de base (ml)",
                        yaxis_title = "pH",
                        xaxis_showgrid = False,
                        yaxis_showgrid = False,
                        margin=dict(
                        l=0,
                        r=10,
                        b=10,
                        t=10,)
                        )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
