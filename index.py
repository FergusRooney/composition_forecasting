import dash
from dash import html
import dash_bootstrap_components as dbc
from dash import dcc
from dash.dependencies import Input, Output, State
import gunicorn
from app import app
from layouts import load_decomposition_layout, welcome_layout, about_project_layout, load_forecast_layout, upload_layout
import callbacks

NAVBAR_LOGO = "assets\logo_UoM_white.svg"


# Navigation bar menu
navbar = dbc.Navbar(style={"height":"80px"},
    children=[
        dbc.Row(style={"width":"100%"},children=[
            dbc.Col(width=6, children=[html.Img(src=NAVBAR_LOGO, height="45px")]),
            dbc.Col(width=6, style={"text-align": "end"},children=[
                dbc.Button("Tools", outline=True, color="secondary", className="mr-1", id="btn_sidebar"),
                dbc.NavItem(dbc.NavLink("Home", href="/"), style={"display":"inline-block"}),
                dbc.NavItem(dbc.NavLink("About Project", href="/about-project"), style={"display":"inline-block"}),
                dbc.NavItem(dbc.NavLink("Further Development", href="/further-development"), style={"display":"inline-block"}),
                dbc.NavItem(dbc.NavLink("Contact Us", href="/contact-us"), style={"display":"inline-block"}),
            ])
            ]
        ),
        
    ],
    #brand="UoM Demand Forecasting",
    #brand_href="/",
    color="#2b123a",
    dark=True,
    #fluid=True,
)

# Styles for sidebar menu
SIDEBAR_STYLE = {
    "position": "fixed",
    #"top": 62.5,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "zIndex": 1,
    "overflowX": "hidden",
    "transition": "all 0.5s",
    "padding": "0.5rem 1rem",
    "backgroundColor": "#2b123a",
    "paddingTop": "80px",
}

SIDEBAR_HIDDEN = {
    "position": "fixed",
    "top": 62.5,
    "left": "-16rem",
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "zIndex": 1,
    "overflowX": "hidden",
    "transition": "all 0.5s",
    "padding": "0rem 0rem",
    "backgroundColor": "#2b123a",
}

# Styles for content, adjusted to fit sidebar menu
CONTENT_STYLE_SIDEBAR = {
    "transition": "marginLeft .5s",
    "marginLeft": "16rem",
    "marginRight": "0",
    "padding": "2rem 1rem",
    "backgroundColor": "#f2f2f2",
}

CONTENT_STYLE_NO_SIDEBAR = {
    "transition": "marginLeft .5s",
    "marginLeft": "2rem",
    "marginRight": "2rem",
    "padding": "2rem 1rem",
    "backgroundColor": "#f2f2f2",
}

sidebar = html.Div(
    [
        html.H2("Tools", className="display-4", style={"margin-top":"20px","color":"white"}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Generation and load forecast", href="/load-decomposition", id="page-1-link"),
                dbc.NavLink("Upload Files", href="/load-prediction", id="page-2-link"),
                dbc.NavLink("Custom View", href="/custom-view", id="page-3-link"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    id="sidebar",
    style=SIDEBAR_STYLE,
)

content = html.Div(

    id="page-content",
    style=CONTENT_STYLE_SIDEBAR)

app.layout = html.Div(
    [
        dcc.Store(id='side_click'),
        dcc.Location(id="url"),
        navbar,
        sidebar,
        content,
    ],
)

@app.callback(
    [
        Output("sidebar", "style"),
        Output("page-content", "style"),
        Output("side_click", "data"),
    ],

    [Input("btn_sidebar", "n_clicks")],
    [
        State("side_click", "data"),
    ]
)
def toggle_sidebar(n, nclick):
    if n:
        if nclick == "SHOW":
            sidebar_style = SIDEBAR_HIDDEN
            content_style = CONTENT_STYLE_NO_SIDEBAR
            cur_nclick = "HIDDEN"
        else:
            sidebar_style = SIDEBAR_STYLE
            content_style = CONTENT_STYLE_SIDEBAR
            cur_nclick = "SHOW"
    else:
        sidebar_style = SIDEBAR_STYLE
        content_style = CONTENT_STYLE_SIDEBAR
        cur_nclick = 'SHOW'

    return sidebar_style, content_style, cur_nclick

@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 4)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/load-decomposition":
        # Treat page 1 as the homepage / index
        return True, False, False
    elif pathname == '/load-prediction':
         return False, True, False
    elif pathname == '/custom-view':
         return False, False, True
    return [pathname == f"/page-{i}" for i in range(1, 4)]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == '/':
         return welcome_layout
    elif pathname == '/load-decomposition':
         return load_decomposition_layout
    elif pathname == '/load-prediction':
         return upload_layout
    elif pathname == '/custom-view':
         return "Upcoming feature for custom view dashboard"
    elif pathname == '/about-project':
         return about_project_layout
    elif pathname == '/further-development':
         return "Upcoming page about work to be done..."
    else:
        return '404 error - page not found'


if __name__ == '__main__': 
    app.run_server(debug=True)
