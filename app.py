
# coding: utf-8

# In[46]:


import pandas as pd
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import plotly.graph_objs as go
import dash_html_components as html
app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


df = pd.read_csv('nama_10_gdp_1_Data.csv')
dfnew = ~df.isin(['European Union (current composition)',
              'European Union (without United Kingdom)',
              'European Union (15 countries)',
              'Euro area (EA11-2000, EA12-2006, EA13-2007, EA15-2008, EA16-2010, EA17-2013, EA18-2014, EA19)',
              'Euro area (19 countries)',
              'Euro area (12 countries)'])
df = df[dfnew]
df.dropna(how='any',subset=["GEO"],axis=0,inplace=True)
df.drop('Flag and Footnotes',axis=1,inplace=True)


# In[47]:


available_indicators = df['NA_ITEM'].unique()
countries = df['GEO'].unique()
timeline = df['TIME'].unique()
units = df['UNIT'].unique()

app.layout = html.Div([
    html.Div([
        html.H2(children='Economic Indicators Report',
                style={
            'textAlign': 'center',
            'margin': 30}
        ),
        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            )],style={'width': '40%', 'display': 'inline-block','margin': 20}),
        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Final consumption expenditure'
            )
        ],
        style={'width': '40%','float':'right','display': 'inline-block','margin': 20}),
      html.Div([
            dcc.RadioItems(
                id='unit',
                options=[{'label': i, 'value': i} for i in units],
                value='Current prices, million euro',
                labelStyle={'display': 'inline-block', 'margin':10}
            )],
            style={'width': '100%', 'display': 'inline-block','margin': 30})]),    
        dcc.Graph(id='indicator-graphic'),
     dcc.Slider(
        id='year--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in df['TIME'].unique()}
        ),
    html.Div(style={'margin-bottom': 60}),
 html.Div([
             html.H2(children=''),
        html.Div([
            dcc.Dropdown(
                id='xaxis-column2',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            )],style={'width': '40%', 'display': 'inline-block','margin': 20}),
        html.Div([
            dcc.Dropdown(
                id='yaxis-column2',
                options=[{'label': i, 'value': i} for i in countries],
                value='Belgium')],
            style={'width': '40%', 'float':'right', 'display': 'inline-block','margin': 20}),
     html.Div([
            dcc.RadioItems(
                id='unit',
                options=[{'label': i, 'value': i} for i in units],
                value='Current prices, million euro',
                labelStyle={'display': 'inline-block','margin':10}
            )],
            style={'width': '88%', 'display': 'inline-block','margin': 30})
    ]),

    dcc.Graph(id='country-indicator-graphic')
])

@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('unit', 'value'),
     dash.dependencies.Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name, unit,
                 year_value):
    dff = df[(df['TIME'] == year_value) & (df['UNIT'] == unit)]

    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            customdata=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],

            mode='markers',
            line=dict(
                color= ('rgb(170,24,175)')),
            marker={
                'size': 15,
                'opacity': 0.5,
                 'colorscale':'Viridis',
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            
            xaxis={'title': xaxis_column_name},
            yaxis={'title': yaxis_column_name},
            title= 'All European Countries',
            margin={'l': 60, 'b': 60, 't': 50, 'r': 60},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('country-indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column2', 'value'),
     dash.dependencies.Input('yaxis-column2', 'value'), 
     dash.dependencies.Input('unit', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name, unit):
        dff = df[(df['GEO'] == yaxis_column_name) & (df['UNIT'] == unit)]
        return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['TIME'],
            y=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='lines',
            line=dict(
                color= ('rgb(170,24,175)')),
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            
            xaxis={'title': xaxis_column_name},
            yaxis={'title': yaxis_column_name},
            margin={'l': 60, 'b': 60, 't': 60, 'r': 60},
            title= 'By Country',
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()

