from dash import html
import dash_bootstrap_components as dbc

layout = dbc.Container([
    html.Div([
        html.P("Chess, a game of timeless elegance and profound complexity, has captivated players for centuries. \
               It represents the epitome of strategy and skill, where the ability to assess one's chances of winning is of paramount importance. \
               In the contemporary world, chess has evolved into an international phenomenon, marked by official competitions conducted by the FIDE \
               (International Chess Federation) to determine grandmasters and, ultimately, the world champion.  \
               Given the pivotal role competitive chess plays in the lives of professional players, \
               there is a growing desire to enhance their odds of success and to devise winning strategies."),
               
        html.P("This project embarks on a remarkable journey to develop a predictive model for chess game outcomes, \
               with the primary aim of creating a tool that empowers players to estimate their chances of winning a game. \
               This estimation will be rooted in an analysis of the current state of the chessboard and will incorporate other relevant factors such as playing style, player ratings, and more.")

    ], style={"margin-bottom":'20px', "display":'inline-block'})
], fluid=True)