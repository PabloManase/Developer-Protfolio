import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output


# Load the dataset
df = pd.read_csv('data/iris_dataset.csv')


# Initiaalize the dash app
app = Dash(__name__)


# Define the layout (what user sees on the page)
app.layout = html.Div([

    # Page title
    html.H1(
        'Iris Dataset — Interactive EDA Dashboard',
        style={
            'textAlign': 'center',
            'fontFamily': 'Arial',
            'color': '#2c3e50'
        }
    ),

    html.P(
        'Use the dropdowns below to explore relationships between features.',
        style={
            'textAlign': 'center',
            'fontFamily': 'Arial',
            'color': '#7f8c8d'
        }
    ),

    html.Hr(),  # Horizontal divider line

    # ROW 1: Two dropdowns side by side
    html.Div([

        # Left dropdown — X-axis selector
        html.Div([
            html.Label(
                'Select X-Axis Feature:',
                style={
                    'fontFamily': 'Arial',
                    'fontWeight': 'bold'
                }
            ),
            dcc.Dropdown(
                id='x-axis-dropdown',
                options=[
                    {'label': 'Sepal Length', 'value': 'sepal_length'},
                    {'label': 'Sepal Width',  'value': 'sepal_width'},
                    {'label': 'Petal Length', 'value': 'petal_length'},
                    {'label': 'Petal Width',  'value': 'petal_width'},
                ],
                value='sepal_length',  # Default selection
                clearable=False
            ),
        ], style={
                'width': '45%',
                'display': 'inline-block',
                'marginRight': '5%'
            }),

        # Right dropdown — Y-axis selector
        html.Div([
            html.Label(
                'Select Y-Axis Feature:',
                style={
                    'fontFamily': 'Arial',
                    'fontWeight': 'bold'
                }
            ),
            dcc.Dropdown(
                id='y-axis-dropdown',
                options=[
                    {'label': 'Sepal Length', 'value': 'sepal_length'},
                    {'label': 'Sepal Width',  'value': 'sepal_width'},
                    {'label': 'Petal Length', 'value': 'petal_length'},
                    {'label': 'Petal Width',  'value': 'petal_width'},
                ],
                value='petal_length',  # Default selection
                clearable=False
            ),
        ], style={'width': '45%', 'display': 'inline-block'}),

    ], style={'padding': '20px'}),

    # ROW 2: Scatter plot (interactive)
    dcc.Graph(id='scatter-plot'),

    html.Hr(),

    # ROW 3: Two static charts side by side
    html.Div([

        # Box plot
        html.Div([
            dcc.Dropdown(
                id='boxplot-feature-dropdown',
                options=[
                    {'label': 'Sepal Length', 'value': 'sepal_length'},
                    {'label': 'Sepal Width',  'value': 'sepal_width'},
                    {'label': 'Petal Length', 'value': 'petal_length'},
                    {'label': 'Petal Width',  'value': 'petal_width'},
                ],
                value='petal_length',
                clearable=False
            ),
            dcc.Graph(id='box-plot'),
        ], style={
            'width': '48%',
            'display': 'inline-block',
            'verticalAlign': 'top'
            }
        ),

        # Species distribution bar chart
        html.Div([
            dcc.Graph(id='bar-chart'),
        ], style={
            'width': '48%',
            'display': 'inline-block',
            'verticalAlign': 'top',
            'marginLeft': '4%'
            }
        ),

    ], style={'padding': '20px'}),

])  # End of layout


# CALLBACKS — run automatically when user changes  dropdown selection

# Callback 1: Update scatter plot when X or Y dropdown changes
@app.callback(
    Output('scatter-plot', 'figure'),  # Which chart to update
    Input('x-axis-dropdown', 'value'),  # Watch X dropdown
    Input('y-axis-dropdown', 'value')  # Watch Y dropdown
)
def update_scatter(x_feature, y_feature):
    """
        Redraw the scatter plot with the selected X and Y features.
    """
    x_label = x_feature.replace("_", " ").title()
    y_label = y_feature.replace("_", " ").title()

    fig = px.scatter(
        df,
        x=x_feature,
        y=y_feature,
        color='species',
        title=f'{x_label} vs {y_label}',
        labels={
            x_feature: x_label,
            y_feature: y_label
        },
        template='plotly_white',
        hover_data=df.columns
    )
    fig.update_traces(marker=dict(size=8, opacity=0.8))
    return fig


# Callback 2: Update box plot when the box plot dropdown changes
@app.callback(
    Output('box-plot', 'figure'),
    Input('boxplot-feature-dropdown', 'value')
)
def update_boxplot(feature):
    """
        Redraw the box plot for the selected feature.
    """
    fig = px.box(
        df,
        x='species',
        y=feature,
        color='species',
        title=f'{feature.replace("_", " ").title()} by Species',
        template='plotly_white',
        points='all'  # Show individual data points
    )
    return fig


# Callback 3: Bar chart is static, but still interactive
@app.callback(
    Output('bar-chart', 'figure'),
    Input('x-axis-dropdown', 'value')
)
def update_bar(_):
    """
        Display species distribution as an interactive bar chart.
    """
    species_counts = df['species'].value_counts().reset_index()
    species_counts.columns = ['species', 'count']

    fig = px.bar(
        species_counts,
        x='species',
        y='count',
        color='species',
        title='Species Distribution',
        template='plotly_white',
        text='count'
    )
    fig.update_traces(textposition='outside')
    return fig


# Program entry point
if __name__ == '__main__':
    app.run(debug=True)
