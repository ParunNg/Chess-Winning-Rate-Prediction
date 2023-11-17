# Import packages
from dash import Dash, dcc, html, callback, Output, Input, State
import numpy as np
import pandas as pd
import pickle
import dash_bootstrap_components as dbc

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.LUX]
app = Dash(__name__, external_stylesheets=external_stylesheets)

def create_rating_diff(df):
    df = df.copy()
    df['rating_diff'] = df['white_rating'] - df['black_rating']
    return df

# paths of all components for car price predictions
model_path = "chess_winner_predictor.pkl"

# load all components
model = pickle.load(open(model_path, 'rb'))

# get all the possible first moves of white and black players
white_first_moves = list(model[0][1].transformers_[-2][1].categories_[0])
black_first_moves = list(model[0][1].transformers_[-2][1].categories_[1])

# App layout
app.layout = dbc.Container([
    html.Div([
        html.H1('Car Price Prediction', style={"margin-bottom":'20px'}),

        html.P("Having trouble setting the perfect price for your car...? No worries, \
               our car price prediction tool provides a means for finding a good selling price of your car based on the car specifications. \
               The car price predictions are based on the output of the machine learning model that we have painstakingly created.")
    ],
    style={"margin":'30px', "margin-bottom":'20px', "display":'inline-block'}),

    dbc.Row([
        html.Div([
            html.H5("Rated"),
            dbc.Label("Enter the max power of the car (must always be positive)"),
            dcc.Dropdown(id="rated", options=['True', 'False'], placeholder="Rated", style={"margin-bottom": '20px'}),

            html.H5("White Rating"),
            dbc.Label("Enter the manufacture year of the car"),
            dcc.Input(id="white_rating", type="number", min=1, max=3000, placeholder="White Rating", style={"margin-bottom": '20px'}), # 1983 is the minimum year in the cars dataset

            html.H5("Black Rating"),
            dbc.Label("Enter the fuel type of the car"),
            dcc.Input(id="black_rating", type="number", min=1, max=3000, placeholder="Black Rating", style={"margin-bottom": '20px'}),

            html.H5("Start Time Limit"),
            dbc.Label("Enter the brand of the car"),
            dcc.Input(id="time_limit", type="number", min=0, max=180, placeholder="Start Time Limit", style={"margin-bottom": '20px'}),

            html.H5("Increment"),
            dbc.Label("Enter the brand of the car"),
            dcc.Input(id="increment", type="number", min=0, max=180, placeholder="Increment", style={"margin-bottom": '20px'}),

            html.H5("White First Move"),
            dbc.Label("Enter the max power of the car (must always be positive)"),
            dcc.Dropdown(id="white_first", options=white_first_moves, placeholder="White First Move", style={"margin-bottom": '20px'}),

            html.H5("Black First Move"),
            dbc.Label("Enter the max power of the car (must always be positive)"),
            dcc.Dropdown(id="black_first", options=black_first_moves, placeholder="Black First Move", style={"margin-bottom": '20px'}),

            html.Div([dbc.Button(id="submit", children="Calculate White Winning Rate", color="primary"),
            html.Br(),

            html.Output(id="win_rate", children="", style={"margin-top": '10px', "background-color": 'navy', "color":'white'})
            ],
            style={"margin-top": "30px"})
        ],
        style={"margin-right":'30px', "margin-left":'30px', "margin-bottom":'30px', "display":'inline-block', "width": '700px'})
    ])
], fluid=True)


@callback(
    Output(component_id="win_rate", component_property="children"),
    State(component_id="rated", component_property="value"),
    State(component_id="white_rating", component_property="value"),
    State(component_id="black_rating", component_property="value"),
    State(component_id="time_limit", component_property="value"),
    State(component_id="increment", component_property='value'),
    State(component_id="white_first", component_property='value'),
    State(component_id="black_first", component_property='value'),
    Input(component_id="submit", component_property='n_clicks'),
    prevent_initial_call=True
)
def calculate_selling_price(rated, white_rating, black_rating, time_limit, increment, white_first, black_first, submit):
    features = {'rated': eval(rated),
                'white_rating': white_rating,
                'black_rating': black_rating,
                'start_time_limit': time_limit,
                'increment': increment,
                'white_first_move': white_first,
                'black_first_move': black_first}

    X = pd.DataFrame(features, index=[0])
    y = np.round(model.predict_proba(X)[:, 1], 2)

    return [f"White Winning Rate is: {y[0]}"]

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8001)