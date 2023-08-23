import plotly.express as px
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

df_world = pd.read_csv('../data/processed/table1.csv')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Data Plotter', style={'fontSize': '2.5rem', 'textAlign': 'center'}),
    dcc.Dropdown(
        id='country-dropdown',
        options=[
            {'label': country, 'value': country}
            for country in df_world['Country'].unique()
        ],
        value='Germany',  # Default selected country
        multi=False,
        style={'width': '50%', 'margin': 'auto'}
    ),
    dcc.Dropdown(
        id='year-dropdown',
        options=[
            {'label': year, 'value': year}
            for year in df_world['Year'].unique()
        ],
        value=2003,  # Default selected year
        multi=False,
        style={'width': '50%', 'margin': 'auto'}
    ),
    dcc.Graph(id='data-plot', style={'width': '80%', 'margin': 'auto'}),
])


@app.callback(
    Output('data-plot', 'figure'),
    Input('country-dropdown', 'value'),
    Input('year-dropdown', 'value')
)
def update_data_plot(selected_country, selected_year):
    filtered_data = df_world[(df_world['Country'] == selected_country) & (df_world['Year'] == selected_year)]

    fig = px.bar(
        filtered_data,
        x='Factor',
        y='Value',
        title=f'Plot for {selected_country} in {selected_year}',
        template='plotly_dark'
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=9036)
