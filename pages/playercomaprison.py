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
from components.BatsmanvsBowler import Batsmanvsbowler
from components.BowlervsBowler import bowlervsbowler
from components.batsmancomparison import batsmancomparison




comparison_content = html.Div([
        dbc.Row([
            Batsmanvsbowler
        ]),
        dbc.Row([
            bowlervsbowler
        ]),
        dbc.Row([
            batsmancomparison
        ])
], style={"padding-top": "40px"})