# Libraries
from dash import html, Dash, Input, Output, callback, dcc
import plotly.express as px
import pandas as pd


#Importing the data
df= pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

#--------------------------------
# The App
app = Dash()

#Layout

app.layout = [
    html.H1(children= 'Title of Dash App', style= {'textAlign': 'center'}),
    dcc.Dropdown(df.country.unique(), 'Kenya', id = 'dropdown-selection'),
    dcc.Graph(id= 'graph-content')
]

#Call back
@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)

def update_graph(value):
    dff = df[df.country == value]
    return px.line(dff, x= 'year', y = 'pop')

#Running the app
if __name__ == '__main__':
    app.run(debug= True)