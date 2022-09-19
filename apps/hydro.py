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


PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

hydro_energy_share = pd.read_csv(DATA_PATH.joinpath("hydro-share-energy.csv"))
per_capita_hydro = pd.read_csv(DATA_PATH.joinpath('per-capita-hydro.csv'))
hydropower_consumption = pd.read_csv(DATA_PATH.joinpath("hydropower-consumption.csv"))
annual_change_hydro_pct = pd.read_csv(DATA_PATH.joinpath('annual-percentage-change-hydro.csv'))
hydro_electricity_share = pd.read_csv(DATA_PATH.joinpath("share-electricity-hydro.csv"))





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
hydro_energy = functools.reduce(functools.partial(pd.merge, on=['Entity','Code','Year']),
                 [hydro_energy_share,hydro_electricity_share,per_capita_hydro,hydropower_consumption,annual_change_hydro_pct
                  ])

hydro_countries = hydro_energy[~hydro_energy['Entity'].isin(regions)]


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
            html.H1('Hydropower'),style ={'textAlign': 'center'}
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
       # ),

   # ]),
    dbc.Row([
        dbc.Col([
            dbc.Label('Countries: '),
            dcc.Dropdown(id='countries_dropdown_hydro',
                         placeholder = 'Select one or more countries',
                         value=['United States','Iceland'],
                         multi = True,
                         options=[{'label': country, 'value': country}
                                 for country in hydro_countries['Entity'].unique()]),
            ],width={'size': 8, "offset": 0}),
        dbc.Col([
            dbc.Label('Year: '),
            dcc.Dropdown(id='year_dropdown_hydro',
                         value = 2021,
                         options = [{'label':Year,'value':Year}
                                    for Year in hydro_countries['Year'].unique()],
            )
        ],width={'size':4,'offset':0})
    ]),
    html.Br(),
    dbc.Row([
         dbc.Tabs([
        dcc.Tab(label = 'Share of primary energy from hydropower', value ='hydro share', children = [
            dbc.Row([
                dbc.Col(dcc.Graph(id='line1_hydro',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4}),
                dbc.Col(dcc.Graph(id='bar1_hydro',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4}),
                dbc.Col(dcc.Graph(id='top20_1_hydro',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4})
                   ])
           ]),
        dcc.Tab(label = 'Energy consumption from hydropower per capita', children = [
            dbc.Row([
            dbc.Col(dcc.Graph(id='line2_hydro',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4}),
            dbc.Col(dcc.Graph(id='bar2_hydro',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4}),
            dbc.Col(dcc.Graph(id='top20_2_hydro',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4})
                   ])
          ]),
        ]),
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col(html.H2('How is the generation of hydropower changing year to year?'),style={'textAlign':'center'}),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Label('Countries: '),
            dcc.Dropdown(id='countries_dropdown_change_hydro',
                         placeholder = 'Select one or more countries',
                         value=['United States','Iceland'],
                         multi = True,
                         options=[{'label': country, 'value': country}
                                 for country in hydro_countries['Entity'].unique()]),
            ],width={'size': 8, "offset": 2}),
    ]),
    html.Br(),
   dbc.Row([
        dbc.Col([
            dcc.Graph(id='annual_change_pct_hydro',figure=make_empty_fig(),style={'backgroundColor':'#E5ECF6'}),
        ],width=8,lg={'size':8,'offset':2}),
        #dbc.Col([
            #dcc.Graph(id='annual_change_twh_home',figure=make_empty_fig(),style={'backgroundColor':'#E5ECF6'}),
       # ],width=6,lg={'size':6}),
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

@app.callback(Output('line1_hydro', 'figure'),
              Input('countries_dropdown_hydro', 'value'))

def update_graph(country):
    dff = hydro_countries[hydro_countries.Entity.isin((country))]
    fig = px.line(data_frame=dff, x='Year', y='Hydro (% equivalent primary energy)', color='Entity',
                  custom_data=['Entity', 'Code', 'Hydro (% equivalent primary energy)'],
                  title=''.join(['Hydro (% equivalent primary energy)', '<br><b>', ', '.join(country), '</b>']))
    fig.update_traces(mode='lines+markers')
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    fig.update_layout(hovermode="x")
    return fig

@app.callback(Output('line2_hydro', 'figure'),
              Input('countries_dropdown_hydro', 'value'))


def update_graph(country):
    dff = hydro_countries[hydro_countries.Entity.isin((country))]
    fig = px.line(data_frame=dff, x='Year', y='Hydro per capita (kWh - equivalent)', color='Entity',
                  custom_data=['Entity', 'Code', 'Hydro per capita (kWh - equivalent)'],
                  title=''.join(['Hydro per capita (kWh - equivalent)', '<br><b>', ', '.join(country), '</b>']))

    fig.update_traces(mode='lines+markers')
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    fig.update_layout(hovermode="x")
    return fig



@app.callback(Output('bar1_hydro', 'figure'),
              Input('countries_dropdown_hydro', 'value'))

def plot_renewables_share_countries_barchart(countries):
    if not countries:
        raise PreventUpdate
    df = hydro_countries[hydro_countries['Entity'].isin(countries)]
    fig = px.bar(df,
                 x='Year',
                 y='Hydro (% equivalent primary energy)',
                 height=100 + (250*len(countries)),
                 facet_row='Entity',
                 color='Entity',
                 labels={'Hydro (% equivalent primary energy)': 'hydropower share(%)'},
                 title=''.join(['Hydro (% equivalent primary energy)', '<br><b>', ', '.join(countries), '</b>']))
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    return fig

@app.callback(Output('bar2_hydro', 'figure'),
              Input('countries_dropdown_hydro', 'value'))

def plot_renewables_share_countries_barchart(countries):
    if not countries:
        raise PreventUpdate
    df = hydro_countries[hydro_countries['Entity'].isin(countries)]
    fig = px.bar(df,
                 x='Year',
                 y='Hydro per capita (kWh - equivalent)',
                 height=100 + (250*len(countries)),
                 facet_row='Entity',
                 color='Entity',
                 labels={'Hydro per capita (kWh - equivalent)': 'Hydropower (KWh)'},
                 title=''.join(['Hydro per capita (kWh - equivalent)', '<br><b>', ', '.join(countries), '</b>']))
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    return fig



@app.callback(Output('top20_1_hydro', 'figure'),
              Input('year_dropdown_hydro', 'value'))
# graph
def plot_countries_by_renewable_share(Year):
    #fig =go.Figure()
    year_df = hydro_countries.loc[hydro_countries['Year']==Year].sort_values(
    'Hydro (% equivalent primary energy)',ascending = False)[:20]
    fig = px.bar(year_df, y='Entity',
                  x='Hydro (% equivalent primary energy)',orientation ='h')
    fig.layout.title = f'Top twenty countries by hydro energy share (%) - {Year}'
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    return fig




@app.callback(Output('top20_2_hydro', 'figure'),
              Input('year_dropdown_hydro', 'value'))
# graph
def plot_countries_by_renewable_share(Year):
    #fig =go.Figure()
    year_df = hydro_countries.loc[hydro_countries['Year']==Year].sort_values(
    'Hydro per capita (kWh - equivalent)',ascending = False)[:20]
    fig= px.bar(year_df, y='Entity',
                  x='Hydro per capita (kWh - equivalent)', orientation='h')
    fig.layout.title = f'Top twenty countries by hydropower generation per capita (KWh) - {Year}'
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    return fig




@app.callback(Output('annual_change_pct_hydro', 'figure'),
              Input('countries_dropdown_change_hydro', 'value'))

def update_graph(country):
    dff = hydro_countries[hydro_countries.Entity.isin((country))]
    fig = px.line(data_frame=dff, x='Year', y='Hydro (% growth)', color='Entity',
                  custom_data=['Entity', 'Code', 'Hydro (% growth)'],
                  title=''.join(['Wind (% growth)', '<br><b>', ', '.join(country), '</b>']))

    fig.update_traces(mode='lines+markers')
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    fig.update_layout(hovermode="x")
    return fig




