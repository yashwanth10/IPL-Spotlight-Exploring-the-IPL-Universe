from dash import Dash, Input, Output, callback, dcc, html
import copy
import plotly.express as px
import pandas as pd

df = pd.read_csv('data/all_season_summary.csv')
df = df.dropna(subset=['season','home_boundaries','away_boundaries','home_score', 'away_score' ])
df['year'] = df['season'].astype(int)
df['year'] = df['year'].astype(str)
df_columns = ['year','home_team','away_team','home_runs', 'away_runs','home_boundaries','away_boundaries']


# boundary data preparation
boundaries_data = df[df_columns]
home_boundaries = boundaries_data.groupby(['year', 'home_team'])['home_boundaries'].mean().reset_index()
home_boundaries = home_boundaries.rename(columns={'home_boundaries': 'Average Boundaries', 'home_team':'team_name'})
home_boundaries['venue'] = 'home'
away_boundaries = boundaries_data.groupby(['year', 'away_team'])['away_boundaries'].mean().reset_index()
away_boundaries = away_boundaries.rename(columns={'away_boundaries': 'Average Boundaries', 'away_team':'team_name'})
away_boundaries['venue'] = 'away'
boundaries_data = pd.concat([away_boundaries, home_boundaries], ignore_index=True)

# run data preparation
run_data = df[df_columns]
home_run = run_data.groupby(['year', 'home_team'])['home_runs'].mean().reset_index()
home_run = home_run.rename(columns={'home_runs': 'Average Run', 'home_team':'team_name'})
home_run['venue'] = 'home'
away_run = run_data.groupby(['year', 'away_team'])['away_runs'].mean().reset_index()
away_run = away_run.rename(columns={'away_runs': 'Average Run', 'away_team':'team_name'})
away_run['venue'] = 'away'
run_data = pd.concat([away_run,home_run], ignore_index=True)



final_fig = html.Div(
    [
        # html.H3("Choose Team"),
        # dcc.Dropdown(
        #     id="teams", 
        #     options=[{'label': team, 'value': team} for team in sorted(boundaries_data['team_name'].unique())], 
        #     value='CSK'
        # ),
        # html.Br(),
        html.Div([
        dcc.Graph(id="boundaries_line"),
    ], style={'width': '49%', 'display': 'inline-block'}),
    #     html.Div([
    #     dcc.Graph(
    #         id='crossfilter-indicator-scatter',
    #         hoverData={'points': [{'customdata': 'Japan'}]}
    #     )
    # ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
        html.Div([ 
        dcc.Graph(id='run_line')
    ], style={'display': 'inline-block', 'width': '49%'}),
    ]
)

@callback(
    Output("boundaries_line", "figure"),
    Output("run_line", "figure"),
    # Input("teams", "value"),
    [Input("query-ipl_team-select", "value")]
)
def line_chart(value):
    team_name=value
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
    value=team_name
    dff = boundaries_data[boundaries_data['team_name']==value]
    fig1 = px.line(
        dff,
        x=dff['year'],
        y=dff["Average Boundaries"],
        color = dff['venue'],
        # template="simple_white",
        labels={"x": "Season", "y": "Average Boundaries"},
        # line_color='red'  
    )
    fig1.update_traces(mode='markers+lines')
    df_run = run_data[run_data['team_name']==value]
    fig2 = px.line(
        df_run,
        x=df_run['year'],
        y=df_run["Average Run"],
        color = df_run['venue'],
        # template="simple_white",
        labels={"x": "Season", "y": "Average Runs"},
        # line_color='red'  
    )
    fig2.update_traces(mode='markers+lines')
    fig2.update_layout(
        plot_bgcolor='rgb(0,0,0,0.3)', paper_bgcolor='rgb(7, 14, 57, 0.8)',yaxis=dict(gridcolor='#74b2d6'),xaxis=dict(gridcolor='#74b2d6'),
        font_color='white',
    legend=dict(
        title_text="Venue",  # Specify the title of the legend
        orientation="h",  # Set the orientation to horizontal
        x=0.5,  # Set the x position to be centered
        y=1.1,  # Set the y position to be above the plot
        bgcolor="rgba(255, 255, 255, 0)",  # Set the background color to be transparent
    )
)
    fig1.update_layout(
        plot_bgcolor='rgb(0,0,0,0.3)', paper_bgcolor='rgb(7, 14, 57, 0.8)',yaxis=dict(gridcolor='#74b2d6'),xaxis=dict(gridcolor='#74b2d6'),
        font_color='white',
    legend=dict(
        title_text="Venue",  # Specify the title of the legend
        orientation="h",  # Set the orientation to horizontal
        x=0.5,  # Set the x position to be centered
        y=1.1,  # Set the y position to be above the plot
        bgcolor="rgba(255, 255, 255, 0)",  # Set the background color to be transparent
    )
)
    return fig1, fig2


