
# coding: utf-8

# In[25]:


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
# df = df.rename(index={'Germany (until 1990 former territory of the FRG)': 'Germany'})
df = df[dfnew]
df.dropna(how='any',subset=["GEO"],axis=0,inplace=True)
df.drop('Flag and Footnotes',axis=1,inplace=True)
df.head()


# In[26]:


available_indicators = df['NA_ITEM'].unique()
countries = df['GEO'].unique()
timeline = df['TIME'].unique()
units = df['UNIT'].unique()

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            )],style={'width': '48%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Final consumption expenditure'
            )
        ],
        style={'width': '48%','float':'right','display': 'inline-block'})]),    
        dcc.Graph(id='indicator-graphic'),
     dcc.Slider(
        id='year--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in df['TIME'].unique()}
#           style={'width': '90%','margin-bottom' : 40}
        ),
    html.Div(style={'margin-bottom': 40}),
 html.Div([
        html.Div([
            dcc.Dropdown(
                id='xaxis-column2',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            )],style={'width': '48%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id='yaxis-column2',
                options=[{'label': i, 'value': i} for i in countries],
                value='Belgium')],
            style={'width': '48%', 'float':'right', 'display': 'inline-block'}),
     html.Div([
            dcc.RadioItems(
                id='unit',
                options=[{'label': i, 'value': i} for i in units],
                value='Current prices, million euro',
                labelStyle={'display': 'inline-block'}
            )],
            style={'width': '48%', 'float':'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='country-indicator-graphic')
])

@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 year_value):
    dff = df[df['TIME'] == year_value]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 35,
                'opacity': 0.5,
                 'colorscale':'Viridis',
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            
            xaxis={'title': xaxis_column_name},
            yaxis={'title': yaxis_column_name},
            margin={'l': 40, 'b': 40, 't': 20, 'r': 50},
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
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            
            xaxis={'title': xaxis_column_name},
            yaxis={'title': yaxis_column_name},
            margin={'l': 40, 'b': 40, 't': 20, 'r': 50},
#             style={'float':'right'},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()

