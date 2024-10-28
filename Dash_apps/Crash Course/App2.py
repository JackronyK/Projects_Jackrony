#import Packages
from dash import html, Dash, dcc, Input, Output, callback, dash_table
import pandas as pd
import plotly.express as px

#Getting the data 
df =pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv")

#Initialize the app
app = Dash()

#App Layout
app.layout = [
    html.Div(children= "My second App with Data, Graph and Controls"),
    html.Hr(),
    dcc.RadioItems(options= ['pop', 'lifeExp', 'gdpPercap'], value= 'lifeExp', id ='radio-button'),
    dash_table.DataTable(data= df.to_dict('records'), page_size= 20),
    dcc.Graph(figure= {}, id= 'graph')
]

# Adding controls to build the interaction
@callback(
    Output(component_id= 'graph', component_property= 'figure'),
    Input(component_id= 'radio-button', component_property= 'value')
)

def update_graph(col_chosen):
    fig = px.histogram(df, x= 'continent', y= col_chosen, histfunc= 'avg', color_discrete_sequence = ['purple'])
    return fig


#Run the app
if __name__ == '__main__':
    app.run(debug= True)