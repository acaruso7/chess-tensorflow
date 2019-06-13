#!/home/acaruso/anaconda3/bin/python
import os
import sys
import pandas as pd
from os import listdir
from os.path import isfile, join


def concat_csv():
    """read and concatenate multiple CSV files generated from parser script"""
    df = pd.DataFrame({})
    X_col_idxs = range(768)
    dtypes = {idx: 'int8' for idx in X_col_idxs} #set dtypes beforehand to save memory
    dtypes[768] = 'str'

    files = [f for f in listdir('./data/parsed') if isfile(join('./data/parsed', f))]

    for csv in files:
        df = pd.concat([df, pd.read_csv(f'./data/parsed/{csv}', sep=',', header=None, dtype=dtypes, memory_map=True)], axis=0)
    return df
    

def clean_data(df):
    """clean response variable and drop duplicate rows"""
    # remove prepended # symbols
    df.iloc[:,-1] = df.iloc[:,-1].apply(lambda x : x[1:] if x.startswith("#") else x) 

    # remove prepended + and - symbols, and convert to float
    df.iloc[:,-1] = df.iloc[:,-1].apply(lambda x: float(x[1:]) if x.startswith('+') 
                          else (-float(x[1:]) if x.startswith('-') else float(x)))
    
    print('# rows with duplicates: ', len(df))
    df = df.drop_duplicates(keep='first')
    print('# rows without duplicates: ', len(df))

    return df


if __name__ == '__main__':
    df = concat_csv()
    clean_df = clean_data(df)
    clean_df.to_csv('./data/model_ready/data.csv', sep=',', header=False, index=False, mode='a', chunksize=100000)



