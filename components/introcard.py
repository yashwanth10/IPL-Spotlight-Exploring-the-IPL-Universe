from dash import html
import dash_bootstrap_components as dbc

IPLIntroCard = html.Div(className=" card-chart-container", children=[

    html.Div(className="home_bio", children=[
        dbc.Row([
            dbc.Col(className="col-lg-6", children=[html.Div(className="card-m-0 me-2 pb-3", children=[
                html.H1(["IPL Spotlite: Exploring the IPL Universe"], 
                    className="card-title m-0 ms-2 me-2 mt-4 mb-2", style={"font-size": "3.2vw",
                                                                            "align-text": "center"}),
                # html.Span(
                #     "From Data Science Point-of-View", style={"color": "#0084d6", "font-size": "1.5vw"})
            ]),
                html.P(["This dashboard presents all you need to know about Indian Premiere League tournaments. You can also check each team's statistics and compare teams with each other in the ",
                        html.A(" Teams", href="/teams",style={"color": "#0084d6"}), " tab.", 
                        ],className="card-title m-0 ms-3 me-2 mt-4 mb-2", style={"fontSize": "18px", "fontFamily": "EB Garamond"}),

                

            ]),

            dbc.Col(className="col-lg-6", children=[html.Img(
                src="./assets/images/Ipl-auction_1703034762917_1703034773943.avif", className="img-fluid")], style={"align-self": "self-end"})
        ]),

    ])
])