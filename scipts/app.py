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


app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

# Read data
df = pd.read_csv('data/ted-talks.csv').dropna()
df['date'] = pd.to_datetime(df['date'])
df = df[df['date'] >= dt.datetime(2000, 1, 1)]
year_min = df['date'].dt.year.min()
year_max = df['date'].dt.year.max()


# HTML webpage layout
app.layout = html.Div([
    html.H1('TED talks', style={'color': 'red'}),
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    # Top TED talks
                    html.Div([
                        html.Div([
                            html.Label('Top '),
                            dcc.Input(
                                id='talks-number',
                                type='number',
                                value=10,
                                min=1,
                                max=df.shape[0],
                                style={'width': '65px',
                                    'margin': '0 5px'}
                            ),
                            html.Label(' TED talks by ')
                        ]),
                        html.Div([
                            dcc.Dropdown(
                                id='talks-dropdown',
                                options=['views', 'view-like ratio'],
                                value='views',
                                clearable=False
                            )
                        ], style={'width': '200px', 'margin':'-32px 0 0 195px', 'color': 'black'}),
                        dcc.Graph(id='talks-content'),
                        dcc.RangeSlider(
                            id='talks-year',
                            min=year_min,
                            max=year_max,
                            step=1,
                            marks={
                                i: {'label': f'{i}', 'style': {
                                    'transform': 'rotate(-45deg)'}}
                                for i in range(year_min, year_max + 1)
                            },
                            value=[year_min, year_max]
                        )
                    ])
                ], width=7),
                dbc.Col([
                    # Top TED speakers
                    html.Div([
                        html.Div([
                            html.Label('Top '),
                            dcc.Input(
                                id='speakers-number',
                                type='number',
                                value=10,
                                min=1,
                                max=df.shape[0],
                                style={'width': '65px', 'margin': '0 5px'}
                            ),
                            html.Label(' TED speakers by ')
                        ]),
                        html.Div([
                            dcc.Dropdown(
                                id='speakers-dropdown',
                                options=['views', 'video count'],
                                value='views',
                                clearable=False
                            )
                        ], style={'width': '200px', 'margin': '-32px 0 0 225px', 'color': 'black'}),
                        dcc.Graph(id='speakers-content')
                    ])
                ], width=5),
            ]),
            html.Br(), 
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    # Time Series Analysis
                    html.Div([
                        html.Div([
                            html.Label('TED talks per ')
                        ]),
                        html.Div([
                            dcc.Dropdown(
                                id='time-series-dropdown',
                                options=['month', 'year'],
                                value='month',
                                clearable=False
                            )
                        ], style={'width': '110px', 'margin': '-28px 0 0 100px', 'color': 'black'}),
                        dcc.Graph(id='time-series-content'),
                        dcc.RangeSlider(
                            id='time-series-year',
                            min=year_min,
                            max=year_max,
                            step=1,
                            marks={
                                i: {'label': f'{i}', 'style': {
                                    'transform': 'rotate(-45deg)'}}
                                for i in range(year_min, year_max + 1)
                            },
                            value=[year_min, year_max]
                        )
                    ])
                ], width=6),
                dbc.Col([
                    # TED talks by speaker
                    html.Div([
                        html.Div([
                            html.Label('Top '),
                            dcc.Input(
                                id='talks-per-speaker-number',
                                type='number',
                                value=10,
                                min=1,
                                max=df.shape[0],
                                style={'width': '65px', 'margin': '0 5px'}
                            ),
                            html.Label(' TED talks by ')
                        ]),
                        html.Div([
                            dcc.Dropdown(
                                id='talks-per-speaker-dropdown',
                                options=sorted(df['author'].str.strip(" '").unique()),
                                value=df.groupby('author').agg(
                                    'count').sort_values('views')[-1:].index[0],
                                clearable=False
                            )
                        ], style={'width': '385px', 'margin': '-32px 0 0 195px', 'color': 'black'}),
                        dcc.Graph(id='talks-per-speaker-content')
                    ])
                ], width=6)
            ])
        ]), color='dark'
    )
], style={'padding': '30px 50px', 'color': 'white'})


# Function to render talks content
@app.callback(
    Output(component_id='talks-content', component_property='figure'),
    Input(component_id='talks-dropdown', component_property='value'),
    Input(component_id='talks-number', component_property='value'),
    Input(component_id='talks-year', component_property='value')
)
def update_talks_content(dropdown, num, year):
    selected_date_df = df[(df['date'].dt.year >= year[0])
                          & (df['date'].dt.year <= year[1])]
    selected_date_df = selected_date_df.sort_values('views')[-num:]
    selected_date_df['date'] = selected_date_df['date'].dt.date

    if dropdown == 'views':
        fig = px.bar(
            selected_date_df,
            x='views',
            y='title',
            hover_data=selected_date_df.columns
        )

        fig.add_trace(go.Bar(
            y=selected_date_df['title'],
            x=selected_date_df['likes'],
            name='likes',
            orientation='h'
        ))

        fig.update_layout(barmode='stack')

        return fig

    elif dropdown == 'view-like ratio':
        top_view_like_ratio = (
            selected_date_df['views'] / selected_date_df['likes']).rename('view_like_ratio')
        top_view_like_ratio = pd.concat(
            [selected_date_df, top_view_like_ratio], axis=1)
        top_view_like_ratio = top_view_like_ratio.sort_values(
            'view_like_ratio')[-num:]

        fig = px.bar(
            top_view_like_ratio,
            x='view_like_ratio',
            y='title',
            hover_data=top_view_like_ratio.columns
        )

        return fig


# Function to render speakers content
@app.callback(
    Output(component_id='speakers-content', component_property='figure'),
    Input(component_id='speakers-dropdown', component_property='value'),
    Input(component_id='speakers-number', component_property='value')
)
def update_speakers_content(dropdown, num):
    if dropdown == 'video count':
        top_speakers_by_count = df.groupby('author').agg(
            'count').sort_values('views')[-num:].reset_index()
        top_speakers_by_count = top_speakers_by_count.rename(
            columns={'views': 'count'})

        fig = px.bar(
            top_speakers_by_count,
            x='count',
            y='author'
        )

        return fig

    elif dropdown == 'views':
        top_speakers_by_views = df.groupby(
            'author').sum().sort_values('views')[-num:].reset_index()

        fig = px.bar(
            top_speakers_by_views,
            x='views',
            y='author'
        )

        return fig


# Function to render talks content
@app.callback(
    Output(component_id='time-series-content', component_property='figure'),
    Input(component_id='time-series-dropdown', component_property='value'),
    Input(component_id='time-series-year', component_property='value')
)
def update_time_series_content(dropdown, year):
    selected_date_df = df[(df['date'].dt.year >= year[0])
                          & (df['date'].dt.year <= year[1])]
    selected_date_df = selected_date_df.sort_values('views')

    if dropdown == 'month':
        videos_per_month = selected_date_df.groupby(
            selected_date_df['date'].dt.month).agg('count')['views'].reset_index()
        videos_per_month = videos_per_month.rename(
            columns={'date': 'month', 'views': 'count'})

        views_per_upload_month = selected_date_df.groupby(
            selected_date_df['date'].dt.month)['views'].mean().reset_index()
        views_per_upload_month = views_per_upload_month.rename(
            columns={'date': 'month'})

        fig = make_subplots(rows=2, cols=1, subplot_titles=(
            "Total videos uploaded per month", "Average views per upload month"))

        fig.append_trace(go.Scatter(
            x=videos_per_month['month'],
            y=videos_per_month['count'],
            name='counts'
        ), row=1, col=1)

        fig.update_xaxes(row=1, col=1, tickvals=np.arange(1, 13))
        fig.update_yaxes(title_text="count", row=1, col=1)

        fig.append_trace(go.Scatter(
            x=views_per_upload_month['month'],
            y=views_per_upload_month['views'],
            name='views'
        ), row=2, col=1)

        fig.update_xaxes(title_text="month", row=2,
                         col=1, tickvals=np.arange(1, 13))
        fig.update_yaxes(title_text="views", row=2, col=1)

        return fig

    elif dropdown == 'year':
        videos_per_year = selected_date_df.groupby(
            selected_date_df['date'].dt.year).agg('count')['views'].reset_index()
        videos_per_year = videos_per_year.rename(
            columns={'date': 'year', 'views': 'count'})

        views_per_upload_year = selected_date_df.groupby(
            selected_date_df['date'].dt.year)['views'].sum().reset_index()
        views_per_upload_year = views_per_upload_year.rename(
            columns={'date': 'year'})

        fig = make_subplots(rows=2, cols=1, subplot_titles=(
            "Total videos uploaded per year", "Total views per upload year"))

        fig.append_trace(go.Scatter(
            x=videos_per_year['year'],
            y=videos_per_year['count'],
            name='counts'
        ), row=1, col=1)

        fig.update_xaxes(row=1, col=1, tickvals=np.arange(
            year[0], year[1] + 1), tickangle=-45)
        fig.update_yaxes(title_text="count", row=1, col=1)

        fig.append_trace(go.Scatter(
            x=views_per_upload_year['year'],
            y=views_per_upload_year['views'],
            name='views'
        ), row=2, col=1)

        fig.update_xaxes(title_text="year", row=2, col=1, tickvals=np.arange(
            year[0], year[1] + 1), tickangle=-45)
        fig.update_yaxes(title_text="views", row=2, col=1)

        return fig


# Function to render talks per speaker content
@app.callback(
    Output(component_id='talks-per-speaker-content', component_property='figure'),
    Input(component_id='talks-per-speaker-dropdown', component_property='value'),
    Input(component_id='talks-per-speaker-number', component_property='value')
)
def update_speakers_content(dropdown, num):
    talks_per_speaker = df[df['author'] == dropdown].sort_values('views')[-num:]
    talks_per_speaker['date'] = talks_per_speaker['date'].dt.date

    fig = px.bar(
        talks_per_speaker,
        x='views',
        y='title',
        hover_data=talks_per_speaker.columns
    )

    return fig


# main call
if __name__ == '__main__':
    app.run_server(debug=True)
