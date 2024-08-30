import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import Dash, dcc, html
import plotly.express as px
import numpy as np
#import altair as alt
#from vega_datasets import data
import pandas as pd
import base64

from components.ipl_teams import IPLTeamStats
from components.pie_chart import Season_select,IPLpiechart
from components.boundry_line_run_line import final_fig
from components.season_performance import Figureperformance
from components.Qualify_final_winners   import qualify
from components.logo_selecter import logo,Players_name,Season_Won



team_content = html.Div([
        dbc.Row([
            IPLTeamStats
        ]),
        dbc.Row([
            logo,
            Players_name,
            Season_Won
            
        ]),
        dbc.Row([
        # Season_select,
        IPLpiechart,
        qualify
        ], style={'display': 'flex', 'flex-wrap': 'nowrap'}),
        dbc.Row([
        final_fig
        ]),
        dbc.Row([
        Figureperformance
        ]),
        # dbc.Row([
        # qualify
        # ])
], style={"padding-top": "40px"})