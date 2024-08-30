import dash
from dash import html
from dash.dependencies import Input, Output
import pandas as pd

# Sample data for logos
image_paths = [
    "./assets/images/csk.png",
    "./assets/images/rcb.png",
    "./assets/images/mi.png",
    "./assets/images/kkr.png",
    "./assets/images/gt.png",
    "./assets/images/lsg.png",
    "./assets/images/pk.png",
    "./assets/images/dc.png",
    "./assets/images/srh.png",
    "./assets/images/rr.png",
]

# Read data from CSV file
df = pd.read_csv("./data/Logo-hover.csv")

# Create logos_data with logo_url and team_code
logos_data = [
    {"logo_url": path, "team_code": code}
    for path, code in zip(image_paths, df["Teams"])
]


home_logo = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=image_data["logo_url"],
                            alt=f"Image {idx + 1}",
                            height=150,
                            width=150,
                        ),
                        html.Div(
                            [
                                html.Div(f"Team: {team['Teams']}", className="data-row"),
                                html.Div(f"Seasons Won: {team['Season Won']}", className="data-row"),
                                html.Div(f"Brand Value: {team['Brand Value']}", className="data-row"),
                                html.Div(f"Fan Base: {team['Fan Base']}", className="data-row"),
                            ],
                            className="data-tooltip",
                        ),
                    ],
                    className="image-container",
                    **{"data-team-code": image_data["team_code"]},
                )
                for idx, (image_data, team) in enumerate(zip(logos_data, df.to_dict(orient="records")))
            ],
            className="home_img",
        )
    ]
)
