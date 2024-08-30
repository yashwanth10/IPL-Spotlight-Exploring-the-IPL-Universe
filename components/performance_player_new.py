import dash
from dash import Input, Output, dcc, html
from dash import  callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import webbrowser
# import dash_core_components as dcc
#import dash_html_components as html
from dash.dependencies import Input, Output
import csv

def read_csv_file(file_path):
    data = []
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            data.append(row)
    return data

batting = read_csv_file('data/all_season_batting_card_1.csv')
bowling_file_path = 'data/all_season_bowling_card_1.csv'
bowling = read_csv_file(bowling_file_path)
li=[2023,2022,2021,2020,2019,2018,2017,2016,2015,2014,2013,2012,2011,2010,2009,2008]

df = pd.read_csv('data/all_season_batting_card_1.csv')
df1 = pd.read_csv('data/all_season_bowling_card_1.csv')
df1['average_boundaries_per_over'] = (df1['foursConceded'] + df1['sixesConceded']) / df1['overs']
df2 = pd.read_csv('data/cricket_data.csv')
df2['Runs_Conceded'] = pd.to_numeric(df2['Runs_Conceded'], errors='coerce')
df2['Wickets_Taken'] = pd.to_numeric(df2['Wickets_Taken'], errors='coerce')
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

def bowl(player_name):
    run=0
    six=0
    four=0
    for row in bowling:
        if row[11]==player_name:
            runs=int(row[14]) if row[14].isdigit() else 0
            run+=runs
            six+=int(row[19]) if row[14].isdigit() else 0
            four+=int(row[18]) if row[14].isdigit() else 0  
    return {"fours": four*4, "sixes": six*6, "others": run-four*4-six*6}

def bat(player_name):
    bou=0
    run=0
    ball=0
    out=0
    four=0
    six=0
    for row in batting:
        if row[11]==player_name:
            
            four+=int(row[15]) if row[15].isdigit() else 0
            six+=int(row[16]) if row[16].isdigit() else 0
            runs = int(row[12]) if row[12].isdigit() else 0
            run+=runs        
    return {"fours": four*4, "sixes": six*6, "others": run-four*4-six*6}

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
    
def read_csv_file(file_path):
    data = []
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            data.append(row)
    return data

player_names = df['fullName'].unique()

def team_comp(player):
    
    di={'LSG': 0, 'KKR':0, 'SRH': 0, 'GT': 0, 'CSK': 0, 'MI': 0, 'RR': 0, 'PBKS': 0, 'RCB': 0, 'DC': 0}
    
    for row in batting:
        if row[11]==player:
            x='CSK'
            if row[8]!=row[3]:
                x=row[3]
            else:
                x=row[4]
            runs=int(row[14]) if row[14].isdigit() else 0
            if x in di:
                di[x]+=runs
    return di

player_names1 = df1['fullName'].unique()

def get_wickets_by_team(player_name):
    
    wickets_by_team = {}
    
    for _, row in df1.iterrows():
        if row['fullName'] == player_name:
            team = row['away_team'] if row['bowling_team'] == row['home_team'] else row['home_team']
            wickets_by_team[team] = wickets_by_team.get(team, 0) + row['wickets']
    return wickets_by_team
    
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


    


All_graph_new = dbc.Container([
    
    dbc.Row([
        dbc.Col([
            html.H3("Choose Player", style={'color': 'white', 'fontSize': 34},className="title-text"),
            dcc.Dropdown(
                id="player", 
                options=[{'label': team, 'value': team} for team in sorted(batsman_data_mod['fullName'].unique())], 
                value='AB de Villiers',
                style={'color': '#000000', 'backgroundColor': '#B87DF9'}
            ),
        ], width=12),
    ], style={'marginBottom': '2px',  'padding': '2px'}),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id="strike_rate_1"), width=6),
        dbc.Col(dcc.Graph(id='runs_1'), width=6),
    ], style={'marginBottom': '10px', 'padding': '10px'}),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='boundaries_1'), width=6),
        dbc.Col(dcc.Graph(id='avg_runs_1'), width=6),
    ], style={'marginBottom': '10px',  'padding': '10px'}),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='runs-by-team'), width=6),
        dbc.Col(dcc.Graph(id='runs-ratio'), width=6),
    ], style={'marginBottom': '10px',  'padding': '10px'}),
    
    dbc.Row([
        dbc.Col([
            html.H1("Bowler Performance Analysis", style={'color': '#1f77b4', 'fontSize': 34}),
            dcc.Dropdown(
                id='bowler-dropdown',
                options=[{'label': bowler, 'value': bowler} for bowler in df1['fullName'].unique()],
                value=df1['fullName'].unique()[0],
                style={'width': '100%', 'color': '#000000', 'backgroundColor': '#B87DF9'}
            )], width = 12),
            ], style={'marginBottom': '2px',  'padding': '2px'}),
    
            dbc.Row([
            dbc.Col(dcc.Graph(id='economy-graph_1'), width=6),
                dbc.Col(dcc.Graph(id='wickets-graph_1'), width=6),
            ], style={'marginBottom': '10px',  'padding': '10px'}),
            
            dbc.Row([
            dbc.Col(dcc.Graph(id='graph_1'), width=6),
            dbc.Col(dcc.Graph(id='player-graph_1'), width=6),
            ], style={'marginBottom': '10px',  'padding': '10px'}),
            
            dbc.Row([
            dbc.Col(dcc.Graph(id='wickets-by-team'), width=6),
            dbc.Col(dcc.Graph(id='wicket-ratio'), width=6),
            ], style={'marginBottom': '10px',  'padding': '10px'}),
    ], fluid=True)
    
@callback(
    Output("strike_rate_1", "figure"),
    Output("boundaries_1", "figure"),
    Output("runs_1", "figure"),
    Output("avg_runs_1", "figure"),
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
    Output('economy-graph_1', 'figure'),
    Input('bowler-dropdown', 'value')
)

def update_graph_1(selected_bowler):
    filtered_df1 = df1[df1['fullName'] == selected_bowler]
    economy_data = filtered_df1.groupby('season').apply(lambda x: x['conceded'].sum() / x['overs'].sum())
    
    fig = px.line(x=economy_data.index, y=economy_data.values, labels={'x': 'Season', 'y': 'Economy'},
                  title=f"Economy of {selected_bowler} Season by Season", template='plotly_dark')
    fig.update_layout(xaxis_title='Season', yaxis_title='Economy')
    return fig

@callback(
    Output('wickets-graph_1', 'figure'),
    Input('bowler-dropdown', 'value')
    
)

def update_graph_2(selected_bowler):
    filtered_df1 = df1[df1['fullName'] == selected_bowler]
    wickets_data = filtered_df1.groupby('season')['wickets'].sum()
    fig = px.line(x=wickets_data.index, y=wickets_data.values, labels={'x': 'Season', 'y': 'Wickets'},
                  title=f"Wickets of {selected_bowler} Season by Season", template='plotly_dark')
    fig.update_layout(xaxis_title='Season', yaxis_title='Wickets')
    return fig

@callback(
    Output('graph_1', 'figure'),
    [Input('bowler-dropdown', 'value')]
)

def update_figure_3(selected_bowler):
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
    Output('player-graph_1', 'figure'),
    [Input('bowler-dropdown', 'value')]
)

def update_graph_4(selected_player):
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

@callback(
    Output('wickets-by-team', 'figure'),
    Input('bowler-dropdown', 'value')
)

def update_figure_5(selected_bowler):
    filtered_df1 = df1[df1['fullName'] == selected_bowler]
    x = get_wickets_by_team(selected_bowler)

    df1_wickets = pd.DataFrame(list(x.items()), columns=['Team', 'Wickets'])

    # Plot the DataFrame
    fig = px.bar_polar(df1_wickets, r='Wickets', theta='Team', color='Wickets',
                       color_continuous_scale=px.colors.sequential.Plasma, 
                       template='plotly_dark', title='Wickets by Team')

    fig.update_layout(
        title_text='Wickets taken by ' + selected_bowler + ' Per Team',
        title_x=0.5,
        font=dict(
            family="Times New Roman, sans-serif",
            size=18,
            color="#FFFFFF"
        )
    )
    return fig

@callback(
    Output('runs-by-team', 'figure'),
    Input('player', 'value')
)

def update_figure_6(selected_bowler):
    x = team_comp(selected_bowler)

    df_runs = pd.DataFrame(list(x.items()), columns=['Team', 'Runs'])

    # Plot the DataFrame
    fig = px.bar_polar(df_runs, r='Runs', theta='Team', color='Runs',
                       color_continuous_scale=px.colors.sequential.Plasma, 
                       template='plotly_dark', title='Wickets by Team')

    fig.update_layout(
        title_text='Runs scored by ' + selected_bowler + ' Per Team',
        title_x=0.5,
        font=dict(
            family="Times New Roman, sans-serif",
            size=18,
            color="#FFFFFF"
        )
    )
    return fig

@callback(
    Output('runs-ratio', 'figure'),
    Input('player', 'value')
)

def update_figure_7(selected_bowler):
    x = bat(selected_bowler)
    print(x)
    df1_runs = pd.DataFrame(list(x.items()), columns=['Division', 'Runs Scored'])

    # Plot the DataFrame
    fig = px.bar(df1_runs, x='Runs Scored', y='Division', color='Runs Scored',
             color_continuous_scale=px.colors.sequential.Plasma, 
             template='plotly_dark', title='Runs Scored',
             orientation='h')

    fig.update_layout(
        title_text='Runs Division of ' + selected_bowler,
        title_x=0.5,
        font=dict(
            family="Times New Roman, sans-serif",
            size=18,
            color="#FFFFFF"
        )
    )
    return fig

@callback(
    Output('wicket-ratio', 'figure'),
    Input('bowler-dropdown', 'value')
)

def update_figure_8(selected_bowler):
    x = bowl(selected_bowler)

    df1_runs = pd.DataFrame(list(x.items()), columns=['Division', 'Runs Conceeded'])

    # Plot the DataFrame
    fig = px.bar(df1_runs, x='Runs Conceeded', y='Division', color='Runs Conceeded',
             color_continuous_scale=px.colors.sequential.Plasma, 
             template='plotly_dark', title='Runs Scored',
             orientation='h')

    fig.update_layout(
        title_text='Runs conceded by ' + selected_bowler,
        title_x=0.5,
        font=dict(
            family="Times New Roman, sans-serif",
            size=18,
            color="#FFFFFF"
        )
    )
    return fig

