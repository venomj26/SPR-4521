#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%%
#rootfilepath='/Users/jhasneha/Documents/SPRINDOT/summer2021/SPRINDOT/Roads_3d/Interstate'
rootfilepath='/Users/jhasneha/Documents/SPRINDOT/summer2021/SPRINDOT/FWD/Full Depth Asphalt Pavement'
#rootfilepath='/Users/jhasneha/Documents/SPRINDOT/summer2021/SPRINDOT/Roads_3d/USroads'


#%%
import os
import pathlib

#def create_df(rootfilepath):
root_files=os.listdir(rootfilepath)
df_roads_SD=pd.DataFrame()
for entry in root_files:
    print(entry)
    if not entry.startswith('.'):
        print("File names: " ,entry)
        destination_root= rootfilepath + '/'+entry
        #print("destination" ,destination_root)
        pattern= "*.xlsx"
        list_p=list(pathlib.Path(destination_root).glob(pattern))
        #print(list_p)
        for index in list_p:
            df=pd.read_excel(index)
            df.columns=df.columns.str.replace(' ', '')
            df.columns=df.columns.str.replace(r'\([^)]*\)', '')
            #print(df.head())
            print(entry, df.describe())
# %%
