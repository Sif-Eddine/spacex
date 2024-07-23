# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
options=[{'label': 'All Sites', 'value': 'ALL'}]
for item in spacex_df["Launch Site"].unique():
    options.append({'label': item, 'value': item})
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(options,value='ALL',
                                placeholder="place holder here",
                                searchable=True,id='site-dropdown'),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                min=0, max=10000, step=1000,
                                marks={x : str(x) for x in range (0,11001,500)},
                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                ])

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Launches from all sites')
        return fig
    else:
        filtered_df = spacex_df[spacex_df["Launch Site"]==entered_site].groupby("class").count()
        fig = px.pie(filtered_df, values='Launch Site', 
        names=['Success', 'Failiure'], 
        title='Success and Failure Launches for site: ' + entered_site)
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output('success-payload-scatter-chart', 'figure'),
              Input('site-dropdown', 'value'), Input('payload-slider', 'value'))
def get_scatter_plot(entered_site, entered_payload):
    filtered_df = spacex_df[(spacex_df["Payload Mass (kg)"] >= entered_payload[0]) & (spacex_df["Payload Mass (kg)"] <= entered_payload[1])]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df,  x='Payload Mass (kg)', 
        y='class',
        title='Payload VS mission outcome for all sites')
        return fig
    else:
        filtered_df = spacex_df[(spacex_df["Launch Site"]==entered_site) & (spacex_df["Payload Mass (kg)"] >= entered_payload[0]) & (spacex_df["Payload Mass (kg)"] <= entered_payload[1])]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', 
        y='class', 
        title='Payload VS mission outcome for site: ' + entered_site)
        return fig


def run_server(self,
               port=8050,
               debug=True,
               threaded=True,
               **flask_run_options):
    self.server.run(port=port, debug=debug, **flask_run_options)
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8051) # or whatever you choose
