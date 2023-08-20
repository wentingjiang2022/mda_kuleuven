import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Load the Plotly 'world' dataset
world = px.data.gapminder().query("year == 2007")

# Filter the dataset to show only European countries
europe = ["Albania", "Austria", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia",
          "Czech Republic", "Denmark", "Finland", "France", "Germany", "Greece", "Hungary",
          "Iceland", "Ireland", "Italy", "Netherlands", "Norway", "Poland", "Portugal",
          "Romania", "Russia", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland",
          "Ukraine", "United Kingdom"]
europe_data = world[world['country'].isin(europe)]

# Create a Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
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


@app.callback(
    Output('map-graph', 'figure'),
    Output('bar-chart', 'figure'),
    Output('line-chart', 'figure'),
    Input('country-dropdown', 'value')
)
def update_figures(selected_country):
    # Filter data for the selected country
    country_data = europe_data[europe_data['country'] == selected_country]

    # Create a scatter plot using Plotly Express
    map_fig = px.scatter_geo(
        country_data,
        locations='iso_alpha',  # Use 'iso_alpha' column for locations
        locationmode='ISO-3',  # Use ISO-3 country codes
        color='continent',  # Color points by continent
        size='pop',  # Size points by population
        hover_name='country',  # Tooltip when hovering over a point
        projection='orthographic',  # Choose a map projection
        title=f'Population and Continent for {selected_country}',
        scope='europe'  # Set the map scope to Europe
    )

    # Dummy data for the bar chart (replace with your data)
    dummy_years = [2002, 2003, 2004, 2005, 2006]
    dummy_disasters = [10, 15, 8, 12, 20]

    # Create a horizontal bar chart using Plotly Express
    bar_fig = px.bar(
        x=dummy_disasters,
        y=dummy_years,
        orientation='h',
        labels={'x': 'Number of Disasters', 'y': 'Year'},
        title=f'Number of Disasters in {selected_country} (Previous 5 Years)'
    )

    # Dummy data for the line chart (replace with your data)
    dummy_years = list(range(2000, 2021))
    dummy_temperatures = [20, 21, 20.5, 21.2, 22, 22.5, 23, 24, 24.5, 25, 26, 26.5,
                          27, 27.5, 28, 28.5, 29, 29.5, 30, 30.5, 31]

    # Create a line chart using Plotly Graph Objects
    line_fig = go.Figure(go.Scatter(x=dummy_years, y=dummy_temperatures, mode='lines+markers'))
    line_fig.update_layout(
        title=f'Surface Temperature Trend in {selected_country}',
        xaxis_title='Year',
        yaxis_title='Surface Temperature (°C)'
    )

    return map_fig, bar_fig, line_fig


if __name__ == '__main__':
    app.run_server(debug=True, port=9008)
