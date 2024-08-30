import dash
from dash import Dash, Input, Output, callback, dcc, html
import dash_bootstrap_components as dbc
import copy
import plotly.express as px
import pandas as pd
import webbrowser
import csv
import numpy as np
import plotly.graph_objs as go

def draw_fig(dff, y_axis, ylabel,type, ti, v):
    if type=='line':
        fig = px.line(
            dff,
            title= ti + ' of ' + v + ' season by season',
            x=dff['year'],
            y=dff[y_axis],
            labels={"year":'Season' , y_axis:ylabel},
            template='plotly_dark'
        )
        fig.update_traces(mode='markers+lines')
    if type=='bar':
        fig = px.bar(
            dff,
            title = ti + ' of ' + v + ' season by season',
            x=dff['year'],
            y=dff[y_axis],
            labels={"year":'Season' , y_axis:ylabel},
            template='plotly_dark',
            color=y_axis,
            color_continuous_scale=px.colors.sequential.Plasma,
            hover_data=[y_axis]
        )

    fig.update_layout(xaxis_tickangle=45)
    return fig


def read_csv_file(file_path):
    data = []
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            data.append(row)
    return data

def calculate_ratio(player_name, bowling):
    ply = {}
    for i in li:
        x = 0
        y = 0
        for row in bowling:
            if row[11] == player_name and i == int(float(row[0])):
                try:
                    wickets = int(row[15]) if row[15].isdigit() else 0
                    runs = int(row[14]) if row[15].isdigit() else 0
                except ValueError:
                    continue
                x += wickets
                y += runs
        if x != 0:
            ply[i] = y / x
    return ply

bowling_file_path = 'data/all_season_bowling_card.csv'
bowling = read_csv_file(bowling_file_path)
li=[2023,2022,2021,2020,2019,2018,2017,2016,2015,2014,2013,2012,2011,2010,2009,2008]
df = pd.read_csv('data/all_season_batting_card.csv')
df1 = pd.read_csv('data/all_season_bowling_card.csv')
df1['average_boundaries_per_over'] = (df1['foursConceded'] + df1['sixesConceded']) / df1['overs']

batsman_cols = ['year','fullName','runs', 'ballsFaced','boundaries','isNotOut']
df = df.dropna(subset=['season','fullName'])
df['year'] = df['season'].astype(int).astype(str)
df['boundaries'] = df['fours']+df['sixes']
batsman_data = df[batsman_cols]

batsman_data_mod = batsman_data.groupby(['year', 'fullName']).agg({
    'runs': 'sum',
    'ballsFaced': 'sum',
    'boundaries': 'sum',
    'isNotOut': lambda x: (x == False).sum()
}).reset_index()

batsman_data_mod['strike_rate'] = batsman_data_mod['runs']/batsman_data_mod['ballsFaced']
batsman_data_mod['strike_rate'] = batsman_data_mod['strike_rate']*100
batsman_data_mod['avg_runs'] = batsman_data_mod['runs']/batsman_data_mod['isNotOut']
batsman_data_mod['boundaries'].astype(int)


All_graph = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H3("Choose Player", style={'color': '#1f77b4', 'fontSize': 34}),
            dcc.Dropdown(
                id="player", 
                options=[{'label': team, 'value': team} for team in sorted(batsman_data_mod['fullName'].unique())], 
                value='AB de Villiers',
                style={'color': '#000000', 'backgroundColor': '#B87DF9'}
            ),
        ], width=12),
    ], style={'marginBottom': '2px', 'padding': '2px'}),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id="strike_rate"), width=6),
        dbc.Col(dcc.Graph(id='runs'), width=6),
    ], style={'marginBottom': '10px',  'padding': '10px'}),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='boundaries'), width=6),
        dbc.Col(dcc.Graph(id='avg_runs'), width=6),
    ], style={'marginBottom': '10px',  'padding': '10px'}),
    
    dbc.Row([
        dbc.Col([
            html.H1("Bowler Performance Analysis", style={'color': '#1f77b4', 'fontSize': 34}),
            dcc.Dropdown(
                id='bowler-dropdown',
                options=[{'label': bowler, 'value': bowler} for bowler in df1['fullName'].unique()],
                value=df1['fullName'].unique()[0],
                style={'width': '100%', 'color': '#000000', 'backgroundColor': '#B87DF9'}
            )
        ], width=12),
    ], style={'marginBottom': '2px',  'padding': '2px'}),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='economy-graph'), width=6),
        dbc.Col(dcc.Graph(id='wickets-graph'), width=6),
    ], style={'marginBottom': '10px',  'padding': '10px'}),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='graph'), width=6),
        dbc.Col(dcc.Graph(id='player-graph'), width=6),
    ], style={'marginBottom': '10px',  'padding': '10px'})
], fluid=True)

@callback(
    Output("strike_rate", "figure"),
    Output("boundaries", "figure"),
    Output("runs", "figure"),
    Output("avg_runs", "figure"),
    Input("player", "value"),
)
def line_chart(value):
    dff = batsman_data_mod[batsman_data_mod['fullName']==value]
    fig1 = draw_fig(dff,'strike_rate',"Strike-Rate",'line','Strike Rate', value)
    fig2 = draw_fig(dff,'boundaries',"Boundaries",'bar', 'Total Boundaries', value)
    fig3 = draw_fig(dff,'runs',"Runs",'line', 'Total Runs', value)
    fig4 = draw_fig(dff,'avg_runs',"Average Runs",'bar', 'Average Runs', value)
    return fig1, fig2, fig3, fig4

@callback(
    Output('economy-graph', 'figure'),
    Input('bowler-dropdown', 'value')
)
def update_economy_graph(selected_bowler):
    filtered_df1 = df1[df1['fullName'] == selected_bowler]
    economy_data = filtered_df1.groupby('season').apply(lambda x: x['conceded'].sum() / x['overs'].sum())
    
    fig = px.line(x=economy_data.index, y=economy_data.values, labels={'x': 'Season', 'y': 'Economy'},
                  title=f"Economy of {selected_bowler} Season by Season", template='plotly_dark')
    fig.update_traces(mode='lines+markers')
    fig.update_layout(xaxis_title='Season', yaxis_title='Economy')
    fig.update_xaxes(tickmode='linear', tick0=min(economy_data.index), dtick=1)
    fig.update_layout(xaxis_tickangle=45)
    return fig

@callback(
    Output('wickets-graph', 'figure'),
    Input('bowler-dropdown', 'value')
)
def update_wickets_graph(selected_bowler):
    filtered_df1 = df1[df1['fullName'] == selected_bowler]
    wickets_data = filtered_df1.groupby('season')['wickets'].sum()
    fig = px.line(x=wickets_data.index, y=wickets_data.values, labels={'x': 'Season', 'y': 'Wickets'},
                  title=f"Wickets of {selected_bowler} Season by Season", template='plotly_dark')
    fig.update_traces(mode='lines+markers')
    fig.update_layout(xaxis_title='Season', yaxis_title='Wickets')
    fig.update_xaxes(tickmode='linear', tick0=min(wickets_data.index), dtick=1)
    fig.update_layout(xaxis_tickangle=45)
    return fig

@callback(
    Output('graph', 'figure'),
    Input('bowler-dropdown', 'value')
)
def update_graph(selected_bowler):
    filtered_df1 = df1[df1['fullName'] == selected_bowler]
    fig = px.bar(filtered_df1, x='season', y='average_boundaries_per_over', color='average_boundaries_per_over',
                 color_continuous_scale=px.colors.sequential.Plasma, template='plotly_dark', title='Average Boundaries per Over by Season',
                 hover_data=['foursConceded', 'sixesConceded'])
    fig.update_layout(
        coloraxis_colorbar=dict(
            x=1,  
            title=None  
        ),
        title_text='Bowling Performance Over the Seasons',
        xaxis_title="Season",
        yaxis_title="Average Boundaries per Over",
    )
    return fig

@callback(
    Output('player-graph', 'figure'),
    Input('bowler-dropdown', 'value')
)
def update_player_graph(selected_player):
    data = calculate_ratio(selected_player, bowling)
    keys = list(data.keys())
    values = list(data.values())
    filtered_df1 = df1[df1['fullName'] == selected_player]
    fig = px.bar(filtered_df1, x=keys, y=values, title='Ratio of Runs Given to Wickets Taken',
                template='plotly_dark',color=values,
                 color_continuous_scale=px.colors.sequential.Plasma)
    fig.update_layout(
        title_text='Ratio of Runs Given to Wickets Taken Over the Years',
        xaxis_title="Year",
        yaxis_title="Bowling average",  
    )
    return fig


