'''
Dashboard Application with Plotly Dash
_____________________________________________
In this program , we will be building a Plotly dash application
for users to perform interactive visual analytics
on Spacec launch data in real time
'''
import wget
from dash import dcc, html , dash
from dash.dependencies import Input,Output
import pandas as pd
import plotly.express as px
import os

app = dash.Dash(__name__)
path = os.path.join(os.getcwd(), 'Week 3 Plotly Dash','assets', 'spacex_launch_dash.csv')
df = pd.read_csv(path)
unique_launch_sites = df['Launch Site'].unique().tolist()
launch_sites = []
launch_sites.append({'label': 'All Sites', 'value': 'All Sites'})
for launch_site in unique_launch_sites:
    launch_sites.append({'label': launch_site, 'value': launch_site})
    
max_payload = df['Payload Mass (kg)'].max()
min_payload = df['Payload Mass (kg)'].min()
app.layout = html.Div(
    children=[
        html.Div([
            html.H1('SpaceX Launch Records Analytics Dashboard',
                    style={'textAlign':'center', 'background-color':'black','color':'red', 'font-size': '40',
                           'padding' : '40px'})
        ], ),
        html.Div([
            dcc.Dropdown(
                id  = 'site-dropdown',
                options = launch_sites,
                placeholder = 'Select Launch Site',
                searchable = True,
                value = 'All Sites',
            ),
            html.Div(dcc.Graph(id='success-pie-chart'))
        ], ),
        html.Div([
            html.Div(
                "Payload Range (Kg) : ",
                style = {'color':'green', 'font-size':'20px'}
            ),
            html.Div([
                dcc.RangeSlider(
                    id = 'payload_slider',
                    min = 0,
                    max = 10000,
                    step = 1000,
                    marks = {
                        0: {'label': '0 Kg', 'style': {'color': '#77b0b1'}},
                        1000: {'label': '1000 Kg'},
                        2000: {'label': '2000 Kg'},
                        3000: {'label': '3000 Kg'},
                        4000: {'label': '4000 Kg'},
                        5000: {'label': '5000 Kg'},
                        6000: {'label': '6000 Kg'},
                        7000: {'label': '7000 Kg'},
                        8000: {'label': '8000 Kg'},
                        9000: {'label': '9000 Kg'},
                        10000: {'label': '10000 Kg', 'style': {'color': '#f50'}},
                    },
                     value = [min_payload,max_payload]
                )
                
            ],style={'padding': '40px 30px'}),
            
            html.Div(dcc.Graph(id= 'success-payload-scatter-chart')
            ),
            
        ]),
    ],style = {'margin': '30px'}
)

@app.callback(
    [
    Output(component_id='success-pie-chart', component_property='figure'),
    Output(component_id = 'success-payload-scatter-chart', component_property = 'figure')],
    [Input(component_id='site-dropdown',component_property='value'),
     Input(component_id = "payload_slider", component_property = "value")]
)
def update_figures(site_dropdown,payload_slider):
    if (site_dropdown == 'All Sites' or site_dropdown == 'None'):
        all_sites = df[df['class'] == 1]
        fig = px.pie(
        all_sites,
        names='Launch Site',
        title='Total Succes Launches by All Sites',
        hole=.2,
        color_discrete_sequence=px.colors.sequential.RdBu
        )
    else:
        for_unique_site = df[df['Launch Site'] == site_dropdown]
        fig = px.pie(
        for_unique_site,
        names='class',
        title=f"Total success for site : {site_dropdown}",
        color_discrete_sequence=px.colors.sequential.RdBu
        )
    
    if (site_dropdown == 'All Sites' or site_dropdown == 'None'):
        low, high = payload_slider
        all_sites  = df
        inrange = (all_sites['Payload Mass (kg)'] > low) & (all_sites['Payload Mass (kg)'] < high)
        fig1 = px.scatter(
                all_sites[inrange], 
                x = "Payload Mass (kg)", 
                y = "class",
                title = 'Correlation Between Payload and Success for All Sites',
                color="Booster Version Category",
                size='Payload Mass (kg)',
                hover_data=['Payload Mass (kg)']
            )
    else:
        low, high = payload_slider
        site_specific  = df.loc[df['Launch Site'] == site_dropdown]
        inrange = (site_specific['Payload Mass (kg)'] > low) & (site_specific['Payload Mass (kg)'] < high)
        fig1 = px.scatter(
                site_specific[inrange],
                x = "Payload Mass (kg)",
                y = "class",
                title = 'Correlation Between Payload and Success for Site : '+site_dropdown,
                color="Booster Version Category",
                size='Payload Mass (kg)',
                hover_data=['Payload Mass (kg)']
            )
    return fig, fig1






if __name__ == '__main__':
    app.run_server(debug = True)