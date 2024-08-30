import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output
from dash import callback

# Load your Excel data into a Pandas DataFrame
df = pd.read_csv('data/points_table (1).csv')

# Create a list of team names to exclude
exclude_teams = ['RPS', 'GL', 'PWI', 'Kochi']

# Define a dictionary mapping team names to colors
team_colors = {
    'CSK': '#FFD700',  # Yellow
    'MI': '#00008B',   # Dark Blue
    'RR': '#FFC0CB',   # Pink
    'SRH': '#FF8C00',  # Dark Orange
    'GT': '#9400D3',   # Dark Violet
    'RCB': '#FF0000',  # Red
    'LSG': '#87CEEB',  # Sky Blue
    'KKR': '#9400D3',  # Dark Violet
    'DC': '#00008B',   # Dark Blue
    'KXIP': '#FF0000'  # Light Red
}

# Define the app layout
# Figureperformance = html.Div([
#     html.H1("Team Performance Analysis"),
#     # dcc.Dropdown(
#     #     id='team-dropdown',
#     #     options=[{'label': team, 'value': team} for team in df['short_name'].unique() if team not in exclude_teams],
#     #     value=df['short_name'].unique()[0],  # Default value is the first team in the dropdown
#     #     style={'width': '50%'}
#     # ),
#     dcc.Graph(id='performance-graph'),
#     dcc.RangeSlider(
#         id='season-slider',
#         min=df['season'].min(),
#         max=df['season'].max(),
#         value=[df['season'].min(), df['season'].max()],
#         marks={str(season): str(season) for season in df['season'].unique()},
#         step=None,
#         className='dark-slider'  # Add a class for styling purposes
#     )
# ])

        
Figureperformance=html.Div([
    # dcc.Dropdown(
    #     id='team-dropdown',
    #     options=[{'label': team, 'value': team} for team in df['short_name'].unique() if team not in exclude_teams],
    #     value=df['short_name'].unique()[0],  # Default value is the first team in the dropdown
    #     style={'width': '50%', 'margin': 'auto', 'textAlign': 'center'}
    # ),
    dcc.Graph(id='performance-graph'),
])
# Define callback to update the graph based on selected team and season range
@callback(
    Output('performance-graph', 'figure'),
    Input("query-ipl_team-select", "value"),
)
def update_graph(selected_team):
    team_name=selected_team
    if team_name=='Royal Challengers Bangaluru':
        team_name='RCB'
    elif team_name=='Chennai Super King':
        team_name='CSK'
    elif team_name=='Mumbai Indians':
        team_name='MI'
    elif team_name=='Delhi Capitals':
        team_name='DC'
    elif team_name=='Kolkata Knight Riders':
        team_name='KKR'
    elif team_name=='Rajasthan Royals':
        team_name='RR'
    elif team_name=='Kings XI Punjab':
        team_name='KXIP'
    elif team_name=='Lucknow Super Giants':
        team_name='LSG'
    elif team_name=='Gujarat Titans':
        team_name='GT'
    else:
        team_name='SRH'
    selected_team=team_name
    filtered_df = df.loc[df['short_name'] == selected_team, :].copy()
    # Calculate the percentage of matches won for each season
    filtered_df['matches_won_percentage'] = (filtered_df['matcheswon'] / filtered_df['matchesplayed']) * 100
    fig = px.bar(filtered_df, x='season', y='matches_won_percentage', color='short_name',  # Use 'short_name' for color mapping
                 color_discrete_map=team_colors,  # Map colors based on team_colors dictionary
                 labels={'matches_won_percentage': 'Matches Won Percentage', 'matcheswon': 'Matches Won'},
                 title=f"Performance of {selected_team} Season by Season",
                 hover_data={'matches_won_percentage': ':.2f%'},  # Display hover data with 2 decimal places
                 height=500  # Set the height of the graph
                 )
    fig.update_layout(
        plot_bgcolor='rgb(0,0,0,0.3)', paper_bgcolor='rgb(7, 14, 57, 0.8)',font_color='white',  # Set background color with opacity
        xaxis=dict(title='Season', showgrid=False, showline=True,gridcolor='#74b2d6'),  # Customize x-axis
        yaxis=dict(title='Matches Won Percentage (%)', showgrid=True, showline=True,gridcolor='#74b2d6'),  # Customize y-axis
        font=dict(family="Arial, sans-serif", size=12,),  # Set font style and size
        margin=dict(l=50, r=50, t=80, b=50),  # Adjust margins
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),  # Position legend
    )
    return fig


