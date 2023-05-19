import pandas as pd
from env import host, username, password
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np




def handle_missing_values(df, prop_required_column, prop_required_row):
    # Drop columns based on the proportion of missing values
    column_threshold = int(df.shape[0] * prop_required_column)
    df = df.dropna(axis=1, thresh=column_threshold)

    # Drop rows based on the proportion of missing values
    row_threshold = int(df.shape[1] * prop_required_row)
    df = df.dropna(axis=0, thresh=row_threshold)

    return df


def get_zillow_data():
    """
    This function connects to the zillow database and retrieves data from the properties_2017 table for
    all 'Single Family Residential' properties. The resulting DataFrame contains the 60 columns of information.
    """
   
    # create the connection url
    url = f'mysql+pymysql://{username}:{password}@{host}/zillow'

    # read the SQL query into a DataFrame
    query = '''
SELECT p.*, predictions_2017.transactiondate, predictions_2017.logerror
FROM properties_2017 AS p
INNER JOIN (
    SELECT parcelid, MAX(transactiondate) AS transactiondate
    FROM predictions_2017
    GROUP BY parcelid
) AS t
ON p.parcelid = t.parcelid
AND p.latitude IS NOT NULL
AND p.longitude IS NOT NULL
AND p.propertylandusetypeid IN (
    SELECT propertylandusetypeid
    FROM propertylandusetype
    WHERE propertylandusetypeid IN (260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 273, 274, 275, 276, 279)
    
)
LEFT JOIN airconditioningtype 
ON p.airconditioningtypeid = airconditioningtype.airconditioningtypeid
LEFT JOIN architecturalstyletype 
ON p.architecturalstyletypeid = architecturalstyletype.architecturalstyletypeid
LEFT JOIN buildingclasstype 
ON p.buildingclasstypeid = buildingclasstype.buildingclasstypeid
LEFT JOIN heatingorsystemtype 
ON p.heatingorsystemtypeid = heatingorsystemtype.heatingorsystemtypeid
LEFT JOIN propertylandusetype 
ON p.propertylandusetypeid = propertylandusetype.propertylandusetypeid
LEFT JOIN storytype 
ON p.storytypeid = storytype.storytypeid
LEFT JOIN typeconstructiontype 
ON p.typeconstructiontypeid = typeconstructiontype.typeconstructiontypeid
INNER JOIN predictions_2017 
ON p.parcelid = predictions_2017.parcelid
AND predictions_2017.transactiondate = predictions_2017.transactiondate
'''
    df = pd.read_sql(query, url)

    return df

def read_csv_file():
    df = pd.read_csv('zillow_data.csv')
    return df

def handle_missing_values(df, prop_required_column, prop_required_row):
    # Drop columns based on the proportion of missing values
    column_threshold = int(df.shape[0] * prop_required_column)
    df = df.dropna(axis=1, thresh=column_threshold)

    # Drop rows based on the proportion of missing values
    row_threshold = int(df.shape[1] * prop_required_row)
    df = df.dropna(axis=0, thresh=row_threshold)

    return df

# Example usage:
# Assuming the data is in a DataFrame named 'data'
# prop_required_column = 0.6
# prop_required_row = 0.75
# cleaned_data = handle_missing_values(data, prop_required_column, prop_required_row)