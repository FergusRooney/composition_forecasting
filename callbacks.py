import math
import time

from dash.dependencies import Input, Output, State
from app import app

import io
import base64
import dash
from dash.dependencies import Output, Input
import pytz
from dash import html
import dash_bootstrap_components as dbc
from dash import dcc
import plotly
import random
import plotly.graph_objs as go
import plotly.express as px
from collections import deque
import flask
from datetime import datetime, timedelta, timezone
import pandas as pd
import pathlib
from tensorflow import keras
from keras import layers

# Import TensorFlow:
import tensorflow as tf
import numpy as np

from decomposition_ann import runner
from os.path import exists
import os

#
# Long callback setup
# Long callback can be useful for doing something while a task is running I.E network training
# However currently as of 10/4/22 it has a bug that means that the callback runs when the page is open so is not usable

# from dash.long_callback import DiskcacheLongCallbackManager
# import diskcache
# from uuid import uuid4
# launch_uid = uuid4()
# cache = diskcache.Cache("./cache")
# long_callback_manager = DiskcacheLongCallbackManager(
#     cache, cache_by=[lambda: launch_uid], expire=60,
# )
# app._long_callback_manager=long_callback_manager

# Local data load dummies



def get_mkl_enabled_flag():

    mkl_enabled = False
    major_version = int(tf.__version__.split(".")[0])
    minor_version = int(tf.__version__.split(".")[1])
    if major_version >= 2:
        if minor_version < 5:
            from tensorflow.python import _pywrap_util_port
        else:
            from tensorflow.python.util import _pywrap_util_port
            onednn_enabled = int(os.environ.get('TF_ENABLE_ONEDNN_OPTS', '0'))
        mkl_enabled = _pywrap_util_port.IsMklEnabled() or (onednn_enabled == 1)
    else:
        mkl_enabled = tf.pywrap_tensorflow.IsMklEnabled()

    if(os.path.exists("var/log/intelAcceleration.txt")):
        f = open("var/log/intelAcceleration.txt", "a")
    else:
        f = open("var/log/intelAcceleration.txt", "x")
    f.write(str(datetime.now())+" Intel acceleration enabled: " +str(mkl_enabled) + "\n")
    f.close()
    print(str(datetime.now())+" Intel acceleration enabled: " +str(mkl_enabled) + "\n")
    return mkl_enabled

get_mkl_enabled_flag()


MELTEMI_DF = pd.read_csv('data/MELTEMI_DF_dummy.csv', parse_dates=['date_time'], sep=';')
MELTEMI_DD = pd.read_csv('data/MELTEMI_DD_dummy.csv', parse_dates=['date_time'], sep=";")
ANSRO_DF = pd.read_csv('data/ANSRO_DF_dummy.csv', parse_dates=['date_time'], sep=';')
ANSRO_DD = pd.read_csv('data/ANSRO_DD_dummy.csv', parse_dates=['date_time'], sep=";")
SOLAR_DUMMY = pd.read_excel('data/solar_Data/dummy_data.xlsx')

size_of_prediction = 4000
ann_prediction_PQ = []
ann_prediction_dd= []
if(os.path.exists("decomposition_ann/predictions_datetime.csv")):
        ann_prediction_dd = pd.read_csv('decomposition_ann/predictions_datetime.csv',parse_dates=['date_time'],sep=',')
if(os.path.exists('decomposition_ann/PQ_composition.csv')):
        ann_prediction_PQ = pd.read_csv('decomposition_ann/PQ_composition.csv',parse_dates=['date_time'],sep=',').head(size_of_prediction)

@app.callback(
    Output('current-time', 'children'),
    Input('time-update', 'n_intervals')
)
def update_current_time(n):
    now = datetime.now(tz=pytz.timezone("Europe/London"))
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return "Current date & time: "+dt_string


@app.callback(
    Output("collapse", "is_open"),
    [Input("legend-collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

def parse_contents(contents, filename, dropdownName):
    content_type, content_string = contents.split(',')
    return "File selected: " + str(filename) + " Dropdown selected: " + dropdownName, content_string

@app.callback(Output('upload-data-text', 'children'),
              Output('currentUpload', 'data'),
              Input('upload-data', 'contents'),
              Input('dropdown-upload-DD','value'),
              Input('Upload-Data-Button', 'n_clicks'),
              Input('upload-data', 'filename'),
              State('currentUpload', 'data'),
              )
def update_output(list_of_contents,dropdownValue,nclicks,filenames,uploadData):
    context = dash.callback_context.triggered
    if context[0]['prop_id'] == "Upload-Data-Button.n_clicks" and uploadData and dropdownValue != None:
        downloadframe = pd.DataFrame()
        decoded =base64.b64decode(uploadData)
        try:
            if 'csv' in filenames[0]:
                # Assume that the user uploaded a CSV file
                downloadframe = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')))

            elif 'xls' in filenames[0]:
                # Assume that the user uploaded an excel file
                downloadframe = pd.read_excel(io.BytesIO(decoded))

        except Exception as e:
            print(e)
            return "Error Processing file", dash.no_update

        Name = "decomposition_ann/" + dropdownValue +".csv"
        downloadframe.to_csv(Name, index=False)
        return filenames[0] +"/  Uploaded as  /" +dropdownValue, dash.no_update
    if dropdownValue == None:
        return "Please Select a dropdown", dash.no_update
    if dropdownValue != None and list_of_contents == None:
        return "Upload a file to put in " + dropdownValue + " first", dash.no_update
    # df = pd.read_csv('data/Last_Upload.csv', parse_dates=['date_time'], sep=';')
        return dropdownValue + " Uploaded", dash.no_update
    if(dropdownValue != None):
        if list_of_contents is not None:
            content_type, content_string = list_of_contents[0].split(',')
            return "File selected: " + str(filenames[0]) + " Dropdown selected: " + dropdownValue, content_string

@app.callback(
    Output("df-info-collapse", "is_open"),
    [Input("df-info-collapse-button", "n_clicks")],

    [State("df-info-collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output('solar-power-graph','figure'),
    Input('graph-update', 'n_intervals')
)
def updateSolarGraph( interval):

    SOLAR_DUMMY = pd.read_excel('data/solar_Data/dummy_data.xlsx')
    SOLAR_DUMMY = SOLAR_DUMMY.tail(SOLAR_DUMMY.shape[0] -1)
    solar_trace = []
    #x_stamps = SOLAR_DUMMY.loc[interval:interval + 294]
    x_stamps = SOLAR_DUMMY
    x_stamps1 = list(pd.to_datetime(x_stamps['date_time'], format='%Y%b%d-%H:%M:%S'))
    x_stamps2 = []
    for entry in x_stamps1:
        x_stamps2.append(entry.to_pydatetime())

    #Logic to get the current date time to look at the data, even if the day of the data is different to the current day. Does not work if the data doesn't start at 00:00
    currentTime = datetime.now(tz=pytz.timezone("Europe/London"))
    currentTimeHours = timedelta(hours=currentTime.hour) + timedelta(minutes=currentTime.minute) + timedelta( seconds=currentTime.second)
    LineTime = (x_stamps2[0] - timedelta(minutes=x_stamps2[0].minute) - timedelta(hours=x_stamps2[0].hour)) + currentTimeHours

    #This rounds the time that is being looked at to the nearest 5 minutes as the output data is every 5 minutes
    discard = timedelta(minutes=LineTime.minute % 5,
                        seconds=LineTime.second,
                        microseconds=LineTime.microsecond)
    LineTime -= discard
    if discard >= timedelta(minutes=2.5):
        LineTime += timedelta(minutes=5)

    solar_trace.append(go.Scatter(
        x=SOLAR_DUMMY['date_time'],
        y=SOLAR_DUMMY['real_power'],
        hoverinfo='x+y',
        mode='lines+markers',
        line=dict(width=0.5, color='#B5179E'),
        stackgroup='two',  # define stack group
        name='Solar Power',
        marker=dict(size=3),
    ))
    solar_trace = [solar_trace]
    data_solar = [val for sublist in solar_trace for val in sublist]

    solar_chart = go.Figure({'data': data_solar,
                           'layout': go.Layout(
                               title="Solar forecast",
                               yaxis_range=(0, SOLAR_DUMMY['real_power'].max()+0.10*SOLAR_DUMMY['real_power'].max()),
                               plot_bgcolor='#ffffff',
                               paper_bgcolor='#ffffff',
                               #xaxis=dict(range=[SOLAR_DUMMY['date_time'].min(), SOLAR_DUMMY['date_time'].max()], type='date'),
                               xaxis=dict(range=[LineTime-timedelta(hours=3), LineTime+timedelta(hours=21)],type='date'),
                               legend=dict(
                                   x=0,
                                   y=1,
                                   traceorder='normal',
                                   font=dict(
                                       size=15, ),
                               ),
                               margin=dict(
                                   l=8,
                                   r=8,
                                   b=8,
                                   t=35,
                                   pad=2
                               ),
                           )
                           })
    solar_chart.add_shape(
        go.layout.Shape(type='line', xref='x', yref='y', editable=True,
                        x0=LineTime, y0=0, x1=LineTime, y1=SOLAR_DUMMY['real_power'].max(),
                        line={'dash': 'solid', "color": "Red", "width": 3}),
    )
    solar_chart.add_annotation(x=LineTime, y=0.75*SOLAR_DUMMY['real_power'].max(), text=str(LineTime), showarrow=False, align="right", width=300)
    solar_chart.update_xaxes(gridcolor="#e5e5e5")
    solar_chart.update_yaxes(gridcolor="#e5e5e5")

    fig = px.scatter(SOLAR_DUMMY, x ='date_time',y = 'real_power')

    solar_chart.update_layout(
        font=dict(
            size=16,
        )
    )
    return solar_chart

def addTimeColumn(pd):
    currentTime = datetime.strptime(datetime.now(tz=pytz.timezone("Europe/London")).strftime("%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S")
    currentTime -= timedelta(hours =currentTime.hour, minutes= currentTime.minute, seconds= currentTime.second)
    dateTimeCol = []
    for x in range(pd.shape[0]):
        dateTimeCol.append(currentTime)
        currentTime = currentTime + timedelta(minutes=1)



    pd.insert(0,"date_time",dateTimeCol)
    return pd


def addTimeToPredictions(predictionFile):
    file = pd.read_csv(predictionFile)
    file = addTimeColumn(file)
    file.columns = ["date_time","CTIM1","QTIM1","RC","RUC","SMPS","lighting"]
    file.to_csv("decomposition_ann/predictions_datetime.csv",index=False)

def generatePQfile(p,q):
    if (not os.path.exists(p) or not os.path.exists(q) ):
        print("path not found PQ")
        return "Error P or Q file not found"
    P = pd.read_csv(p,names=["P"])
    #print(P)
    Q = pd.read_csv(q,names=["Q"])
    #print(Q)
    P.insert(1,"Q",Q["Q"])
    P=addTimeColumn(P)
    P.to_csv("decomposition_ann/PQ_composition.csv", index=False)

# Long callback allows you to change an output to something while the callback is running
# @app.long_callback(
#     output=Output('forecast_tag_success', 'children'),
#     inputs=Input('Forecast-Data-Button', 'n_clicks'),
#     running=[
#         (Output('forecast_tag_loading', 'children'),"Forecasting in progress", "Forecasting finished"),
#         ],
#     prevent_initial_call=True,
# )
# def forecast_button(clicks):
#     if clicks ==0:
#         return dash.no_update
#     if (not os.path.exists("decomposition_ann/test_modelLSTM")):
#         return "Model not found"
#     runner.main(3)
#     addTimeToPredictions("decomposition_ann/predictions.csv")
#     generatePQfile("decomposition_ann/total_P_new20.csv", "decomposition_ann/total_Q_new20.csv")
#
#     ann_prediction_dd = pd.read_csv('decomposition_ann/predictions_datetime.csv', parse_dates=['date_time'], sep=',')
#     ann_prediction_PQ = pd.read_csv('decomposition_ann/PQ_composition.csv', parse_dates=['date_time'], sep=',')
#     return "Forecasting executed!"


@app.callback(
    Output('forecast_tag_loading','children'),
    Input('Forecast-Data-Button','n_clicks'),
    prevent_initial_call=True,
)
def display_forecast_msg(btn):
    return "Forecasting in progress"

# @app.long_callback(
#     output=(Output('forecast_tag_success', 'children')),
#     inputs=((Input('forecast_tag_loading','children')),
#             (State('Forecast-Data-Button','n_clicks'))),
#     prevent_inital_call=True,
# )

@app.callback(
    Output('forecast_tag_success', 'children'),
    Input('Forecast-Data-Button', 'n_clicks'),
prevent_initial_call = True,)
def forecastNetworks_forecast(n):

    if(n <1):
        return dash.no_update
    if (not os.path.exists("decomposition_ann/test_modelLSTM")):
        return "Model not found"
    start_time = time.perf_counter()
    runner.main(3)
    addTimeToPredictions("decomposition_ann/predictions.csv")
    generatePQfile("decomposition_ann/total_P_new20.csv", "decomposition_ann/total_Q_new20.csv")
    forecastTime ="{:.2f}".format( time.perf_counter() - start_time)
    get_mkl_enabled_flag()
    return "Succesfully forecast data in " + forecastTime + "s"

@app.callback(
    Output('train_tag_loading','children'),
    Input('Train-Data-Button', 'n_clicks'),
    #manager=long_callback_manager,
    prevent_initial_call=True,
)
def trainNetworks_buttonPressed(clicks):

    return "Training in progress. This may take some time"

@app.callback(
    Output('train_tag_success', 'children'),
    Input('train_tag_loading','children'),
    State('Train-Data-Button','n_clicks'),
    prevent_initial_call=True,)
def trainCallbacks_train(i,click):

    if(click < 1):
        return dash.no_update
    start_time = time.perf_counter()
    totalQ = os.path.exists("decomposition_ann/total_P_new20.csv")
    totalP = os.path.exists("decomposition_ann/total_Q_new20.csv")
    decomp = os.path.exists("decomposition_ann/decomposition_new20.csv")
    if (not totalQ):
        return "Total Q file not found"
    if (not totalP):
        return "Total P file not found"
    if (not decomp):
        return "decomposition_ann file not found"
    runner.main(1)
    TrainTime = "{:.2f}".format(time.perf_counter() - start_time)
    return "Succesfully trained model in " + TrainTime + "s"


@app.callback(Output('select_point_dropdown', 'value'),[Input('MELTEMI-choice', "n_clicks"), Input('ANSRO-choice', "n_clicks")])
def update_point_selection_using_imageMap(one, two):
    ctx = dash.callback_context
    if ctx.triggered[0]['prop_id'] == 'MELTEMI-choice.n_clicks':
        return 'MELTEMI'
    if ctx.triggered[0]['prop_id'] == 'ANSRO-choice.n_clicks':
        return 'ANSRO'
    return dash.no_update


@app.callback(
    Output('dummy_div','children'),
    Output('data-in-store','data'),
    Input('delete-data-button','n_clicks'),
    Input('forecast_tag_success', 'children'),
    State('data-in-store','data'),
    prevent_initial_call = True,
)
def delete_data(n,forecast_input,data):
    ctx = dash.callback_context
    if ctx.triggered[0]['prop_id'] =="forecast_tag_success.children":
        update_graph_flag = dict(data)
        update_graph_flag.pop('FilesDeleted',None)
        return dash.no_update, update_graph_flag

    if (os.path.exists("decomposition_ann/predictions.csv")):#
        os.remove("decomposition_ann/predictions.csv")
    if (os.path.exists("decomposition_ann/predictions_datetime.csv")):
        os.remove("decomposition_ann/predictions_datetime.csv")
    if (os.path.exists("decomposition_ann/PQ_composition.csv")):
        os.remove("decomposition_ann/PQ_composition.csv")
    outputData = dict(data)
    outputData['FilesDeleted'] = True
    return "forecast files deleted",outputData

@app.callback(
    Output("test-div","children"),
    Input("test-button","n_clicks"),

    prevent_initial_call = True,
)
def calculateOverallError(n):
    loadPredictions = pd.read_csv('decomposition_ann/predictions.csv',
                     sep=',')
    loadComposition = pd.read_csv('decomposition_ann/decomposition_new20.csv',
                                  sep=',')
    errors = []
    for x in range(6):
        errors.append(100*(loadPredictions.iloc[:,x]-loadComposition.iloc[:,x])/(loadComposition.iloc[:,x]))

    with open('average_error_file.txt', 'w') as f:
        for x in errors:
            for y in x.values:
                if not math.isnan(y):
                    f.write(str(y) + ",")

            f.write("\n")

    return "yes"


@app.callback(
    Output('prediction-store-dd', 'data'),
    Output('prediction-store-df', 'data'),
    Input('data-in-store', 'data'),
)
def update_stored_files(data):
    if (not os.path.exists("decomposition_ann/predictions_datetime.csv")):
        return dash.no_update
    if (not os.path.exists('decomposition_ann/PQ_composition.csv')):
        return dash.no_update
    dd = pd.read_csv('decomposition_ann/predictions_datetime.csv', parse_dates=['date_time'],
                     sep=',')
    pq = pd.read_csv('decomposition_ann/PQ_composition.csv', parse_dates=['date_time'],
                     sep=',').head(size_of_prediction)
    dd = dd.to_dict()
    pq = pq.to_dict()
    print("stored data outputted")
    return dd, pq

# Callback for LoadDecompositionChart,LoadForecastGraph,PieChart,Predicted&ObservedPowerGraphs
@app.callback(
    [#Output('load-decomposition-graph', 'figure'),
    Output('load-graph-P', 'figure'),
    Output('load-graph-Q', 'figure'),
    Output('pie-chart-P', 'figure'),
    Output('pie-chart-Q', 'figure'),
    Output('active-demand-forecasted', 'children'),
    Output('active-demand-actual', 'children'),
    Output('active-demand-error', 'children'),
    Output('reactive-demand-forecasted', 'children'),
    Output('reactive-demand-actual', 'children'),
    Output('reactive-demand-error', 'children'),
    Output('p-ctim1-error', 'children'),
    Output('p-qtim1-error', 'children'),
    Output('p-rc-error', 'children'),
    Output('p-ruc-error', 'children'),
    Output('p-smps-error', 'children'),
    Output('p-l-error', 'children'),
    Output('p-controllable-error', 'children'),
    Output('q-ctim1-error', 'children'),
    Output('q-qtim1-error', 'children'),
    Output('q-rc-error', 'children'),
    Output('q-ruc-error', 'children'),
    Output('q-smps-error', 'children'),
    Output('q-l-error', 'children'),
    Output('q-controllable-error', 'children'),
    ],
    [Input('graph-update', 'n_intervals'),
     Input("select_point_dropdown", "value"),
     Input('prediction-store-dd', 'data'),
     Input('prediction-store-df', 'data'),
     State('data-in-store','data'),
    #Input("select_load", "value")
    ],
    prevent_initial_call=False,
    )
def update_graph(n, net_point_choice,dd_Data, df_Data, stored_data): #
    #Melemi_dd and df are "dummy data" from the first project
    dd_select = MELTEMI_DD
    df_select = MELTEMI_DF

    #This part relates to the future "Select network point" feature
    # if net_point_choice == 'MELTEMI':
    #     dd_select = MELTEMI_DD
    #     df_select = MELTEMI_DF
    # elif net_point_choice == "ANSRO":
    #     dd_select = ANSRO_DD
    #     df_select = ANSRO_DF
    # else:
    #     dd_select = None
    #     df_select = None
    #     return dash.no_update

    stored_data = dict(stored_data)

    # if (not os.path.exists("decomposition_ann/predictions_datetime.csv")):
    #     return dash.no_update
    # if (not os.path.exists('decomposition_ann/PQ_composition.csv')):
    #     return dash.no_update

    if dd_Data is None or "FilesDeleted" in stored_data:
        return go.Figure(), go.Figure(), go.Figure(), go.Figure(), "0", "0", "0", "0", "0", "0", "0","0","0","0","0","0","0","0","0","0","0","0","0","0"

    if df_Data is None or "FilesDeleted" in stored_data:
        return go.Figure(), go.Figure(), go.Figure(), go.Figure(), "0", "0", "0", "0", "0", "0", "0","0","0","0","0","0","0","0","0","0","0","0","0","0"

    #ann_data_select =
    ann_data_select =pd.DataFrame.from_dict(df_Data)
    ann_data_select['date_time'] = pd.to_datetime(ann_data_select['date_time'], format = '%Y-%m-%dT%H:%M:%S')

    dd_select = pd.DataFrame.from_dict(dd_Data)
    dd_select['date_time'] = pd.to_datetime(dd_select['date_time'], format = '%Y-%m-%dT%H:%M:%S')
    #Get an array of all the date times for the X axis of graphs from the data
    x_stamp_ann =  list(pd.to_datetime(ann_data_select['date_time']))

    x_stamp_ann_time=[]
    for entry in x_stamp_ann:
        x_stamp_ann_time.append(entry.to_pydatetime())




    currentTime = datetime.now(tz=pytz.timezone("Europe/London"))
    #get the current time in format hour:minute:second
    currentTimeHours = timedelta(hours=currentTime.hour) + timedelta(minutes=currentTime.minute) + timedelta(seconds=currentTime.second)

    #This line adds to the current time in hours to the Day at the start of the date array
    #This could make the time tracking innacurate if the data is more than a day old but is used for prototyping
    LineTime = (x_stamp_ann_time[0] - timedelta(minutes=x_stamp_ann_time[0].minute) - timedelta(hours=x_stamp_ann_time[0].hour)) + currentTimeHours

    #Commented code updates the graph values every 5 mintes
    # granularity = 5
    # discard = timedelta(minutes=LineTime.minute %granularity,
    #                              seconds=LineTime.second,
    #                              microseconds=LineTime.microsecond)
    # LineTime -= discard
    # if discard >= timedelta(minutes=granularity/2):
    #     LineTime += timedelta(minutes=granularity)

    #Update graph every 1 minute (This is granularity of data). Note this callback updates with the DCC.interval componant
    #Seconds and microseconds removed to match current time with format of data
    LineTime = LineTime - timedelta(seconds=LineTime.second,microseconds=LineTime.microsecond)

    index_for_time = int(ann_data_select.index[ann_data_select["date_time"] == LineTime].values[0])
    observed_data = dd_select
    # get forecated decompositon values at current timestep and multipy be real power values at current timestep for error box
    forecated_error_row = dd_select.loc[dd_select["date_time"] == LineTime]
    forecasted_error_values = forecated_error_row.drop(columns='date_time').values[0]
    PQ_values = ann_data_select.loc[ann_data_select["date_time"] == LineTime]

    # check that file path exists to prevent error incase it hasn't been uploaded yet
    if (os.path.exists("decomposition_ann/decomposition_new20.csv")):
        observed_data = pd.read_csv('decomposition_ann/decomposition_new20.csv').iloc[index_for_time].values
    PQ_values = PQ_values.drop(columns='date_time').values[0]

    # multiply predicted decomposition weights by either P or Q observed load
    current_decomp_p = []
    for x in forecasted_error_values:
        current_decomp_p.append(x * PQ_values[0])
    current_decomp_q = []
    for x in forecasted_error_values:
        current_decomp_q.append(x * PQ_values[1])
    observed_data_p = []
    observed_data_q = []
    for x in observed_data:
        observed_data_p.append(x * PQ_values[0])
        observed_data_q.append(x * PQ_values[1])

    dd_P_error_info_tab_data = ["{:.2f}".format((1 - (forecasted / observed)) * 100) for forecasted, observed in
                                zip(current_decomp_p, observed_data_p)]
    dd_Q_error_info_tab_data = ["{:.2f}".format((1 - (forecasted / observed)) * 100) for forecasted, observed in
                                zip(current_decomp_q, observed_data_q)]

    p_controllable_load = current_decomp_p[0] + current_decomp_p[1] + current_decomp_p[2]
    p_uncontrollable_load = current_decomp_p[3] + current_decomp_p[4] + current_decomp_p[5]
    q_controllable_load = current_decomp_q[0] + current_decomp_q[1] + current_decomp_q[2]
    q_uncontrollable_load = current_decomp_q[3] + current_decomp_q[4] + current_decomp_q[5]

    # add 3 categories of controllable load to info tab
    P_controllable_error = (1 - ( p_controllable_load / (
                observed_data_p[0] + observed_data_p[1] + observed_data_p[2]))) * 100
    Q_controllable_error = (1 - (q_controllable_load / (
                observed_data_q[0] + observed_data_q[1] + observed_data_q[2]))) * 100

    dd_P_error_info_tab_data.append("{:.2f}".format(P_controllable_error))
    dd_Q_error_info_tab_data.append("{:.2f}".format(Q_controllable_error))

    # in the curretn case, P and Q is not forecasted so the values are the same
    df_active_demand_actual = PQ_values[0]
    df_active_demand_forecasted = PQ_values[0]
    df_active_demand_error = "{:.2f}".format((1 - (df_active_demand_forecasted / df_active_demand_actual)) * 100)
    df_reactive_demand_actual = PQ_values[1]
    df_reactive_demand_forecasted = PQ_values[1]
    df_reactive_demand_error = "{:.2f}".format((1 - (df_reactive_demand_forecasted / df_reactive_demand_actual)) * 100)

    df_active_demand_actual = "{:.2f}".format(df_active_demand_actual)
    df_active_demand_forecasted = "{:.2f}".format(df_active_demand_forecasted)
    df_reactive_demand_actual = "{:.2f}".format(df_reactive_demand_actual)
    df_reactive_demand_forecasted="{:.2f}".format(df_reactive_demand_forecasted)
    # Demand Forecast
    trace_df_P = []

    trace_df_P.append(go.Scatter(
        x=x_stamp_ann_time[0:-1],
        y=(dd_select[["RUC", "SMPS", "lighting"]].sum(axis=1)) * ann_data_select["P"],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, color='#B5179E'),
        stackgroup='two',  # define stack group
        name='P uncontrollable (Pc)',
    ))

    trace_df_P.append(go.Scatter(
        x=x_stamp_ann_time[0:-1],
        y=(dd_select[["CTIM1", "QTIM1", "RC"]].sum(axis=1))*ann_data_select["P"],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, color='#3F37C9'),
        stackgroup='two', # define stack group
        name = 'P controllable (Puc)',
    ))

    traces_df = [trace_df_P]
    data_df = [val for sublist in traces_df for val in sublist]


    #There is an issue where the zoom level resets every DCC.interval period
    #There is a fix for this but I can't get it to work
    #Look up " uirevision "

    df_chart_P = go.Figure({ 'data': data_df,
                'layout': go.Layout(
                    title="P Forecast",
                    yaxis_range=(0, ann_data_select["P"].max()),
                    plot_bgcolor= '#ffffff',
                    paper_bgcolor= '#ffffff',
                    xaxis=dict(range=[LineTime-timedelta(hours=3), LineTime+timedelta(hours=19)], type='date'),
                    legend=dict(
                        x=0,
                        y=1,
                        traceorder='normal',
                        font=dict(
                            size=17,),
                    ),
                    margin=dict(
                        l=8,
                        r=8,
                        b=8,
                        t=35,
                        pad=2
                    ),
                )
    })

    df_chart_P.update_xaxes(gridcolor="#e5e5e5")
    df_chart_P.update_yaxes(gridcolor="#e5e5e5")
    df_chart_P.add_shape(
        go.layout.Shape(type='line', xref='x', yref='y', editable=True,
                        x0=LineTime, y0=0, x1=LineTime, y1=40, line={'dash': 'solid',"color":"Red","width":3}),
    )
    lineTextP_c = "Pc:  " +"{:.2f}".format(p_controllable_load) + " MW"
    lineTextP_uc ="Puc: " + "{:.2f}".format(p_uncontrollable_load) + " MW"
    df_chart_P.add_annotation(x=LineTime+timedelta(hours =1, minutes =30),y=ann_data_select["P"].max()*0.8,text=lineTextP_c,showarrow=False, align="right", width=180)
    df_chart_P.add_annotation(x=LineTime+timedelta(hours =1, minutes =38),y=ann_data_select["P"].max()*0.75,text=lineTextP_uc,showarrow=False, align="right", width=180)

    # Demand forecat Q
    trace_df_Q = []

    trace_df_Q.append(go.Scatter(
        x=x_stamp_ann_time[0:-1],
        y=(dd_select[["RUC", "SMPS", "lighting"]].sum(axis=1)) * ann_data_select["Q"],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, color='#B5179E'),
        stackgroup='two',  # define stack group
        name='Q uncontrollable (Qc)',
    ))

    trace_df_Q.append(go.Scatter(
        x=x_stamp_ann_time[0:-1],
        y=(dd_select[["CTIM1", "QTIM1", "RC"]].sum(axis=1)) * ann_data_select["Q"],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, color='#3F37C9'),
        stackgroup='two', # define stack group
        name = 'Q controllable (Quc)',
    ))



    traces_df = [trace_df_Q]
    data_df = [val for sublist in traces_df for val in sublist]


    df_chart_Q = go.Figure({ 'data': data_df,
                'layout': go.Layout(
                    title="Q Forecast",
                    yaxis_range=(0, ann_data_select["Q"].max()),
                    plot_bgcolor= '#ffffff',
                    paper_bgcolor= '#ffffff',
                    xaxis=dict(range=[LineTime-timedelta(hours=3), LineTime+timedelta(hours=19)], type='date'),
                    legend=dict(
                        x=0,
                        y=1,
                        traceorder='normal',
                        font=dict(
                            size=17,),
                    ),
                    margin=dict(
                        l=8,
                        r=8,
                        b=8,
                        t=35,
                        pad=2
                    ),
                )
    })

    df_chart_Q.update_xaxes(gridcolor="#e5e5e5")
    df_chart_Q.update_yaxes(gridcolor="#e5e5e5", title_text = "Mvar")
    df_chart_P.update_yaxes(gridcolor="#e5e5e5", title_text = "MW")
    df_chart_Q.add_shape(
        go.layout.Shape(type='line', xref='x', yref='y', editable=True,
                        x0=LineTime, y0=0, x1=LineTime, y1=45, line={'dash': 'solid',"color":"Red","width":3}),
    )
    lineTextQ_c = "Qc:  " + "{:.2f}".format(q_controllable_load) +" MVar"
    lineTextQ_uc ="Quc: " + "{:.2f}".format(q_uncontrollable_load) +" MVar"
    df_chart_Q.add_annotation(x=LineTime+timedelta(hours = 1,minutes =45),y=ann_data_select["Q"].max()*0.8,text=lineTextQ_c,showarrow=False, align="right", width=180)
    df_chart_Q.add_annotation(x=LineTime + timedelta(hours=1, minutes=52), y=ann_data_select["Q"].max() * 0.73, text=lineTextQ_uc,
                              showarrow=False, align="right", width=180)

    names=['CTIM1','QTIM1','RC','RUC','SMPS','L']

    # Select the pie chart values for the current time
    QDF = dd_select[['date_time','CTIM1','QTIM1','RC','RUC','SMPS','lighting']] #s elect P demand decomposition items
    dd_values = QDF.loc[QDF['date_time'] == LineTime]
    dd_values = dd_values[['CTIM1','QTIM1','RC','RUC','SMPS','lighting']].values[0]

    labels = ['CTIM1','QTIM1','RC','RUC','SMPS','lighting']
    pie_chart_P = go.Figure(data=[go.Pie(labels=labels, values=dd_values,textinfo='label+percent', insidetextorientation='radial', title="Real power composition "),])

    #setting visual options for Pie chart P
    pie_chart_P.update_layout(showlegend=False)
    pie_chart_P.update_traces(textposition='inside')
    pie_chart_P.update_layout(uniformtext_minsize=15, uniformtext_mode='hide')
    pie_chart_P.update_layout(margin=dict(t=0, b=0, l=0, r=0, pad=0))
    pie_colours = ['#CBE4F9','#CDF5F6','#EFF9DA','#F9EBDF','#F9D8D6','#D6CDEA']
    pie_chart_P.update_traces(marker=dict(colors=pie_colours))

    # Pie chart Q
    QDF = dd_select[['date_time','CTIM1','QTIM1','RC','RUC','SMPS','lighting']]
    dd_values = QDF.loc[QDF['date_time']== LineTime]
    dd_values = dd_values[['CTIM1','QTIM1','RC','RUC','SMPS','lighting']].values[0]

    labels = ['CTIM1','QTIM1','RC','RUC','SMPS','lighting']
    pie_chart_Q = go.Figure(data=[go.Pie(labels=labels, values=dd_values, textinfo='label+percent', insidetextorientation='radial', title="Reactive power composition"),])

    pie_chart_Q.update_layout(showlegend=False)
    pie_chart_Q.update_traces(textposition='inside')
    pie_chart_Q.update_layout(uniformtext_minsize=15, uniformtext_mode='hide')
    pie_chart_Q.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    pie_chart_Q.update_traces(marker=dict(colors=pie_colours))

    df_chart_Q.update_layout(font=dict(size=20), height=550, title_x=0.5,title_y=0.95)
    df_chart_P.update_layout(font=dict(size=20),height=550,title_x=0.5,title_y=0.95)

    pie_chart_P.update_layout(font=dict(size=24),height=550)
    pie_chart_Q.update_layout(font=dict(size=24),height=550)

    #calculateOverallError()

    return df_chart_P, df_chart_Q, pie_chart_P, pie_chart_Q, df_active_demand_actual, df_active_demand_forecasted, df_active_demand_error, df_reactive_demand_actual, df_reactive_demand_forecasted, df_reactive_demand_error, *dd_P_error_info_tab_data, *dd_Q_error_info_tab_data

#This part is an artefact from previous implementation

    # # Demand Decomposition
    # trace_dd = []
    # if load_type_choice == 'REAL':
    #     # Real power decomposition
    #     trace_dd.append(go.Scatter(
    #         x= x_stamps2[0:-1],
    #         y= ann_prediction_dd['CTIM1'].values,
    #         hoverinfo='x+y',
    #         mode='lines+markers',
    #         line=dict(width=0.5, color='rgb(93, 66, 245)'),
    #         stackgroup='one', # define stack group
    #         name = 'CTIM1'
    #     ))
    #
    #     trace_dd.append(go.Scatter(
    #         x= x_stamps2[0:-1],
    #         y=ann_prediction_dd['QTIM1'].values,
    #         hoverinfo='x+y',
    #         mode='lines+markers',
    #         line=dict(width=0.5, color='rgb(20, 156, 219)'),
    #         stackgroup='one',
    #         name = "QTIM1"
    #     ))
    #
    #     trace_dd.append(go.Scatter(
    #         x= x_stamps2[0:-1],
    #         y=ann_prediction_dd['RC'].values,
    #         hoverinfo='x+y',
    #         mode='lines+markers',
    #         line=dict(width=0.5, color='rgb(12, 171, 54)'),
    #         stackgroup='one',
    #         name = "RC"
    #     ))
    #
    #     trace_dd.append(go.Scatter(
    #         x= x_stamps2[0:-1],
    #         y=ann_prediction_dd['RUC'].values,
    #         hoverinfo='x+y',
    #         mode='lines+markers',
    #         line=dict(width=0.5, color='rgb(219, 145, 15)'),
    #         stackgroup='one',
    #         name = "RUC"
    #     ))
    #
    #     trace_dd.append(go.Scatter(
    #         x= x_stamps2[0:-1],
    #         y=ann_prediction_dd['SMPS'].values,
    #         hoverinfo='x+y',
    #         mode='lines+markers',
    #         line=dict(width=0.5, color='rgb(219, 90, 15)'),
    #         stackgroup='one',
    #         name = "SMPS"
    #     ))
    #
    #     trace_dd.append(go.Scatter(
    #         x= x_stamps2[0:-1],
    #         y=ann_prediction_dd['lightning'].values,
    #         hoverinfo='x+y',
    #         mode='lines+markers',
    #         line=dict(width=0.5, color='rgb(235, 206, 19)'),
    #         stackgroup='one',
    #         name = "Lightning"
    #     ))
    #
    # if load_type_choice == 'REACTIVE':
    #     # Reactive power decomposition
    #     trace_dd.append(go.Scatter(
    #         x= x_stamps2[0:-1],
    #         y= ann_prediction_dd['CTIM1'].values,
    #         hoverinfo='x+y',
    #         mode='lines+markers',
    #         line=dict(width=0.5, color='rgb(93, 66, 245)'),
    #         stackgroup='two', # define stack group
    #         name = 'CTIM1'
    #     ))
    #
    #     trace_dd.append(go.Scatter(
    #         x= x_stamps2[0:-1],
    #         y=ann_prediction_dd['QTIM1'].values,
    #         hoverinfo='x+y',
    #         mode='lines+markers',
    #         line=dict(width=0.5, color='rgb(20, 156, 219)'),
    #         stackgroup='two',
    #         name = "QTIM1"
    #     ))
    #
    #     trace_dd.append(go.Scatter(
    #         x= x_stamps2[0:-1],
    #         y=ann_prediction_dd['RC'].values,
    #         hoverinfo='x+y',
    #         mode='lines+markers',
    #         line=dict(width=0.5, color='rgb(12, 171, 54)'),
    #         stackgroup='two',
    #         name = "RC"
    #     ))
    #
    #     trace_dd.append(go.Scatter(
    #         x= x_stamps2[0:-1],
    #         y=ann_prediction_dd['RUC'].values,
    #         hoverinfo='x+y',
    #         mode='lines+markers',
    #         line=dict(width=0.5, color='rgb(219, 145, 15)'),
    #         stackgroup='two',
    #         name = "RUC"
    #     ))
    #
    #     trace_dd.append(go.Scatter(
    #         x= x_stamps2[0:-1],
    #         y=ann_prediction_dd['SMPS'].values,
    #         hoverinfo='x+y',
    #         mode='lines+markers',
    #         line=dict(width=0.5, color='rgb(219, 90, 15)'),
    #         stackgroup='two',
    #         name = "SMPS"
    #     ))
    #
    #     trace_dd.append(go.Scatter(
    #         x= x_stamps2[0:-1],
    #         y=ann_prediction_dd['lightning'].values,
    #         hoverinfo='x+y',
    #         mode='lines+markers',
    #         line=dict(width=0.5, color='rgb(235, 206, 19)'),
    #         stackgroup='two',
    #         name = "Lightning"
    #     ))
    #
    # traces_dd = [trace_dd]
    # data_dd = [val for sublist in traces_dd for val in sublist]
    # dd_chart = go.Figure({ 'data': data_dd,
    #             'layout': go.Layout(
    #                 yaxis_range=(0, 40),
    #                 plot_bgcolor= '#ffffff',
    #                 paper_bgcolor= '#ffffff',
    #                 xaxis=dict(range=[x_stamps2[0], x_stamps2[-1]], type='date'),
    #                 legend=dict(
    #                     x=0,
    #                     y=1,
    #                     traceorder='normal',
    #                     font=dict(
    #                         size=12,),
    #                 ),
    #                 margin=dict(
    #                     l=8,
    #                     r=8,
    #                     b=8,
    #                     t=8,
    #                     pad=2
    #                 ),
    #             )
    # })
    # dd_chart.update_xaxes(gridcolor="#e5e5e5")
    # dd_chart.update_yaxes(gridcolor="#e5e5e5")
    # dd_chart.add_shape(
    #     go.layout.Shape(type='line', xref='x', yref='y', editable=True,
    #                     x0=LineTime, y0=0, x1=LineTime, y1=45, line={'dash': 'solid',"color":"Red","width":3}),
    # )
