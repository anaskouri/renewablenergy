#import the required package


import os
import plotly
import plotly.express as px
import plotly.graph_objects as go
import dash
import jupyter_dash as jd
from jupyter_dash import JupyterDash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
import pandas as pd
pd.options.display.max_columns = None
import pathlib
from app import app
#from pandasql import sqldf



PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

solar_energy_share = pd.read_csv(DATA_PATH.joinpath("solar-share-energy.csv"))
per_capita_solar = pd.read_csv(DATA_PATH.joinpath('per-capita-solar.csv'))
solar_consumption = pd.read_csv(DATA_PATH.joinpath("solar-energy-consumption.csv"))
annual_change_solar_pct = pd.read_csv(DATA_PATH.joinpath('annual-percentage-change-solar.csv'))
annual_change_solar_twh = pd.read_csv(DATA_PATH.joinpath('annual-change-solar.csv'))
solar_electricity_share = pd.read_csv(DATA_PATH.joinpath("share-electricity-solar.csv"))
installed_solar_capacity = pd.read_csv(DATA_PATH.joinpath("installed-solar-PV-capacity.csv"))



regions = ['Africa', 'Africa (BP)', 'Asia', 'Asia Pacific (BP)', 'CIS (BP)',
       'Central America (BP)', 'Eastern Africa (BP)', 'Europe',
       'Europe (BP)', 'European Union (27)', 'High-income countries',
       'Lower-middle-income countries', 'Middle Africa (BP)',
       'Middle East (BP)', 'Non-OECD (BP)', 'North America',
       'North America (BP)', 'OECD (BP)', 'Oceania', 'Other Africa (BP)',
       'Other Asia Pacific (BP)', 'Other CIS (BP)',
       'Other Caribbean (BP)', 'Other Europe (BP)',
       'Other Middle East (BP)', 'Other Northern Africa (BP)',
       'Other South America (BP)', 'Other South and Central America (BP)',
       'Other Southern Africa (BP)', 'South America',
       'South and Central America (BP)', 'Upper-middle-income countries',
       'Western Africa (BP)','World']


import functools
solar_energy = functools.reduce(functools.partial(pd.merge, on=['Entity','Code','Year']),
                 [solar_energy_share,solar_electricity_share,per_capita_solar,solar_consumption,annual_change_solar_pct,
                  annual_change_solar_twh,installed_solar_capacity
                 ])

solar_energy_countries = solar_energy[~solar_energy['Entity'].isin(regions)]

solar_energy_countries = solar_energy_countries.rename(columns={'Solar Capacity':'Installed solar capacity (GW)'})

cividis0 = px.colors.sequential.Cividis[0]

def make_empty_fig():
    fig = go.Figure()
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig.layout.plot_bgcolor = '#E5ECF6'
    return fig

def multiline_indicator(indicator):
    final = []
    split = indicator.split()
    for i in range(0, len(split), 3):
        final.append(' '.join(split[i:i+3]))
    return '<br>'.join(final)



#create the app layout

layout = html.Div([
    dbc.Row([
        dbc.Col(
            html.H1('Solar Energy'),style ={'textAlign': 'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.H2('Our world in Data'), style ={'textAlign': 'center'}
        ),
    ]),
    html.Br(),
    #dbc.Row([
        #dbc.Col(
           # html.H2('How much of our primary energy comes from renewables?'),style ={'textAlign': 'center'}
       # ),

    #]),
    dbc.Row([
        dbc.Col([
            dbc.Label('Countries: '),
            dcc.Dropdown(id='countries_dropdown_solar',
                         placeholder = 'Select one or more countries',
                         value=['United States','Australia'],
                         multi = True,
                         options=[{'label': country, 'value': country}
                                 for country in solar_energy_countries['Entity'].unique()]),
            ],width={'size': 8, "offset": 0}),
        dbc.Col([
            dbc.Label('Year: '),
            dcc.Dropdown(id='year_dropdown_solar',
                         value = 2021,
                         options = [{'label':Year,'value':Year}
                                    for Year in solar_energy_countries['Year'].unique()],
            )
        ],width={'size':4,'offset':0})
    ]),
    html.Br(),
    dbc.Row([
         dbc.Tabs([
        dcc.Tab(label = 'Share of primary energy from solar', children = [
            dbc.Row([
                dbc.Col(dcc.Graph(id='line1_solar',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4}),
                dbc.Col(dcc.Graph(id='bar1_solar',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4}),
                dbc.Col(dcc.Graph(id='top20_1_solar',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4})
                   ])
           ]),
        dcc.Tab(label = 'Energy consumption from solar per capita', children = [
            dbc.Row([
            dbc.Col(dcc.Graph(id='line2_solar',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4}),
            dbc.Col(dcc.Graph(id='bar2_solar',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4}),
            dbc.Col(dcc.Graph(id='top20_2_solar',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4})
                   ])
          ]),
        dcc.Tab(label = 'Installed solar capacity', children = [
            dbc.Row([
            dbc.Col(dcc.Graph(id='line3_solar',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4}),
            dbc.Col(dcc.Graph(id='bar3_solar',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4}),
            dbc.Col(dcc.Graph(id='top20_3_solar',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4})
                   ])
          ]),
        ]),
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col(html.H2('How is the generation of solar energy changing year to year?'),style={'textAlign':'center'}),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Label('Countries: '),
            dcc.Dropdown(id='countries_dropdown_change_solar',
                         placeholder = 'Select one or more countries',
                         value=['United States','Australia'],
                         multi = True,
                         options=[{'label': country, 'value': country}
                                 for country in solar_energy_countries['Entity'].unique()]),
            ],width={'size': 8, "offset": 2}),
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='annual_change_pct_solar',figure=make_empty_fig(),style={'backgroundColor':'#E5ECF6'}),
        ],width=6,lg={'size':6}),
        dbc.Col([
            dcc.Graph(id='annual_change_twh_solar',figure=make_empty_fig(),style={'backgroundColor':'#E5ECF6'}),
        ],width=6,lg={'size':6}),
    ]),
    html.Br(),
     dbc.Tabs([
        dbc.Tab([
            html.Ul([
                html.Br(),
                html.Li('Created by: Anas Kouri'),   
                html.Li('Temporal Coverage: 1985 - 2021'),
                html.Li([
                    'Source: ',
                     html.A(children= 'https://ourworldindata.org/renewable-energy' ,
                           href='https://ourworldindata.org/renewable-energy')
            ])
        ])
        ], label = 'Key Facts'),
        dbc.Tab([
            html.Ul([
                html.Br(),
                html.Li('General statistics about renewable energy across the globe'),
            ])
        ], label = 'Project info')
   ], style={'backgroundColor': '#E5ECF6'})


])



@app.callback(Output('line1_solar', 'figure'),
              Input('countries_dropdown_solar', 'value'))

def update_graph(country):
    dff = solar_energy_countries[solar_energy_countries.Entity.isin((country))]
    fig = px.line(data_frame=dff, x='Year', y='Solar (% equivalent primary energy)', color='Entity',
                  custom_data=['Entity', 'Code', 'Solar (% equivalent primary energy)'],
                  title=''.join(['Solar (% equivalent primary energy)', '<br><b>', ', '.join(country), '</b>']))
    fig.update_traces(mode='lines+markers')
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    fig.update_layout(hovermode="x")
    return fig

@app.callback(Output('bar1_solar', 'figure'),
              Input('countries_dropdown_solar', 'value'))

def plot_renewables_share_countries_barchart(country):
    if not country:
        raise PreventUpdate
    df = solar_energy_countries[solar_energy_countries['Entity'].isin(country)]
    fig = px.bar(df,
                 x='Year',
                 y='Solar (% equivalent primary energy)',
                 height=100 + (250*len(country)),
                 facet_row='Entity',
                 color='Entity',
                 labels={'Solar (% equivalent primary energy)': 'Solar share(%)'},
                 title=''.join(['Solar (% equivalent primary energy)', '<br><b>', ', '.join(country), '</b>']))
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    return fig






@app.callback(Output('line2_solar', 'figure'),
              Input('countries_dropdown_solar', 'value'))
def update_graph(country):
    dff = solar_energy_countries[solar_energy_countries.Entity.isin((country))]
    fig = px.line(data_frame=dff, x='Year', y='Solar per capita (kWh - equivalent)', color='Entity',
                  custom_data=['Entity', 'Code', 'Solar per capita (kWh - equivalent)'],
                  title=''.join(['Solar per capita (kWh - equivalent)', '<br><b>', ', '.join(country), '</b>']))

    fig.update_traces(mode='lines+markers')
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    fig.update_layout(hovermode="x")
    return fig


@app.callback(Output('bar2_solar', 'figure'),
              Input('countries_dropdown_solar', 'value'))


def plot_renewables_share_countries_barchart(country):
    if not country:
        raise PreventUpdate
    df = solar_energy_countries[solar_energy_countries['Entity'].isin(country)]
    fig = px.bar(df,
                 x='Year',
                 y='Solar per capita (kWh - equivalent)',
                 height=100 + (250*len(country)),
                 facet_row='Entity',
                 color='Entity',
                 labels={'Solar per capita (kWh - equivalent)': 'Solar Energy (KWh)'},
                 title=''.join(['Solar per capita (kWh - equivalent)', '<br><b>', ', '.join(country), '</b>']))
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    return fig


@app.callback(Output('top20_1_solar', 'figure'),
              Input('year_dropdown_solar', 'value'))
# graph
def plot_countries_by_renewable_share(Year):
    #fig =go.Figure()
    year_df = solar_energy_countries.loc[solar_energy_countries['Year']==Year].sort_values(
    'Solar (% equivalent primary energy)',ascending = False)[:20]
    fig = px.bar(year_df, y='Entity',
                  x='Solar (% equivalent primary energy)',orientation ='h')
    fig.layout.title = f'Top twenty countries by solar energy share (%) - {Year}'
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    return fig


@app.callback(Output('top20_2_solar', 'figure'),
              Input('year_dropdown_solar', 'value'))
# graph
def plot_countries_by_renewable_share(Year):
    #fig =go.Figure()
    year_df = solar_energy_countries.loc[solar_energy_countries['Year']==Year].sort_values(
    'Solar per capita (kWh - equivalent)',ascending = False)[:20]
    fig = px.bar(year_df, y='Entity',
                  x='Solar per capita (kWh - equivalent)',orientation = 'h')
    fig.layout.title = f'Top twenty countries by solar energy per capita (KWh) - {Year}'
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    return fig





@app.callback(Output('line3_solar', 'figure'),
              Input('countries_dropdown_solar', 'value'))
def update_graph(country):
    dff = solar_energy_countries[solar_energy_countries.Entity.isin((country))]
    fig = px.line(data_frame=dff, x='Year', y='Installed solar capacity (GW)', color='Entity',
                  custom_data=['Entity', 'Code', 'Installed solar capacity (GW)'],
                  title=''.join(['Installed solar capacity (GW)', '<br><b>', ', '.join(country), '</b>']))

    fig.update_traces(mode='lines+markers')
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    fig.update_layout(hovermode="x")
    return fig



@app.callback(Output('bar3_solar', 'figure'),
              Input('countries_dropdown_solar', 'value'))


def plot_renewables_share_countries_barchart(country):
    if not country:
        raise PreventUpdate
    df = solar_energy_countries[solar_energy_countries['Entity'].isin(country)]
    fig = px.bar(df,
                 x='Year',
                 y='Installed solar capacity (GW)',
                 height=100 + (250*len(country)),
                 facet_row='Entity',
                 color='Entity',
                 labels={'Installed solar capacity (GW)': 'Solar capacity (GW)'},
                 title=''.join(['Installed solar capacity (GW)', '<br><b>', ', '.join(country), '</b>']))
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    return fig



@app.callback(Output('top20_3_solar', 'figure'),
              Input('year_dropdown_solar', 'value'))
# graph
def plot_countries_by_renewable_share(Year):
    #fig =go.Figure()
    year_df = solar_energy_countries.loc[solar_energy_countries['Year']==Year].sort_values(
    'Installed solar capacity (GW)',ascending = False)[:20]
    fig =px.bar(year_df,y='Entity',
                  x='Installed solar capacity (GW)',orientation = 'h')
    fig.layout.title = f'Top twenty countries by istalled solar capacity (GW) - {Year}'
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    return fig




@app.callback(Output('annual_change_pct_solar', 'figure'),
              Input('countries_dropdown_change_solar', 'value'))

def update_graph(country):
    dff = solar_energy_countries[solar_energy_countries.Entity.isin((country))]
    fig = px.line(data_frame=dff, x='Year', y='Solar (% growth)', color='Entity',
                  custom_data=['Entity', 'Code', 'Solar (% growth)'],
                  title=''.join(['Solar (% growth)', '<br><b>', ', '.join(country), '</b>']))

    fig.update_traces(mode='lines+markers')
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    fig.update_layout(hovermode="x")
    return fig


@app.callback(Output('annual_change_twh_solar', 'figure'),
              Input('countries_dropdown_change_solar', 'value'))

def update_graph(country):
    dff = solar_energy_countries[solar_energy_countries.Entity.isin((country))]
    fig = px.line(data_frame=dff, x='Year', y='Solar (TWh growth - equivalent)', color='Entity',
                  custom_data=['Entity', 'Code', 'Solar (TWh growth - equivalent)'],
                  title=''.join(['Solar (TWh growth)', '<br><b>', ', '.join(country), '</b>']))

    fig.update_traces(mode='lines+markers')
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    fig.update_layout(hovermode="x")
    return fig

