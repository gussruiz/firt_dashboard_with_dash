import pandas as pd
import plotly.express as px
from sklearn.datasets import load_wine
from dash import Dash, html, dcc
from dash.dependencies import Input, Output


def load_data():
    wine = load_wine()
    wine_df = pd.DataFrame(wine.data, columns=wine.feature_names)
    wine_df['WineType'] = [wine.target_names[t] for t in wine.target]
    return wine_df


wine_df = load_data()
ingredients = wine_df.drop(columns=['WineType']).columns

avg_wine_df = wine_df.groupby('WineType').mean().reset_index()


def create_scatter_chart(x_axis="alcohol", y_axis="malic_acid", color_encode=False):
    scatter_fig = px.scatter(wine_df, x=x_axis, y=y_axis,
                             color='WineType' if color_encode else None,
                             title="{} vs {}".format(x_axis.capitalize(), y_axis.capitalize()))
    scatter_fig.update_layout(height=600)
    return scatter_fig


def create_bar_chart(ingredients=["alcohol", "malic_acid", "ash"]):
    bar_fig = px.bar(avg_wine_df, x="WineType", y=ingredients,
                     title="Avg. Ingredients per Wine Type")
    bar_fig.update_layout(height=600)
    return bar_fig


x_axis = dcc.Dropdown(id="x_axis", options=[{'label': ing, 'value': ing} for ing in ingredients],
                      value="alcohol", clearable=False, style={"display": "inline-block", "width": "48%"})
y_axis = dcc.Dropdown(id="y_axis", options=[{'label': ing, 'value': ing} for ing in ingredients],
                      value="malic_acid", clearable=False, style={"display": "inline-block", "width": "48%"})
color_encode = dcc.Checklist(id="color_encode", options=[
                             {'label': 'Color Encode', 'value': 'Color Encode'}])

multi_select = dcc.Dropdown(id="multi_select", options=[{'label': ing, 'value': ing} for ing in ingredients],
                            value=["alcohol", "malic_acid", "ash"], multi=True, clearable=False)

app = Dash(title="Wine Analysis")

app.layout = html.Div(
    children=[
        html.H1("Wine Analysis Dataset", style={"text-align": "center"}),
        html.Div("Explore relationships between various ingredients used in the creation of three different types of wine (class_0, class_1 & class_2)", style={
                 "text-align": "center"}),
        html.Br(),
        html.Div(
            children=[
                x_axis,
                y_axis,
                color_encode,
                dcc.Graph(id="scatter_chart", figure=create_scatter_chart())
            ],
            style={"display": "inline-block", "width": "48%"}
        ),
        html.Div(
            children=[
                multi_select, html.Br(),
                dcc.Graph(id="bar_chart", figure=create_bar_chart())
            ],
            style={"display": "inline-block", "width": "48%"}
        )

    ],
    style={"padding": "50px"}
)


@app.callback(Output("scatter_chart", "figure"), [Input("x_axis", "value"), Input("y_axis", "value"), Input("color_encode", "value")])
def update_scatter_chart(x_axis, y_axis, color_encode):
    return create_scatter_chart(x_axis, y_axis, color_encode)


@app.callback(Output("bar_chart", "figure"), Input("multi_select", "value"))
def update_bar_chart(ingredients):
    return create_bar_chart(ingredients)


if __name__ == "__main__":
    app.run_server(debug=True)
