import pandas as pd
from Scripts.config.secretsData import *

def readFromPandas():
    df = pd.read_csv(path_for_excel)
    print(df)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def readFromPandasMailed():
    df = pd.read_csv(path_for_mailed)
    df['Date'] = pd.to_datetime(df['Date'])
    return df
    



