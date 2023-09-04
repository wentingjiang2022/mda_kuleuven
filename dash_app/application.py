import joblib
import plotly.express as px
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import shap
import numpy as np
from flask import Flask

application = Flask(__name__)
world = px.data.gapminder().query("year == 2007")
df_map = pd.read_csv('table1.csv')
df_model = pd.read_csv('df_model.csv') # pd.read_csv('country_focus.csv')
model_ready = pd.read_csv('model_ready.csv')
X = model_ready.drop('Total Deaths', axis=1)
y = model_ready['Total Deaths']

#app = dash.Dash(__name__, suppress_callback_exceptions=True)
app = dash.Dash(__name__,server=application)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        html.H1('Mortality study in heatwaves', id='title',
        style={'fontSize': '2.5rem', 'marginBottom': '20px', 'textAlign': 'center',
       'color': 'orange'}),
        dcc.Tabs(id='tabs', value='tab-1', children=[
            dcc.Tab(label='World view', value='tab-1', className='nav-link'),
            dcc.Tab(label='Mortality factors', value='tab-2', className='nav-link')
        ], style={'fontSize': '1.5rem'}),
        html.Div(id='page-content')
    ], className='nav'),
])

@app.callback(Output('page-content', 'children'), Input('tabs', 'value'))
def display_page(tab_value):
    if tab_value == 'tab-2':
        return html.Div([
            html.H1('Select year', style={'fontSize': '1.5rem', 'marginTop': '20px'}),
            html.Div([
                dcc.Dropdown(
                    id='year-dropdown',
                    options=[
                        {'label': year, 'value': year}
                        for year in [2003, 2006, 2007, 2019, 2020, 2022]
                    ],
                    value=2003,  # Default selected country
                    multi=False
                ),
                dcc.Graph(id='map-graph'),
            ], style={'width': '65%', 'display': 'inline-block'}),

            html.Div([
                dcc.Graph(id='bar-chart')
            ], style={'width': '35%', 'display': 'inline-block'}),

            html.Div([
                dcc.Graph(id='line-chart1')
            ], style={'width': '45%', 'display': 'inline-block'}),
            html.Div([
                dcc.Graph(id='line-chart2')
            ], style={'width': '45%', 'display': 'inline-block'}),
        ])
    else:
        return html.Div([
            dcc.Graph(id='world-map'),
            dcc.Slider(
                id='year-slider',
                min=2003,
                max=2022,
                step=1,
                value=2003,
                marks={str(year): str(year) for year in range(2003, 2023)},
            ),
            html.Button('Replay', id='play-button', n_clicks=0),
            dcc.Interval(
                id='interval-component',
                interval=1000,  # in milliseconds
                n_intervals=0
            ),
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
        selected_year = 2003  # Start from the beginning

    # Create a choropleth map using Plotly Express
    fig = px.choropleth(df_map, locations='CODE', color=str(selected_year),
                        color_continuous_scale='RdYlGn_r', template="plotly_dark",
                        title=f'Mortality during heatwave in {selected_year+1}')

    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=1,
        title_x=0.5,
        margin={"r": 0, "t": 80, "l": 0, "b": 0},
        paper_bgcolor='darkblue',
        font_color='white',
    )
    fig.update_coloraxes(colorbar_title="")

    fig.update_geos(showframe=False)
    fig.update_geos(
        projection_type='mercator',
        showland=True,
        landcolor='white',
        bgcolor='darkblue')

    new_year = selected_year + 1 if selected_year < 2022 else 2003

    return fig, new_year

@app.callback(
    Output('map-graph', 'figure'),
    Output('bar-chart', 'figure'),
    Output('line-chart1', 'figure'),
    Output('line-chart2', 'figure'),
    Input('year-dropdown', 'value')
)
def update_country_charts(selected_year):

    df_year = df_model[df_model['Year']==selected_year]
    seq_selected = df_year.Seq.unique()[0] #take first sequence
    country_impacted = df_year[df_year['Seq']==seq_selected].Country.unique()
    country_data = world[world['country'].isin(country_impacted)]

    map_fig = px.scatter_geo(
        country_data,
        locations='iso_alpha',
        locationmode='ISO-3',
        color='continent',
        size='pop',
        hover_name='country',
        projection='orthographic',
        title=f'Population and Continent for {selected_year}',
        scope='europe'
    )

    mortality = df_year[df_year['Seq']==seq_selected]['Total Deaths']
    bar_fig = px.bar(
        x=mortality,
        y=country_impacted,
        orientation='h',
        labels={'x': 'Mortality', 'y': 'Country'},
        title=f'Mortality in {selected_year}'
    )

    df = X[(X['Year'] == selected_year) & (X['Seq'] == seq_selected)]

    index_values = df.index
    filtered_df2 = pd.DataFrame(y.loc[index_values])

    # take the two countries with largest mortality of that year
    sorted_df = filtered_df2.sort_values(by='Total Deaths', ascending=False)
    index_list = sorted_df.index[:2]

    countries = [col for col in df.columns if col.startswith('Country_')]
    df_two_countries = df.loc[index_list][countries]
    columns_with_true = [col for col in df_two_countries.columns if df_two_countries[col].any()]
    rf_model = joblib.load('random_forest_model.pkl')
    explainer = shap.Explainer(rf_model)

    plots = []
    for i in columns_with_true:
        observation = df[df[i] == 1].iloc[0]
        shap_values = explainer.shap_values(observation)
        feature_names = df.columns
        sorted_indices = np.argsort(np.abs(shap_values))
        sorted_feature_names = [feature_names[i] for i in sorted_indices]
        sorted_shap_values = [shap_values[i] for i in sorted_indices]

        colors = ['lightgreen' if shap_value < 0 else 'lightcoral' for shap_value in sorted_shap_values]
        color_mapping = {'green': 'lightgreen', 'red': 'lightcoral'}

        fig = px.bar(
            x=sorted_shap_values,
            y=sorted_feature_names,
            color=colors,
            color_discrete_map=color_mapping,  # Explicitly set color mapping
            orientation='h',
            labels={'x': 'SHAP Value', 'y': 'Feature'},
            title = f'Feature Importance for {i.split("_")[1]}'
        )

        fig.update_layout(showlegend=False)
        plots.append(fig)

    shap1 = plots[0]
    shap2 = plots[1]

    return map_fig, bar_fig, shap1, shap2

if __name__ == '__main__':
    application.run()
    #app.run_server(debug=True, port=9100)
