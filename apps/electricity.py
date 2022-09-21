
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

rene_electricity= pd.read_csv(DATA_PATH.joinpath("modern-renewable-energy-consumption.csv"))
elec_energy_share = pd.read_csv(DATA_PATH.joinpath('share-electricity-renewables.csv'))
elec_hydro_share = pd.read_csv(DATA_PATH.joinpath("share-electricity-hydro.csv"))
elec_wind_share = pd.read_csv(DATA_PATH.joinpath("share-electricity-wind.csv"))
elec_solar_share = pd.read_csv(DATA_PATH.joinpath("share-electricity-solar.csv"))

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
elec = functools.reduce(functools.partial(pd.merge, on=['Entity','Code','Year']),[rene_electricity,
                                                                                  elec_energy_share,elec_hydro_share,
                                                                                  elec_wind_share,elec_solar_share])
elec_countries = elec[~elec['Entity'].isin(regions)]

elec_countries['Geo Biomass Other (% electricity)'] = elec_countries['Renewables (% electricity)'] * elec_countries['Geo Biomass Other - TWh']/(elec_countries['Wind Generation - TWh']+elec_countries['Solar Generation - TWh']+elec_countries['Hydro Generation - TWh']+elec_countries['Geo Biomass Other - TWh'])


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
            html.H1('Electricity from renewable energy'),style ={'textAlign': 'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.H2('Our world in Data'), style ={'textAlign': 'center'}
        ),
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col(
            html.H2('Breakdown of renewables in Electricity'),style ={'textAlign': 'center'}
        ),

    ]),
    dbc.Row([
        dbc.Col([
            dbc.Label('Countrie: '),
            dcc.Dropdown(id='countries_dropdown_elec1',
                         placeholder = 'Select one or more countries',
                         value='United States',
                         multi = False,
                         options=[{'label': country, 'value': country}
                                 for country in elec_countries['Entity'].unique()]),
            ],width={'size': 8, "offset": 2}),
    ]),
    html.Br(),
    dbc.Row([
         dbc.Col([
             dcc.Graph(id='line_chart_elec',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),
         ],width=6, lg={'size': 6}),
         dbc.Col([
             dcc.Graph(id='line_chart_elec1',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),
                 ],width=6, lg={'size': 6}),
           ]),
    html.Br(),
    dbc.Row([
        dbc.Col(
            html.H2('How much of our electricity comes from renewable sources?'),style ={'textAlign': 'center'}
        ),

    ]),
    dbc.Row([
        dbc.Col([
            dbc.Label('Countries: '),
            dcc.Dropdown(id='countries_dropdown_elec',
                         placeholder = 'Select one or more countries',
                         value=['United States','Iceland'],
                         multi = True,
                         options=[{'label': country, 'value': country}
                                 for country in elec_countries['Entity'].unique()]),
            ],width={'size': 8, "offset": 0}),
        dbc.Col([
            dbc.Label('Year: '),
            dcc.Dropdown(id='year_dropdown_elec',
                         value = 2021,
                         options = [{'label':Year,'value':Year}
                                    for Year in elec_countries['Year'].unique()],
            )
        ],width={'size':4,'offset':0})
    ]),
    html.Br(),
    dbc.Row([
         dbc.Tabs([
        dcc.Tab(label = 'Electricity from Renewables', children = [
            dbc.Row([
                dbc.Col(dcc.Graph(id='line_elec_ene',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4}),
                dbc.Col(dcc.Graph(id='bar_elec_ene',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4}),
                dbc.Col(dcc.Graph(id='top20_elec_ene',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4})
                   ])
           ]),
        dcc.Tab(label = 'Electricity from Hydro', children = [
            dbc.Row([
            dbc.Col(dcc.Graph(id='line_elec_hydro',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4}),
            dbc.Col(dcc.Graph(id='bar_elec_hydro',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4}),
            dbc.Col(dcc.Graph(id='top20_elec_hydro',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4})
                   ])
          ]),
        dcc.Tab(label = 'Electricity from Wind', children = [
            dbc.Row([
            dbc.Col(dcc.Graph(id='line_elec_wind',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4}),
            dbc.Col(dcc.Graph(id='bar_elec_wind',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4}),
            dbc.Col(dcc.Graph(id='top20_elec_wind',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4})
                   ])
          ]),
        dcc.Tab(label = 'Electricity from Solar', children = [
            dbc.Row([
            dbc.Col(dcc.Graph(id='line_elec_solar',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4}),
            dbc.Col(dcc.Graph(id='bar_elec_solar',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4}),
            dbc.Col(dcc.Graph(id='top20_elec_solar',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4})
                   ])
          ]),
         dcc.Tab(label = 'Electricity from Geo Biomass Other', children = [
            dbc.Row([
            dbc.Col(dcc.Graph(id='line_elec_geo',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4}),
            dbc.Col(dcc.Graph(id='bar_elec_geo',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4}),
            dbc.Col(dcc.Graph(id='top20_elec_geo',figure=make_empty_fig(),style={'backgroundColor': '#E5ECF6'}),width=4, lg= {'size': 4})
                   ])
          ]),
        ]),
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


]),


@app.callback(Output('line_chart_elec', 'figure'),
              Input('countries_dropdown_elec1', 'value'))

def update_graph(country):
    dff = elec_countries[elec_countries['Entity'] == country]
    fig = px.line(data_frame=dff, x='Year', y=['Wind Generation - TWh', 'Solar Generation - TWh', 'Geo Biomass Other - TWh','Hydro Generation - TWh'],
                  custom_data=['Entity', 'Code'],
                  title=f'Breakdown of renewables in Electricity (TWh) <br><b> {country}')
    fig.update_traces(mode='lines+markers')
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    fig.update_layout(hovermode="x")
    return fig

@app.callback(Output('line_chart_elec1', 'figure'),
              Input('countries_dropdown_elec1', 'value'))

def update_graph(country):
    dff = elec_countries[elec_countries['Entity'] == country]
    fig = px.line(data_frame=dff, x='Year', y=[ 'Hydro (% electricity)', 'Wind (% electricity)',
       'Solar (% electricity)', 'Geo Biomass Other (% electricity)'],
                  custom_data=['Entity', 'Code'],
                  title=f'Breakdown of renewables in Electricity (%) <br><b> {country}')
    fig.update_traces(mode='lines+markers')
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    fig.update_layout(hovermode="x")
    return fig



@app.callback(Output('line_elec_ene', 'figure'),
              Input('countries_dropdown_elec', 'value'))

def update_graph(country):
    dff = elec_countries[elec_countries['Entity'].isin(country)]
    fig = px.line(data_frame=dff, x='Year', y='Renewables (% electricity)',
                  color='Entity',
                  custom_data=['Entity', 'Code', 'Renewables (% electricity)'],
                  title=''.join(['Renewables (% electricity)', '<br><b>', ', '.join(country), '</b>']))
    fig.update_traces(mode='lines+markers')
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    fig.update_layout(hovermode="x")
    return fig

@app.callback(Output('bar_elec_ene', 'figure'),
              Input('countries_dropdown_elec', 'value'))

def plot_renewables_share_countries_barchart(country):
    if not country:
        raise PreventUpdate
    df = elec_countries[elec_countries['Entity'].isin(country)]
    fig = px.bar(df,
                 x='Year',
                 y='Renewables (% electricity)',
                 height=100 + (250*len(country)),
                 facet_row='Entity',
                 color='Entity',
                 labels={'Renewables (% electricity)': 'Renewables (% electricity)'},
                 title=''.join(['Renewables (% electricity)', '<br><b>', ', '.join(country), '</b>']))
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    return fig


@app.callback(Output('top20_elec_ene', 'figure'),
              Input('year_dropdown_elec', 'value'))
# graph
def plot_countries_by_renewable_share(Year):
    #fig =go.Figure()
    year_df = elec_countries.loc[elec_countries['Year']==Year].sort_values(
    'Renewables (% electricity)',ascending = False)[:20]
    fig = px.bar(year_df, y='Entity',
                  x='Renewables (% electricity)',orientation = 'h')
    fig.layout.title = f'Top twenty countries by Renewables (% electricity) - {Year}'
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    return fig

@app.callback(Output('line_elec_hydro', 'figure'),
              Input('countries_dropdown_elec', 'value'))

def update_graph(country):
    dff = elec_countries[elec_countries['Entity'].isin(country)]
    fig = px.line(data_frame=dff, x='Year', y='Hydro (% electricity)',
                  color='Entity',
                  custom_data=['Entity', 'Code', 'Hydro (% electricity)'],
                  title=''.join(['Hydro (% electricity)', '<br><b>', ', '.join(country), '</b>']))
    fig.update_traces(mode='lines+markers')
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    fig.update_layout(hovermode="x")
    return fig

@app.callback(Output('bar_elec_hydro', 'figure'),
              Input('countries_dropdown_elec', 'value'))

def plot_renewables_share_countries_barchart(country):
    if not country:
        raise PreventUpdate
    df = elec_countries[elec_countries['Entity'].isin(country)]
    fig = px.bar(df,
                 x='Year',
                 y='Hydro (% electricity)',
                 height=100 + (250*len(country)),
                 facet_row='Entity',
                 color='Entity',
                 labels={'Hydro (% electricity)': 'Hydro (% electricity)'},
                 title=''.join(['Hydro (% electricity)', '<br><b>', ', '.join(country), '</b>']))
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    return fig


@app.callback(Output('top20_elec_hydro', 'figure'),
              Input('year_dropdown_elec', 'value'))
# graph
def plot_countries_by_renewable_share(Year):
    #fig =go.Figure()
    year_df = elec_countries.loc[elec_countries['Year']==Year].sort_values(
    'Hydro (% electricity)',ascending = False)[:20]
    fig = px.bar(year_df, y='Entity',
                  x='Hydro (% electricity)',orientation ='h')
    fig.layout.title = f'Top twenty countries by Hydro (% electricity) - {Year}'
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    return fig

@app.callback(Output('line_elec_wind', 'figure'),
              Input('countries_dropdown_elec', 'value'))

def update_graph(country):
    dff = elec_countries[elec_countries['Entity'].isin(country)]
    fig = px.line(data_frame=dff, x='Year', y='Wind (% electricity)',
                  color='Entity',
                  custom_data=['Entity', 'Code', 'Wind (% electricity)'],
                  title=''.join(['Wind (% electricity)', '<br><b>', ', '.join(country), '</b>']))
    fig.update_traces(mode='lines+markers')
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    fig.update_layout(hovermode="x")
    return fig

@app.callback(Output('bar_elec_wind', 'figure'),
              Input('countries_dropdown_elec', 'value'))

def plot_renewables_share_countries_barchart(country):
    if not country:
        raise PreventUpdate
    df = elec_countries[elec_countries['Entity'].isin(country)]
    fig = px.bar(df,
                 x='Year',
                 y='Wind (% electricity)',
                 height=100 + (250*len(country)),
                 facet_row='Entity',
                 color='Entity',
                 labels={'Wind (% electricity)': 'Wind (% electricity)'},
                 title=''.join(['Wind (% electricity)', '<br><b>', ', '.join(country), '</b>']))
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    return fig


@app.callback(Output('top20_elec_wind', 'figure'),
              Input('year_dropdown_elec', 'value'))
# graph
def plot_countries_by_renewable_share(Year):
    #fig =go.Figure()
    year_df = elec_countries.loc[elec_countries['Year']==Year].sort_values(
    'Wind (% electricity)',ascending = False)[:20]
    fig = px.bar(year_df,y='Entity',
                  x='Wind (% electricity)',orientation ='h')
    fig.layout.title = f'Top twenty countries by Wind (% electricity) - {Year}'
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    return fig

@app.callback(Output('line_elec_solar', 'figure'),
              Input('countries_dropdown_elec', 'value'))

def update_graph(country):
    dff = elec_countries[elec_countries['Entity'].isin(country)]
    fig = px.line(data_frame=dff, x='Year', y='Solar (% electricity)',
                  color='Entity',
                  custom_data=['Entity', 'Code', 'Solar (% electricity)'],
                  title=''.join(['Solar (% electricity)', '<br><b>', ', '.join(country), '</b>']))
    fig.update_traces(mode='lines+markers')
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    fig.update_layout(hovermode="x")
    return fig

@app.callback(Output('bar_elec_solar', 'figure'),
              Input('countries_dropdown_elec', 'value'))

def plot_renewables_share_countries_barchart(country):
    if not country:
        raise PreventUpdate
    df = elec_countries[elec_countries['Entity'].isin(country)]
    fig = px.bar(df,
                 x='Year',
                 y='Solar (% electricity)',
                 height=100 + (250*len(country)),
                 facet_row='Entity',
                 color='Entity',
                 labels={'Solar (% electricity)': 'Solar (% electricity)'},
                 title=''.join(['Wind (% electricity)', '<br><b>', ', '.join(country), '</b>']))
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    return fig


@app.callback(Output('top20_elec_solar', 'figure'),
              Input('year_dropdown_elec', 'value'))
# graph
def plot_countries_by_renewable_share(Year):
    #fig =go.Figure()
    year_df = elec_countries.loc[elec_countries['Year']==Year].sort_values(
    'Solar (% electricity)',ascending = False)[:20]
    fig = px.bar(year_df,y='Entity',
                  x='Solar (% electricity)',orientation ='h')
    fig.layout.title = f'Top twenty countries by Solar (% electricity) - {Year}'
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    return fig

@app.callback(Output('line_elec_geo', 'figure'),
              Input('countries_dropdown_elec', 'value'))

def update_graph(country):
    dff = elec_countries[elec_countries['Entity'].isin(country)]
    fig = px.line(data_frame=dff, x='Year', y='Geo Biomass Other (% electricity)',
                  color='Entity',
                  custom_data=['Entity', 'Code', 'Geo Biomass Other (% electricity)'],
                  title=''.join(['Geo Biomass Other (% electricity)', '<br><b>', ', '.join(country), '</b>']))
    fig.update_traces(mode='lines+markers')
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    fig.update_layout(hovermode="x")
    return fig

@app.callback(Output('bar_elec_geo', 'figure'),
              Input('countries_dropdown_elec', 'value'))

def plot_renewables_share_countries_barchart(country):
    if not country:
        raise PreventUpdate
    df = elec_countries[elec_countries['Entity'].isin(country)]
    fig = px.bar(df,
                 x='Year',
                 y='Geo Biomass Other (% electricity)',
                 height=100 + (250*len(country)),
                 facet_row='Entity',
                 color='Entity',
                 labels={'Geo Biomass Other (% electricity)': 'Geo Bio (% electricity)'},
                 title=''.join(['Geo Biomass Other (% electricity)', '<br><b>', ', '.join(country), '</b>']))
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    return fig


@app.callback(Output('top20_elec_geo', 'figure'),
              Input('year_dropdown_elec', 'value'))
# graph
def plot_countries_by_renewable_share(Year):
    #fig =go.Figure()
    year_df = elec_countries.loc[elec_countries['Year']==Year].sort_values(
    'Geo Biomass Other (% electricity)',ascending = False)[:20]
    fig =px.bar(year_df,y='Entity',
                  x='Geo Biomass Other (% electricity)',orientation ='h')
    fig.layout.title = f'Top twenty countries by Geo Biomass (% electricity) - {Year}'
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig['layout']['title']['font'] = dict(size=14)
    return fig
