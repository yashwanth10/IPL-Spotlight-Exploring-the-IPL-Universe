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

from components.performance_player import All_graph
from components.performance_player_new import All_graph_new




player_performance = html.Div([
        dbc.Row([
            All_graph_new
        ]),
        
       
], style={"padding-top": "40px"})