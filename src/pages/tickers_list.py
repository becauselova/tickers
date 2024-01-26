import dash
dash.register_page(__name__, path="/")

from dash import dcc, html, callback, Input, Output, State
import yfinance as yf
from datetime import datetime
import pandas as pd
import pathlib

# app = Dash(__name__)
# https://www.tiingo.com/
#https://github.com/ranaroussi/yfinance

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../dataset").resolve()
nsdq = pd.read_csv(DATA_PATH.joinpath("NASDAQcompanylist.csv"))
nsdq.set_index('Symbol', inplace=True)

print(nsdq.head())
options =[]
for tic in nsdq.index:
    #{'label':'user sees','value':'script sees'}
    mydict={}
    mydict['label']=nsdq.loc[tic]['Name']+''+tic
    mydict['value'] = tic
    options.append(mydict)

# OR: options.append({'label':'{} {}'.format(tic, nsdq.loc[tic]['Name']),'value':tic})

layout = html.Div([
            html.H1('Динамика тикеров'),
            html.Div([html.H3('Введите тикер:', style={'paddingRight':'30px'}),
            dcc.Dropdown(
                id='pick',
                options=options,
                value=['TSLA'],
                multi=True
            )
            ], style={'display':'inline-block', 'verticalAlign':'top','width':'40%'}),
            html.Div([html.H3('Выберите период:'),
                      dcc.DatePickerRange(id='pick-a-date',
                                          min_date_allowed='2015-1-1',
                                          max_date_allowed =datetime.today(),
                                          start_date='2020-1-1',
                                          end_date=datetime.today(),
                                          with_portal = True
                                          )
                      ], style={'display':'inline-block'}),
            html.Div([
                    html.Button(id='push-button',
                                n_clicks=0,
                                children='OK',
                                style={'fontSize': 24,'marginLeft':'30px'})
            ], style ={'display':'inline-block'}),
            dcc.Graph(id='diagram',
                        figure={'data':[
                            {'x': [1,2], 'y':[3,1]}
                        ],
                    }
                )
            ])

@callback(Output('diagram', 'figure'),
               [Input('push-button', 'n_clicks')],
               [State('pick','value'),
               State('pick-a-date','start_date'),
               State('pick-a-date', 'end_date')])

def update_graph(n_clicks,stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[:10],'%Y-%m-%d')
    end = datetime.strptime(end_date[:10],'%Y-%m-%d')
    traces =[]
    for tic in stock_ticker:
        data = yf.download(tic, start, end)
        traces.append({'x': data.index, 'y': data['Close'],'name':tic})
    fig = {
        'data': traces,
        'layout':{'title': ', '.join(stock_ticker)+' Closing Prices'}
    }
    return fig