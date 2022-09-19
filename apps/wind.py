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

wind_energy_share = pd.read_csv(DATA_PATH.joinpath("wind-share-energy.csv"))
per_capita_wind = pd.read_csv(DATA_PATH.joinpath('per-capita-wind.csv'))
wind_generation = pd.read_csv(DATA_PATH.joinpath("Wind-generation.csv"))
annual_change_wind_pct = pd.read_csv(DATA_PATH.joinpath('annual-percentage-change-wind.csv'))
annual_change_wind_twh = pd.read_csv(DATA_PATH.joinpath('annual-change-wind.csv'))
wind_electricity_share = pd.read_csv(DATA_PATH.joinpath("share-electricity-wind.csv"))

installed_wind_capacity = pd.read_csv(DATA_PATH.joinpath("cumulative-installed-wind-energy-capacity-gigawatts.csv"))


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
wind_energy = functools.reduce(functools.partial(pd.merge, on=['Entity','Code','Year']),
                 [wind_energy_share,wind_electricity_share,per_capita_wind,wind_generation,annual_change_wind_pct,annual_change_wind_twh,
                  installed_wind_capacity
                 ])

wind_energy_countries = wind_energy[~wind_energy['Entity'].isin(regions)]
wind_energy_countries.rename(columns ={'Wind Capacity': 'Installed wind capacity (GW)'},inplace=True)

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




layout = html.Div([
    dbc.Row([
        dbc.Col(
            html.H1('Wind Energy'),style ={'textAlign': 'center'}
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
            #html.H2('How much of our primary energy comes from renewables?'),style ={'textAlign': 'center'}
        #),

    #]),
    dbc.Row([
        dbc.Col([
            dbc.Label('Countries: '),
            dcc.Dropdown(id='countries_dropdown_wind',
                         placeholder = 'Select one or more countries',
                         value=['United States','Denmark'],
                         multi = True,
                         options=[{'label': country, 'value': country}
                                 for country in wind_energy_countries['Entity'].unique()]),
            ],width={'size': 8, "offset": 0}),
        dbc.Col([
            dbc.Label('Year: '),
            dcc.Dropdown(id='year_dropdown_wind',
                         value = 2021,
                         options = [{'label':Year,'value':Year}
                                    for Year in wind_energy_countries['Year'].unique()],
            )
        ],width={'size':4,'offset':0})
    ]),
    html.Br(),
    dbc.Row([
         dbc.Tabs([
        dcc.Tab(label = 'Share of primary energy from wind', children = [
            dbc.Row([
                dbc.Col(dcc.Graph(id='line1_wind',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4}),
                dbc.Col(dcc.Graph(id='bar1_wind',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4}),
                dbc.Col(dcc.Graph(id='top20_1_wind',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4})
                   ])
           ]),
        dcc.Tab(label = 'Energy consumption from wind per capita', children = [
            dbc.Row([
            dbc.Col(dcc.Graph(id='line2_wind',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4}),
            dbc.Col(dcc.Graph(id='bar2_wind',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4}),
            dbc.Col(dcc.Graph(id='top20_2_wind',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4})
                   ])
          ]),

        dcc.Tab(label = 'Installed wind capacity', children = [
            dbc.Row([
            dbc.Col(dcc.Graph(id='line3_wind',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4}),
            dbc.Col(dcc.Graph(id='bar3_wind',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4}),
            dbc.Col(dcc.Graph(id='top20_3_wind',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4})
                   ])
          ]),
        ]),
       ]),
    html.Br(),
    dbc.Row([
        dbc.Col(html.H2('How is the generation of wind energy changing year to year?'),style={'textAlign':'center'}),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Label('Countries: '),
            dcc.Dropdown(id='countries_dropdown_change_wind',
                         placeholder = 'Select one or more countries',
                         value=['United States','Denmark'],
                         multi = True,
                         options=[{'label': country, 'value': country}
                                 for country in wind_energy_countries['Entity'].unique()]),
            ],width={'size': 8, "offset": 2}),
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='annual_change_pct_wind',figure=make_empty_fig(),style={'backgroundColor':'#E5ECF6'}),
        ],width=6,lg={'size':6}),
        dbc.Col([
            dcc.Graph(id='annual_change_twh_wind',figure=make_empty_fig(),style={'backgroundColor':'#E5ECF6'}),
        ],width=6,lg={'size':6}),
    ]),
    html.Br(),
     dbc.Tabs([
        dbc.Tab([
            html.Ul([
                html.Br(),
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


@app.callback(Output('line1_wind', 'figure'),
              Input('countries_dropdown_wind', 'value'))

def update_graph(country):
    dff = wind_energy_countries[wind_energy_countries.Entity.isin((country))]
    fig = px.line(data_frame=dff, x='Year', y='Wind (% equivalent primary energy)', color='Entity',
                  custom_data=['Entity', 'Code', 'Wind (% equivalent primary energy)'],
                  title=''.join(['Wind (% equivalent primary energy)', '<br><b>', ', '.join(country), '</b>']))
    fig.update_traces(mode='lines+markers')
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    fig.update_layout(hovermode="x")
    return fig


@app.callback(Output('bar1_wind', 'figure'),
              Input('countries_dropdown_wind', 'value'))

def plot_renewables_share_countries_barchart(countries):
    if not countries:
        raise PreventUpdate
    df = wind_energy_countries[wind_energy_countries['Entity'].isin(countries)]
    fig = px.bar(df,
                 x='Year',
                 y='Wind (% equivalent primary energy)',
                 height=100 + (250*len(countries)),
                 facet_row='Entity',
                 color='Entity',
                 labels={'Wind (% equivalent primary energy)': 'Wind share (%)'},
                 title=''.join(['Wind (% equivalent primary energy)', '<br><b>', ', '.join(countries), '</b>']))
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    return fig



@app.callback(Output('line2_wind', 'figure'),
              Input('countries_dropdown_wind', 'value'))

def update_graph(country):
    dff = wind_energy_countries[wind_energy_countries.Entity.isin((country))]
    fig = px.line(data_frame=dff, x='Year', y='Wind per capita (kWh - equivalent)', color='Entity',
                  custom_data=['Entity', 'Code', 'Wind per capita (kWh - equivalent)'],
                  title=''.join(['Wind per capita (kWh - equivalent)', '<br><b>', ', '.join(country), '</b>']))

    fig.update_traces(mode='lines+markers')
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    fig.update_layout(hovermode="x")
    return fig

@app.callback(Output('bar2_wind', 'figure'),
              Input('countries_dropdown_wind', 'value'))

def plot_renewables_share_countries_barchart(countries):
    if not countries:
        raise PreventUpdate
    df = wind_energy_countries[wind_energy_countries['Entity'].isin(countries)]
    fig = px.bar(df,
                 x='Year',
                 y='Wind per capita (kWh - equivalent)',
                 height=100 + (250*len(countries)),
                 facet_row='Entity',
                 color='Entity',
                 labels={'Wind per capita (kWh - equivalent)': 'Wind energy (KWh)'},
                 title=''.join(['Wind per capita (kWh - equivalent)', '<br><b>', ', '.join(countries), '</b>']))
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    return fig


@app.callback(Output('top20_1_wind', 'figure'),
              Input('year_dropdown_wind', 'value'))
# graph
def plot_countries_by_renewable_share(Year):
    #fig =go.Figure()
    year_df = wind_energy_countries.loc[wind_energy_countries['Year']==Year].sort_values(
    'Wind (% equivalent primary energy)',ascending = False)[:20]
    fig =px.bar(year_df,y='Entity',
                  x='Wind (% equivalent primary energy)',orientation = 'h')
    fig.layout.title = f'Top twenty countries by wind energy share (%) - {Year}'
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    return fig



@app.callback(Output('top20_2_wind', 'figure'),
              Input('year_dropdown_wind', 'value'))
# graph
def plot_countries_by_renewable_share(Year):
    #fig =go.Figure()
    year_df = wind_energy_countries.loc[wind_energy_countries['Year']==Year].sort_values(
    'Wind per capita (kWh - equivalent)',ascending = False)[:20]
    fig = px.bar(year_df,y='Entity',
                  x='Wind per capita (kWh - equivalent)',orientation = 'h')
    fig.layout.title = f'Top twenty countries by wind energy per capita (KWh) - {Year}'
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    return fig





@app.callback(Output('line3_wind', 'figure'),
              Input('countries_dropdown_wind', 'value'))

def update_graph(country):
    dff = wind_energy_countries[wind_energy_countries.Entity.isin((country))]
    fig = px.line(data_frame=dff, x='Year', y='Installed wind capacity (GW)', color='Entity',
                  custom_data=['Entity', 'Code', 'Installed wind capacity (GW)'],
                  title=''.join(['Installed wind capacity (GW)', '<br><b>', ', '.join(country), '</b>']))
    fig.update_traces(mode='lines+markers')
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    fig.update_layout(hovermode="x")
    return fig




@app.callback(Output('bar3_wind', 'figure'),
              Input('countries_dropdown_wind', 'value'))

def plot_renewables_share_countries_barchart(countries):
    if not countries:
        raise PreventUpdate
    df = wind_energy_countries[wind_energy_countries['Entity'].isin(countries)]
    fig = px.bar(df,
                 x='Year',
                 y='Installed wind capacity (GW)',
                 height=100 + (250*len(countries)),
                 facet_row='Entity',
                 color='Entity',
                 labels={'Installed wind capacity (GW)': 'Wind capacity (GW)'},
                 title=''.join(['Installed wind capacity (GW)', '<br><b>', ', '.join(countries), '</b>']))
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    return fig



@app.callback(Output('top20_3_wind', 'figure'),
              Input('year_dropdown_wind', 'value'))
# graph
def plot_countries_by_renewable_share(Year):
    #fig =go.Figure()
    year_df = wind_energy_countries.loc[wind_energy_countries['Year']==Year].sort_values(
    'Installed wind capacity (GW)',ascending = False)[:20]
    fig = px.bar(year_df,y='Entity',
                  x='Installed wind capacity (GW)',orientation ='h')
    fig.layout.title = f'Top twenty countries by installed wind capacity (GW) - {Year}'
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    return fig



@app.callback(Output('annual_change_pct_wind', 'figure'),
              Input('countries_dropdown_change_wind', 'value'))

def update_graph(country):
    dff = wind_energy_countries[wind_energy_countries.Entity.isin((country))]
    fig = px.line(data_frame=dff, x='Year', y='Wind (% growth)', color='Entity',
                  custom_data=['Entity', 'Code', 'Wind (% growth)'],
                  title=''.join(['Wind (% growth)', '<br><b>', ', '.join(country), '</b>']))

    fig.update_traces(mode='lines+markers')
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    fig.update_layout(hovermode="x")
    return fig


@app.callback(Output('annual_change_twh_wind', 'figure'),
              Input('countries_dropdown_change_wind', 'value'))

def update_graph(country):
    dff = wind_energy_countries[wind_energy_countries.Entity.isin((country))]
    fig = px.line(data_frame=dff, x='Year', y='Wind (TWh growth - equivalent)', color='Entity',
                  custom_data=['Entity', 'Code', 'Wind (TWh growth - equivalent)'],
                  title=''.join(['Wind (TWh growth)', '<br><b>', ', '.join(country), '</b>']))

    fig.update_traces(mode='lines+markers')
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    fig.update_layout(hovermode="x")
    return fig


