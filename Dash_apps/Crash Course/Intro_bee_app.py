## Libraries
import pandas as pd
import  numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash,html,dcc,Input,Output


app = Dash(__name__)

# -------------------------------------------------------
#importing and cleaning th edata 
df =pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Other/Dash_Introduction/intro_bees.csv")

#Grouping
df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace= True)



# --------------------------------------------------------
# App Layout
app.layout = html.Div(
    [
        html.H1("Web Application Dashbords with Dash", style={'text-align':'center'}),
        dcc.Dropdown(
            id="slct_year",
            options=[
                {"label":'2015', 'value':2015},
                {"label":'2016', 'value':2016},
                {"label":'2017', 'value':2017},
                {"label":'2018', 'value':2018},
                {"label":'All', 'value':'All'}],
            multi= False,
            value=2015,
            style={"width": "48.0%"}
        ),

        html.Div(id= 'output_container', children= []),
        html.Br(),

        dcc.Graph(id='my_bee_map', figure={})
    ]
)

# ---------------------------------------------------------------------------
#connect the plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
     [Input(component_id='slct_year', component_property='value')]
)

def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    dff = df.copy()
    if option_slctd == 'All':
        container = "The user chose all Years"
        dff = dff[dff["Affected by"] == "Varroa_mites"] # No year is filtered

    else:
        container = f"The year chosen by user was: {option_slctd}"
        dff = dff[(dff["Year"] == option_slctd) & (dff["Affected by"] == "Varroa_mites")]


    #plotly Express
    fig = px.choropleth(
        data_frame= dff,
        locationmode='USA-states',
        locations='state_code',
        scope= 'usa',
        color= 'Pct of Colonies Impacted',
        hover_data=['State', 'Pct of Colonies Impacted'],
        color_continuous_scale= px.colors.sequential.YlOrRd,
        labels={"Pct of Colonies Impacted": " % of Bee Colonies"},
        template='plotly_dark'
    )
    return container, fig

# -------------------
if __name__ == '__main__':
    app.run(debug=True)