import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from dash import callback

# Sample data
data = {
    'Batsman': ['A', 'B', 'C', 'D', 'E'],
    'Bowler': ['X', 'Y', 'Z', 'X', 'Y'],
    'Runs_Scored': [50, 30, 40, 60, 70],
    'Balls_Faced': [30, 40, 50, 60, 70],
    'Player_Out': ['No', 'Yes', 'No', 'Yes', 'No'],
    'ID': [1, 2, 3, 4, 5]
}
df = pd.read_csv('data/batsman_vs_bowler.csv')



# Create the layout of the app
Batsmanvsbowler = html.Div([
    html.H1("Cricket Performance Analysis", className="title-text"),
        html.P("Select Batsman",className="title-text"),
    html.Div([
        dcc.Dropdown(
            id='batsman-dropdown',
            # className= "comparison-dropdown",
            options=[{'label': i, 'value': i} for i in df['Batsman'].unique()],
            value=df['Batsman'].unique()[0],
            placeholder="Select a batsman"
        )
    ],
    className="comparison-dropdown"),
        html.P("Select Bowler",className="title-text"),
    html.Div([
        dcc.Dropdown(
            id='bowler-dropdown',
            options=[{'label': i, 'value': i} for i in df['Bowler'].unique()],
            value=df['Bowler'].unique()[0],
            placeholder="Select a bowler"
        )
    ],className="comparison-dropdown"),
    html.Div(id='table-container'),
    dcc.Graph(id='line-graph',className="graph-bg"),
    # dcc.Graph(id='scatter-id-vs-runs'),
    dcc.Graph(id='scatter-id-vs-strike-rate',className="graph-bg"),
    # dcc.Graph(id='scatter-id-vs-avg'),
    # dcc.Graph(id='correlated-scatter-plot'),
    # dcc.Graph(id='batsman-comparison-graph')
])

# Define callback to update the graph and table based on dropdown selections
@callback(
    [Output('line-graph', 'figure'),
     Output('table-container', 'children')],
    [Input('batsman-dropdown', 'value'),
     Input('bowler-dropdown', 'value')]
)
def update_graph(selected_batsman, selected_bowler):
    filtered_df = df[(df['Batsman'] == selected_batsman) & (df['Bowler'] == selected_bowler)]
    # fig = px.line(filtered_df, x='ID', y='Runs_Scored', title=f"{selected_batsman} vs. {selected_bowler}")
    fig = px.scatter(filtered_df, x='ID', y='Runs_Scored', size='Runs_Scored', title=f"{selected_batsman} vs. {selected_bowler}",
                 labels={'ID': 'Season', 'Runs_Scored': 'Runs Scored'}, size_max=30)
    fig.update_layout(xaxis=dict(gridcolor='#74b2d6'),yaxis=dict(gridcolor='#74b2d6')) 
    fig.update_layout(plot_bgcolor='rgb(0,0,0,0.3)', paper_bgcolor='rgb(7, 14, 57, 0.8)',font_color='white')
   # Calculate overall runs, balls faced, and strike rate
    overall_runs = filtered_df['Runs_Scored'].sum()
    overall_balls_faced = filtered_df['Balls_Faced'].sum()
    if overall_balls_faced==0:
        overall_balls_faced=1
    overall_strike_rate = (overall_runs / overall_balls_faced) * 100
    # else: 
    #     overall_strike_rate=0

    # Calculate total time faced (assuming 1 ball takes 1 minute)
    total_time_faced = len(filtered_df)
    num_times_out = len(filtered_df[filtered_df['Player_Out'] == selected_batsman])
    if num_times_out==0:
        num_times_out=1
    avg =  overall_runs/num_times_out

    # Create table data
    table_data = pd.DataFrame({
        'Batsman': [selected_batsman],
        'Bowler': [selected_bowler],
        'Overall_Runs': [overall_runs],
        'Overall_Balls_Faced': [overall_balls_faced],
        'Overall_Strike_Rate': [overall_strike_rate],
        'Total_Time_Faced': [total_time_faced],
        'Times_Out': [num_times_out],
        'batsman_avg': [avg]
    })

    # table = html.Table([
    #     html.Thead(html.Tr([html.Th(col) for col in table_data.columns])),
    #     html.Tbody([html.Tr([html.Td(table_data.iloc[i][col]) for col in table_data.columns]) for i in range(len(table_data))])
    # ])
    # Define CSS styles
    table_style = {
    'backgroundColor': 'rgb(7, 14, 57, 0.8)',
    'color': 'white',
    'textAlign': 'center',  # Align text in the center
    'border': '1px solid black',  # Add border to cells
    'borderCollapse': 'collapse',  # Collapse borders
    'padding': '10px',  # Add padding to cells
    }
    header_style = {
    **table_style,
    'borderBottom': '2px solid black',  # Add border at the bottom of header cells
    }

# Create the table using Dash HTML components
    table = html.Table(
    # Table header
        [
            html.Tr([html.Th(col, style=header_style) for col in table_data.columns], style=table_style)
        ]
        +
        # Table body rows
        [
            html.Tr(
                [
                    html.Td(table_data.iloc[i][col], style=table_style)  # Apply style to each cell
                    for col in table_data.columns
                ]
            )
            for i in range(len(table_data))
        ],
        style=table_style,
        className="table-styling"  # Apply style to the entire table
    )

    return fig, table

# # Callback for scatter plot: ID vs Runs_Scored
# @app.callback(
#     Output('scatter-id-vs-runs', 'figure'),
#     [Input('batsman-dropdown', 'value'),
#      Input('bowler-dropdown', 'value')]
# )
# def update_scatter_id_vs_runs(selected_batsman, selected_bowler):
#     filtered_df = df[(df['Batsman'] == selected_batsman) & (df['Bowler'] == selected_bowler)]
#     fig = px.scatter(filtered_df, x='ID', y='Runs_Scored', title='ID vs Runs_Scored')
#     return fig

# Callback for scatter plot: ID vs Strike_Rate
@callback(
    Output('scatter-id-vs-strike-rate', 'figure'),
    [Input('batsman-dropdown', 'value'),
     Input('bowler-dropdown', 'value')]
)
def update_scatter_id_vs_strike_rate(selected_batsman, selected_bowler):
    filtered_df = df[(df['Batsman'] == selected_batsman) & (df['Bowler'] == selected_bowler)]
    filtered_df['Strike_Rate'] = (filtered_df['Runs_Scored'] / filtered_df['Balls_Faced']) * 100
    fig = px.line(filtered_df, x='ID', y='Strike_Rate', title='ID vs Strike_Rate', labels={'ID': 'Season', 'Strike_Rate': 'Strike Rate'})
    fig.update_traces(line=dict(color='#74b2d6'))
    fig.update_traces(line=dict(width=3))

# Update grid color
    fig.update_layout(yaxis=dict(gridcolor='#74b2d6'))  
    fig.update_layout(plot_bgcolor='rgb(0,0,0,0.3)', paper_bgcolor='rgb(7, 14, 57, 0.8)',font_color='white')
    
    return fig
# Callback for correlated scatter plot



# Run the app
