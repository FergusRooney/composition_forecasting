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

#
# MELTEMI_DF = pd.read_csv('data\MELTEMI_DF_dummy.csv', parse_dates=['date_time'], sep=';')
# MELTEMI_DD = pd.read_csv('data\MELTEMI_DD_dummy.csv', parse_dates=['date_time'], sep=";")
# ANSRO_DF = pd.read_csv('data\ANSRO_DF_dummy.csv', parse_dates=['date_time'], sep=';')
# ANSRO_DD = pd.read_csv('data\ANSRO_DD_dummy.csv', parse_dates=['date_time'], sep=";")
# SOLAR_DUMMY = pd.read_excel('data\solar_Data\dummy_data.xlsx')

