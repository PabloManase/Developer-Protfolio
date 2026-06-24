import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

# Load the customer dataset
df = pd.read_csv("../data/customer_data.csv")
# Select only the two features used for clustering.
X = df[["AnnualIncome", "SpendingScore"]]

# Perform the initial K-Means clustering at K=5
kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
df["Cluster"] = kmeans.fit_predict(X).astype(str)

# APPLICATION INITIALISATION
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    # Page Title
    html.H2("Customer Segmentation Dashboard",
            className="text-center mt-4 mb-4"),

    # Cluster Count Slider
    dbc.Row([
        dbc.Col([
            html.Label("Number of Clusters"),
            dcc.Slider(id="k-slider", min=2, max=10, step=1,
                       value=5, marks={i: str(i) for i in range(2, 11)}),
        ], width=12)
    ], className="mb-4"),

    # TOP CHART ROW: Scatter plot & Bar chart
    dbc.Row([
        dbc.Col(dcc.Graph(id="scatter-plot"), width=8),
        dbc.Col(dcc.Graph(id="bar-chart"),   width=4),
    ]),

    # BOTTOM CHART ROW: Elbow chart & Income histogram
    dbc.Row([
        dbc.Col(dcc.Graph(id="elbow-chart"), width=6),
        dbc.Col(dcc.Graph(id="income-hist"), width=6),
    ])
], fluid=True)  # dashboard spans the full browser window width


# CALLBACK: DYNAMIC CHART UPDATES
@app.callback(
    Output("scatter-plot", "figure"),
    Output("bar-chart",    "figure"),
    Output("elbow-chart",  "figure"),
    Output("income-hist",  "figure"),
    Input("k-slider", "value"),
)
def update_charts(k):
    """
    Re-cluster the customer data at the selected K and rebuild all four charts.
 
    This function is called every time the user moves the cluster slider.
    It re-runs K-Means with the new K value and returns four updated Plotly
    figures, which Dash renders in the corresponding chart panels.
 
    Parameters
        k : int
            Number of clusters selected by the user via the slider (range 2–10).
 
    Returns:
        scatter : plotly.graph_objects.Figure
            Scatter plot of AnnualIncome vs SpendingScore, coloured by cluster.
        bar : plotly.graph_objects.Figure
            Bar chart showing the number of customers in each cluster.
        elbow : plotly.graph_objects.Figure
            Line chart showing inertia vs K with a vertical marker at the current K.
        hist : plotly.graph_objects.Figure
            Stacked histogram of AnnualIncome distributions per cluster.
    """
    
    # Create a fresh KMeans model with the user-selected number of clusters.
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    df["Cluster"] = km.fit_predict(X).astype(str)

    # CHART 1: SCATTER PLOT
    scatter = px.scatter(
        df, x="AnnualIncome", y="SpendingScore",
        color="Cluster", title="Customer Clusters",
        hover_data=["CustomerID"],
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    # CHART 2: CLUSTER SIZE BAR CHART
    bar = px.bar(
        df.groupby("Cluster").size().reset_index(name="Count"),
        x="Cluster", y="Count", title="Cluster Sizes",
        color="Cluster",
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    # CHART 3: ELBOW METHOD LINE CHART
    inertias = [KMeans(n_clusters=i, random_state=42, n_init=10)
                .fit(X).inertia_ for i in range(1, 11)]
    elbow = px.line(
        x=list(range(1, 11)), y=inertias,
        labels={"x": "Clusters", "y": "Inertia"},
        title="Elbow Method", markers=True
    )
    elbow.add_vline(x=k, line_dash="dash", line_color="red")

    # CHART 4: INCOME DISTRIBUTION HISTOGRAM
    hist = px.histogram(
        df, x="AnnualIncome", color="Cluster",
        title="Income Distribution by Cluster",
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    # Return all four figures in the same order as the Output declarations
    return scatter, bar, elbow, hist

# Program Entry Point
if __name__ == "__main__":
    app.run(debug=True)
