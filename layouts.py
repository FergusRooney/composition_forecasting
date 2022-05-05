from dash import html
from dash import dcc
import dash_bootstrap_components as dbc


from components import left_pane, load_decomposition_chart, pie_chart_pane, image_selector_pane, explanation_tab, \
    current_time_tab, real_bar_chart, reactive_bar_chart, df_info_tab, df_info_tab_collapse, load_chart_Q, load_chart_P, \
    dd_error_info_tab_P, dd_error_info_tab_Q, pie_chart_pane_P, pie_chart_pane_Q, upload_data, upload_dropdown,upload_dropdown_demand_decomposition, \
    upload_buttons, solar_forecast_pane, wind_forecast_pane, wind_solar_info_tab, forecast_button, train_button,forecast_text_loading,forecast_text_success, \
    train_text_loading,train_text_success, delete_data_button, dummyDiv,test_button

welcome_layout = html.Div(children=[
    html.Div(children=[
        dbc.Row(children=[
            dbc.Col(
                children=[
                    html.H3(
                        children="Welcome to our project!"
                    ),
                    html.P(
                        children="University of Manchester project on Power Network demand-side management."
                    ),
                    html.P(
                        children="This website is still in development..."
                    ),
                ],
                className="panel",
                width=4
            ),
            dbc.Col(
                children=[
                    html.H3(
                        children="Contributors"
                    ),
                    dbc.ListGroup(
                        children=[
                            dbc.ListGroupItem("Edvinas Vrublevskis"),
                            dbc.ListGroupItem("Dr. Jelena Ponocko"),
                            dbc.ListGroupItem("Prof. Jovica Milanovic"),
                            dbc.ListGroupItem("Fergus Rooney")
                        ]
                    )
                ],
                className="panel",
                width=4
            ),
        ],
        ),
    ])
])

about_project_layout = html.Div(children=[
    dbc.Row(children=[
        dbc.Col(
            children=[

            ],
            className="panel",
            width=9
        ),
    ],
    )
])

upload_layout = html.Div(children=[
    dbc.Row(children=[

    ],
    )
])

load_decomposition_layout = html.Div(
    children=[
        html.Div(className='main',
                 children=[
                     dbc.Row(children=[
                         dbc.Col(
                             children=[image_selector_pane],
                             width="auto"
                         ),


                         dbc.Row(
                             children=[dbc.Col(
                                 children=[
                                     html.H3(
                                         children="Upload files"
                                     ),
                                     dbc.Col(style={"max-width": 350},
                                             children=[upload_data, upload_dropdown_demand_decomposition, upload_buttons, test_button],
                                             ),
                                 ],
                                 className="panel",
                                 width=9
                             ),
                             ]),
                         dbc.Col(style={"max-width": 350},children=[forecast_button,html.H3(children=["\n\n"]), train_button,html.H3(children=["\n\n"]),
                                                                    delete_data_button,forecast_text_loading, forecast_text_success
                                                                    ,train_text_loading,train_text_success,dummyDiv], width=1),

                        dbc.Col(style={"max-width": 350},
                             children=[current_time_tab,df_info_tab_collapse],
                             width=2
                             ),
                    dbc.Col(style={"max-width": 350},
                             children=[explanation_tab],
                             width=1
                             ),

                         # dbc.Col(
                         #     children=[solar_forecast_pane],
                         #     width=6
                         # ),
                     ]),
                     dbc.Row([
                         dbc.Col(
                             children=[load_chart_P],
                             width=8
                         ),
                         dbc.Col(
                             children=[pie_chart_pane_P],
                             width=3
                         ),
                         dbc.Col(
                             children=[dd_error_info_tab_P],
                             width=1
                         ),

                     ],class_name="g-0",),

                     dbc.Row(children=[
                         dbc.Col(
                             children=[load_chart_Q],
                             width=8,

                         ),
                         dbc.Col(
                             children=[pie_chart_pane_Q],
                             width=3
                         ),
                         dbc.Col(
                             children=[dd_error_info_tab_Q],
                             width=1
                         )
                     ],style={"height": "100vh"}
                     ),


                     dbc.Row(
                         children=[
                             dbc.Col(
                                 children=[],
                                 width=8
                             ),
                         ]
                     ),
                 ]),
    ])


future_work_layout = html.Div(
    children=[
        html.Div(className='main',
                 children=[
                     dbc.Row(children=[
                         dbc.Col(
                             children=[image_selector_pane],
                             width="auto"
                         ),
                         dbc.Col(style={"max-width": 350},
                                 children=[current_time_tab, explanation_tab],
                                 width=3
                                 ),
                         dbc.Col(style={"max-width": 350},
                                 children=[df_info_tab_collapse],
                                 width=3
                                 ),
                         dbc.Row(
                             children=[dbc.Col(
                                 children=[
                                     html.H3(
                                         children="Upload files"
                                     ),
                                     dbc.Col(
                                             children=[upload_data, upload_dropdown_demand_decomposition, upload_buttons],
                                             ),
                                     dbc.Col(children=[forecast_button, train_button])
                                 ],
                                 className="panel",
                                 width=9
                             )]),

                         # dbc.Col(
                         #     children=[solar_forecast_pane],
                         #     width=6
                         # ),
                     ]),
                     dbc.Row(children=[
                         dbc.Col(children=[wind_forecast_pane], width=5),
                         dbc.Col(children=[solar_forecast_pane], width=6),
                         dbc.Col(children=[wind_solar_info_tab], width=1),
                     ],
                     ),

                     dbc.Row(children=[
                         dbc.Col(
                             children=[load_chart_P],
                             width=9
                         ),
                         dbc.Col(
                             children=[pie_chart_pane_P],
                             width=2
                         ),
                         dbc.Col(
                             children=[dd_error_info_tab_P],
                             width=1
                         ),

                     ]
                     ),

                     dbc.Row(children=[
                         dbc.Col(
                             children=[load_chart_Q],
                             width=9
                         ),
                         dbc.Col(
                             children=[pie_chart_pane_Q],
                             width=2
                         ),
                         dbc.Col(
                             children=[dd_error_info_tab_Q],
                             width=1
                         )
                     ]
                     ),
                     dbc.Row(
                         children=[
                             dbc.Col(
                                 children=[],
                                 width=8
                             ),
                         ]
                     ),
                 ]),
    ])

# DOES NOT WORK, NEEDS SEPARATE CALLBACKS
load_forecast_layout = html.Div(
    children=[
        html.Div(className='main',
                 children=[
                     dbc.Row(children=[
                         dbc.Col(
                             children=[image_selector_pane],
                             width=3,
                         ),
                         dbc.Col(
                             children=[current_time_tab],
                             width=3
                         ),
                         dbc.Col(
                             children=[explanation_tab],
                             width=4
                         ),
                     ]),

                     dbc.Row(children=[
                         dbc.Col(
                             children=[real_bar_chart],
                             width=6
                         ),

                         dbc.Col(
                             children=[reactive_bar_chart],
                             width=6
                         ),
                     ]
                     ),

                     dbc.Row(children=[
                         dbc.Col(
                             children=[load_decomposition_chart],
                             width=9
                         ),
                         dbc.Col(
                             children=[df_info_tab],
                             width=3
                         ),
                     ]
                     ),

                 ]),
    ])