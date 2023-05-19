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