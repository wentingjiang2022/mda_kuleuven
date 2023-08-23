import plotly.express as px
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import shap
import numpy as np
from flask import Flask
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

application = Flask(__name__)

# Load the Plotly 'world' dataset
world = px.data.gapminder().query("year == 2007")

# Filter the dataset to show only European countries
europe = ["Albania", "Austria", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia",
          "Czech Republic", "Denmark", "Finland", "France", "Germany", "Greece", "Hungary",
          "Iceland", "Ireland", "Italy", "Netherlands", "Norway", "Poland", "Portugal",
          "Romania", "Russia", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland",
          "Ukraine", "United Kingdom"]
europe_data = world[world['country'].isin(europe)]

df_world_0 = pd.read_csv('table1.csv')
df_world = pd.read_csv('country_focus.csv')
df_model = pd.read_csv('df_model.csv')

files = ['poverty', 'housing_deprive', 'forest', 'elder', 'population', 'gdp',
         'unemployment', 'child_population', 'disabled']
features = ['Year', 'Country', 'Seq',
            'Max_temp',
            'Days_over_30', 'Start Month',
            'Region',
            ] + files

df_select = df_model[features]
columns_to_encode = ['Region', 'Country']
# Get dummies for the specified columns
dummies = pd.get_dummies(df_select[columns_to_encode], columns=columns_to_encode, prefix=columns_to_encode)

X = pd.concat([df_select, dummies], axis=1).drop(columns_to_encode, axis=1)
y = df_model['Total Deaths']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    test_size=0.3, random_state=42)

rf_model = RandomForestRegressor(n_estimators=400)
rf_model.fit(X_train, y_train)

#app = dash.Dash(__name__, suppress_callback_exceptions=True)
app = dash.Dash(__name__,server=application)

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
                        for country in df_world['Year'].unique()
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
          #  dcc.Graph(id='line-plot')  # Add a dynamic line plot
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
    fig = px.choropleth(df_world_0, locations='CODE', color=str(selected_year),
                        color_continuous_scale='RdYlGn_r', template="plotly_dark",
                        title=f'Mortality during heatwave in {selected_year}')

    fig.update_layout(mapbox_style="carto-positron",
                      mapbox_zoom=1)

    # Adjust the margin and add space between the title and top margin
    fig.update_layout(title_x=0.5, margin={"r": 0, "t": 100, "l": 0, "b": 0})

    fig.update_geos(showframe=False)

    new_year = selected_year + 1 if selected_year < 2022 else 2003

    return fig, new_year


@app.callback(
    Output('map-graph', 'figure'),
    Output('bar-chart', 'figure'),
    Output('line-chart1', 'figure'),
    Output('line-chart2', 'figure'),
    Input('country-dropdown', 'value')
)
def update_country_charts(selected_country):
    # Filter data for the selected country

    df_year = df_world[df_world['Year']==selected_country]
    seq_selected = df_year.Seq.unique()[0]
    country_impacted = df_year[df_year['Seq']==seq_selected].Country.unique()
    country_data = europe_data[europe_data['country'].isin(country_impacted)]

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
    dummy_years = country_impacted
    dummy_disasters = df_year[df_year['Seq']==seq_selected]['Total Deaths']

    # Create a horizontal bar chart using Plotly Express for the bar chart
    bar_fig = px.bar(
        x=dummy_disasters,
        y=dummy_years,
        orientation='h',
        labels={'x': 'Number of Disasters', 'y': 'Year'},
        title=f'Number of Disasters in {selected_country} (Previous 5 Years)'
    )

    #loaded_model = joblib.load('../notebooks/random_forest_model.pkl')

    #selected_year = selected_country
   # seq = seq_selected
    df = X[(X['Year'] == selected_country) & (X['Seq'] == seq_selected)]

    index_values = df.index

    # Filter df2 based on the index values from df1
    filtered_df2 = pd.DataFrame(y.loc[index_values])
    sorted_df = filtered_df2.sort_values(by='Total Deaths', ascending=False)
    index_list = sorted_df.index[:2]

    # Create a list of countries column names
    countries = [col for col in df.columns if col.startswith('Country_')]

    df_two_countries = df.loc[index_list][countries]
    columns_with_true = [col for col in df_two_countries.columns if df_two_countries[col].any()]

    # Create a SHAP explainer object for the random forest model
    explainer = shap.Explainer(rf_model)

    # List to store the generated plots
    plots = []
    # Iterate through each country column
    # List to store the generated plots
    plots = []

    # Create the first plot using Plotly Express
    for i in columns_with_true:
        observation = df[df[i] == 1].iloc[0]

        # Calculate SHAP values for the observation
        shap_values = explainer.shap_values(observation)

        # Example feature names list
        feature_names = df.columns  # Update this based on your actual feature names

        # Sort the features and SHAP values by their absolute values
        sorted_indices = np.argsort(np.abs(shap_values))
        sorted_feature_names = [feature_names[i] for i in sorted_indices]
        sorted_shap_values = [shap_values[i] for i in sorted_indices]

        # Determine colors based on SHAP values
       # colors = ['red' if value > 0 else 'yellow' for value in sorted_shap_values]

        colors = ['green' if value < 0 else 'red' for value in sorted_shap_values]
        # Explicitly set color mapping for consistent colors
        color_mapping = {'green': 'green', 'red': 'red'}

        # Create a Plotly Express bar plot with colors
        fig = px.bar(
            x=sorted_shap_values,
            y=sorted_feature_names,
            color=colors,
            color_discrete_map=color_mapping,  # Explicitly set color mapping

            orientation='h',
            labels={'x': 'SHAP Value', 'y': 'Feature'},
            title=f'Feature Importance for {i}',
            # showlegend=False  # Turn off the legend
        )

        fig.update_layout(showlegend=False)

        # Append the plot to the list
        plots.append(fig)

    shap1 = plots[0]
    shap2 = plots[1]

    return map_fig, bar_fig, shap1, shap2

if __name__ == '__main__':
    application.run()
    #app.run_server(debug=True, port=9235)
