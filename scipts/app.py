# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import datetime as dt
from turtle import bgcolor
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dash import Dash, dcc, html, Input, Output
from plotly.subplots import make_subplots


app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# Read data
df = pd.read_csv("data/ted-talks.csv").dropna()
df["date"] = pd.to_datetime(df["date"])
df = df[df["date"] >= dt.datetime(2000, 1, 1)]
year_min = df["date"].dt.year.min()
year_max = df["date"].dt.year.max()


# HTML webpage layout
app.layout = html.Div(
    [
        html.H1(
            "TED talks",
            style=dict(color="red", textShadow="rgb(127, 2, 2) 2px 2px 2px"),
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    # Top TED talks
                                    dbc.Card(
                                        [
                                            dbc.CardBody(
                                                [
                                                    html.Div(
                                                        [
                                                            html.Label("Top "),
                                                            dcc.Input(
                                                                id="talks-number",
                                                                type="number",
                                                                value=10,
                                                                min=1,
                                                                max=df.shape[0],
                                                                style=dict(
                                                                    width="65px",
                                                                    margin="0 5px",
                                                                ),
                                                            ),
                                                            html.Label(" TED talks"),
                                                        ]
                                                    ),
                                                    dcc.Graph(id="talks-content"),
                                                    dcc.RangeSlider(
                                                        id="talks-year",
                                                        min=year_min,
                                                        max=year_max,
                                                        step=1,
                                                        marks={
                                                            i: {
                                                                "label": f"{i}",
                                                                "style": {
                                                                    "transform": "rotate(-45deg)",
                                                                    "color": "white",
                                                                },
                                                            }
                                                            for i in range(
                                                                year_min, year_max + 1
                                                            )
                                                        },
                                                        value=[year_min, year_max],
                                                    ),
                                                ]
                                            )
                                        ]
                                    )
                                ],
                                width=12,
                            )
                        ]
                    ),
                    html.Br(),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    # Top TED speakers
                                    dbc.Card(
                                        [
                                            dbc.CardBody(
                                                [
                                                    html.Div(
                                                        [
                                                            html.Label("Top "),
                                                            dcc.Input(
                                                                id="speakers-number",
                                                                type="number",
                                                                value=10,
                                                                min=1,
                                                                max=df.shape[0],
                                                                style=dict(
                                                                    width="65px",
                                                                    margin="0 5px",
                                                                ),
                                                            ),
                                                            html.Label(
                                                                " TED speakers by "
                                                            ),
                                                        ]
                                                    ),
                                                    html.Div(
                                                        [
                                                            dcc.Dropdown(
                                                                id="speakers-dropdown",
                                                                options=[
                                                                    "views",
                                                                    "video count",
                                                                ],
                                                                value="views",
                                                                clearable=False,
                                                                style=dict(
                                                                    color="black"
                                                                ),
                                                            )
                                                        ],
                                                        style=dict(
                                                            width="200px",
                                                            margin="-32px 0 0 225px",
                                                        ),
                                                    ),
                                                    dcc.Graph(id="speakers-content"),
                                                ]
                                            )
                                        ]
                                    )
                                ],
                                width=6,
                            ),
                            dbc.Col(
                                [
                                    # TED talks by speaker
                                    dbc.Card(
                                        [
                                            dbc.CardBody(
                                                [
                                                    html.Div(
                                                        [
                                                            html.Label("Top "),
                                                            dcc.Input(
                                                                id="talks-per-speaker-number",
                                                                type="number",
                                                                value=10,
                                                                min=1,
                                                                max=df.shape[0],
                                                                style=dict(
                                                                    width="65px",
                                                                    margin="0 5px",
                                                                ),
                                                            ),
                                                            html.Label(
                                                                " TED talks by "
                                                            ),
                                                        ]
                                                    ),
                                                    html.Div(
                                                        [
                                                            dcc.Dropdown(
                                                                id="talks-per-speaker-dropdown",
                                                                options=sorted(
                                                                    df["author"]
                                                                    .str.strip(" '")
                                                                    .unique()
                                                                ),
                                                                value=df.groupby(
                                                                    "author"
                                                                )
                                                                .agg("count")
                                                                .sort_values("views")[
                                                                    -1:
                                                                ]
                                                                .index[0],
                                                                clearable=False,
                                                                style=dict(
                                                                    color="black"
                                                                ),
                                                            )
                                                        ],
                                                        style=dict(
                                                            width="385px",
                                                            margin="-32px 0 0 195px",
                                                        ),
                                                    ),
                                                    dcc.Graph(
                                                        id="talks-per-speaker-content"
                                                    ),
                                                ]
                                            )
                                        ]
                                    )
                                ],
                                width=6,
                            ),
                        ]
                    ),
                    html.Br(),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    # Time Series Analysis
                                    dbc.Card(
                                        [
                                            dbc.CardBody(
                                                [
                                                    html.Div(
                                                        [html.Label("TED talks per ")]
                                                    ),
                                                    html.Div(
                                                        [
                                                            dcc.Dropdown(
                                                                id="time-series-dropdown",
                                                                options=[
                                                                    "month",
                                                                    "year",
                                                                ],
                                                                value="month",
                                                                clearable=False,
                                                                style=dict(
                                                                    color="black"
                                                                ),
                                                            )
                                                        ],
                                                        style=dict(
                                                            width="110px",
                                                            margin="-28px 0 0 100px",
                                                        ),
                                                    ),
                                                    dcc.Graph(id="time-series-content"),
                                                    dcc.RangeSlider(
                                                        id="time-series-year",
                                                        min=year_min,
                                                        max=year_max,
                                                        step=1,
                                                        marks={
                                                            i: {
                                                                "label": f"{i}",
                                                                "style": {
                                                                    "transform": "rotate(-45deg)",
                                                                    "color": "white",
                                                                },
                                                            }
                                                            for i in range(
                                                                year_min, year_max + 1
                                                            )
                                                        },
                                                        value=[year_min, year_max],
                                                    ),
                                                ]
                                            )
                                        ]
                                    )
                                ],
                                width=12,
                            )
                        ]
                    ),
                ]
            )
        ),
    ],
    style=dict(padding="30px 50px", color="white"),
)


# Function to render talks content
@app.callback(
    Output("talks-content", "figure"),
    Input("talks-number", "value"),
    Input("talks-year", "value"),
)
def update_talks_content(num, year):
    selected_date_df = df[
        (df["date"].dt.year >= year[0]) & (df["date"].dt.year <= year[1])
    ]
    selected_date_df = selected_date_df.sort_values("views")[-num:]
    selected_date_df["date"] = selected_date_df["date"].dt.date

    fig = px.bar(
        selected_date_df, x="views", y="title", hover_data=selected_date_df.columns
    )

    fig.update_traces(marker_color="indianred")

    fig.add_trace(
        go.Bar(
            y=selected_date_df["title"],
            x=selected_date_df["likes"],
            name="likes",
            orientation="h",
            marker_color="lightsalmon",
        )
    )

    fig.update_layout(
        barmode="stack",
        plot_bgcolor="rgba(0,0,0,0.1)",
        paper_bgcolor="rgba(0,0,0,0)",
        autosize=True,
        template="plotly_dark",
    )

    return fig


# Function to render speakers content
@app.callback(
    Output("speakers-content", "figure"),
    Input("speakers-dropdown", "value"),
    Input("speakers-number", "value"),
)
def update_speakers_content(dropdown, num):
    fig = go.Figure()

    if dropdown == "video count":
        top_speakers_by_count = (
            df.groupby("author").agg("count").sort_values("views")[-num:].reset_index()
        )
        top_speakers_by_count = top_speakers_by_count.rename(columns={"views": "count"})

        fig = px.bar(top_speakers_by_count, x="count", y="author")

    elif dropdown == "views":
        top_speakers_by_views = (
            df.groupby("author").sum().sort_values("views")[-num:].reset_index()
        )

        fig = px.bar(top_speakers_by_views, x="views", y="author")

    fig.update_traces(marker_color="indianred")
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0.1)",
        paper_bgcolor="rgba(0,0,0,0)",
        autosize=True,
        template="plotly_dark",
    )
    fig.update_xaxes(showline=True)
    fig.update_yaxes(showline=True)

    return fig


# Function to render talks per speaker content
@app.callback(
    Output("talks-per-speaker-content", "figure"),
    Input("talks-per-speaker-dropdown", "value"),
    Input("talks-per-speaker-number", "value"),
)
def update_speakers_content(dropdown, num):
    talks_per_speaker = df[df["author"] == dropdown].sort_values("views")[-num:]
    talks_per_speaker["date"] = talks_per_speaker["date"].dt.date

    fig = px.bar(
        talks_per_speaker, x="views", y="title", hover_data=talks_per_speaker.columns
    )

    fig.update_traces(marker_color="indianred")
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0.1)",
        paper_bgcolor="rgba(0,0,0,0)",
        autosize=True,
        template="plotly_dark",
    )
    fig.update_xaxes(showline=True)
    fig.update_yaxes(showline=True)

    return fig


# Function to render time series content
@app.callback(
    Output("time-series-content", "figure"),
    Input("time-series-dropdown", "value"),
    Input("time-series-year", "value"),
)
def update_time_series_content(dropdown, year):
    selected_date_df = df[
        (df["date"].dt.year >= year[0]) & (df["date"].dt.year <= year[1])
    ]
    selected_date_df = selected_date_df.sort_values("views")

    fig = go.Figure()

    if dropdown == "month":
        videos_per_month = (
            selected_date_df.groupby(selected_date_df["date"].dt.month)
            .agg("count")["views"]
            .reset_index()
        )
        videos_per_month = videos_per_month.rename(
            columns={"date": "month", "views": "count"}
        )

        views_per_upload_month = (
            selected_date_df.groupby(selected_date_df["date"].dt.month)["views"]
            .mean()
            .reset_index()
        )
        views_per_upload_month = views_per_upload_month.rename(
            columns={"date": "month"}
        )

        fig = make_subplots(
            rows=2,
            cols=1,
            subplot_titles=(
                "Total videos uploaded per month",
                "Average views per upload month",
            ),
        )

        fig.append_trace(
            go.Scatter(
                x=videos_per_month["month"],
                y=videos_per_month["count"],
                name="counts",
            ),
            row=1,
            col=1,
        )

        fig.update_xaxes(row=1, col=1, tickvals=np.arange(1, 13))
        fig.update_yaxes(title_text="count", row=1, col=1)

        fig.append_trace(
            go.Scatter(
                x=views_per_upload_month["month"],
                y=views_per_upload_month["views"],
                name="views",
            ),
            row=2,
            col=1,
        )

        fig.update_xaxes(title_text="month", row=2, col=1, tickvals=np.arange(1, 13))
        fig.update_yaxes(title_text="views", row=2, col=1)

    elif dropdown == "year":
        videos_per_year = (
            selected_date_df.groupby(selected_date_df["date"].dt.year)
            .agg("count")["views"]
            .reset_index()
        )
        videos_per_year = videos_per_year.rename(
            columns={"date": "year", "views": "count"}
        )

        views_per_upload_year = (
            selected_date_df.groupby(selected_date_df["date"].dt.year)["views"]
            .sum()
            .reset_index()
        )
        views_per_upload_year = views_per_upload_year.rename(columns={"date": "year"})

        fig = make_subplots(
            rows=2,
            cols=1,
            subplot_titles=(
                "Total videos uploaded per year",
                "Total views per upload year",
            ),
        )

        fig.append_trace(
            go.Scatter(
                x=videos_per_year["year"], y=videos_per_year["count"], name="counts"
            ),
            row=1,
            col=1,
        )

        fig.update_xaxes(
            row=1, col=1, tickvals=np.arange(year[0], year[1] + 1), tickangle=-45
        )
        fig.update_yaxes(title_text="count", row=1, col=1)

        fig.append_trace(
            go.Scatter(
                x=views_per_upload_year["year"],
                y=views_per_upload_year["views"],
                name="views",
            ),
            row=2,
            col=1,
        )

        fig.update_xaxes(
            title_text="year",
            row=2,
            col=1,
            tickvals=np.arange(year[0], year[1] + 1),
            tickangle=-45,
        )
        fig.update_yaxes(title_text="views", row=2, col=1)

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0.1)",
        paper_bgcolor="rgba(0,0,0,0)",
        autosize=True,
        template="plotly_dark",
    )
    fig.update_xaxes(showline=True)
    fig.update_yaxes(showline=True)

    return fig


# main call
if __name__ == "__main__":
    app.run_server(debug=True)
