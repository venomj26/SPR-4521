#%%
import os
import pathlib
import pandas as pd
import csv
import numpy as np
year_list=[]
rootfilepath_m="/Users/jhasneha/Documents/spring2022/SPRINDOT/interState"
# dict_pavements_df={}
# road_types_list=[]
# pavement_types_list=[]
road_list=[]
appended_df_list=[]
merged_df=pd.DataFrame()
road_files=os.listdir(rootfilepath_m)
for road in sorted(road_files):
    if not road.startswith('.'):
        print("the current road is: ", road)
        road_list.append(road)
        rootfilepath=rootfilepath_m +'/'+road
        bound_files=os.listdir(rootfilepath)
        for bound in sorted(bound_files):
            i=0

            if not bound.startswith('.'):
                print("the current bound and lane is: ", bound)
                partitioned_key=bound.partition("-") 
                bound_road=partitioned_key[0]
                lane=partitioned_key[2]
                destination_root= rootfilepath + '/'+ bound
                parametric_files= os.listdir(destination_root)
                for parameters in sorted(parametric_files):
                    if not parameters.startswith('.'):
                        if parameters.endswith('.xlsx'):
                                df_fwd=pd.DataFrame()
                                df_fwd=pd.read_excel(destination_root +'/'+parameters)
                                df_fwd.columns = df_fwd.columns.str.replace(' ', '')
                                df_fwd.columns = df_fwd.columns.str.replace(r'\([^)]*\)', '')
                                df_fwd.columns = df_fwd.columns.str.replace(' ', '')
                                df_fwd.columns = df_fwd.columns.str.replace(r'\([^)]*\)', '')
                                df_fwd=df_fwd.rename(columns={"SBorWBFWDStation":"DMI","NBorEBFWDStation":"DMI"})
                                df_fwd=df_fwd.rename(columns={"SubgradeDeflection":"D48"})
                                df_fwd=df_fwd.rename(columns={"SurfaceDeflection":"D0"})
                                df_fwd=df_fwd.rename(columns={"SCI300":"SCI"})
                                df_fwd=df_fwd.rename(columns={"Lat":"Latitude"})
                                df_fwd=df_fwd.rename(columns={"Long":"Longitude"})
                                df_fwd["Latitude"]=df_fwd["Latitude"].astype(float)
                                df_fwd["Longitude"]=df_fwd["Longitude"].astype(float)
                                df_fwd["Road"]= road
                                df_fwd["Bound"]=bound
                                print("fwd file found",df_fwd.head())
                                appended_df_list.append(df_fwd)
                
df_fwd_merged_IS =pd.concat(appended_df_list)
df_fwd_merged_IS["Latiude"]= df_fwd_merged_IS["Latitude"].replace(" ", np.nan)
df_fwd_merged_IS= df_fwd_merged_IS.dropna(axis=0, subset=["Latitude"])
df_fwd_merged_IS.to_csv("fwd_merged_IS.csv")
# %%
# %%
df_IS = pd.read_csv("/Users/jhasneha/Documents/Spring2021/SPR_indot/SPRprojectcodes/fwd_merged_IS.csv")
df_I69=df_IS.loc[df_IS['Road'] == 'I69']
df_I69.to_csv("/Users/jhasneha/Documents/Spring2021/SPR_indot/SPRprojectcodes/fwd_merged_I69.csv")

# %%
df_SR = pd.read_csv("/Users/jhasneha/Documents/Spring2021/SPR_indot/SPRprojectcodes/fwd_merged_SR.csv")
df_SR327=df_SR.loc[df_SR['Road'] == 'SR327']
df_SR327.to_csv("/Users/jhasneha/Documents/Spring2021/SPR_indot/SPRprojectcodes/fwd_merged_SR327.csv")

# %%
df_US = pd.read_csv("/Users/jhasneha/Documents/Spring2021/SPR_indot/SPRprojectcodes/fwd_merged_USH.csv")
df_US421=df_US.loc[df_US['Road'] == 'US421']
df_US421.to_csv("/Users/jhasneha/Documents/Spring2021/SPR_indot/SPRprojectcodes/fwd_merged_US421.csv")


# %%
