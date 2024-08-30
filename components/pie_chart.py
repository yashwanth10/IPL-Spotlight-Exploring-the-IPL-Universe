import plotly.express as px
import pandas as pd
from dash import html, dcc
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_loading_spinners as dls
from dash import callback
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

# Read the CSV file into a DataFrame
# df = pd.read_csv('data/all_season_summary.csv')
# df1 = pd.read_csv('data/IPL.csv')

def compute(team_name,season):
    # Read the CSV file into a DataFrame
    df = pd.read_csv('data/all_season_summary.csv')

    # Take inputs from the user: season and team name
    season = int(season)
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
        team_name='PBKS'
    elif team_name=='Lucknow Super Giants':
        team_name='LSG'
    elif team_name=='Gujarat Titans':
        team_name='GT'
    else:
        team_name='SRH'

    # Filter the DataFrame based on the user-provided season and team name
    # df = df[(df['season'] == season) & ((df['home_team'] == team_name) | (df['away_team'] == team_name))]

    # Count home wins where the winner is the same as the team name
    home_win_count = df[(df['home_team'] == team_name) & (df['winner'] == team_name)& (df['season'] == season)].shape[0]

    # Count away wins where the winner is the same as the team name
    away_win_count = df[(df['away_team'] == team_name) & (df['winner'] == team_name)&(df['season'] == season)].shape[0]

    # print(home_win_count)
    # print(f"Away win count for {team_name} in season {season}: {away_win_count}")

    return home_win_count,away_win_count

Season_select = html.Div(className="col-lg-4 col-md-3 col-sm-3 card-chart-container season_dropdown", children=[html.Div(className="card-chart", children=[
        html.Div(className="card-chart",style={'padding-top': '25px','width':'370px'}, children=[
            html.Div(className="card-chart-container", style={'margin-left': '52px'},children=[
                html.Div(className="card-m-2 me-4 pb-2  ",
                        children=[
                            dbc.Select(
                                className= "dropdown_bg",
                                id="season-select",
                                value="2023",
                                options=[
                                    {"label": str(year), "value": str(year)}  for year in range(2012, 2024)
                                ],
                                style={"width": "14rem"}
                            )
                        ]),

            ])

        ])
    ])]
    )


IPLpiechart = html.Div(className="card-chart-container col-lg-4 md-1 sm-1",style={'padding-left': '10px','width':'500px'},
                    children=[
                        html.Div(
                            className="card-chart ",
                            children=[
                                Season_select,
                                html.H4(id = 'my-head11', children = "Results",
                                    className=" card-chart-container ", style={"font-size": "1.5vw", "text-align" : "center", 'padding-top': '25px', 'color': 'white'}),
                                        dls.Roller(
                                            id="final",
                                            children=[
                                    ], debounce=0
                                )
                            ]
                        )

                    ]
                    )



# Season_select = html.Div([
#     html.Div(
#         className="col-lg-4 col-md-3 col-sm-3 card-chart-container season_dropdown",
#         children=[
#             html.Div(
#                 className="card-chart",
#                 children=[
#                     html.Div(
#                         className="card-chart",
#                         style={'padding-top': '25px'},
#                         children=[
#                             html.Div(
#                                 className="card-chart-container",
#                                 style={'margin-left': '52px'},
#                                 children=[
#                                     html.Div(
#                                         className="card-m-2 me-4 pb-2",
#                                         children=[
#                                             dbc.Select(
#                                                 className="dropdown_bg",
#                                                 id="season-select",
#                                                 value="2023",
#                                                 options=[
#                                                     {"label": str(year), "value": str(year)} for year in range(2012, 2024)
#                                                 ],
#                                                 style={"width": "14rem"}
#                                             )
#                                         ]
#                                     ),
#                                 ]
#                             )
#                         ]
#                     )
#                 ]
#             )
#         ]
#     ),
#     html.Div(
#         className="card-chart-container col-lg-4 md-1 sm-1",
#         children=[
#             html.Div(
                
#                 className="card-chart",
#                 children=[
#                     html.H4(
#                         id='my-head11',
#                         children="Results",
#                         className="card-chart-container",
#                         style={"font-size": "1.5vw", "text-align": "center", 'padding-top': '25px', 'color': 'white'}
#                     ),
#                     dls.Roller(
#                         id="final",
#                         children=[],
#                         debounce=0
#                     )
#                 ]
#             )
#         ]
#     )
# ])


@callback(
    Output("final", "children"),
    Output("my-head11", "children"),
    [Input("query-ipl_team-select", "value"),
     Input("season-select", "value")]
    #State("goals-df", "data"),
    #State("qualified-teams-df" , "data")
)

def update_figures(query_team,season):
    # tstats = pd.read_csv('data/team_stats.csv')
    home_win,away_win=compute(query_team,season)
    # print(query_team,season,home_win,away_win)
    # df = tstats.query(f"team_name=='{query_team}'")
    data = dict(labels=['Home won', 'Away won'],
            values=[home_win,away_win])
    colors = [ '#e53935']
    fig = px.pie(data, values='values', names='labels',
                )
    fig.update_traces(marker=dict(colors=colors))
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(plot_bgcolor='rgb(0,0,0,0.3)', paper_bgcolor='rgb(7, 14, 57, 0.8)')
    
    

    return dcc.Graph(figure=fig
        .update_layout(paper_bgcolor="rgb(0,0,0,0)",
                    showlegend = False,
                    plot_bgcolor="rgb(0,0,0,0)",
                    legend=dict(
                    bgcolor="#fff"),
                    font_family="Public Sans, Amiri, Qatar2022, Poppins,",
                    
                    ),
        config={
        "displayModeBar": False},
        style={"height" : "25.875rem"}

    ) , f'Match results of {query_team}'