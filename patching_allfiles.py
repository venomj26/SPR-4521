#%%
import os
import pathlib
import pandas as pd
import csv
import numpy as np
#%%
year_list=[]
rootfilepath_m="/Users/jhasneha/Documents/spring2022/SPRINDOT/stateRoad/SR38"  
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
            i = 0
            if not bound.startswith('.'):
                print("the current bound and lane is: ", bound)
                partitioned_key=bound.partition("-") 
                bound_road=partitioned_key[0]
                lane=partitioned_key[2]
                destination_root= rootfilepath + '/'+ bound
                parametric_files= os.listdir(destination_root)
                for parameters in sorted(parametric_files):
                    if not parameters.startswith('.'):
                        if parameters.endswith('.xlsx') or parameters.endswith('.csv'):
                            print(parameters)
                            if 'IRI' in parameters:
                                df_IRI=pd.DataFrame()
                                df_IRI=pd.read_csv(destination_root +'/'+parameters)
                                df_IRI.columns = df_IRI.columns.str.replace(' ', '')
                                df_IRI.columns = df_IRI.columns.str.replace(r'\([^)]*\)', '')
                                print('IRI file found')
                            elif 'AASHTO' in parameters:
                                df_aashto=pd.DataFrame()
                                df_aashto=pd.read_csv(destination_root +'/'+parameters)
                                df_aashto.columns = df_aashto.columns.str.replace(' ', '')
                                df_aashto.columns = df_aashto.columns.str.replace(r'\([^)]*\)', '')
                                print("AASHTO file found")
                            else:
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
                                print("fwd file found",df_fwd.head())
            print("here in loop value of i is", i) 
            i=i+1               
            print("Merging df will start now")
            from merge_parameters import merged_cd_iri_fwd
            df_merged= merged_cd_iri_fwd(df_aashto,df_IRI,df_fwd)
            df_merged["Bound"]=bound_road
            df_merged["Lane"]= lane
            df_merged["Road"]=road
            df_merged=df_merged.rename(columns={'Density_x_x':'density_z4','R_IRI_x':'R_IRI','Density_y_x':'density_z2','L_IRI_x':'L_IRI'})
            lat_dict= dict(zip(df_IRI.RefDMI, df_IRI.GPSLat))
            df_merged['Latitude']=df_merged['DMI'].map(lat_dict)
            lon_dict= dict(zip(df_IRI.RefDMI, df_IRI.GPSLng))
            df_merged['Longitude']=df_merged['DMI'].map(lon_dict)
            appended_df_list.append(df_merged)
            print("inserted file is",road)
merged_df=pd.concat(appended_df_list)


#deleting extra columns added due to joining of fwd dataframe with CD twice for checking purpose
merged_df.drop(merged_df.columns[[6,7,8,9,10,11,12]], axis=1, inplace=True)


#%%


# """################### new"""
"""@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"""
#%%
cond_new = [
    ((merged_df['L_IRI']>1000)| (merged_df['R_IRI']>1000)),
    ((merged_df['L_IRI'] > 330) & (merged_df['L_IRI'] < 1000)) | ((merged_df['R_IRI'] > 330) & (merged_df['R_IRI'] <1000)) | ((merged_df['D48']>1.8) | (merged_df['SCI']>8)),
    ((merged_df['D48']>1.80) | (merged_df['BCI']>4)),
    (((merged_df['L_IRI'] > 330) & (merged_df['L_IRI'] < 1000)) | ((merged_df['R_IRI'] > 330) & (merged_df['R_IRI'] <1000)) | ((merged_df['D48']>1.4) & (merged_df['D48']<1.80)) | ((merged_df['BCI']>3) & (merged_df['BCI']<4)) | (merged_df['BDI']>8.8)),
    (((merged_df['L_IRI'] > 330) & (merged_df['L_IRI'] < 1000)) | ((merged_df['R_IRI'] > 330) & (merged_df['R_IRI'] <1000))|((merged_df['BDI']<8.8) &(merged_df['BDI']>4.5))|(merged_df['SCI']>8)|(merged_df['D0']>36.4)),  
    (((merged_df['L_IRI'] > 70) & (merged_df['L_IRI'] < 330)) | ((merged_df['R_IRI'] > 70) & (merged_df['R_IRI'] <330))|((merged_df['SCI']>6) & (merged_df['SCI']<8))|((merged_df['D0']>24.6)&(merged_df['D0']<36.4))),   
    ((merged_df['L_IRI'] < 70) & (merged_df['R_IRI'] < 70) & (merged_df['D48']<1.8) & (merged_df['BCI']<3) &(merged_df['BDI']<4.5)& (merged_df['SCI']<6)&(merged_df['D0']<24.6)),
    ((merged_df['L_IRI'] < 70) & (merged_df['R_IRI'] < 70) )]
choice_new = ['high_IRI', 'Full_depth_patching','Full_depth_patching_fwd','Full_depth_patching_warning','Surface_patching','Surface_patching_warning', 'Good_condition','Good_condition']
merged_df['Patching_color_map'] = np.select(cond_new, choice_new, default='need_to_be_checked')






#%%
patching_depth={'Good_condition':1,'high_IRI':8, 'Full_depth_patching':7,'Full_depth_patching_fwd':6,'Full_depth_patching_warning':5,'Surface_patching':3,'Surface_patching_warning':2,'need_to_be_checked':4}
merged_df['Patching_depth']=merged_df['Patching_color_map'].map(patching_depth)

"""@@@@@@@@@@@@@@@@@@@@@@@@@

this is for the patching table for the app

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"""

#%%
patching_color={1:'green',8:'blue', 7:'red',6:'orangered',5:'orange',3:'salmon',2:'yellow',4:'grey'}
merged_df['Patching_color']=merged_df['Patching_depth'].map(patching_color)



# %%
merged_df["Lane"]=merged_df["Lane"].replace("","NA")
merged_df = merged_df.dropna(axis=0, subset=['Latitude'])
merged_df = merged_df.dropna(axis=0, subset=['Longitude'])


merged_df=merged_df.fillna(0.0)

#merged_df=merged_df.replace(0.0,"NA")
# %%
merged_df.to_csv("patching_allfiles.csv")


#%%
df_test_SR=pd.read_csv("/Users/jhasneha/Documents/spring2022/SPRINDOT/roadSchoolDemoData/SR327/SR327_demo_patching.csv")
dfSrGoodRoads=df_test_SR.loc[df_test_SR['Patching_color'] == 'green']
df_SR_Sampled=df_test_SR.groupby("Patching_color").apply(lambda x: x.sample(frac=.04)).reset_index(drop=True)
df_SR_Sampled.to_csv("/Users/jhasneha/Documents/spring2022/SPRINDOT/roadSchoolDemoData/SR327/Sampled_SR327_demo_patching.csv")

# %%
df_test_IS=pd.read_csv("//Users/jhasneha/Documents/spring2022/SPRINDOT/roadSchoolDemoData/I69withImages/I69_demo_patching.csv")
dfIsGoodRoads=df_test_IS.loc[df_test_IS['Patching_color'] == 'green']
df_IS_Sampled=df_test_IS.groupby("Patching_color").apply(lambda x: x.sample(frac=.02)).reset_index(drop=True)
# df_IS_Sampled.to_csv("Sampled_patching_IS.csv")
df_IS_Sampled=df_IS_Sampled.reset_index()
df_IS_Sampled.to_csv("/Users/jhasneha/Documents/spring2022/SPRINDOT/roadSchoolDemoData/I69withImages/Sampled_I69_demo_patching.csv")

# %%
df_test_US=pd.read_csv("/Users/jhasneha/Documents/spring2022/SPRINDOT/roadSchoolDemoData/US421/US421_demo_patching.csv")
dfUsGoodRoads=df_test_US.loc[df_test_US['Patching_color'] == 'green']
df_US_Sampled=df_test_US.groupby("Patching_color").apply(lambda x: x.sample(frac=.2)).reset_index(drop=True)
# df_IS_Sampled.to_csv("Sampled_patching_IS.csv")
df_US_Sampled.to_csv("/Users/jhasneha/Documents/spring2022/SPRINDOT/roadSchoolDemoData/US421/Sampled_US421_demo_patching.csv")


# %%
shit_sr_manipulation=pd.read_csv("/Users/jhasneha/Documents/spring2022/SPRINDOT/roadSchoolDemoData/SR327/SR327_demo_patching.csv")
shit_sr_manipulation["image2D"]= shit_sr_manipulation["image2D"].astype(str) +'_0.jpg'
df_SR_Sampled_M=shit_sr_manipulation.groupby("Patching_color").apply(lambda x: x.sample(frac=.02)).reset_index(drop=True)
df_SR_Sampled_M.to_csv("/Users/jhasneha/Documents/spring2022/SPRINDOT/roadSchoolDemoData/SR327/Sampled_SR327_demo_patching_image.csv")

# %%
