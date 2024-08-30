import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash import callback
from dash.exceptions import PreventUpdate
import pandas as pd
import csv

df = pd.read_csv('data/team_players_mapping_2.csv')

def read_csv_file(file_path):
    data = []
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            data.append(row)
    return data

batting_file_path = 'data/all_season_batting_card_1.csv'
bowling_file_path = 'data/all_season_bowling_card_1.csv'
batting = read_csv_file(batting_file_path)
bowling = read_csv_file(bowling_file_path)

team_path='data/team_players_mapping_2.csv'
teamdata=read_csv_file(team_path)


def bowl(player_name):
    run=0
    wic=0
    ball=0
    overs=0
    for row in bowling:
        if row[11]==player_name:
            overs = int(float(row[12])) if row[12].replace('.', '', 1).isdigit() else 0
            wickets = int(row[15]) if row[15].isdigit() else 0
            runs=int(row[14]) if row[14].isdigit() else 0
            ball+=overs*6
            wic+=wickets
            run+=runs
    eco=0
    str=0
    avg=0
    if overs!=0:
        eco=run*6/ball
    if wic!=0:
        str=(ball/wic)
        avg=run/wic
    return [wic,round(str,2),round(avg,2),round(eco,2)]

def bat(player_name):
    bou=0
    run=0
    ball=0
    out=0
    for row in batting:
        if row[11]==player_name:
            four = int(row[15]) if row[15].isdigit() else 0
            six = int(row[16]) if row[16].isdigit() else 0
            bou+=four+six
            ballsfaced = int(row[13]) if row[13].isdigit() else 0
            ball+=ballsfaced
            runs = int(row[12]) if row[12].isdigit() else 0
            run+=runs
            x=row[19]
            if x=='FALSE':
                out+=1
    str=0
    avg=0
    if ball!=0:
        str=run*100/ball
    if out!=0:
        avg=run/out
    return [run,bou,round(str,2),round(avg,2)]

def allrounder(player_name):
    x=bat(player_name)
    y=bowl(player_name)
    return [x[0],round(x[2],2),y[0],round(y[3],2)]

def play(player):
    li=[]
    x= df[df['Player Name']==player]['Role'].tolist()
    # for row in teamdata:
    #     if row[1]==player:
    #         x=row[2]
    if x[0]=='Bowler':
        li=bowl(player)
    elif x[0]=='All Rounder':
        li=allrounder(player)
    else:
        li=bat(player)
    return li


def player_average_points(player_name):
    player = {}
    
    # Calculate batting points
    for row in batting:
        if row[0] == '2023' and row[11] == player_name:
            x = 0
            runs = int(row[12]) if row[12].isdigit() else 0
            match_id = int(row[1])
            ballsfaced = int(row[13]) if row[13].isdigit() else 0
            four = int(row[15]) if row[15].isdigit() else 0
            six = int(row[16]) if row[16].isdigit() else 0
            strikeRate = float(row[17]) if row[17].replace('.', '', 1).isdigit() else 0.0
            
            x += runs
            if runs == 0:
                x -= 2
            x += four
            x += 2 * six
            if 30 <= runs < 50:
                x += 4
            elif 50 <= runs < 100:
                x += 8
            elif runs >= 100:
                x += 16
            
            if ballsfaced >= 10:
                if strikeRate > 170:
                    x += 6
                elif 150 < strikeRate <= 170:
                    x += 4
                elif 130 < strikeRate <= 150:
                    x += 2
                elif 50 < strikeRate <= 60:
                    x -= 2
                elif 40 < strikeRate <= 50:
                    x -= 4
                elif strikeRate <= 40:
                    x -= 6
            
            player[match_id] = x
    
    # Calculate bowling points
    for row in bowling:
        if row[0] == '2023' and row[11] == player_name:
            x = 0
            wickets = int(row[15]) if row[15].isdigit() else 0
            match_id = int(row[1])
            maiden = int(row[13]) if row[13].isdigit() else 0
            economy = float(row[16]) if row[16].replace('.', '', 1).isdigit() else 0.0
            overs = float(row[12]) if row[12].replace('.', '', 1).isdigit() else 0.0
            
            x += 25 * wickets
            x += 12 * maiden
            
            if wickets >= 5:
                x += 16
            elif wickets == 4:
                x += 8
            elif wickets == 3:
                x += 4
            
            if overs >= 2:
                if economy < 5:
                    x += 6
                elif 5 <= economy < 6:
                    x += 4
                elif 6 <= economy <= 7:
                    x += 2
                elif 10 <= economy <= 11:
                    x -= 2
                elif economy > 11 and economy <= 12:
                    x -= 4
                elif economy > 12:
                    x -= 6
            
            if match_id in player:
                player[match_id] += x
            else:
                player[match_id] = x
    
    if player:
        average_points = sum(player.values()) / len(player)
    else:
        average_points = 0
    
    return round(average_points, 1)

# # Example usage
# player_name = 'Virat Kohli'
# average_points = player_average_points(player_name)
# print("Average points for {}: {:.2f}".format(player_name, average_points))

df = pd.read_csv('data/team_players_mapping_2.csv')

def create_table(data_frame, tab_id):
    table = html.Table([
            html.Thead(
                html.Tr([ html.Th('Player name'), html.Th('Points')]) # html.Th('Select'),
            ),
            html.Tbody([
                html.Tr([
                    # html.Td(dcc.Checklist(
                    #     id={'type': 'player-checkbox', 'index': i, 'tab': tab_id},
                    #     options=[{'label': '', 'value': 'selected'}],
                    #     value=[]
                    # )),
                    html.Td(row['Player']), 
                    html.Td(row['Points'])
                ])
                for i, row in data_frame.iterrows()
            ])
        ])
    return table

def create_batsman_tile(player):
    path = 'assets/Team Images/'+player+'.webp'
    l = play(player)
    tile = html.Div(
        children=[
            html.Img(src=path,alt=player,height=150,width=150),
            html.Div(id = 'player_states', children = [
                html.H4('Runs',style={'color': 'white'}),
                html.Div(id='runs', children=str(l[0]),style={'color': 'white'}),
                html.H4('Boundary',style={'color': 'white'}),
                html.Div(id='boundary', children=str(l[1]),style={'color': 'white'}),
                html.H4('Strike Rate',style={'color': 'white'}),
                html.Div(id='strike_rate', children=str(l[2]),style={'color': 'white'}),
                html.H4('Average',style={'color': 'white'}),
                html.Div(id='average', children=str(l[3]),style={'color': 'white'})
            ])
        ]
    )

    return tile

def create_bowler_tile(player):
    l = play(player)
    path = 'assets/Team Images/'+player+'.webp'
    tile = html.Div(
        children=[
            html.Img(src=path,alt=player,height=150,width=150),
            html.Div(id = 'player_states', children = [
                html.H4('Wickets',style={'color': 'white'}),
                html.Div(id='wickets', children=str(l[0]),style={'color': 'white'}),
                html.H4('Strike Rate',style={'color': 'white'}),
                html.Div(id='strike_rate', children=str(l[1]),style={'color': 'white'}),
                html.H4('Average',style={'color': 'white'}),
                html.Div(id='average', children=str(l[2]),style={'color': 'white'}),
                html.H4('Economy',style={'color': 'white'}),
                html.Div(id='economy', children=str(l[3]),style={'color': 'white'})
            ])
        ]
    )
    return tile

def create_allRounder(player):
    path = 'assets/Team Images/'+player+'.webp'
    l = play(player)
    tile = html.Div(
        children=[
            html.Div([html.Img(src=path, alt=player, height=150, width=150)]),
            html.Div(id = 'player_states',style={'color': 'white'}, children = [
                html.H4('Runs',style={'color': 'white'}),
                html.Div(id='runs',style={'color': 'white'}, children=str(l[0])),
                html.H4('Strike Rate',style={'color': 'white'}),
                html.Div(id='strike_rate',style={'color': 'white'}, children=str(l[1])),
                html.H4('Wickets',style={'color': 'white'}),
                html.Div(id='wickets', style={'color': 'white'},children=str(l[2])),
                html.H4('Economy',style={'color': 'white'}),
                html.Div(id='economy',style={'color': 'white'}, children=str(l[3]))
            ])
        ]
    )
    
    return tile

def create_df(players_df, role):
    return players_df[players_df['Role']==role].sort_values(by='Points', ascending=False)








selected_players = []
top_11_players = []
# Define the layout
final_output = html.Div(style={'display': 'flex', 'justify-content': 'space-between'},children=[
    html.Div(style={'width': '40%'}, children=[
        html.Div(style={'display': 'flex', 'flex-direction': 'column'},children=[
            dcc.Dropdown(
                id='team_dropdown1',
                options=[{'label': team, 'value': team} for team in df['Team Name'].unique()],
                value='CSK'
            ),
            dcc.Dropdown(
                id='team_dropdown2',
                options=[{'label': team, 'value': team} for team in df['Team Name'].unique()],
                value='MI'
            )
        ]),
        html.Div(children=[
            dcc.Dropdown(
                id='players_team_a', multi=True
            ),
            # html.Div(id='output-div1'),  # Placeholder div for displaying selected options
            dcc.Dropdown(
                id='players_team_b', multi=True
            ),
            # html.Div(id='output-div2'),  # Placeholder div for displaying selected options
            dcc.Tabs(id='tabs', value='batsman', children=[
                dcc.Tab(label='Batsman',style={'color': 'black', 'fontWeight': 'bold'},value='batsman', children=[
                    html.Div(id='batsman-table')
                ]),
                dcc.Tab(label='Bowler', value='bowler',style={'color': 'black', 'fontWeight': 'bold'},children=[
                    html.Div(id='bowler-table')
                ]),
                dcc.Tab(label='Wicket Keeper', value='wicket_keeper',style={'color': 'black', 'fontWeight': 'bold'},children=[
                    html.Div(id='wic_keep_table')
                ]),
                dcc.Tab(label='All Rounder', value='all_rounder',style={'color': 'black', 'fontWeight': 'bold'},children=[
                    html.Div(id='all_rounder_table')
                ])
            ]),
            html.Div(id='selected-players-output')
        ]),
        # html+++.Div(id='selected_players', style={'display': 'none'})
        
    ]),
    html.Div(style={'width': '40%'}, children=[
        html.Div(style={'margin-bottom': '10px'}, children=[
            html.Button(" Top 11 Players", id="add-item-btn",style={'margin-left': '10px','border-radius': '5px'},)
        ]),
        html.Div(id="stacked-items",style={'color': 'white','margin-left':'10px'})
    ]),
    # html.Div(style={'width': '40%', 'display':'grid'}, children=[
    #     html.Div([html.Div(style={'display':'grid'},id = 'pl1'), html.Div(style={'display':'grid'},id = 'pl2')]),
    #     html.Div([html.Div(style={'display':'grid'},id = 'pl3'), html.Div(style={'display':'grid'},id = 'pl4'), html.Div(style={'display':'grid'},id = 'pl5')]),
    #     html.Div([html.Div(style={'display':'grid'},id = 'pl6'), html.Div(style={'display':'grid'},id = 'pl7'), html.Div(style={'display':'grid'},id = 'pl8')]),
    #     html.Div([html.Div(style={'display':'grid'},id = 'pl9'), html.Div(style={'display':'grid'},id = 'pl10'), html.Div(style={'display':'grid'},id = 'pl11')]),
    # ])
   html.Div(style={'width': '100%', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start'}, children=[
    html.Button("Show Player", id="add-item-btn2",style={'margin-left': '10px','border-radius': '5px'}),
    html.Div(style={'width': '40%', 'display': 'inline-grid'}, children=[
        html.Div(style={'display': 'grid', 'grid-template-columns': '1fr 1fr 1fr'}, children=[
            html.Div(style={'display': 'grid','margin':'10px'}, id='pl1'),
            html.Div(style={'display': 'grid','margin':'10px'}, id='pl2'),
            html.Div(style={'display': 'grid','margin':'10px'}, id='pl3')
        ]),
        html.Div(style={'display': 'grid', 'grid-template-columns': '1fr 1fr 1fr'}, children=[
            html.Div(style={'display': 'grid','margin':'10px'}, id='pl4'),
            html.Div(style={'display': 'grid','margin':'10px'}, id='pl5'),
            html.Div(style={'display': 'grid','margin':'10px'}, id='pl6')
        ]),
        html.Div(style={'display': 'grid', 'grid-template-columns': '1fr 1fr 1fr'}, children=[
            html.Div(style={'display': 'grid','margin':'10px'}, id='pl7'),
            html.Div(style={'display': 'grid','margin':'10px'}, id='pl8'),
            html.Div(style={'display': 'grid','margin':'10px'}, id='pl9')
        ]),
        html.Div(style={'display': 'grid', 'grid-template-columns': '1fr 1fr 1fr'}, children=[
            html.Div(style={'display': 'grid','margin':'10px'}, id='pl10'),
            html.Div(style={'display': 'grid','margin':'10px'}, id='pl11')
        ])
    ])

])

    # html.Div(style={'width': '40%', 'display':'grid'}, children=[
    # html.Div([html.Div(style={'display':'grid'},id = f'pl{i+1}') for i in range(4)]),
# ])

])



@callback(
    [Output('players_team_a', 'options'),
     Output('players_team_b', 'options')],
    [Input('team_dropdown1', 'value'),
     Input('team_dropdown2', 'value'),
     Input('players_team_a', 'value'),
     Input('players_team_b', 'value')]
)
def update_team(team_a, team_b, selected_players_a, selected_players_b):
    selected_players_a = selected_players_a or []
    selected_players_b = selected_players_b or []
    team_df_a = df[df['Team Name'] == team_a]
    team_df_b = df[df['Team Name'] == team_b]
    global selected_players
    selected_players = selected_players_a + selected_players_b
    players_1 = [{'label': player, 'value': player, 'disabled': player not in selected_players_a and len(selected_players_a)>=11} for player in team_df_a['Player Name']]
    players_2 = [{'label': player, 'value': player, 'disabled': player not in selected_players_b and len(selected_players_b)>=11} for player in team_df_b['Player Name']]
    return players_1, players_2


@callback(
    Output('batsman-table', 'children'),
    Output('bowler-table', 'children'),
    Output('wic_keep_table', 'children'),
    Output('all_rounder_table', 'children'),
    Input('players_team_a', 'value'),
    Input('players_team_b', 'value')
)
def generate_table_content(team_a, team_b):
    global selected_players
    selected_players = team_a or []
    selected_players.extend(team_b or [])
    role = [df[df['Player Name']==player]['Role'].values[0] for player in selected_players]
    points = [player_average_points(player) for player in selected_players]
    players_df = pd.DataFrame({'Player':selected_players, 'Role':role, 'Points':points})
    batsman = create_df(players_df, 'Batsman')
    bowler = create_df(players_df,'Bowler')
    wic_keep = create_df(players_df,'Wicket Keeper')
    all_round = create_df(players_df,'All Rounder')
    bat = create_table(batsman, 'batsman')
    bowl = create_table(bowler, 'bowler')
    wk = create_table(wic_keep, 'wicket_keeper')
    ar = create_table(all_round, 'all_rounder')
    return bat, bowl, wk, ar

@callback(
    Output("stacked-items", "children"),
    Input("add-item-btn", "n_clicks")
)
def add_item(n_clicks):
    if n_clicks:
        global selected_players
        points = [player_average_points(player) for player in selected_players]
        sl_df = pd.DataFrame({'Players':selected_players, 'Points':points}).sort_values(by='Points', ascending=False).head(11)
        players =sl_df['Players'].tolist()
        global top_11_players 
        top_11_players = players
        if len(selected_players) >= 4:
            items = [html.Div(item) for item in players]
            selected_players.clear()  # Clear the global list after printing
            return items
    return []

@callback(
    Output("pl1", "children"),
    Output("pl2", "children"),
    Output("pl3", "children"),
    Output("pl4", "children"),
    Output("pl5", "children"),
    Output("pl6", "children"),
    Output("pl7", "children"),
    Output("pl8", "children"),
    Output("pl9", "children"),
    Output("pl10", "children"),
    Output("pl11", "children"),
    Input("add-item-btn2", "n_clicks")
)
# def update_11_team(n_clicks):
#     global top_11_players
#     tiles = []
#     for player in top_11_players:
#         if player in ['Wicket Keeper', 'Batsman']:
#             tile = create_batsman_tile(player)
#         elif player =='Bowler':
#             tile = create_bowler_tile(player)
#         else:
#             tile = create_allRounder(player)
#         tiles.append(tile)
#         # p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11
#     return tiles

def update_11_team(n_clicks):
    global top_11_players
    if n_clicks is None:
        raise PreventUpdate
    tiles = []
    for player in top_11_players:
        x= df[df['Player Name']==player]['Role'].tolist()
        if x[0] == 'All Rounder':
            tile = create_allRounder(player)
        elif x[0] =='Bowler':
            tile = create_bowler_tile(player)
        else:
            tile = create_batsman_tile(player)
        tiles.append(tile)
    return tiles
    

