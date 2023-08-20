import plotly.express as px
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import time

# Create dummy data
data = {
    'CODE': ['USA', 'CAN', 'MEX', 'BRA', 'ARG', 'CHN', 'IND', 'RUS', 'AUS', 'ZAF'],
    '2000': [25, 15, 10, 8, 12, 18, 22, 14, 16, 9],
    '2001': [24, 14, 9, 7, 11, 17, 21, 13, 15, 8],
    '2002': [23, 13, 8, 6, 10, 16, 20, 12, 14, 7],
    '2003': [22, 12, 7, 5, 9, 15, 19, 11, 13, 6],
    '2004': [21, 11, 6, 4, 8, 14, 18, 10, 12, 5],
    '2005': [30, 20, 12, 10, 14, 22, 25, 16, 18, 11],
    '2006': [29, 19, 11, 9, 13, 21, 24, 15, 17, 10],
    '2007': [28, 18, 10, 8, 12, 20, 23, 14, 16, 9],
    '2008': [27, 17, 9, 7, 11, 19, 22, 13, 15, 8],
    '2009': [26, 16, 8, 6, 10, 18, 21, 12, 14, 7],
    '2010': [35, 25, 15, 12, 16, 28, 30, 18, 20, 13]
}

df_world = pd.DataFrame(data)

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='world-map'),
    dcc.Slider(
        id='year-slider',
        min=2000,
        max=2010,
        step=1,
        value=2005,
        marks={str(year): str(year) for year in range(2000, 2011)},
    ),
    html.Button('Play', id='play-button', n_clicks=0),
    dcc.Interval(
        id='interval-component',
        interval=1000,  # in milliseconds
        n_intervals=0
    )
])


@app.callback(
    Output('world-map', 'figure'),
    Output('year-slider', 'value'),
    Input('year-slider', 'value'),
    Input('play-button', 'n_clicks'),
    Input('interval-component', 'n_intervals')
)
def update_world_map(selected_year, play_button_clicks, interval_intervals):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'play-button':
        selected_year = 2000  # Start from the beginning

    # Create a choropleth map using Plotly Express
    fig = px.choropleth(df_world, locations='CODE', color=str(selected_year),
                        color_continuous_scale='RdYlGn_r', template="plotly_dark",
                        title=f'Weltweiter CO2-Ausstoß in {selected_year}')

    # Set mapbox properties
    fig.update_layout(mapbox_style="carto-positron",
                      mapbox_zoom=1)

    # Set title and margins
    fig.update_layout(title_x=0.5, margin={"r": 0, "t": 30, "l": 0, "b": 0})

    new_year = selected_year + 1 if selected_year < 2010 else 2000

    return fig, new_year


if __name__ == '__main__':
    app.run_server(debug=True, port=9040)
