# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import datetime as dt
from keyring import set_keyring
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dash import Dash, dcc, html, Input, Output
from plotly.subplots import make_subplots


app = Dash(__name__)

# Read data
df = pd.read_csv('data/ted-talks.csv').dropna()
df['date'] = pd.to_datetime(df['date'])
df = df[df['date'] >= dt.datetime(2000, 1, 1)]

# HTML webpage layout
app.layout = html.Div([

    # html.Img(src='../assets/ted.png'),
    html.H1('TED talks'),

    html.Div([
        dcc.Tabs(id="tabs", value='top-views', children=[
            dcc.Tab(label='Top views', value='top-views'),
            dcc.Tab(label='Top view-like ratio', value='top-view-like-ratio')
        ]),
        html.Br(),
        html.Div([
            html.Label('Top ', style={'margin': '0 0 0 50px'}),
            dcc.Input(
                id='number',
                type='number',
                value=10,
                min=1,
                max=df.shape[0],
                style={'width': '55px'}
            ),
            html.Label(' TED talks'),
            dcc.Graph(id='tabs-content'),
            dcc.RangeSlider(
                id='year',
                min=2000, 
                max=2022, 
                step=1,
                marks={
                    i: {'label': f'{i}', 'style': {'transform': 'rotate(-45deg)'}} 
                    for i in range(2000, 2023)
                }, 
                value=[2000, 2022]
            )
        ])
    ]),

], style={'padding': '10px 50px'})


# Function to render tab content
@app.callback(
    Output(component_id='tabs-content', component_property='figure'),
    Input(component_id='tabs', component_property='value'),
    Input(component_id='number', component_property='value'),
    Input(component_id='year', component_property='value')
)
def render_content(tab, num, year):
    if tab == 'top-views':
        selected_date_df = df[(df['date'].dt.year >= year[0]) & (df['date'].dt.year <= year[1])]
        selected_date_df = selected_date_df.sort_values('views')[-num:]
        selected_date_df['date'] = selected_date_df['date'].dt.date

        fig = px.bar(
            selected_date_df,
            x='views',
            y='title',
            hover_name='title',
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


    elif tab == 'top-view-like-ratio':
        selected_date_df = df[(df['date'].dt.year >= year[0]) & (df['date'].dt.year <= year[1])]
        selected_date_df = selected_date_df.sort_values('views')[-num:]
        selected_date_df['date'] = selected_date_df['date'].dt.date

        top_view_like_ratio = (selected_date_df['views'] / selected_date_df['likes']).rename('view_like_ratio')
        top_view_like_ratio = pd.concat([selected_date_df, top_view_like_ratio], axis=1)
        top_view_like_ratio = top_view_like_ratio.sort_values('view_like_ratio')[-num:]

        fig = px.bar(
            top_view_like_ratio,
            x='view_like_ratio',
            y='title',
            hover_name='title',
            hover_data=top_view_like_ratio.columns
        )
        
        return fig


# main call
if __name__ == '__main__':
    app.run_server(debug=True)
