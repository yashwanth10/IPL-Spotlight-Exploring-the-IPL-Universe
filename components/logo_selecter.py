import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash import callback
import pandas as pd




trophy_icon = '🏆'
sad_emoji = '😢'
# logo = html.Div([
#     html.Div(id='logo-container')
# ])

# team_players = {
#     'Chennai Super King': ['Player 1', 'Player 2', 'Player 3'],
#     'Delhi Capitals': ['Player 4', 'Player 5', 'Player 6'],
#     'Team C': ['Player 7', 'Player 8', 'Player 9']
# }

logo=html.Div(className="chart-container main_dropdown", children=[html.Div(className="card-chart", children=[
        html.Div(className="card-chart",style={'padding-top': '25px'}, children=[
            html.Div(className="card-chart-container", style={'margin-left': '0px','size':'500px','height': '370px'},children=[
                html.Div(className="card-m-3 me-3 pb-3",
                        children=[
                            
                            html.Div(id='logo-container', className="img-logo")
                            
                        ]),

            ])

        ])
    ])]
    )

Players_name=html.Div(className="chart-container main_dropdown", children=[html.Div(className="card-chart", children=[
        html.Div(className="card-chart",style={'padding-top': '25px'}, children=[
            html.Div(className="card-chart-container", style={'margin-left': '5px','size':'500px','max-height': '370px','overflow-y': 'auto'},children=[
                html.Div(className="card-m-3 me-3 pb-3",
                        children=[
                            
                            html.Div(id='players')
                            
                        ]),

            ])

        ])
    ])]
    )

Season_Won=html.Div(className="chart-container main_dropdown", children=[html.Div(className="card-chart", children=[
        html.Div(className="card-chart",style={'padding-top': '25px'}, children=[
            html.Div(className="card-chart-container", style={'margin-left': '5px','size':'500px','height': '370px','overflow-y': 'auto'},children=[
                html.Div(className="card-m-3 me-3 pb-3",
                        children=[
                            html.H4(
                        id='my-head11',
                        children="Season Won",
                        className="card-chart-container",
                        style={"font-size": "1.5vw", "text-align": "center", 'padding-top': '25px', 'color': 'white'}
                    ),
                            html.Div(id='seasonwon')
                            
                        ]),

            ])

        ])
    ])]
    )

@callback(
    Output('logo-container', 'children'),
    [Input('query-ipl_team-select', 'value')]
)
def update_logo(selected_option):
    # print(selected_option)
    if selected_option == 'Chennai Super King':
        # print("hi")
        return html.Img(src='/assets/images/csk.png', style={'width': '10','height':'10'})
    elif selected_option == 'Mumbai Indians':
        # print("hi")
        return html.Img(src='/assets/images/mi.png')
    elif selected_option == 'Royal Challengers Bangaluru':
        return html.Img(src='/assets/images/rcb.png')
    elif selected_option == 'Delhi Capitals':
        return html.Img(src='/assets/images/dc.png')
    elif selected_option == 'Sunrisers Hyderabad':
        return html.Img(src='/assets/images/srh.png')
    elif selected_option == 'Rajasthan Royals':
        return html.Img(src='/assets/images/rr.png')
    elif selected_option == 'Kolkata Knight Riders':
        return html.Img(src='/assets/images/kkr.png')
    elif selected_option == 'Kings XI Punjab':
        return html.Img(src='/assets/images/pk.png')
    elif selected_option == 'Lucknow Super Giants':
        return html.Img(src='/assets/images/lsg.png')
    elif selected_option == 'Gujarat Titans':
        return html.Img(src='/assets/images/gt.png')
    else:
        return html.Img(src='/assets/images/kkr.png')
    

@callback(
    Output('players', 'children'),
    [Input('query-ipl_team-select', 'value')]
)
def update_players(selected_option):
    if selected_option=='Kings XI Punjab':
        selected_option='PBKS'
    df_players_data = pd.read_csv("data/team_players_mapping.csv")
    team_players = df_players_data[df_players_data['Team Name'] == selected_option]['Player Name'].tolist()
    
    player_list = html.Ul([html.Li(player) for player in team_players])
    return player_list



@callback(
    Output('seasonwon', 'children'),
    [Input('query-ipl_team-select', 'value')]
)
def update_seasonwon(team_name):
    df_season_data = pd.read_csv("data/season wise winning teams_1.csv")
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
        team_name='KXIV'
    elif team_name=='Lucknow Super Giants':
        team_name='LSG'
    elif team_name=='Gujarat Titans':
        team_name='GT'
    else:
        team_name='SRH'
    seasons = df_season_data[df_season_data['Team'] == team_name]['Year'].tolist()
    
    if seasons:
        season_list = []
        for season in seasons:
            season_list.append(html.Div([
                html.Span(season),
                html.Span(trophy_icon, style={'margin-left': '5px'})
            ]))
        return season_list
    else:
        return html.Div([
            html.Span("No seasons won by "),
            html.Span(team_name, style={'font-weight': 'bold'}),
            html.Span(sad_emoji, style={'margin-left': '5px'})
        ])
    # players = team_players[selected_option]
    # player_list = html.Ul([html.Li(player) for player in players])
    # return player_list