import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, Input, Output, dcc, html
from dash import callback

df = pd.read_csv('data/Team_data.csv')

# Replace "PBKS" with "KXIP" in the data (if necessary)
df.loc[df['Team Name'] == "PBKS", 'Team Name'] = "KXIP"

# qualify = html.Div([
#     # dcc.Input(id='team-name-input', type='text', placeholder='Enter the team name'),
#     html.Div(id='team-stats')
# ])


    
qualify = html.Div(className="col-lg-4 col-md-3 col-sm-3 card-chart-container season_dropdown", children=[html.Div(className="card-chart", children=[
        html.Div(className="card-chart",style={'padding-top': '25px','width':'700px','height':'630px'}, children=[
            html.Div(className="card-chart-container", style={'margin-left': '52px'},children=[
                html.Div(className="card-m-2 me-4 pb-2  ",
                        children=[
                                                    dcc.RadioItems(
                                    id='radio-buttons',
                                    options=[
                                        {'label': 'Qualification Summary', 'value': 'pie1'},
                                        {'label': 'Finals Summary', 'value': 'pie2'},
                                        {'label': 'Finals vs Wins', 'value': 'pie3'}

                                    ],
                                    value='pie1',
                                    labelStyle={'display': 'block'}
                                ),
                                html.Div(id='pie-chart-container', style={'background-color': 'none'})
                        ]),

            ])

        ])
    ])]
    )
# qualify=html.Div([
#     dcc.RadioItems(
#         id='radio-buttons',
#         options=[
#             {'label': 'Qualify', 'value': 'pie1'},
#             {'label': 'Final', 'value': 'pie2'},
#             {'label': 'Win', 'value': 'pie3'}

#         ],
#         value='pie1',
#         labelStyle={'display': 'block'}
#     ),
#     html.Div(id='pie-chart-container')
# ], style={'width': '30%'})

@callback(
    Output('pie-chart-container', 'children'),
    [Input("query-ipl_team-select", "value"),
        Input('radio-buttons', 'value')]
)
def update_team_stats(team_name,selected_radio):
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
    if team_name:
        team_data = df.loc[df['Team Name'] == team_name]
        if not team_data.empty:
            qualifiers = team_data['Qualifiers'].values[0]
            finals = team_data['Finals'].values[0]
            total_seasons = team_data['Total Seasons'].values[0]
            winners = team_data['Winners'].values[0]
            not_finals = total_seasons - qualifiers

            labels1 = ['Qualifiers', 'Not Qualified']
            sizes1 = [qualifiers, not_finals]
            colors1 = ['#66b3ff', '#99ff99']

            labels2 = ['Not Make For Finals', 'Finals']
            sizes2 = [qualifiers - finals, finals]
            colors2 = ['#ffcc99', '#ff9999']

            labels3 = ['Runner UP', 'Wins']
            sizes3 = [finals - winners, winners]
            colors3 = ['#ffb3e6', '#66b3ff']

            # fig = make_subplots(rows=1, cols=3, specs=[[{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]])

            # fig.add_trace(go.Pie(labels=labels1, values=sizes1, marker_colors=colors1, hoverinfo='label+percent+value',
            #                      pull=[0.05, 0.05], textinfo='percent+label', name=f'{team_name} Qualification Summary'), 1,
            #                      1)

            # fig.add_trace(go.Pie(labels=labels2, values=sizes2, marker_colors=colors2, hoverinfo='label+percent+value',
            #                      pull=[0.05, 0.05], textinfo='percent+label', name=f'{team_name} Finals Summary'), 1,
            #                      2)

            # fig.add_trace(go.Pie(labels=labels3, values=sizes3, marker_colors=colors3, hoverinfo='label+percent+value',
            #                      pull=[0.05, 0.05], textinfo='percent+label', name=f'{team_name} Finals vs Wins'), 1, 3)

            # fig.update_layout(
            #     title_text=f"<b>Team Statistics: {team_name}</b>"
            # )
            if selected_radio == 'pie1':
                return dcc.Graph(
                    id='pie-chart',
                    figure={
                        'data': [go.Pie(labels=labels1, values=sizes1, marker_colors=colors1, hoverinfo='label+percent+value',
                                 pull=[0.05, 0.05], textinfo='percent+label', name=f'{team_name} Qualification Summary')],
                        'layout': go.Layout(title='Qualification Summary',paper_bgcolor='rgb(7, 14, 57, 0.8)')
                    }
                )
            elif selected_radio == 'pie2':
                return dcc.Graph(
                    id='pie-chart',
                    figure={
                        'data': [go.Pie(labels=labels2, values=sizes2, marker_colors=colors2, hoverinfo='label+percent+value',
                                 pull=[0.05, 0.05], textinfo='percent+label', name=f'{team_name} Finals Summary')],
                        'layout': go.Layout(title='Finals Summary',paper_bgcolor='rgb(7, 14, 57, 0.8)')
                    }
                )

            elif selected_radio == 'pie3':
                return dcc.Graph(
                    id='pie-chart',
                    figure={
                        'data': [go.Pie(labels=labels3, values=sizes3, marker_colors=colors3, hoverinfo='label+percent+value',
                                 pull=[0.05, 0.05], textinfo='percent+label', name=f'{team_name} Finals vs Wins')],
                        'layout': go.Layout(title='Finals vs Wins',paper_bgcolor='rgb(7, 14, 57, 0.8)')
                    }
                )

            # return dcc.Graph(figure=fig)
        else:
            return "No data available for the specified team."
    return None



