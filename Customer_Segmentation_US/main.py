import pandas as pd
import plotly.express as px
from dash import Input, Output, html, dcc, Dash
from IPython.display import VimeoVideo
from scipy.stats.mstats import trimmed_var
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


# Importing the data
def wrangle(filepath):
    """
    Read SCF data file into ``DataFrame``.

    Returns only credit fearful households whose net worth is less than $2 million.

    Parameters
    ----------
    filepath : str
        Location of CSV file.
    """
    df = pd.read_csv(filepath)
    # Filtering
    df = df[(df['NETWORTH'] < 2e6) & (df['TURNFEAR'] == 1)]
    return df


file_path = "https://raw.githubusercontent.com/JackronyK/Projects_Jackrony/main/Customer_Segmentation_US/SCFP2022.csv"
df = wrangle(file_path)


#----------------------------------------------------------------------

# Getting high Var Features
def get_high_var_features(trimmed=True, return_feat_names=True):
    """
    Returns the five highest-variance features of ``df``.

    Parameters
    ----------
    trimmed : bool, default=True
        If ``True``, calculates trimmed variance, removing bottom and top 10%
        of observations.

    return_feat_names : bool, default=False
        If ``True``, returns feature names as a ``list``. If ``False``
        returns ``Series``, where index is feature names and values are
        variances.
    """
    # Calculate Variance
    if trimmed:
        top_five_features = (
            df.apply(trimmed_var).sort_values().tail(5)
        )
    else:
        top_five_features = df.var().sort_values().tail(5)

    # Extract names
    if return_feat_names:
        top_five_features = top_five_features.index.to_list()
    return top_five_features


#----------------------------------------------------------------------

## The App

# External CSS for a dark theme
external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/bootswatch/4.5.2/darkly/bootstrap.min.css']

## The App
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Callback to update bar chart
@app.callback(
    Output("bar-chart", "figure"),
    Input("trim-button", "value")
)
def serve_bar_chart(trimmed_input=True):
    """
    Returns a horizontal bar chart of five highest-variance features.

    Parameters
    ----------
    trimmed : bool, default=True
        If ``True``, calculates trimmed variance, removing bottom and top 10%
        of observations.
    """
    # Get features
    top_five_features = get_high_var_features(trimmed=trimmed_input, return_feat_names=False)
    fig = px.bar(
        x=top_five_features,
        y=top_five_features.index,
        orientation="h",
        color_discrete_sequence=["purple"]
    )
    fig.update_layout(
        xaxis_title="Variance",
        yaxis_title="Features"
    )

    return fig


## model metrics
def get_model_metrics(trimmed_input = True, k= 2, return_metrics = False):
    """
    Build ``KMeans`` model based on five highest-variance features in ``df``.

    Parameters
    ----------
    trimmed : bool, default=True
        If ``True``, calculates trimmed variance, removing bottom and top 10%
        of observations.

    k : int, default=2
        Number of clusters.

    return_metrics : bool, default=False
        If ``False`` returns ``KMeans`` model. If ``True`` returns ``dict``
        with inertia and silhouette score.

    """

    #Get high var features
    features= get_high_var_features(trimmed=trimmed_input, return_feat_names= True)

    #Createing feature matix
    X= df[features]

    #build the model
    model = make_pipeline(StandardScaler(), KMeans(n_clusters = k, random_state = 42))
    model.fit(X)
    if return_metrics:
        #calculate inertia
        i = model['kmeans'].inertia_
        #calculate silhoutte score
        ss = silhouette_score(X, model["kmeans"].labels_)
        # return dictionary to user
        metrics = {
            "inertia": round(i),
            "silhoette": round(ss, 3)
        }
        return metrics

    return model


###Serve Function
@app.callback(
        Output("metrics", "children"),
        Input("trim-button", "value"),
        Input("kmeans-slider", "value")
)
def serve_metrics(trimmed_input = True, k= 2):
    """
    Returns list of ``H3`` elements containing inertia and silhouette score
    for ``KMeans`` model.

    Parameters
    ----------
    trimmed : bool, default=True
        If ``True``, calculates trimmed variance, removing bottom and top 10%
        of observations.

    k : int, default=2
        Number of clusters.
    """
    #Get Metrics
    metrics = get_model_metrics(trimmed_input=trimmed_input, k= k, return_metrics= True)

    #Add the metrics to HTML elements
    text = [
        html.H3(f"Inertia: {metrics['inertia']}"),
        html.H3(f"Silhouette Score: {metrics['silhoette']}")
    ]
    return text

##PCA Scatter Plot
def get_pca_labels(trimmed = True, k= 2):
    
    """
    ``KMeans`` labels.

    Parameters
    ----------
    trimmed : bool, default=True
        If ``True``, calculates trimmed variance, removing bottom and top 10%
        of observations.

    k : int, default=2
        Number of clusters.
    """
    #Feature Matrix
    features = get_high_var_features(trimmed= trimmed, return_feat_names= True)
    X = df[features]

    #Build Transfomer
    transfomer = PCA(n_components=2, random_state= 42)

    #transform
    X_t = transfomer.fit_transform(X)
    X_pca = pd.DataFrame(X_t, columns= ["PC1", "PC2"] )

    #Labels
    model = get_model_metrics(trimmed_input= trimmed, k=k, return_metrics= False)
    X_pca["labels"] = model['kmeans'].labels_.astype(str)
    X_pca.sort_values(by= "labels", inplace= True)

    return X_pca

#PCA Scatter server
@app.callback(
        Output("pca-scatter", "figure"),
        Input ("trim-button", "value"),
        Input("kmeans-slider", "value")
)
def serve_scatter_plot(trimmed = True, k= 2):
    """Build 2D scatter plot of ``df`` with ``KMeans`` labels.

    Parameters
    ----------
    trimmed : bool, default=True
        If ``True``, calculates trimmed variance, removing bottom and top 10%
        of observations.

    k : int, default=2
        Number of clusters.
    """
    
    fig = px.scatter(

        data_frame= get_pca_labels(trimmed=trimmed, k= k),
        x= "PC1",
        y="PC2",
        color= "labels",
        title= "PCA Representation of Clusters"
    )
    fig.update_layout(xaxis_title = "PC1", yaxis_title = "PC2")
    return fig



# App Layout
app.layout = html.Div(
    [
        # Application Title
        html.H1("Survey of Consumer Finances"),
        # Bar Chart Elements
        html.H2("High Variances Features"),
        # Bar chart Graph
        dcc.Graph(id="bar-chart"),
        # Radio button for trimming options
        dcc.RadioItems(
            options=[
                {'label': 'Trimmed Var', 'value': True},
                {'label': 'Not Trimmed Var', 'value': False}
            ],
            value=True,
            id='trim-button'
        ),
        html.H2("K-Means Clustering"),
        html.H3("Number of Clusters"),
        dcc.Slider(min=2, max=12, step=1, value=2,id='kmeans-slider'),
        html.Div(id = 'metrics'),
        #PCA Scatter Plot
        dcc.Graph(id = "pca-scatter")

    ]
)


# Running the app
if __name__ == '__main__':
    app.run_server(debug=True)
