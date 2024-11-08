import requests
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as np
import seaborn as sns
from shapely.geometry import shape

#----------------------------------------------------------#
'''
GET COMMUNITY-DISTRICT & PROJECT-LEVEL HOUSING DATABASE:
'''
community_district_url = 'https://data.cityofnewyork.us/resource/dbdt-5s7j.json'
project_level_url = 'https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/ArcGIS/rest/services/Housing_Database/FeatureServer/0/query'

# Define parameters for the project-level query:
params = {
    'where': '1=1',        # Retrieve all records
    'outFields': '*',       # Select all fields
    'f': 'json'             # Response format as JSON
}


def fetch_data(url, params=None):
    '''
    This function fetches data from the urls defined above and stores
    them in a pandas datafrome. The precise method of storing the data
    depends on whether the data is in a "features" format.
    '''
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        # Check if data is in a "features" format for ArcGIS data:
        if 'features' in data:
            return pd.DataFrame([feature['attributes'] for feature in data['features']])
        return pd.DataFrame(data)
    else:
        print(f"Failed to retrieve data from {url}: Status {response.status_code}")
        return None

# Load data in to df's by calling function:
community_district_df = fetch_data(community_district_url)
project_df = fetch_data(project_level_url, params)

#----------------------------------------------------------#
'''
CLEAN community_district_df AND CONVERT TO GEODATAFRAME:
'''
# Create borough column:
community_district_df['borough'] = community_district_df['commntydst'].apply(
    lambda x: 'Bronx' if x.startswith('1') else
              'Brooklyn' if x.startswith('2') else
              'Manhattan' if x.startswith('3') else
              'Queens' if x.startswith('4') else
              'Staten Island' if x.startswith('5') else
              'Unknown'  # If unknown
)

# Convert GeoJSON "the_geom" string column to shapely:
community_district_df['the_geom'] = community_district_df['the_geom'].apply(lambda x: shape(x))

# Convert community_district_df to a GeoDataFrame:
community_district_df = gpd.GeoDataFrame(community_district_df, geometry='the_geom')

#----------------------------------------------------------#


