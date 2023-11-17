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
white_first_moves = list(model.named_steps['preprocessor'].
                         named_steps['transformers'].transformers_[-1][1].categories_[0])
black_first_moves = list(model.named_steps['preprocessor'].
                         named_steps['transformers'].transformers_[-1][1].categories_[1])

num_cols = ['white_rating', 'black_rating', 'start_time_limit', 'increment']

# App layout
app.layout = dbc.Container([
    html.Div([
        html.H1('Victory Vision', style={"margin-bottom":'20px'})],
    style={"margin":'30px', "margin-bottom":'20px', "display":'inline-block'}),

    dbc.Row([
        html.Div([
            html.H5("Rated"),
            dbc.Label("Whether a chess match is rated or not"),
            dcc.Dropdown(id="rated", options=['True', 'False'], value='True', clearable=False, style={"margin-bottom": '20px'}),

            html.H5("White Rating"),
            dbc.Label("Enter the rating of white player"),
            dbc.Input(id="white_rating", type="number", min=1, max=3000, placeholder="White Rating", style={"margin-bottom": '20px'}), # 1983 is the minimum year in the cars dataset

            html.H5("Black Rating"),
            dbc.Label("Enter the rating of black player"),
            dbc.Input(id="black_rating", type="number", min=1, max=3000, placeholder="Black Rating", style={"margin-bottom": '20px'}),

            html.H5("Start Time Limit"),
            dbc.Label("Enter the start time limit of a chess match (If there is no time limit, leave it as 0)"),
            dbc.Input(id="time_limit", type="number", min=0, max=180, placeholder="Start Time Limit", style={"margin-bottom": '20px'}),

            html.H5("Increment"),
            dbc.Label("Enter the time increment every time a player ends their turn (If there is no increment, leave it as 0)"),
            dbc.Input(id="increment", type="number", min=0, max=180, placeholder="Increment", style={"margin-bottom": '20px'}),

            html.H5("White First Move"),
            dbc.Label("Enter the white player's first move in a chess match"),
            dcc.Dropdown(id="white_first", options=white_first_moves, placeholder="White First Move", style={"margin-bottom": '20px'}),

            html.H5("Black First Move"),
            dbc.Label("Enter the black player's first move in a chess match"),
            dcc.Dropdown(id="black_first", options=black_first_moves, placeholder="Black First Move", style={"margin-bottom": '20px'}),

            html.Div([dbc.Button(id="submit", children="Calculate White Winning Rate", color="primary"),
            html.Br(),

            html.Output(id="win_rate", children="", style={"margin-top": '10px', "background-color": 'DarkGoldenRod', "color":'white'})
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
    X[num_cols] = X[num_cols].astype(float)
    y = np.round(model.predict_proba(X)[:, 1][0]*100, 2)

    return [f"White Player Winning Rate is: {y}%"]

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)