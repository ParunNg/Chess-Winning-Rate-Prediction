# Import necessary libraries 
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app
from transform import create_rating_diff
from pages import home, prediction

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "DarkGrey",
    "display":'inline-block',
    "font-weight": "bold"
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


# Define the index page layout
sidebar = html.Div([
    html.H3("Victory Vision", style={"text-align": "center"}),
    html.Hr(),
    dbc.Nav(
    children=[
        dbc.NavItem(dbc.NavLink("Introduction", href="/", active="exact")),
        dbc.NavItem(dbc.NavLink("Prediction", href="/prediction", active="exact"))
    ],
    vertical=True,
    pills=True
    )], style=SIDEBAR_STYLE)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

# Create the callback to handle mutlipage inputs
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])

def display_page(pathname):
    if pathname == '/':
        return home.layout
    if pathname == '/prediction':
        return prediction.layout
    else: # if redirected to unknown link
        return home.layout

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)