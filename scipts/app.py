# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import datetime as dt
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
            "TED Talks",
            style=dict(color="red", textShadow="rgb(127, 2, 2) 2px 2px 2px"),
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    # Top talks
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
                                                                min=1,
                                                                style=dict(
                                                                    width="65px",
                                                                    margin="0 5px",
                                                                ),
                                                            ),
                                                            html.Label(" talks"),
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
                                width=7,
                            ),
                            dbc.Col(
                                [
                                    # Top speakers
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
                                                                min=1,
                                                                style=dict(
                                                                    width="65px",
                                                                    margin="0 5px",
                                                                ),
                                                            ),
                                                            html.Label(" speakers"),
                                                        ]
                                                    ),
                                                    html.Br(),
                                                    html.Label(
                                                        "Bubble size indicates video counts",
                                                        style=dict(
                                                            margin="0 0 0 150px"
                                                        ),
                                                    ),
                                                    dcc.Graph(
                                                        id="speakers-content",
                                                        style=dict(
                                                            margin="-50px 0 0 0"
                                                        ),
                                                    ),
                                                ]
                                            )
                                        ]
                                    )
                                ],
                                width=5,
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
                                                            margin="-29px 0px 0px 100px",
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
                            ),
                        ]
                    ),
                    html.Br(),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    # talks by speaker
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
                                                                min=1,
                                                                style=dict(
                                                                    width="65px",
                                                                    margin="0 5px",
                                                                ),
                                                            ),
                                                            html.Label(" talks by "),
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
                                                            width="400px",
                                                            margin="-32px 0px 0px 160px",
                                                        ),
                                                    ),
                                                    html.Div(
                                                        id="talks-per-speaker-content"
                                                    ),
                                                ]
                                            )
                                        ]
                                    )
                                ],
                                width=12,
                            ),
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
    Output("talks-number", "value"),
    Input("talks-number", "value"),
    Input("talks-year", "value"),
)
def update_talks_content(num, year):
    if num is None:
        num = 8

    selected_date_df = df[
        (df["date"].dt.year >= year[0]) & (df["date"].dt.year <= year[1])
    ]
    selected_date_df = selected_date_df.sort_values("views")[-num:]
    selected_date_df["date"] = selected_date_df["date"].dt.strftime("%b, %Y")

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

    return fig, min(num, selected_date_df.shape[0])


# Function to render speakers content
@app.callback(
    Output("speakers-content", "figure"),
    Output("speakers-number", "value"),
    Input("speakers-number", "value"),
)
def update_speakers_content(num):
    if num is None:
        num = 10

    top_speakers_by_count = df.groupby("author").agg("count").reset_index()
    top_speakers_by_count = top_speakers_by_count[["author", "title"]].rename(
        columns={"title": "video_count"}
    )
    df_with_count = df.sort_values("views")[-num:].merge(
        top_speakers_by_count, on="author"
    )

    fig = px.scatter(
        df_with_count,
        x="views",
        y="author",
        color="likes",
        size="video_count",
        size_max=30,
        color_continuous_scale=px.colors.sequential.Redor,
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0.1)",
        paper_bgcolor="rgba(0,0,0,0)",
        autosize=True,
        template="plotly_dark",
        legend={"itemsizing": "trace"},
    )
    fig.update_xaxes(showline=True)
    fig.update_yaxes(showline=True)

    return fig, min(num, df_with_count.shape[0])


# Function to render talks per speaker content
@app.callback(
    Output("talks-per-speaker-content", "children"),
    Output("talks-per-speaker-number", "value"),
    Input("talks-per-speaker-number", "value"),
    Input("talks-per-speaker-dropdown", "value"),
)
def update_talks_per_speaker_content(num, dropdown):
    if num is None:
        num = 5

    author_df = df[df["author"] == dropdown].sort_values("views", ascending=False)[:num]
    author_df["date"] = author_df["date"].dt.strftime("%b, %Y")
    author_df["views"] = author_df["views"].apply(
        lambda n: f"{n / 1e6}M" if n > 1e6 else f"{n / 1e3}K" if n > 1e3 else f"{n}"
    )
    author_df["likes"] = author_df["likes"].apply(
        lambda n: f"{n / 1e6}M" if n > 1e6 else f"{n / 1e3}K" if n > 1e3 else f"{n}"
    )

    return (
        dbc.Table(
            [
                html.Thead(
                    html.Tr(
                        [html.Th(col) for col in author_df.drop("link", axis=1).columns]
                    )
                )
            ]
            + [
                html.Tbody(
                    [
                        html.Tr(
                            [
                                html.Td(
                                    html.A(
                                        author_df.loc[index, "title"],
                                        href=author_df.loc[index, "link"],
                                    )
                                )
                            ]
                            + [
                                html.Td(cell)
                                for cell in author_df.drop(["title", "link"], axis=1)
                                .loc[index, :]
                                .values
                            ]
                        )
                        for index in author_df.index
                    ]
                )
            ]
        ),
        min(num, author_df.shape[0]),
    )


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

        fig.update_xaxes(title_text="month", row=1, col=1, tickvals=np.arange(1, 13))
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
            title_text="year",
            row=1,
            col=1,
            tickvals=np.arange(year[0], year[1] + 1),
            tickangle=-45,
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
        height=720,
    )
    fig.update_xaxes(showline=True)
    fig.update_yaxes(showline=True)

    return fig


# main call
if __name__ == "__main__":
    app.run_server(debug=True)
