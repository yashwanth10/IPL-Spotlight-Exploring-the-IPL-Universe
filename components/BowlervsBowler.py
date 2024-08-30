import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from dash import callback

df = pd.read_csv('data/all_season_bowling_card.csv')
filtered_df = df[(df['season'] >= 2008) & (df['season'] <= 2022)]
# Convert 'economyRate' column to numeric (ignore errors to handle NaN or non-numeric values)
# df['economyRate'] = pd.to_numeric(df['economyRate'], errors='coerce')


bowlervsbowler = html.Div([
    html.P("Select Bowler 1",className="title-text"),
    html.Div([
    dcc.Dropdown(
        id='player-dropdown1',
        options=[{'label': player, 'value': player} for player in df['fullName'].unique()],
        value=df['fullName'].iloc[0],  # Default value for player 1
        clearable=False
    )],className="comparison-dropdown"),
    html.P("Select Bowler 2",className="title-text"),
    html.Div([
    dcc.Dropdown(
        id='player-dropdown2',
        options=[{'label': player, 'value': player} for player in df['fullName'].unique()],
        value=df['fullName'].iloc[1],  # Default value for player 2
        clearable=False
    )],className="comparison-dropdown"),
   
    dcc.Graph(id='economy_rate_histogram',className="graph-bg"),
    dcc.Graph(id='avg_graph',className="graph-bg"),
])


@callback(
    Output('economy_rate_histogram', 'figure'),
    [Input('player-dropdown1', 'value'),
     Input('player-dropdown2', 'value')]
)
def update_economy_rate_histogram(player1, player2):
    if player1 and player2:
        filtered_player_df = filtered_df[(filtered_df['fullName'] == player1) | (filtered_df['fullName'] == player2)]
    elif player1:
        filtered_player_df = filtered_df[filtered_df['fullName'] == player1]
    elif player2:
        filtered_player_df = filtered_df[filtered_df['fullName'] == player2]
    else:
        filtered_player_df = filtered_df
    # Convert 'economyRate' column to numeric type
    filtered_player_df['economyRate'] = pd.to_numeric(filtered_player_df['economyRate'], errors='coerce')

    # Calculate mean economy rate for each season for both players
    mean_economy_rate = filtered_player_df.groupby(['fullName', 'season'])['economyRate'].mean().reset_index()

    # Round the mean economy rate to 2 decimal places
    mean_economy_rate['economyRate'] = mean_economy_rate['economyRate'].round(2)

    fig = px.histogram(mean_economy_rate, x='season', y='economyRate', color='fullName',
                 title='Mean Economy Rate Comparison (2008-2022)',
                 labels={'season': 'Season', 'economyRate': 'Mean Economy Rate', 'fullName': 'Player'},
                 barmode='group')
    fig.update_xaxes(tickvals=list(range(2008, 2023)), ticktext=[str(year) for year in range(2008, 2023)])
    fig.update_layout(yaxis=dict(gridcolor='#74b2d6'))  
    fig.update_layout(plot_bgcolor='rgb(0,0,0,0.3)', paper_bgcolor='rgb(7, 14, 57, 0.8)',font_color='white')
    return fig

# Convert 'conceded' column to numeric type
df['conceded'] = pd.to_numeric(df['conceded'], errors='coerce')

# Calculate the total runs given by each player for each season
total_runs_given = df.groupby(['fullName', 'season'])['conceded'].sum().reset_index()

# Convert 'wickets' column to numeric type
df['wickets'] = pd.to_numeric(df['wickets'], errors='coerce')

# Calculate the total wickets taken by each player for each season
total_wickets_taken = df.groupby(['fullName', 'season'])['wickets'].sum().reset_index()

# Merge the total_runs_given and total_wickets_taken DataFrames on fullName and season
merged_df = pd.merge(total_runs_given, total_wickets_taken, on=['fullName', 'season'], suffixes=('_runs', '_wickets'))

# Replace 0 wickets with 1 to avoid division by zero
merged_df['wickets'] = merged_df['wickets'].replace(0, 1)

# Calculate the average runs conceded per wicket for each player in each season
merged_df['average_per_wicket'] = merged_df['conceded'] / merged_df['wickets']

# Round the average to 2 decimal places
merged_df['average_per_wicket'] = merged_df['average_per_wicket'].round(2)

# Filter the data for seasons from 2008 to 2022
merged_df = merged_df[(merged_df['season'] >= 2008) & (merged_df['season'] <= 2022)]

# Display the DataFrame with the average runs conceded per wicket for each player in each season
# print(merged_df[['fullName', 'season', 'average_per_wicket']])

# Display the DataFrame with the average runs conceded per wicket for each player in each season
# print(merged_df[['fullName', 'season', 'average_per_wicket']])
@callback(
    Output('avg_graph', 'figure'),
    [Input('player-dropdown1', 'value'),
     Input('player-dropdown2', 'value')]
)
def update_avg_graph(player1, player2):
    if player1 and player2:
        filtered_player_df = merged_df[(merged_df['fullName'] == player1) | (merged_df['fullName'] == player2)]
    elif player1:
        filtered_player_df = merged_df[merged_df['fullName'] == player1]
    elif player2:
        filtered_player_df = merged_df[merged_df['fullName'] == player2]
    else:
        filtered_player_df = merged_df

    fig = px.bar(filtered_player_df, x='season', y='average_per_wicket', color='fullName',
                 title='Average Runs Conceded per Wicket Comparison',
                 labels={'season': 'Season', 'average_per_wicket': 'Average Runs Conceded per Wicket', 'fullName': 'Player'},
                 barmode='group')
    fig.update_xaxes(tickvals=list(range(2008, 2023)), ticktext=[str(year) for year in range(2008, 2023)])
    fig.update_layout(yaxis=dict(gridcolor='#74b2d6'))  
    fig.update_layout(plot_bgcolor='rgb(0,0,0,0.3)', paper_bgcolor='rgb(7, 14, 57, 0.8)',font_color='white')
    return fig



