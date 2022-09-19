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

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

energy_share = pd.read_csv(DATA_PATH.joinpath("renewable-share-energy.csv"))
renewable_per_capita = pd.read_csv(DATA_PATH.joinpath('per-capita-renewables.csv'))
renewable_consumption = pd.read_csv(DATA_PATH.joinpath('modern-renewable-energy-consumption.csv'))
annual_change_pct = pd.read_csv(DATA_PATH.joinpath('annual-percentage-change-renewables.csv'))
annual_change_twh = pd.read_csv(DATA_PATH.joinpath('annual-change-renewables.csv'))
electricity_share = pd.read_csv(DATA_PATH.joinpath('share-electricity-renewables.csv'))

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
energy = functools.reduce(functools.partial(pd.merge, on=['Entity','Code','Year']),
                 [energy_share,electricity_share,renewable_per_capita,renewable_consumption,annual_change_pct,
                  annual_change_twh])

energy_countries = energy[~energy['Entity'].isin(regions)]


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
            html.H1('Renewable Energy Statistics'),style ={'textAlign': 'center'}
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
            dcc.Dropdown(id='countries_dropdown_test',
                         placeholder = 'Select one or more countries',
                         value=['United States','Iceland'],
                         multi = True,
                         options=[{'label': country, 'value': country}
                                 for country in energy_countries['Entity'].unique()]),
            ],width={'size': 8, "offset": 0}),
        dbc.Col([
            dbc.Label('Year: '),
            dcc.Dropdown(id='year_dropdown_test',
                         value = 2021,
                         options = [{'label':Year,'value':Year}
                                    for Year in energy_countries['Year'].unique()],
            )
        ],width={'size':4,'offset':0})
    ]),
    html.Br(),
    dbc.Row([
         dbc.Tabs([
        dcc.Tab(label = 'Share of primary energy from renewables', children = [
            dbc.Row([
                dbc.Col(dcc.Graph(id='line1',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4}),
                dbc.Col(dcc.Graph(id='bar1',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4}),
                dbc.Col(dcc.Graph(id='top20_1',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4})
                   ])
           ]),
        dcc.Tab(label = 'Renewable energy per capita', children = [
            dbc.Row([
            dbc.Col(dcc.Graph(id='line2',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4}),
            dbc.Col(dcc.Graph(id='bar2',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4}),
            dbc.Col(dcc.Graph(id='top20_2',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4})
                   ])
          ]),
        ]),
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col(html.H2('How is the generation of renewable energy changing year to year?'),style={'textAlign':'center'}),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Label('Countries: '),
            dcc.Dropdown(id='countries_dropdown_change_home',
                         placeholder = 'Select one or more countries',
                         value=['United States','Iceland'],
                         multi = True,
                         options=[{'label': country, 'value': country}
                                 for country in energy_countries['Entity'].unique()]),
            ],width={'size': 8, "offset": 2}),
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='annual_change_pct_home',figure=make_empty_fig(),style={'backgroundColor':'#E5ECF6'}),
        ],width=6,lg={'size':6}),
        dbc.Col([
            dcc.Graph(id='annual_change_twh_home',figure=make_empty_fig(),style={'backgroundColor':'#E5ECF6'}),
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

@app.callback(Output('line1', 'figure'),
              Input('countries_dropdown_test', 'value'))

def update_graph(country):
    dff = energy_countries[energy_countries.Entity.isin((country))]
    fig = px.line(data_frame=dff, x='Year', y='Renewables (% equivalent primary energy)', color='Entity',
                  custom_data=['Entity', 'Code', 'Renewables (% equivalent primary energy)'],
                  labels={'Renewables (% equivalent primary energy)': 'Renewables (% primary energy)'},
                  title=''.join(['Renewables (% equivalent primary energy)', '<br><b>', ', '.join(country), '</b>']))
    fig.update_traces(mode='lines+markers')
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    fig.update_layout(hovermode="x")
    return fig


@app.callback(Output('line2', 'figure'),
              Input('countries_dropdown_test', 'value'))

def update_graph(country):
    dff = energy_countries[energy_countries.Entity.isin((country))]
    fig = px.line(data_frame=dff, x='Year', y='Renewables per capita (kWh - equivalent)', color='Entity',
                  custom_data=['Entity', 'Code', 'Renewables per capita (kWh - equivalent)'],
                  labels={'Renewables per capita (kWh - equivalent)': 'Renewables per capita (kWh)'},
                  title=''.join(['Renewables per capita (kWh - equivalent)', '<br><b>', ', '.join(country), '</b>']))

    fig.update_traces(mode='lines+markers')
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    fig.update_layout(hovermode="x")
    return fig

@app.callback(Output('bar1', 'figure'),
              Input('countries_dropdown_test', 'value'))

def plot_renewables_share_countries_barchart(country):
    if not country:
        raise PreventUpdate
    df = energy_countries[energy_countries['Entity'].isin(country)]
    fig = px.bar(df,
                 x='Year',
                 y='Renewables (% equivalent primary energy)',
                 height=100 + (250*len(country)),
                 facet_row='Entity',
                 color='Entity',
                 labels={'Renewables (% equivalent primary energy)': 'Energy share(%)'},
                 title=''.join(['Renewables (% equivalent primary energy)', '<br><b>', ', '.join(country), '</b>']))
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    return fig


@app.callback(Output('bar2', 'figure'),
              Input('countries_dropdown_test', 'value'))

def plot_renewables_share_countries_barchart(country):
    if not country:
        raise PreventUpdate
    df = energy_countries[energy_countries['Entity'].isin(country)]
    fig = px.bar(df,
                 x='Year',
                 y='Renewables per capita (kWh - equivalent)',
                 height=100 + (250*len(country)),
                 facet_row='Entity',
                 color='Entity',
                 labels={'Renewables per capita (kWh - equivalent)': 'Energy (KWh)'},
                 title=''.join(['Renewables per capita (kWh - equivalent)', '<br><b>', ', '.join(country), '</b>']))
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    return fig

@app.callback(Output('top20_1', 'figure'),
              Input('year_dropdown_test', 'value'))
# graph
def plot_countries_by_renewable_share(Year):
    #fig =go.Figure()
    year_df = energy_countries.loc[energy_countries['Year']==Year].sort_values(
    'Renewables (% equivalent primary energy)',ascending = False)[:20]
    fig = px.bar(year_df, y='Entity',
                  x='Renewables (% equivalent primary energy)',orientation='h')
    fig.layout.title = f'Top twenty countries by renewable energy share (%) - {Year}'
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    #fig.layout.template = 'plotly_dark'
    return fig


@app.callback(Output('top20_2', 'figure'),
              Input('year_dropdown_test', 'value'))
# graph
def plot_countries_by_renewable_share(Year):
    #fig =go.Figure()
    year_df = energy_countries.loc[energy_countries['Year']==Year].sort_values(
    'Renewables per capita (kWh - equivalent)',ascending = False)[:20]
    fig = px.bar(year_df, y='Entity',
                  x='Renewables per capita (kWh - equivalent)',orientation = 'h')
    fig.layout.title = f'Top twenty countries renewables energy per capita (KWh) - {Year}'
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    #fig.layout.template = 'plotly_dark'
    return fig


@app.callback(Output('annual_change_pct_home', 'figure'),
              Input('countries_dropdown_change_home', 'value'))

def update_graph(country):
    dff = energy_countries[energy_countries.Entity.isin((country))]
    fig = px.line(data_frame=dff, x='Year', y='Renewables (% growth)', color='Entity',
                  custom_data=['Entity', 'Code', 'Renewables (% growth)'],
                  title=''.join(['Renewables (% growth)', '<br><b>', ', '.join(country), '</b>']))

    fig.update_traces(mode='lines+markers')
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=12)
    fig.update_layout(hovermode="x")
    return fig


@app.callback(Output('annual_change_twh_home', 'figure'),
              Input('countries_dropdown_change_home', 'value'))

def update_graph(country):
    dff = energy_countries[energy_countries.Entity.isin((country))]
    fig = px.line(data_frame=dff, x='Year', y='Renewables (TWh growth - equivalent)', color='Entity',
                  custom_data=['Entity', 'Code', 'Renewables (TWh growth - equivalent)'],
                  title=''.join(['Renewables (TWh growth)', '<br><b>', ', '.join(country), '</b>']))

    fig.update_traces(mode='lines+markers')
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    fig.update_layout(hovermode="x")
    return fig
