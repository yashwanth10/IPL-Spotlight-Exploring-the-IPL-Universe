from dash import html
import dash_bootstrap_components as dbc
# from components.attach_map import mapping
from components.introcard import IPLIntroCard
from components.home_page_logo import home_logo

iplHome = html.Div([
    dbc.Row([
            IPLIntroCard,
            ]),
    dbc.Row([
            home_logo,
            ])
], style={"padding-top": "40px"})