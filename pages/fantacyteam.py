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

from components.dream11 import final_output




fantacy_team = html.Div([
        dbc.Row([
            final_output
        ]),
        
       
], style={"padding-top": "40px"})