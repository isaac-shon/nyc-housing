import dash
import pandas as pd
import geopandas as gpd
from dash import html, dcc

# Convert community_district_df to a GeoDataFrame:
community_district_df = gpd.GeoDataFrame(community_district_df, geometry='the_geom')


app = dash.Dash(__name__, use_pages=True)

app.layout = html.Div(
    [
        # main app framework
        html.Div("Python Multipage App with Dash", style={'fontSize':50, 'textAlign':'center'}),
        html.Div([
            dcc.Link(page['name']+"  |  ", href=page['path'])
            for page in dash.page_registry.values()
        ]),
        html.Hr(),

        # content of each page
        dash.page_container
    ]
)


if __name__ == "__main__":
    app.run(debug=True)