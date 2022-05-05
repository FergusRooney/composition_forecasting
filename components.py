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
from datetime import datetime
import pandas as pd

# Image selector related
filename = '/assets/rsz_network_diagram_mod.png'

upload_data = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '5px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload', children=[
        html.Div(id='upload-data-text', children='''
                Upload data:
            ''')
    ]), dcc.Store(id='currentUpload', data=[], storage_type="local")
])

image_pane = html.Div([
    html.MapEl([
        html.Area(id="MELTEMI-choice", target='', alt='Test Network', title='Test Network', href='#',
                  coords='168,46,13', shape='circle'),
        html.Area(id="ANSRO-choice", target='', alt='ANSRO', title='ANSRO', href='#', coords='238,154,13',
                  shape='circle'),
    ],
        name='map'),
    html.Img(src=filename, useMap='#map')
])

image_selector_pane = html.Div(className='image_selector_pane default-pane', children=[
    html.H2('Select network point'),
    dcc.Dropdown(
        id='select_point_dropdown',
        options=[
            {'label': 'Test Network', 'value': 'MELTEMI'},
            {'label': 'BUS1', 'value': 'BUS1'},
            {'label': 'BUS1', 'value': 'BUS1'},
        ],
        placeholder='Select network point',
    ),
    image_pane
])

left_pane = html.Div(className='left-pane',
                     children=[
                         html.H2('Other useful information'),
                         html.P('''Refactor code for trace addition'''),
                         html.P('''Figure out a way to design page avoiding native Dash approach''')
                     ])

load_decomposition_selector = html.Div(className='load-decomposition-selector', children=[
    dcc.Dropdown(
        id='select_load',
        options=[
            {'label': 'REAL', 'value': 'REAL'},
            {'label': 'REACTIVE', 'value': 'REACTIVE'},
        ],
        placeholder='Select type of load to examine',
    ),
])

upload_buttons = html.Div(
    children=[
        html.Button('Upload', id='Upload-Data-Button', n_clicks=0),
        html.Div(id="upload_htmlDiv")
    ],
)
test_button = html.Div(
    children=[
        html.Button('Test', id='test-button', n_clicks=0),
        html.Div(id="test-div")
    ],
)



forecast_button = html.Div(children=[
    html.Button('Forecast', id='Forecast-Data-Button', n_clicks=0,
                style={
                    'background-color': '#B5179E',
                    'width' : '180px',
                    'padding' : '4px 0',

                    'position': 'relative',
                    'left' : '0%',
                    'right' : '100%',
                    'border-radius': '3px',
                    'color': 'white',
                    'font-size': '30px',
                    'min-width': '100px'
                }),
    html.Div(id='forecast-htmldiv', children=[]),
    dcc.Store(id='prediction-store-dd', data=[], storage_type="local"),dcc.Store(id='prediction-store-df', data=[], storage_type="local"),
    dcc.Store(id='data-in-store',data=[], storage_type="local"),
    ]
)

dummyDiv= html.Div(id='dummy_div', children=[])

delete_data_button = html.Div(children=[
    html.Button('Delete data', id='delete-data-button', n_clicks=0,
                style={
                    'background-color': '#B5179E',
                    'width' : '180px',
                    'padding' : '4px 0',

                    'position': 'relative',
                    'left' : '0%',
                    'right' : '100%',
                    'border-radius': '3px',
                    'color': 'white',
                    'font-size': '30px',
                    'min-width': '100px'
                }),
    html.Div(id='forecast-htmldiv', children=[])]
)

forecast_text_loading = html.Div(children=[],id='forecast_tag_loading')
forecast_text_success = html.Div(children=[],id='forecast_tag_success')
train_text_loading = html.Div(children=[],id='train_tag_loading')
train_text_success = html.Div(children=[], id = 'train_tag_success')

train_button = html.Div(
    html.Button('Train', id='Train-Data-Button', n_clicks=0,
                style={
                    'background-color': '#B5179E',
                    'width': '180px',
                    'padding': '4px 0',

                    'position': 'relative',
                    'left' : '0%',
                    'right' : '100%',
                    'border-radius': '3px',
                    'color': 'white',
                    'font-size': '30px',
                    'min-width': '100px'
                })
)


upload_dropdown = html.Div(children=[dcc.Dropdown(
    id='dropdown-upload',
    options=[
        {'label': 'Solar input', 'value': 'Solar_input'},
        {'label': 'Solar data', 'value': 'Solar_Data'},
        {'label': 'Demand Decomposition input', 'value': 'DD_input'},
        {'label': 'Demand Decomposition data', 'value': 'DD_data'},
        {'label': 'Demand Forecast input', 'value': 'DF_input'},
        {'label': 'Demand Forecast data', 'value': 'DF_data'},
        {'label': 'Demand Forecast input', 'value': 'DF_input'},
        {'label': 'Demand Forecast data', 'value': 'DF_data'},
        {'label': 'Wind input', 'value': 'wind_input'},
        {'label': 'Wind data', 'value': 'DF_data'},
    ]
)]
)
upload_dropdown_demand_decomposition = html.Div(children=[dcc.Dropdown(
    id='dropdown-upload-DD',
    options=[
        {'label': 'Total P', 'value': 'total_P_new20'},
        {'label': 'Total Q', 'value': 'total_Q_new20'},
        {'label': 'Historical composition data', 'value': 'decomposition_new20'},
    ]
)]
)




load_decomposition_chart = html.Div(className='default-pane',
                                    children=[
                                        html.Div(className='chart-description',
                                                 children=[
                                                     html.H2('Load decomposition'),
                                                     load_decomposition_selector,

                                                     dcc.Graph(id='load-decomposition-graph',
                                                               config={'displayModeBar': False, },
                                                               animate=True,
                                                               ),

                                                     dcc.Interval(
                                                         id='graph-update',
                                                         interval=5000,
                                                         n_intervals=0
                                                     ),
                                                 ])
                                    ])

load_chart_P = html.Div(className='default-pane',
                        children=[
                            html.Div(className='chart-description',
                                     children=[
                                         # html.H2('Power Demand Forecasting'),

                                         dcc.Graph(id='load-graph-P',
                                                   config={'displayModeBar': False, },
                                                   animate=True,
                                                   ),

                                         dcc.Interval(
                                             id='graph-update',
                                             interval=5000,
                                             n_intervals=0
                                         ),
                                     ])
                        ])

load_chart_Q = html.Div(className='default-pane',
                        children=[
                            html.Div(className='chart-description',
                                     children=[
                                         # html.H2('Power Demand Forecasting'),

                                         dcc.Graph(id='load-graph-Q',
                                                   config={'displayModeBar': False, },
                                                   animate=True,

                                                   ),

                                         dcc.Interval(
                                             id='graph-update',
                                             interval=5000,
                                             n_intervals=0
                                         ),

                                     ])
                        ])

solar_forecast_pane = html.Div(className='default-pane',
                               children=[
                                   html.Div(className='solar-Class',
                                            children=[

                                                dcc.Graph(id='solar-power-graph',
                                                          config={'displayModeBar': False, },
                                                          animate=True,
                                                          ),

                                                dcc.Interval(
                                                    id='graph-update',
                                                    interval=5000,
                                                    n_intervals=0
                                                ),

                                            ])
                               ])
wind_forecast_pane = html.Div(className='default-pane',
                              children=[
                                  html.Div(className='wind-Class',
                                           children=[
                                               dcc.Graph(id='wind-power-graph',
                                                         config={'displayModeBar': False, },
                                                         animate=True,
                                                         ),

                                               dcc.Interval(
                                                   id='graph-update',
                                                   interval=5000,
                                                   n_intervals=0
                                               ),

                                           ])
                              ])

pie_chart_pane = html.Div(className='default-pane', style={'max-width': 400, 'min-width': 400},
                          children=[
                              html.Div(className='chart-description',
                                       children=[
                                           dcc.Graph(id='pie-chart',
                                                     config={'displayModeBar': False, },
                                                     animate=True,
                                                     ),

                                           dcc.Interval(
                                               id='graph-update',
                                               interval=5000,
                                               n_intervals=0
                                           ),

                                       ])
                          ])

pie_chart_pane_P = html.Div(className='default-pane',
                            children=[
                                html.Div(className='chart-description',
                                         children=[
                                             dcc.Graph(id='pie-chart-P',
                                                       config={'displayModeBar': False, },
                                                       animate=True,
                                                       ),

                                             dcc.Interval(
                                                 id='graph-update',
                                                 interval=5000,
                                                 n_intervals=0
                                             ),

                                         ])
                            ])

pie_chart_pane_Q = html.Div(className='default-pane',
                            children=[
                                html.Div(className='chart-description',
                                         children=[
                                             dcc.Graph(id='pie-chart-Q',
                                                       config={'displayModeBar': False, },
                                                       animate=True,
                                                       ),

                                             dcc.Interval(
                                                 id='graph-update',
                                                 interval=5000,
                                                 n_intervals=0
                                             ),

                                         ])
                            ])

explanation_tab = html.Div(style={"marginLeft": 0,'width' : '180px'},
                           children=[
                               dbc.Button(
                                   "Load Composition Legend",
                                   id="legend-collapse-button",
                                   className="mb-3",
                                   color="primary",
                               ),
                               dbc.Collapse(
                                   dbc.Card(dbc.CardBody([
                                       html.P([
                                           "CTIM1 - Constant Torque Induction Motors", html.Br(),
                                           "QTIM1 - Quadratic Torque Induction Motors", html.Br(),
                                           "RC - Controllable Resistive Loads", html.Br(),
                                           "RUC - Uncontrollable Resistive Loads", html.Br(),
                                           "SMPS - Electronic Devices", html.Br(),
                                           "L - Lightning"]
                                       ),
                                   ])),
                                   id="collapse",
                               ),
                           ]
                           )

current_time_tab = html.Div(className='default-pane',
                            children=[
                                dcc.Interval(
                                    id='time-update',
                                    interval=1000,
                                    n_intervals=0
                                ),
                                html.Div(id="current-time"),
                            ])

df_active_info_tab = html.Div(className='default-pane2',
                              children=[
                                  html.Div(children=[
                                      html.Div('Forecasted P (MW)'),
                                      html.Div(className='numeric-pane', id="active-demand-forecasted"),
                                  ],
                                      style={'display': 'inline-block', 'margin': 5}),

                                  html.Div(children=[
                                      html.Div('Actual P (MW)'),
                                      html.Div(className='numeric-pane', id="active-demand-actual"),
                                  ],
                                      style={'display': 'inline-block', 'margin': 5}),
                                  html.Br(),
                                  html.Div(children=[
                                      html.Div('Error P (%)'),
                                      html.Div(className='numeric-pane', id="active-demand-error"),
                                  ],
                                      style={'display': 'inline-block', 'margin': 5}),

                              ])

df_reactive_info_tab = html.Div(className='default-pane2',
                                children=[
                                    html.Div(children=[
                                        html.Div('Forecasted Q (MW)'),
                                        html.Div(className='numeric-pane', id="reactive-demand-forecasted"),
                                    ],
                                        style={'display': 'inline-block', 'margin': 5}),

                                    html.Div(children=[
                                        html.Div('Actual Q (MW)'),
                                        html.Div(className='numeric-pane', id="reactive-demand-actual"),
                                    ],
                                        style={'display': 'inline-block', 'margin': 5}),
                                    html.Br(),
                                    html.Div(children=[
                                        html.Div('Error Q (%)'),
                                        html.Div(className='numeric-pane', id="reactive-demand-error"),
                                    ],
                                        style={'display': 'inline-block', 'margin': 5}),

                                ])

dd_error_info_tab_P = html.Div(className='default-pane',
                               children=[
                                   html.H4("P Errors %"),
                                   html.Div(children=[
                                       html.Div('CTIM1'),
                                       html.Div(className='numeric-pane', id="p-ctim1-error"),
                                   ],
                                       style={'display': 'inline-block', 'margin': 1,  'font-size': '21px'}),

                                   html.Div(children=[
                                       html.Div('QTIM1'),
                                       html.Div(className='numeric-pane', id="p-qtim1-error"),
                                   ],
                                       style={'display': 'inline-block', 'margin': 1, 'font-size': '21px'}),

                                   html.Div(children=[
                                       html.Div("RC"),
                                       html.Div(className='numeric-pane', id="p-rc-error"),
                                   ],
                                       style={'display': 'inline-block', 'margin': 1, 'font-size': '21px'}),

                                   html.Br(),
                                   html.Div(children=[
                                       html.Div("RUC"),
                                       html.Div(className='numeric-pane', id="p-ruc-error"),
                                   ],
                                       style={'display': 'inline-block', 'margin': 1, 'font-size': '21px'}),

                                   html.Div(children=[
                                       html.Div("SMPS"),
                                       html.Div(className='numeric-pane', id="p-smps-error"),
                                   ],
                                       style={'display': 'inline-block', 'margin': 1,  'font-size': '21px'}),


                                   html.Div(children=[
                                       html.Div("L"),
                                       html.Div(className='numeric-pane', id="p-l-error"),
                                   ],
                                       style={'display': 'inline-block', 'margin': 1, 'font-size': '21px'}),
                                   html.Div(
                                        children=[
                                            html.Div("Pc"),
                                            html.Div(className='numeric-pane', id="p-controllable-error"),
                                        ],
                                       style={'display': 'inline-block', 'margin': 1, 'font-size': '21px'},
                                   ),

                               ], style = {'height':'560px'})
wind_solar_info_tab = html.Div(className='default-pane',
                               children=[

                                   html.H4("Wind and Solar Errors"),
                                   html.Div(children=[
                                       html.Div('Wind '),
                                       html.Div(className='numeric-pane', id="wind-error"),
                                   ],
                                       style={'display': 'inline-block', 'margin': 5}),

                                   html.Div(children=[
                                       html.Div('Solar'),
                                       html.Div(className='numeric-pane', id="solar-error"),
                                   ],
                                       style={'display': 'inline-block', 'margin': 5}),

                               ])

dd_error_info_tab_Q = html.Div(className='default-pane',
                               children=[

                                   html.H4("Q Errors %"),
                                   html.Div(children=[
                                       html.Div('CTIM1'),
                                       html.Div(className='numeric-pane', id="q-ctim1-error"),
                                   ],
                                       style={'display': 'inline-block', 'margin': 1, 'font-size': '21px'},),

                                   html.Div(children=[
                                       html.Div('QTIM1'),
                                       html.Div(className='numeric-pane', id="q-qtim1-error"),
                                   ],
                                       style={'display': 'inline-block', 'margin': 1, 'font-size': '21px'},),

                                   html.Div(children=[
                                       html.Div("RC"),
                                       html.Div(className='numeric-pane', id="q-rc-error"),
                                   ],
                                       style={'display': 'inline-block', 'margin': 1, 'font-size': '21px'},),
                                   html.Br(),
                                   html.Div(children=[
                                       html.Div("RUC"),
                                       html.Div(className='numeric-pane', id="q-ruc-error"),
                                   ],
                                       style={'display': 'inline-block', 'margin': 1, 'font-size': '21px'},),

                                   html.Div(children=[
                                       html.Div("SMPS"),
                                       html.Div(className='numeric-pane', id="q-smps-error"),
                                   ],
                                       style={'display': 'inline-block', 'margin': 1, 'font-size': '21px'},),

                                   html.Div(children=[
                                       html.Div("L"),
                                       html.Div(className='numeric-pane', id="q-l-error"),
                                   ],
                                       style={'display': 'inline-block', 'margin': 1, 'font-size': '21px'},),
                                    html.Div(
                                        children=[
                                            html.Div("Qc"),
                                            html.Div(className='numeric-pane', id="q-controllable-error"),
                                        ],
                                       style={'display': 'inline-block', 'margin': 1, 'font-size': '21px'},
                                   ),
                               ], style = {'height':'560px'})

df_info_tab = html.Div(children=[
    df_active_info_tab,
    html.Hr(),
    df_reactive_info_tab,
])


df_info_tab_collapse = html.Div(style={"marginLeft": 10},
                                children=[
                                    dbc.Button(
                                        "Load Forecast Accuracy",
                                        id="df-info-collapse-button",
                                        className="mb-3",
                                        color="primary",
                                    ),
                                    dbc.Collapse(
                                        dbc.Card(dbc.CardBody([
                                            df_active_info_tab,
                                            df_reactive_info_tab
                                        ])),
                                        id="df-info-collapse",
                                    ),
                                ]
                                )

real_bar_chart = html.Div(className='real-bar-description default-pane',
                          children=[
                              dcc.Graph(id='real-bar-chart',
                                        config={'displayModeBar': False, },
                                        animate=True,
                                        ),

                              dcc.Interval(
                                  id='real-bar-update',
                                  interval=5000,
                                  n_intervals=0
                              ),
                          ])

reactive_bar_chart = html.Div(className='reactive-bar-description default-pane',
                              children=[
                                  dcc.Graph(id='reactive-bar-chart',
                                            config={'displayModeBar': False, },
                                            animate=True,
                                            ),
                              ])
