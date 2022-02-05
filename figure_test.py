from dash.dependencies import Input, Output, State
from app import app

import dash 
from dash.dependencies import Output, Input
import dash_html_components as html 
import dash_bootstrap_components as dbc
import dash_core_components as dcc 
import plotly 
import random 
import plotly.graph_objs as go 
import plotly.express as px
from collections import deque 
import flask
from datetime import datetime
import pandas as pd

"""
trace = []
trace.append(go.Scatter(
    x=[0,10], 
    y=[5], 
    hoverinfo='x+y',
    mode='lines+markers',
    line=dict(width=0.5, color='rgb(255, 0, 0)'),
    stackgroup='two', # define stack group
    name = 'M'
))
traces = [trace]
data = [val for sublist in traces for val in sublist]

figure = go.Figure({ 'data': data,
                'layout': go.Layout(
                    yaxis_range=(0, 50),
                    plot_bgcolor= 'rgba(0, 0, 0, 0)', 
                    paper_bgcolor= 'rgba(0, 0, 0, 0)',
                    xaxis=dict(range=[0,10], type='date'),
                )

    })
figure.add_shape(
    go.layout.Shape(type='line', xref='x', yref='y', editable=True,
                    x0=3, y0=0, x1=3, y1=45, line={'dash': 'dash',"color":"RoyalBlue","width":12}),

)

figure.show()
"""
names=['RL_CTIM1','RL_QTIM1']
dd_select = pd.read_csv('data\MELTEMI_DD_dummy.csv', parse_dates=['date_time'], sep=";")
bar = go.Figure(data=[
    go.Bar(name='Predicted', x=names, y=dd_select[['RL_CTIM1','RL_QTIM1']].iloc[2]),
    go.Bar(name='Obersver', x=names, y=dd_select[['RL_CTIM1_obv','RL_QTIM1_obv']].iloc[2])
])
bar.update_layout(barmode='group')
bar.show()