import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from dash import callback

df2 = pd.read_csv('data/batsman_vs_bowler.csv')


batsmancomparison = html.Div([
    html.P("Select Batsman 1",className="title-text"),
    html.Div([
    dcc.Dropdown(
        id='player-dropdown11',
        options=[{'label': player, 'value': player} for player in df2['Batsman'].unique()],
        value=df2['Batsman'].iloc[0],  # Default value for player 1
        clearable=False,
        style={'color': '#000000'}
    
    )],
    className="comparison-dropdown"),
    html.P("Select Batsman 2",className="title-text"),
    html.Div([
    dcc.Dropdown(
        id='player-dropdown22',
        options=[{'label': player, 'value': player} for player in df2['Batsman'].unique()],
        value=df2['Batsman'].iloc[1],  # Default value for player 2
        clearable=False
    )],className="comparison-dropdown"),
    dcc.Graph(id='avg_graph_batsman',className="graph-bg"),
    dcc.Graph(id='strikerate_graph_batsman',className="graph-bg"),


])
# Convert 'economyRate' column to numeric (ignore errors to handle NaN or non-numeric values)
# df['economyRate'] = pd.to_numeric(df['economyRate'], errors='coerce')


# Calculate total runs scored by each player in each season
total_runs_scored = df2.groupby(['Batsman', 'ID'])['Runs_Scored'].sum().reset_index()

# Calculate total balls faced by each player in each season
total_balls_faced = df2.groupby(['Batsman', 'ID'])['Balls_Faced'].sum().reset_index()

# Calculate total times out for each player in each season
total_times_out = df2[df2['Player_Out'] != 'Not Out'].groupby(['Batsman', 'ID']).size().reset_index(name='Times_Out')

# Merge total_runs_scored and total_times_out DataFrames
merged_df2 = pd.merge(total_runs_scored, total_times_out, on=['Batsman', 'ID'], how='outer')

# Merge total_runs_scored and total_times_out DataFrames
merged_df3_strikerate = pd.merge(total_runs_scored, total_balls_faced, on=['Batsman', 'ID'], how='outer')


# Fill NaN values with 0 for players who were not out in a season
merged_df2.fillna({'Times_Out': 0}, inplace=True)

# # Display the DataFrame with total runs scored and total times out for each player in each season
# print(merged_df2)
# Calculate runs scored per dismissal for each player in each season
merged_df2['Runs_Per_Dismissal'] = merged_df2['Runs_Scored'] / merged_df2['Times_Out']
merged_df3_strikerate['strike_rate']= (merged_df3_strikerate['Runs_Scored']/merged_df3_strikerate['Balls_Faced'])*100
# Round the Runs_Per_Dismissal to 2 decimal places
merged_df2['Runs_Per_Dismissal'] = merged_df2['Runs_Per_Dismissal'].round(2)

# Display the DataFrame with runs scored per dismissal for each player in each season
# print(merged_df2[['Batsman', 'ID', 'Runs_Per_Dismissal']])

@callback(
    Output('avg_graph_batsman', 'figure'),
    [Input('player-dropdown11', 'value'),
     Input('player-dropdown22', 'value')]
)
def update_avg_graph_batsman(player1, player2):
    if player1 and player2:
        filtered_player_df2 = merged_df2[(merged_df2['Batsman'] == player1) | (merged_df2['Batsman'] == player2)]
    elif player1:
        filtered_player_df2 = merged_df2[merged_df2['Batsman'] == player1]
    elif player2:
        filtered_player_df2 = merged_df2[merged_df2['Batsman'] == player2]
    else:
        filtered_player_df2 = merged_df2

    fig2 = px.bar(filtered_player_df2, x='ID', y='Runs_Per_Dismissal', color='Batsman',
             title='Comparison of Runs per Dismissal for Batsmen',
             labels={'ID': 'Season', 'Runs_Per_Dismissal': 'Runs per Dismissal', 'Batsman': 'Batsman'},
             barmode='group')

    fig2.update_xaxes(tickvals=list(range(2008, 2023)), ticktext=[str(year) for year in range(2008, 2023)])
    fig2.update_layout(yaxis=dict(gridcolor='#74b2d6'))  
    fig2.update_layout(plot_bgcolor='rgb(0,0,0,0.3)', paper_bgcolor='rgb(7, 14, 57, 0.8)',font_color='white')
    return fig2


@callback(
    Output('strikerate_graph_batsman', 'figure'),
    [Input('player-dropdown11', 'value'),
     Input('player-dropdown22', 'value')]
)
def update_strikerate_graph_batsman(player1, player2):
    if player1 and player2:
        filtered_player_df2_strikeRate = merged_df3_strikerate[(merged_df3_strikerate['Batsman'] == player1) | (merged_df3_strikerate['Batsman'] == player2)]
    elif player1:
        filtered_player_df2_strikeRate = merged_df3_strikerate[merged_df3_strikerate['Batsman'] == player1]
    elif player2:
        filtered_player_df2_strikeRate = merged_df3_strikerate[merged_df3_strikerate['Batsman'] == player2]
    else:
        filtered_player_df2_strikeRate = merged_df3_strikerate

    # Calculate strike rate (runs_scored / balls_faced) for each player in each season
    filtered_player_df2_strikeRate['Strike_Rate'] = (filtered_player_df2_strikeRate['Runs_Scored'] / filtered_player_df2_strikeRate['Balls_Faced'])*100

    fig3 = px.bar(filtered_player_df2_strikeRate, x='ID', y='Strike_Rate', color='Batsman',
             title='Comparison of Strike Rate for Batsmen',
             labels={'ID': 'Season', 'Strike_Rate': 'Strike Rate', 'Batsman': 'Batsman'},
             barmode='group')

    fig3.update_xaxes(tickvals=list(range(2008, 2023)), ticktext=[str(year) for year in range(2008, 2023)])
    fig3.update_layout(yaxis=dict(gridcolor='#74b2d6'))  
    fig3.update_layout(plot_bgcolor='rgb(0,0,0,0.3)', paper_bgcolor='rgb(7, 14, 57, 0.8)',font_color='white')
    return fig3




