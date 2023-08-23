import plotly.express as px
import plotly.graph_objects as go  # Import Plotly Graph Objects
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Load the Plotly 'world' dataset
world = px.data.gapminder().query("year == 2007")

# Filter the dataset to show only European countries
europe = ["Albania", "Austria", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia",
          "Czech Republic", "Denmark", "Finland", "France", "Germany", "Greece", "Hungary",
          "Iceland", "Ireland", "Italy", "Netherlands", "Norway", "Poland", "Portugal",
          "Romania", "Russia", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland",
          "Ukraine", "United Kingdom"]
europe_data = world[world['country'].isin(europe)]

df_world = pd.read_csv('../data/processed/table1.csv')

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        html.H1('Mortality study in heatwaves', id='title',
                style={'fontSize': '2.5rem', 'marginBottom': '20px', 'textAlign': 'center',
                       'background': 'linear-gradient(to right, yellow, red)',
                       'backgroundClip': 'text', 'color': 'transparent'}),
        dcc.Tabs(id='tabs', value='tab-1', children=[
            dcc.Tab(label='World view', value='tab-1', className='nav-link'),
            dcc.Tab(label='Mortality factors', value='tab-2', className='nav-link')
        ], style={'fontSize': '1.5rem'}),
        html.Div(id='page-content')
    ], className='nav'), #style={'backgroundColor': 'lightyellow'}),
])

@app.callback(Output('page-content', 'children'), Input('tabs', 'value'))
def display_page(tab_value):
    if tab_value == 'tab-2':
        return html.Div([
            html.H1('Select country', style={'fontSize': '1.5rem', 'marginTop': '20px'}),
            html.Div([
                dcc.Dropdown(
                    id='country-dropdown',
                    options=[
                        {'label': country, 'value': country}
                        for country in europe_data['country'].unique()
                    ],
                    value='Germany',  # Default selected country
                    multi=False
                ),
                dcc.Graph(id='map-graph'),
            ], style={'width': '65%', 'display': 'inline-block'}),

            html.Div([
                dcc.Graph(id='bar-chart')
            ], style={'width': '35%', 'display': 'inline-block'}),

            html.Div([
                dcc.Graph(id='line-chart')
            ], style={'width': '100%', 'display': 'inline-block'})
        ])
    else:
        return html.Div([
            dcc.Graph(id='world-map'),
            dcc.Slider(
                id='year-slider',
                min=2003,
                max=2023,
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
            dcc.Graph(id='line-plot')  # Add a dynamic line plot
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
    fig = px.choropleth(df_world, locations='CODE', color=str(selected_year),
                        color_continuous_scale='RdYlGn_r', template="plotly_dark",
                        title=f'Mortality during heatwave in {selected_year}')

    fig.update_layout(mapbox_style="carto-positron",
                      mapbox_zoom=1)

    # Adjust the margin and add space between the title and top margin
    fig.update_layout(title_x=0.5, margin={"r": 0, "t": 100, "l": 0, "b": 0})

    fig.update_geos(showframe=False)

    new_year = selected_year + 1 if selected_year < 2023 else 2003

    return fig, new_year

@app.callback(
    Output('line-plot', 'figure'),  # Output for the line plot
    Input('interval-component', 'n_intervals')
)
def update_line_plot(n_intervals):
    # Calculate the total deaths for each year from 2003 to 2023
    year_range = range(2003, 2023)
    total_deaths = [df_world[str(year)].sum() for year in year_range]

    # Create a dynamic line plot
    line_fig = px.line(x=year_range, y=total_deaths, labels={'x': 'Year', 'y': 'Total Deaths'},
                       template="plotly_dark", title='Total Deaths from 2003 to 2023')

    return line_fig


# add
@app.callback(
    Output('map-graph', 'figure'),
    Output('bar-chart', 'figure'),
    Output('line-chart', 'figure'),
    Input('country-dropdown', 'value')
)
def update_country_charts(selected_country):
    # Filter data for the selected country
    country_data = europe_data[europe_data['country'] == selected_country]

    # Create a scatter
    # plot using Plotly Express for the map
    map_fig = px.scatter_geo(
        country_data,
        locations='iso_alpha',
        locationmode='ISO-3',
        color='continent',
        size='pop',
        hover_name='country',
        projection='orthographic',
        title=f'Population and Continent for {selected_country}',
        scope='europe'
    )

    # Dummy data for the bar chart
    dummy_years = [2002, 2003, 2004, 2005, 2006]
    dummy_disasters = [10, 15, 8, 12, 20]

    # Create a horizontal bar chart using Plotly Express for the bar chart
    bar_fig = px.bar(
        x=dummy_disasters,
        y=dummy_years,
        orientation='h',
        labels={'x': 'Number of Disasters', 'y': 'Year'},
        title=f'Number of Disasters in {selected_country} (Previous 5 Years)'
    )

    # Dummy data for the line chart
    dummy_years = list(range(2000, 2021))
    dummy_temperatures = [20, 21, 20.5, 21.2, 22, 22.5, 23, 24, 24.5, 25, 26, 26.5,
                          27, 27.5, 28, 28.5, 29, 29.5, 30, 30.5, 31]

    # Create a line chart using Plotly Graph Objects for the line chart
    line_fig = go.Figure(go.Scatter(x=dummy_years, y=dummy_temperatures, mode='lines+markers'))
    line_fig.update_layout(
        title=f'Surface Temperature Trend in {selected_country}',
        xaxis_title='Year',
        yaxis_title='Surface Temperature (°C)'
    )

    return map_fig, bar_fig, line_fig

# there can be multiple heatwave for a country in a each?
# if so, the user will indicate which one, if not, the user only needs to select the year
# the bar shows how different factors contribute to the mortality, based on SHAP Values
# the overview bar below shows the feature importance for all factors across all countries

if __name__ == '__main__':
    app.run_server(debug=True, port=9035)
