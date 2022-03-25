import pandas as pd

def preprocess(df,region_df):
    # filtering for summer olympics
    df = df[df['Season'] == 'Summer']
    # merge with region_df
    df = df.merge(region_df, on='NOC', how='left')
    # dropping duplicates
    df.drop_duplicates(inplace=True)
    # one hot encoding medals
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    return df

def post2020oly(medals1_df):
    return medals1_df

def post2020olya(df1):
    return df1

def post2020olyp(ind_athletes_df):
    return ind_athletes_df
