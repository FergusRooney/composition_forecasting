from dash.dependencies import Input, Output, State
from app import app

import io
import base64
import dash 
from dash.dependencies import Output, Input
from dash import html
import dash_bootstrap_components as dbc
from dash import dcc
import plotly 
import random 
import plotly.graph_objs as go 
import plotly.express as px
from collections import deque 
import flask
from datetime import datetime, timedelta
import pandas as pd
import pathlib
from tensorflow import keras

# Import TensorFlow:
import tensorflow as tf

# Local data load dummies
import os
print(os.getcwd())
print(os.path.abspath(__file__))
#MELTEMI_DF = pd.read_csv('gs:/data/MELTEMI_DF_dummy.csv', parse_dates=['date_time'], sep=';')
# MELTEMI_DD = pd.read_csv('app/data/MELTEMI_DD_dummy.csv', parse_dates=['date_time'], sep=";")
# ANSRO_DF = pd.read_csv('data/ANSRO_DF_dummy.csv', parse_dates=['date_time'], sep=';')
# ANSRO_DD = pd.read_csv('data/ANSRO_DD_dummy.csv', parse_dates=['date_time'], sep=";")
# SOLAR_DUMMY = pd.read_excel('data/solar_Data/dummy_data.xlsx')

#
# @app.callback(
#     Output('current-time', 'children'),
#     Input('time-update', 'n_intervals')
# )
# def update_current_time(n):
#     now = datetime.now()
#     dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#     return "Current date & time: "+dt_string
#
#
# @app.callback(
#     Output("collapse", "is_open"),
#     [Input("legend-collapse-button", "n_clicks")],
#     [State("collapse", "is_open")],
# )
# def toggle_collapse(n, is_open):
#     if n:
#         return not is_open
#     return is_open
#
# def parse_contents(contents, filename, dropdownName):
#     content_type, content_string = contents.split(',')
#     return "File selected: " + str(filename) + " Dropdown selected: " + dropdownName, content_string
#
#
# @app.callback(Output('upload-data-text', 'children'),
#               Output('currentUpload', 'data'),
#               Input('upload-data', 'contents'),
#               Input('dropdown-upload','value'),
#               Input('Upload-Data-Button', 'n_clicks'),
#               Input('upload-data', 'filename'),
#               State('currentUpload', 'data'),
#               prevent_initial_callback=True)
# def update_output(list_of_contents,dropdownValue,nclicks,filenames,uploadData):
#     context = dash.callback_context.triggered
#     if context[0]['prop_id'] == "Upload-Data-Button.n_clicks" and uploadData and dropdownValue != None:
#         downloadframe = pd.DataFrame()
#         decoded =base64.b64decode(uploadData)
#         try:
#             if 'csv' in filenames[0]:
#                 # Assume that the user uploaded a CSV file
#                 downloadframe = pd.read_csv(
#                     io.StringIO(decoded.decode('utf-8')))
#
#             elif 'xls' in filenames[0]:
#                 # Assume that the user uploaded an excel file
#                 downloadframe = pd.read_excel(io.BytesIO(decoded))
#
#         except Exception as e:
#             print(e)
#             return "Error Processing file", dash.no_update
#
#         Name = "data/" + dropdownValue +".csv"
#         downloadframe.to_csv(Name, index=False)
#         print("Lets fucking go")
#         return filenames[0] +"/  Uploaded as  /" +dropdownValue, dash.no_update
#     if dropdownValue == None:
#         return "Please Select a dropdown", dash.no_update
#     if dropdownValue != None and list_of_contents == None:
#         return "Upload a file to put in " + dropdownValue + " first", dash.no_update
#     # df = pd.read_csv('data/Last_Upload.csv', parse_dates=['date_time'], sep=';')
#         return dropdownValue + " Uploaded", dash.no_update
#     if(dropdownValue != None):
#         if list_of_contents is not None:
#             content_type, content_string = list_of_contents[0].split(',')
#             return "File selected: " + str(filenames[0]) + " Dropdown selected: " + dropdownValue, content_string
#
#
#
#
#
# @app.callback(
#     Output("df-info-collapse", "is_open"),
#     [Input("df-info-collapse-button", "n_clicks")],
#
#     [State("df-info-collapse", "is_open")],
# )
# def toggle_collapse(n, is_open):
#     if n:
#         return not is_open
#     return is_open
#
#
#
#
# @app.callback(
#     Output('solar-power-graph','figure'),
#     Input('graph-update', 'n_intervals')
# )
# def updateSolarGraph( interval):
#
#     SOLAR_DUMMY = pd.read_excel('data\solar_Data\dummy_data.xlsx')
#     SOLAR_DUMMY = SOLAR_DUMMY.tail(SOLAR_DUMMY.shape[0] -1)
#     solar_trace = []
#
#
#     #x_stamps = SOLAR_DUMMY.loc[interval:interval + 294]
#     x_stamps = SOLAR_DUMMY
#     x_stamps1 = list(pd.to_datetime(x_stamps['date_time'], format='%Y%b%d-%H:%M:%S'))
#     x_stamps2 = []
#     for entry in x_stamps1:
#         x_stamps2.append(entry.to_pydatetime())
#
#     #Logic to get the current date time to look at the data, even if the day of the data is different to the current day. Does not work if the data doesn't start at 00:00
#     currentTime = datetime.now()
#     currentTimeHours = timedelta(hours=currentTime.hour) + timedelta(minutes=currentTime.minute) + timedelta( seconds=currentTime.second)
#     LineTime = (x_stamps2[0] - timedelta(minutes=x_stamps2[0].minute) - timedelta(hours=x_stamps2[0].hour)) + currentTimeHours
#
#     #This rounds the time that is being looked at to the nearest 5 minutes as the output data is every 5 minutes
#     discard = timedelta(minutes=LineTime.minute % 5,
#                         seconds=LineTime.second,
#                         microseconds=LineTime.microsecond)
#     LineTime -= discard
#     if discard >= timedelta(minutes=2.5):
#         LineTime += timedelta(minutes=5)
#
#     solar_trace.append(go.Scatter(
#         x=SOLAR_DUMMY['date_time'],
#         y=SOLAR_DUMMY['real_power'],
#         hoverinfo='x+y',
#         mode='lines+markers',
#         line=dict(width=0.5, color='#B5179E'),
#         stackgroup='two',  # define stack group
#         name='Solar Power',
#         marker=dict(size=3),
#     ))
#     solar_trace = [solar_trace]
#     data_solar = [val for sublist in solar_trace for val in sublist]
#
#     solar_chart = go.Figure({'data': data_solar,
#                            'layout': go.Layout(
#                                title="Solar forecast (MW)",
#                                yaxis_range=(0, SOLAR_DUMMY['real_power'].max()+0.10*SOLAR_DUMMY['real_power'].max()),
#                                plot_bgcolor='#ffffff',
#                                paper_bgcolor='#ffffff',
#                                #xaxis=dict(range=[SOLAR_DUMMY['date_time'].min(), SOLAR_DUMMY['date_time'].max()], type='date'),
#                                xaxis=dict(range=[LineTime-timedelta(hours=3), LineTime+timedelta(hours=21)],type='date'),
#                                legend=dict(
#                                    x=0,
#                                    y=1,
#                                    traceorder='normal',
#                                    font=dict(
#                                        size=15, ),
#                                ),
#                                margin=dict(
#                                    l=8,
#                                    r=8,
#                                    b=8,
#                                    t=35,
#                                    pad=2
#                                ),
#                            )
#                            })
#     solar_chart.add_shape(
#         go.layout.Shape(type='line', xref='x', yref='y', editable=True,
#                         x0=LineTime, y0=0, x1=LineTime, y1=SOLAR_DUMMY['real_power'].max(),
#                         line={'dash': 'solid', "color": "Red", "width": 3}),
#     )
#     solar_chart.add_annotation(x=LineTime, y=0.75*SOLAR_DUMMY['real_power'].max(), text=str(LineTime), showarrow=False, align="right", width=300)
#     solar_chart.update_xaxes(gridcolor="#e5e5e5")
#     solar_chart.update_yaxes(gridcolor="#e5e5e5")
#
#
#     fig = px.scatter(SOLAR_DUMMY, x ='date_time',y = 'real_power')
#
#     solar_chart.update_layout(
#         font=dict(
#             size=16,
#         )
#     )
#     return solar_chart
#
#
#
#
#
# @app.callback(
#     Output('upload_htmlDiv','children'),
#     Input('Train-Data-Button', 'n_clicks'),
#     prevent_initial_call=True
# )
# def trainNetworks(clicks):
#     print("clicked")
#     data = [pd.read_csv('data\DD_data.csv', sep=";"), pd.read_csv('data\solar_Data.csv', sep=";"),pd.read_csv('data\solar_forecast.csv', sep=";"),pd.read_csv('data\DD_forecast.csv', sep=";"),pd.read_csv('data\DF_data.csv', sep=";"), pd.read_csv('data\DF_forecast.csv', sep=";")]
#     stats =[html.P("AVG MAX  MIN STD")]
#     for x in data:
#         stats.append( html.P(str(round(x['real_power'].mean(), 3)) + " "+str(round(x['real_power'].max(), 3)) + " "+str(round(x['real_power'].min(), 3)) + " "+str(round(x['real_power'].std(), 3)),))
#         stats.append
#     children = stats
#
#     model = tf.keras.Sequential([
#         tf.keras.layers.Dense(10, activation='relu'),
#         tf.keras.layers.Dense(10, activation='relu'),
#         tf.keras.layers.Dense(1)
#     ])
#
#     model.compile(optimizer='adam',
#                   loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
#                   metrics=['accuracy'])
#
#
#     model.save('data/modelTest')
#     return children
#
#
# @app.callback(Output('select_point_dropdown', 'value'),[Input('MELTEMI-choice', "n_clicks"), Input('ANSRO-choice', "n_clicks")])
# def update_point_selection_using_imageMap(one, two):
#     ctx = dash.callback_context
#     if ctx.triggered[0]['prop_id'] == 'MELTEMI-choice.n_clicks':
#         return 'MELTEMI'
#     if ctx.triggered[0]['prop_id'] == 'ANSRO-choice.n_clicks':
#         return 'ANSRO'
#     return dash.no_update
#
#
#
#
# # Callback for LoadDecompositionChart,LoadForecastGraph,PieChart,Predicted&ObservedPowerGraphs
# @app.callback(
#     [#Output('load-decomposition-graph', 'figure'),
#     Output('load-graph-P', 'figure'),
#     Output('load-graph-Q', 'figure'),
#     Output('pie-chart-P', 'figure'),
#     Output('pie-chart-Q', 'figure'),
#     Output('active-demand-forecasted', 'children'),
#     Output('active-demand-actual', 'children'),
#     Output('active-demand-error', 'children'),
#     Output('reactive-demand-forecasted', 'children'),
#     Output('reactive-demand-actual', 'children'),
#     Output('reactive-demand-error', 'children'),
#     Output('p-ctim1-error', 'children'),
#     Output('p-qtim1-error', 'children'),
#     Output('p-rc-error', 'children'),
#     Output('p-ruc-error', 'children'),
#     Output('p-smps-error', 'children'),
#     Output('p-l-error', 'children'),
#     Output('q-ctim1-error', 'children'),
#     Output('q-qtim1-error', 'children'),
#     Output('q-rc-error', 'children'),
#     Output('q-ruc-error', 'children'),
#     Output('q-smps-error', 'children'),
#     Output('q-l-error', 'children'),],
#     [Input('graph-update', 'n_intervals'),
#     Input("select_point_dropdown", "value"),
#     #Input("select_load", "value")
#     ]
#     )
# def update_graph(n, net_point_choice): #load_type_choice is legacy, please remove
#
#
#     load_type_choice = "REAL"
#
#     dd_select = MELTEMI_DD
#     df_select = MELTEMI_DF
#
#     if net_point_choice == 'MELTEMI':
#         dd_select = MELTEMI_DD
#         df_select = MELTEMI_DF
#     elif net_point_choice == "ANSRO":
#         dd_select = ANSRO_DD
#         df_select = ANSRO_DF
#     else:
#         dd_select = None
#         df_select = None
#         return dash.no_update
#
#     #dd_select = pd.read_csv('data\input.csv', parse_dates=['date_time'], sep=";")
#
#
#     # Time tracking logic (mock)
#     x_stamps = df_select
#     x_stamps1 = list(pd.to_datetime(x_stamps['date_time'],format='%Y%b%d-%H:%M:%S'))
#     x_stamps2 = []
#
#     for entry in x_stamps1:
#         x_stamps2.append(entry.to_pydatetime())
#     currentTime = datetime.now()
#     currentTimeHours = timedelta(hours=currentTime.hour) + timedelta(minutes=currentTime.minute) + timedelta(seconds=currentTime.second)
#     LineTime = (x_stamps2[0] - timedelta(minutes=x_stamps2[0].minute) - timedelta(hours=x_stamps2[0].hour)) + currentTimeHours
#
#     discard = timedelta(minutes=LineTime.minute % 5,
#                                  seconds=LineTime.second,
#                                  microseconds=LineTime.microsecond)
#     LineTime -= discard
#     if discard >= timedelta(minutes=2.5):
#         LineTime += timedelta(minutes=5)
#
#     # Demand Forecast
#     trace_df_P = []
#     trace_df_P.append(go.Scatter(
#         x=x_stamps2[0:-1],
#         y=(dd_select[["RL_CTIM1", "RL_QTIM1", "RL_RC"]].sum(axis=1)),
#         hoverinfo='x+y',
#         mode='lines+markers',
#         line=dict(width=0.5, color='#3F37C9'),
#         stackgroup='two', # define stack group
#         name = 'P controllable',
#         marker=dict(size=3),
#     ))
#
#     trace_df_P.append(go.Scatter(
#         x= x_stamps2[0:-1],
#         y=(dd_select[["RL_RUC", "RL_SMPS", "RL_Lightning"]].sum(axis=1)),
#         hoverinfo='x+y',
#         mode='lines+markers',
#         line=dict(width=0.5, color='#B5179E'),
#         stackgroup='two', # define stack group
#         name = 'P uncontrollable',
#         marker=dict(size=3),
#     ))
#
#
#     traces_df = [trace_df_P]
#     data_df = [val for sublist in traces_df for val in sublist]
#
#
#     df_chart_P = go.Figure({ 'data': data_df,
#                 'layout': go.Layout(
#                     title="P Forecast (MW)",
#                     yaxis_range=(0, 30),
#                     plot_bgcolor= '#ffffff',
#                     paper_bgcolor= '#ffffff',
#                     xaxis=dict(range=[LineTime-timedelta(hours=3), LineTime+timedelta(hours=19)], type='date'),
#                     legend=dict(
#                         x=0,
#                         y=1,
#                         traceorder='normal',
#                         font=dict(
#                             size=12,),
#                     ),
#                     margin=dict(
#                         l=8,
#                         r=8,
#                         b=8,
#                         t=35,
#                         pad=2
#                     ),
#                 )
#     })
#
#     df_chart_P.update_xaxes(gridcolor="#e5e5e5")
#     df_chart_P.update_yaxes(gridcolor="#e5e5e5")
#     df_chart_P.add_shape(
#         go.layout.Shape(type='line', xref='x', yref='y', editable=True,
#                         x0=LineTime, y0=0, x1=LineTime, y1=45, line={'dash': 'solid',"color":"Red","width":3}),
#     )
#     df_chart_P.add_annotation(x=LineTime,y=40,text=str(LineTime),showarrow=False, align="right", width=300)
#
#     # Demand forecat Q
#     trace_df_Q = []
#     trace_df_Q.append(go.Scatter(
#         x=x_stamps2[0:-1],
#         y=(dd_select[["RCT_CTIM1", "RCT_QTIM1", "RCT_RC"]].sum(axis=1)),
#         hoverinfo='x+y',
#         mode='lines+markers',
#         line=dict(width=0.5, color='#3F37C9'),
#         stackgroup='two', # define stack group
#         name = 'Q controllable',
#         marker=dict(size=3),
#     ))
#
#     trace_df_Q.append(go.Scatter(
#         x= x_stamps2[0:-1],
#         y= (dd_select[["RCT_RUC", "RCT_SMPS", "RCT_Lightning"]].sum(axis=1)),
#         hoverinfo='x+y',
#         mode='lines+markers',
#         line=dict(width=0.5, color='#B5179E'),
#         stackgroup='two', # define stack group
#         name = 'Q uncontrollable',
#         marker=dict(size=3),
#     ))
#
#
#     traces_df = [trace_df_Q]
#     data_df = [val for sublist in traces_df for val in sublist]
#
#
#     df_chart_Q = go.Figure({ 'data': data_df,
#                 'layout': go.Layout(
#                     title="Q Forecast (MVar)",
#                     yaxis_range=(0, 10),
#                     plot_bgcolor= '#ffffff',
#                     paper_bgcolor= '#ffffff',
#                     xaxis=dict(range=[LineTime-timedelta(hours=3), LineTime+timedelta(hours=19)], type='date'),
#                     legend=dict(
#                         x=0,
#                         y=1,
#                         traceorder='normal',
#                         font=dict(
#                             size=12,),
#                     ),
#                     margin=dict(
#                         l=8,
#                         r=8,
#                         b=8,
#                         t=35,
#                         pad=2
#                     ),
#                 )
#     })
#
#     df_chart_Q.update_xaxes(gridcolor="#e5e5e5")
#     df_chart_Q.update_yaxes(gridcolor="#e5e5e5", title_text = "[Mvar]")
#     df_chart_Q.add_shape(
#         go.layout.Shape(type='line', xref='x', yref='y', editable=True,
#                         x0=LineTime, y0=0, x1=LineTime, y1=45, line={'dash': 'solid',"color":"Red","width":3}),
#     )
#     df_chart_Q.add_annotation(x=LineTime,y=40,text=str(LineTime),showarrow=False, align="right", width=300)
#     df_active_demand_actual = 3
#     df_active_demand_forecasted = df_select['real_power'][n]
#     df_active_demand_error = "{:.2f}".format(df_active_demand_actual/df_active_demand_forecasted * 100)
#     df_reactive_demand_actual = 6
#     df_reactive_demand_forecasted = df_select['reactive_power'][n]
#     df_reactive_demand_error = "{:.2f}".format(df_reactive_demand_actual/df_reactive_demand_forecasted * 100)
#
#
#     # Demand Decomposition
#     trace_dd = []
#     if load_type_choice == 'REAL':
#         # Real power decomposition
#         trace_dd.append(go.Scatter(
#             x= x_stamps2[0:-1],
#             y= dd_select['RL_CTIM1'].values,
#             hoverinfo='x+y',
#             mode='lines+markers',
#             line=dict(width=0.5, color='rgb(93, 66, 245)'),
#             stackgroup='one', # define stack group
#             name = 'CTIM1'
#         ))
#
#         trace_dd.append(go.Scatter(
#             x= x_stamps2[0:-1],
#             y=dd_select['RL_QTIM1'].values,
#             hoverinfo='x+y',
#             mode='lines+markers',
#             line=dict(width=0.5, color='rgb(20, 156, 219)'),
#             stackgroup='one',
#             name = "QTIM1"
#         ))
#
#         trace_dd.append(go.Scatter(
#             x= x_stamps2[0:-1],
#             y=dd_select['RL_RC'].values,
#             hoverinfo='x+y',
#             mode='lines+markers',
#             line=dict(width=0.5, color='rgb(12, 171, 54)'),
#             stackgroup='one',
#             name = "RC"
#         ))
#
#         trace_dd.append(go.Scatter(
#             x= x_stamps2[0:-1],
#             y=dd_select['RL_RUC'].values,
#             hoverinfo='x+y',
#             mode='lines+markers',
#             line=dict(width=0.5, color='rgb(219, 145, 15)'),
#             stackgroup='one',
#             name = "RUC"
#         ))
#
#         trace_dd.append(go.Scatter(
#             x= x_stamps2[0:-1],
#             y=dd_select['RL_SMPS'].values,
#             hoverinfo='x+y',
#             mode='lines+markers',
#             line=dict(width=0.5, color='rgb(219, 90, 15)'),
#             stackgroup='one',
#             name = "SMPS"
#         ))
#
#         trace_dd.append(go.Scatter(
#             x= x_stamps2[0:-1],
#             y=dd_select['RL_Lightning'].values,
#             hoverinfo='x+y',
#             mode='lines+markers',
#             line=dict(width=0.5, color='rgb(235, 206, 19)'),
#             stackgroup='one',
#             name = "Lightning"
#         ))
#
#     if load_type_choice == 'REACTIVE':
#         # Reactive power decomposition
#         trace_dd.append(go.Scatter(
#             x= x_stamps2[0:-1],
#             y= dd_select['RCT_CTIM1'].values,
#             hoverinfo='x+y',
#             mode='lines+markers',
#             line=dict(width=0.5, color='rgb(93, 66, 245)'),
#             stackgroup='two', # define stack group
#             name = 'CTIM1'
#         ))
#
#         trace_dd.append(go.Scatter(
#             x= x_stamps2[0:-1],
#             y=dd_select['RCT_QTIM1'].values,
#             hoverinfo='x+y',
#             mode='lines+markers',
#             line=dict(width=0.5, color='rgb(20, 156, 219)'),
#             stackgroup='two',
#             name = "QTIM1"
#         ))
#
#         trace_dd.append(go.Scatter(
#             x= x_stamps2[0:-1],
#             y=dd_select['RCT_RC'].values,
#             hoverinfo='x+y',
#             mode='lines+markers',
#             line=dict(width=0.5, color='rgb(12, 171, 54)'),
#             stackgroup='two',
#             name = "RC"
#         ))
#
#         trace_dd.append(go.Scatter(
#             x= x_stamps2[0:-1],
#             y=dd_select['RCT_RUC'].values,
#             hoverinfo='x+y',
#             mode='lines+markers',
#             line=dict(width=0.5, color='rgb(219, 145, 15)'),
#             stackgroup='two',
#             name = "RUC"
#         ))
#
#         trace_dd.append(go.Scatter(
#             x= x_stamps2[0:-1],
#             y=dd_select['RCT_SMPS'].values,
#             hoverinfo='x+y',
#             mode='lines+markers',
#             line=dict(width=0.5, color='rgb(219, 90, 15)'),
#             stackgroup='two',
#             name = "SMPS"
#         ))
#
#         trace_dd.append(go.Scatter(
#             x= x_stamps2[0:-1],
#             y=dd_select['RCT_Lightning'].values,
#             hoverinfo='x+y',
#             mode='lines+markers',
#             line=dict(width=0.5, color='rgb(235, 206, 19)'),
#             stackgroup='two',
#             name = "Lightning"
#         ))
#
#     traces_dd = [trace_dd]
#     data_dd = [val for sublist in traces_dd for val in sublist]
#
#     dd_chart = go.Figure({ 'data': data_dd,
#                 'layout': go.Layout(
#                     yaxis_range=(0, 40),
#                     plot_bgcolor= '#ffffff',
#                     paper_bgcolor= '#ffffff',
#                     xaxis=dict(range=[x_stamps2[0], x_stamps2[-1]], type='date'),
#                     legend=dict(
#                         x=0,
#                         y=1,
#                         traceorder='normal',
#                         font=dict(
#                             size=12,),
#                     ),
#                     margin=dict(
#                         l=8,
#                         r=8,
#                         b=8,
#                         t=8,
#                         pad=2
#                     ),
#                 )
#
#     })
#
#     dd_chart.update_xaxes(gridcolor="#e5e5e5")
#     dd_chart.update_yaxes(gridcolor="#e5e5e5")
#     dd_chart.add_shape(
#         go.layout.Shape(type='line', xref='x', yref='y', editable=True,
#                         x0=LineTime, y0=0, x1=LineTime, y1=45, line={'dash': 'solid',"color":"Red","width":3}),
#     )
#
#     # Real bar chart
#     names=['CTIM1','QTIM1','RC','RUC','SMPS','L']
#     dd_select = pd.read_csv('data\MELTEMI_DD_dummy.csv', parse_dates=['date_time'], sep=";")
#
#     dd_P_error_info_forecasted = dd_select[['RL_CTIM1','RL_QTIM1','RL_RC','RL_RUC','RL_SMPS','RL_Lightning']].iloc[n]
#     dd_P_error_info_observed = dd_select[['RL_CTIM1_obv','RL_QTIM1_obv','RL_RC_obv','RL_RUC_obv','RL_SMPS_obv','RL_Lightning_obv']].iloc[n]
#     dd_P_error_info_tab_data = ["{:.2f}".format((1-(forecasted/observed))*100) for forecasted, observed in zip(dd_P_error_info_forecasted, dd_P_error_info_observed)]
#
#     dd_Q_error_info_forecasted = dd_select[['RCT_CTIM1','RCT_QTIM1','RCT_RC','RCT_RUC','RCT_SMPS','RCT_Lightning']].iloc[n]
#     dd_Q_error_info_observed = dd_select[['RCT_CTIM1_obv','RCT_QTIM1_obv','RCT_RC_obv','RCT_RUC_obv','RCT_SMPS_obv','RCT_Lightning_obv']].iloc[n]
#     dd_Q_error_info_tab_data = ["{:.2f}".format((1-(forecasted/observed))*100) for forecasted, observed in zip(dd_Q_error_info_forecasted, dd_Q_error_info_observed)]
#
#
#     # Pie chart index dummy
#     ind = [n, n+294]
#
#     # Pie chart P
#
#     # Select the pie chart values to be of the current time
#     QDF = dd_select[['date_time','RL_CTIM1','RL_QTIM1','RL_RC','RL_RUC','RL_SMPS','RL_Lightning']] #select P demand decomposition items
#     dd_values = QDF.loc[QDF['date_time'] == LineTime]
#     dd_values = dd_values[['RL_CTIM1','RL_QTIM1','RL_RC','RL_RUC','RL_SMPS','RL_Lightning']].values[0]
#
#     labels = ['RL_CTIM1','RL_QTIM1','RL_RC','RL_RUC','RL_SMPS','RL_Lightning']
#     pie_chart_P = go.Figure(data=[go.Pie(labels=labels, values=dd_values, textinfo='label+percent', insidetextorientation='radial', title="Real power composition "),])
#
#     pie_chart_P.update_layout(showlegend=False)
#     pie_chart_P.update_traces(textposition='inside')
#     pie_chart_P.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
#     pie_chart_P.update_layout(margin=dict(t=0, b=0, l=0, r=0, pad=0))
#
#     # Pie chart Q
#     QDF = dd_select[['date_time','RCT_CTIM1','RCT_QTIM1','RCT_RC','RCT_RUC','RCT_SMPS','RCT_Lightning']]
#     dd_values = QDF.loc[QDF['date_time']== LineTime]
#     dd_values = dd_values[['RCT_CTIM1','RCT_QTIM1','RCT_RC','RCT_RUC','RCT_SMPS','RCT_Lightning']].values[0]
#
#     labels = ['RCT_CTIM1','RCT_QTIM1','RCT_RC','RCT_RUC','RCT_SMPS','RCT_Lightning']
#     pie_chart_Q = go.Figure(data=[go.Pie(labels=labels, values=dd_values, textinfo='label+percent', insidetextorientation='radial', title="Reactive power composition"),])
#
#     pie_chart_Q.update_layout(showlegend=False)
#     pie_chart_Q.update_traces(textposition='inside')
#     pie_chart_Q.update_layout(uniformtext_minsize=4, uniformtext_mode='hide')
#     pie_chart_Q.update_layout(margin=dict(l=0, r=0, t=0, b=0))
#
#     df_chart_Q.update_layout(font=dict(size=16))
#     df_chart_P.update_layout(font=dict(size=16))
#     pie_chart_P.update_layout(font=dict(size=20))
#     pie_chart_Q.update_layout(font=dict(size=20))
#
#
#     return df_chart_P, df_chart_Q, pie_chart_P, pie_chart_Q, df_active_demand_actual, df_active_demand_forecasted, df_active_demand_error, df_reactive_demand_actual, df_reactive_demand_forecasted, df_reactive_demand_error, *dd_P_error_info_tab_data, *dd_Q_error_info_tab_data
