import numpy as np
import pandas as pd
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import dash_table.FormatTemplate as FormatTemplate
from dash_table.Format import Symbol
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from .html_layout import html_layout
import datetime

df = pd.read_csv("https://opendata.ecdc.europa.eu/covid19/casedistribution/csv")

def convert_to_time(x):
    return datetime.datetime.strptime(x,'%d/%m/%Y')

df["date"] = df.apply(lambda x: convert_to_time(x['dateRep']), axis = 1)
df.rename(columns = {'cases':'new_cases','countriesAndTerritories':'location','continentExp':'continent','popData2018':'population'},inplace = True)
df.sort_values(by = ['location', 'date'], inplace = True)

world_df = df.groupby(['date'])[['new_cases','deaths']].sum()
world_df['location'] = 'the World'
world_df.reset_index(inplace=True)

frames = [df, world_df]
df = pd.concat(frames, sort=True)

df['total_cases'] = df.groupby(['location'])['new_cases'].apply(lambda x: x.cumsum())
df['total_deaths'] = df.groupby(['location'])['deaths'].apply(lambda x: x.cumsum())

df_table = df[df['date']==df['date'].max()]
df_table = df_table[['location','total_cases','total_deaths','population']]

population_total = df_table['population'].sum()

df_table.loc[df_table['location'] == 'the World', ['population']] = population_total

df_table['% total cases to population']=df_table.apply(lambda x: round(float(x['total_cases'])/x['population'],8), axis=1)
df_table['% total deaths to total cases']=df_table.apply(lambda x: round(float(x['total_deaths'])/x['total_cases'],8), axis=1)
df_table['total_cases'] = df_table['total_cases']
df_table['total_deaths'] = df_table['total_deaths']
df_table['population'] = df_table['population']

df_table['location'] = df_table['location'].apply(lambda x: x.replace("Holy_See","Vatican City"))
df_table['location'] = df_table['location'].replace("_"," ", regex=True)

df_table['Rank (total cases %)'] = df_table['% total cases to population'].rank(method='first',ascending=False)
df_table['Rank (death rate %)'] = df_table['% total deaths to total cases'].rank(method='first',ascending=False)



df_max_date = (df['date'].max()).strftime('%d %B %Y')

moving_average = ((pd.DataFrame(df.groupby(['location']).rolling(30,min_periods=1)['new_cases'].mean())).reset_index()).set_index('level_1')
moving_average.index.name=None
moving_average.rename(columns={'location':'location2','new_cases':'moving_average'}, inplace=True)
#moving_average.fillna(1)


df = pd.concat([df, moving_average], axis=1)

def create_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(server=server,
                         routes_pathname_prefix='/projects/covid-19-dashboards/',
                         external_stylesheets=['/static/css/custom_dash.css','/static/css/custom.css','/static/css/bootstrap.min.css']
                         )

    dash_app.index_string = html_layout

    colors = {
    'background': '#111111',
    'text': '#111111'
    }

    #today = datetime.datetime.now().strftime('%d %B')

    #markdown_text = '''

    #Update

    #'''

    dash_app.layout = html.Div([

            dcc.Tabs(
                        id="tabs-with-classes",
                        #value='tab-2',
                        parent_className='custom-tabs',
                        className='custom-tabs-container',
                        children =
                        [

            dcc.Tab(label='COVID-19 visualisation by country',
                    #value='tab-1',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    children = [

            html.Div(id='dash-container',

            children=[

           # html.H2(children='''
           # COVID-19 visualisation by country''',
           # style={'textAlign': 'center'}),


            dcc.Markdown('Updated {}'.format(df_max_date),
                style = {'textAlign':'center', 'font-weight':'bold', 'font-family':'system-ui','font-size':'16', 'margin-top':'10px'}),

            html.Div(id='covid-dropdown',
            children = [

            html.Div([dcc.Dropdown(id='input-covid-dropdown',
               options = [{'label': i, 'value': i} for i in df.location.unique()],
                value = 'the World',
                style = {'textAlign':'center','verticalAlign':'middle','margin-top':'5px','border-color': '#3f85f7','font-weight':'bold'}
                )], className = 'col-md-6 offset-md-3')
            ],
            className = 'row'),

            html.Div(id = 'graph-styles', children =
                [
                html.Div([dcc.Graph(id='output-covid-graph')],
                    className = 'col-sm-6'),

                html.Div([dcc.Graph(id='output-covid-graph2')],
                    className = 'col-sm-6')
                ],
                className = 'row'
                )
                ])]),



            dcc.Tab(label='COVID-19 cases by population percentage',
                    #value='tab-1',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    children =
                    [

            html.Div(id='dash-container_tab2-main',

                children = [

                html.Div([dcc.Graph(id='output-covid-graph3',
                        figure = {
                "data": [
                    {
                        "x": df_table.sort_values(by='% total cases to population',ascending=False)[:50]["location"],
                        "y": df_table.sort_values(by='% total cases to population',ascending=False)[:50]['% total cases to population']*100,
                        "type": "bar",
                        "name": "cases to pop (%)",
                        "marker": {"color": '#3f85f7', 'font':dict(family='system-ui')}
                        }#,
               #     {
               #         "x": df_table.sort_values(by='population',ascending=False)[:10]["location"],
               #         "y": df_table['% total deaths to population'],
               #         "type": "bar",
               #         "name": "deaths to pop (%)"
               #         #"marker": {"color": colors},
               #     }
                ],
                "layout": {
                    "xaxis": {"automargin": True,'tickfont': dict(family='system-ui', size=13)},
                    "yaxis": {
                        "automargin": True},
                       # "title": 'column'},
                    "title": dict(text= "<b>Total Cases per Population (%)<br>(top 50 countries)</b>", font=dict(family='system-ui', size = 16)),
                    "legend": {"x":'0','y':'1.2'}
                   # "height": 250,
                   # "margin": {"t": 10, "l": 10, "r": 10},

                }

                }
                        )]),

                html.Div([dash_table.DataTable(
                                id='datatable-row-ids',
                                columns=[
                                    #{"name": i, "id": i} for i in df_table.columns

                                {
                                'id': 'Rank (total cases %)',
                                #'name': 'Location',
                                'type': 'numeric',
                                'format': FormatTemplate.money(0).symbol(Symbol.no)
                                },
                                {
                                'id': 'location',
                                'name': 'Location',
                                'type': 'text'
                                }, {
                                'id': 'population',
                                'name': 'Population',
                                'type': 'numeric',
                                'format': FormatTemplate.money(0).symbol(Symbol.no)
                                },
                                 {
                                'id': 'total_cases',
                                'name': 'Total Cases',
                                'type': 'numeric',
                                'format': FormatTemplate.money(0).symbol(Symbol.no)
                                },
                                {
                                'id': '% total cases to population',
                                'name': 'Cases per population (%)',
                                'type': 'numeric',
                                'format': FormatTemplate.percentage(4)
                                },
                                {
                                'id': 'total_deaths',
                                'name': 'Total Deaths',
                                'type': 'numeric',
                                'format': FormatTemplate.money(0).symbol(Symbol.no)
                                },
                                {
                                'id': '% total deaths to total cases',
                                'name': 'Death rate (%)',
                                'type': 'numeric',
                                'format': FormatTemplate.percentage(4)
                                }
                                ],
                            data=df_table.sort_values(by='% total cases to population', ascending=False).to_dict('records'),
                            style_table = {'margin-top':'10px','overflowX':'auto'},
                            style_data = {'border': '1px solid white'},
                            style_data_conditional=[
                                        {
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': 'rgb(248, 248, 248)'
                                        }
                                        ],
                            style_cell = {'textAlign':'center', 'minWidth':'50px','width':'50px','maxWidth':'50px','whiteSpace':'normal','font-family':'system-ui','font-size':12},
                            style_header = {'fontWeight':'bold'},
                            editable=True,
                       #     filter_action="native",
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable="single",
                       #     row_selectable="multi",
                       #    row_deletable=True,
                            selected_columns=[],
                       #     selected_rows=[],
                            page_action="native",
                            page_current= 0,
                            page_size= 10,
                            )

                        ]) #close div id datatable-rows-id


                ])  #close div

                ]),  #close tab2

            dcc.Tab(label='COVID-19 death rate percentage',
                    #value='tab-1',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    children =
                    [

            html.Div(id='dash-container_tab3-main',

                children = [


                                html.Div([dcc.Graph(id='output-covid-graph4',
                        figure = {
                "data": [
                    {
                        "x": df_table.sort_values(by='% total deaths to total cases',ascending=False)[:50]["location"],
                        "y": df_table.sort_values(by='% total deaths to total cases',ascending=False)[:50]['% total deaths to total cases']*100,
                        "type": "bar",
               #         "name": " (%)",
                        "marker": {"color": '#3f85f7', 'font':dict(family='system-ui')}
                        }#,

                ],
                "layout": {
                    "xaxis": {"automargin": True, 'tickfont': dict(family='system-ui', size=13)},
                    "yaxis": {
                        "automargin": True},
                       # "title": 'column'},
                    "title": dict(text= "<b>Death Rate (%)<br>(top 50 coutries)</b>", font=dict(family='system-ui', size = 16)),
                   # "legend": {"x":'0','y':'1.2'}
                   # "height": 250,
                   # "margin": {"t": 10, "l": 10, "r": 10},

                }

                }
                        )]),

                html.Div([dash_table.DataTable(
                                id='datatable-row-ids2',
                                columns=[
                                    #{"name": i, "id": i} for i in df_table.columns

                                {
                                'id': 'Rank (death rate %)',
                                #'name': 'Location',
                                'type': 'numeric',
                                'format': FormatTemplate.money(0).symbol(Symbol.no)
                                },

                                {
                                'id': 'location',
                                'name': 'Location',
                                'type': 'text'
                                }, {
                                'id': 'population',
                                'name': 'Population',
                                'type': 'numeric',
                                'format': FormatTemplate.money(0).symbol(Symbol.no)
                                },
                                 {
                                'id': 'total_cases',
                                'name': 'Total Cases',
                                'type': 'numeric',
                                'format': FormatTemplate.money(0).symbol(Symbol.no)
                                },
                                {
                                'id': '% total cases to population',
                                'name': 'Cases per population (%)',
                                'type': 'numeric',
                                'format': FormatTemplate.percentage(4)
                                },
                                 {
                                'id': 'total_deaths',
                                'name': 'Total Deaths',
                                'type': 'numeric',
                                'format': FormatTemplate.money(0).symbol(Symbol.no)
                                },
                                {
                                'id': '% total deaths to total cases',
                                'name': 'Death rate (%)',
                                'type': 'numeric',
                                'format': FormatTemplate.percentage(4)
                                }
                                ],
                            data=df_table.sort_values(by='% total deaths to total cases', ascending=False).to_dict('records'),
                            style_table = {'margin-top':'10px','overflowX':'auto'},
                            style_data = {'border': '1px solid white'},
                            style_data_conditional=[
                                        {
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': 'rgb(248, 248, 248)'
                                        }
                                        ],
                            style_cell = {'textAlign':'center', 'minWidth':'50px','width':'50px','maxWidth':'50px','whiteSpace':'normal','font-family':'system-ui','font-size':12},
                            style_header = {'fontWeight':'bold'},
                            editable=True,
                       #     filter_action="native",
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable="single",
                       #     row_selectable="multi",
                       #    row_deletable=True,
                            selected_columns=[],
                       #     selected_rows=[],
                            page_action="native",
                            page_current= 0,
                            page_size= 10,
                            )

                        ]) #close div id datatable-rows-id

                        ])
                        ])  #close tab3
                        ])  #close Tabs
                        ])  #close main div




    @dash_app.callback(
            Output('output-covid-graph', 'figure'),
            [Input('input-covid-dropdown', 'value')]
            )

    def update_value(input_data):

        dff = df[df['location']==input_data]
        df_max_date = df[(df['date'] == df['date'].max())]
        total_cases_for_today = 1

        return {
                'data': [dict(
                    x = df[df['location']==input_data]['date'],
                    y = df[df['location']==input_data]['total_cases'],
                    type = 'line',
                    fill = 'tozeroy',
                    marker= {'color': '#3f85f7'},
                    fillcolor= 'e7f4fa',
                    text= {'color': '#111111'}
                    )],
                'layout': {
                    'title': dict(text=('<b>Total cases in '+input_data+'<br>{}</b>').format(format(list(df[(df['date'] == df['date'].max()) & (df['location']==input_data)]['total_cases'])[0],',d')),
                        font=dict(family='system-ui', size = 16)),
                #'plot_bgcolor': colors['background'],
                'font': {'color': colors['text']}
                }
                }


    @dash_app.callback(
            Output('output-covid-graph2', 'figure'),
            [Input('input-covid-dropdown', 'value')]
            )

    def update_value(input_data):

        dff = df[df['location']==input_data]


        return {
                'data': [
                        dict(
                            x=df[df['location']==input_data]['date'],
                            y= df[df['location']==input_data]['new_cases'],
                            type='bar',
                            name ='New Cases',
                            marker= {'color': '#3f85f7'}#, 'color:hover':'#111111'} wyp: ededed
                    ),

                        dict(
                            x = df[df['location']==input_data]['date'],
                            y = df[df['location']==input_data]['moving_average'],
                            type = 'scatter',
                            name ='Mean',
                            marker= {'color': '#fa501f'}#, 'color:hover':'#111111'} wyp: ededed
                    )],

                'layout': {
                    'title': dict(text = ('<b>Daily increase for '+input_data+'<br>{}</b>').format(format(list(df[(df['date'] == df['date'].max()) & (df['location']==input_data)]['new_cases'])[0],',d')),
                    font=dict(family='system-ui', size = 16)),
                #'plot_bgcolor': colors['background'],
                #'showlegend':False,
                'legend': dict(orientation='h'),
                'font': {'color': colors['text']},
                }
                }

    @dash_app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    [Input('datatable-interactivity', 'selected_columns')]
)
    def update_styles(selected_columns):
        return [{'if': { 'column_id': i },'background_color': '#D2F3FF' } for i in selected_columns]

    return dash_app.server
