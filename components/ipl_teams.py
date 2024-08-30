from dash.dependencies import Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html
import dash_loading_spinners as dls
from dash import callback
import plotly.express as px

df_teams = pd.read_csv("data/IPL.csv")




IPLTeamStats = html.Div(className="chart-container main_dropdown", children=[html.Div(className="card-chart", children=[
        html.Div(className="card-chart",style={'padding-top': '25px','width':'1200px'}, children=[
            html.Div(className="card-chart-container", style={'margin-left': '52px','size':'500px'},children=[
                html.Div(className="card-m-3 me-3 pb-3",
                        children=[
                            dbc.Select(
                                className= "dropdown_bg custom-dropdown",
                                id="query-ipl_team-select",
                                value="Chennai Super King",
                                options=[
                                    {"label": l, "value": l} for l in df_teams.team_name.values
                                ],
                                style={"width": "20rem"}
                            ),
                            html.P(className="card-text mb-1 fs-sm mt-4 ml-4 pl-4",
                                    id="ipl_team-code-text",
                                    style={'color': 'white', "font-size": "15px", "align" : "center"},
                                    children=[f"Team Code: "])
                            # html.P(className="card-text mb-1 fs-sm",
                            #         id="team-region-text",
                            #         children=[f"Region:"]),
                            # html.P(className="card-text mb-1 fs-sm",
                            #         id="team-confederation-text",
                            #         children=[f"Conf: "]),
                            # html.A(id="query-team-wiki-link",
                            #         href = '',
                            #         target="_blank",
                            #         style={"font-size": "0.7rem", "color" : "blue"})
                        ]),

            ])

        ])
    ])]
    )






@callback(
    Output("ipl_team-code-text", "children"),
    # Output("team-region-text", "children"),
    # Output("team-confederation-text", "children"),
    # Output("query-team-wiki-link", "href"),
    # Output("query-team-wiki-link", "children"),
    # Output("team-flag-main", "src"),
    [Input("query-ipl_team-select", "value")]
    # State("teams-df", "data"),
)

def update_team_select(value):
    teams_df = pd.read_csv("data/IPL.csv")
    team_code = f"Team Code: {teams_df.loc[teams_df.team_name==value , 'team_code'].values[0]}"
    # team_region = f"Region: {teams_df.loc[teams_df.team_name==value , 'region_name'].values[0]}"
    # team_confederation = f"Confedration: {teams_df.loc[teams_df.team_name==value , 'confederation_code'].values[0]}"
    # wiki_link = teams_df.loc[teams_df.team_name ==value, 'team_wikipedia_link'].values[0]
    # team_flag = f"assets/flags/{value}.svg"
    # winning_times = df_teams1.loc[df_teams1.team_name ==value]["winning_times"].values[0]
    # winning_years = "- ".join(df_teams2.loc[df_teams2.winner ==value, "year"].values.astype("str"))
    # matches_count = df_teams1.loc[df_teams1.team_name ==value]["count_matches"].values[0]
    
    
    
    return team_code
# , team_region, team_confederation, wiki_link, f"Read More About {value}", team_flag, winning_times, winning_years, matches_count
