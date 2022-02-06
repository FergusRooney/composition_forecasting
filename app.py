import flask
import dash
  
# Server side configs
server = flask.Flask(__name__) # define flask app.server
app = dash.Dash(__name__,
                suppress_callback_exceptions=True,
                server=server,
                external_stylesheets=["assets\classic.css"])#[dbc.themes.SOLAR]) # NOTE: Bootstrap theme SANDSTONE does not operate well with the sidebar menu and navbar menu
server = app.server
app.title = "Demand-Response dashboard"