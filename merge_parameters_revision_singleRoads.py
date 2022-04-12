#%%
import os
import pathlib
import pandas as pd
import csv
import numpy as np
year_list=[]
road="I69"
rootfilepath_m=("/Users/jhasneha/Documents/spring2022/SPRINDOT/roadSchoolDemoData/"+road+"withImages")  
# dict_pavements_df={}
# road_types_list=[]
# pavement_types_list=[]
road_list=[]
appended_df_list=[]

merged_df=pd.DataFrame()
road_files=os.listdir(rootfilepath_m)
for bound in sorted(road_files):
    if not bound.startswith('.'):
        print("the current road is: ", bound)
        rootfilepath=rootfilepath_m +'/'+bound
        partitioned_key=bound.partition("-") 
        bound_road=partitioned_key[0]
        lane=partitioned_key[2]
        iri_files=os.listdir(rootfilepath)
        for file in sorted(iri_files):
            i = 0
            if file.endswith('.xlsx') or file.endswith('.csv'):
                print("printing file",file)
                if 'IRI' in file:
                    df_IRI=pd.DataFrame()
                    df_IRI=pd.read_csv(rootfilepath+'/'+file)
                    df_IRI.columns = df_IRI.columns.str.replace(' ', '')
                    df_IRI.columns = df_IRI.columns.str.replace(r'\([^)]*\)', '')
                    print('IRI file found')
                elif 'AASHTO' in file:
                    df_aashto=pd.DataFrame()
                    df_aashto=pd.read_csv(rootfilepath+'/'+file)
                    df_aashto.columns = df_aashto.columns.str.replace(' ', '')
                    df_aashto.columns = df_aashto.columns.str.replace(r'\([^)]*\)', '')
                    print("AASHTO file found")
                else:
                    df_fwd=pd.DataFrame()
                    df_fwd=pd.read_excel(rootfilepath+'/'+file)
                    df_fwd.columns = df_fwd.columns.str.replace(' ', '')
                    df_fwd.columns = df_fwd.columns.str.replace(r'\([^)]*\)', '')
                    df_fwd.columns = df_fwd.columns.str.replace(' ', '')
                    df_fwd.columns = df_fwd.columns.str.replace(r'\([^)]*\)', '')
                    df_fwd=df_fwd.rename(columns={"SBorWBFWDStation":"DMI","NBorEBFWDStation":"DMI"})
                    df_fwd=df_fwd.rename(columns={"SubgradeDeflection":"D48"})
                    df_fwd=df_fwd.rename(columns={"SurfaceDeflection":"D0"})
                    df_fwd=df_fwd.rename(columns={"SCI300":"SCI"})
                    print("fwd file found")
        print("here in loop value of i is", i) 
        i=i+1               
        print("Merging df will start now")
        from merge_parameters import merged_cd_iri_fwd
        df_merged= merged_cd_iri_fwd(df_aashto,df_IRI,df_fwd)
        df_merged["Bound"]=bound_road
        df_merged["Lane"]= lane
        df_merged["Road"]=road
        #print(df_merged.head())
        df_merged=df_merged.rename(columns={'GPSLng_road':'Longitude','GPSLat_road':'Latitude'})
        # lat_dict= dict(zip(df_IRI.RefDMI, df_IRI.GPSLat))
        # df_merged['Latitude']=df_merged['DMI'].map(lat_dict)
        # lon_dict= dict(zip(df_IRI.RefDMI, df_IRI.GPSLng))
        # df_merged['Longitude']=df_merged['DMI'].map(lon_dict)
        appended_df_list.append(df_merged)
        print("inserted file is",bound)
merged_df=pd.concat(appended_df_list)


#deleting extra columns added due to joining of fwd dataframe with CD twice for checking purpose
#merged_df.drop(merged_df.columns[[6,7,8,9,10,11,12]], axis=1, inplace=True)


#%%
# #main chunk of merging parameters
# nearest_df=pd.DataFrame()
# for index,row in df_fwd.iterrows():
#     index_value=int(row["DMI"])
#     ind = df_IRI["RefDMI_road"].sub(index_value).abs().idxmin()
#     print (ind)
#     df_test =  df_IRI.loc[ind,:]
#     nearest_df=nearest_df.append(df_test,ignore_index=True)

# df_IRI_nearest=nearest_df.reset_index()
# df_fwd_m=df_fwd[["DMI","D0","D48","SCI","BDI","BCI","Lat","Long"]].copy() #some dont have AUPP calculated
# df_fwd_m=df_fwd_m.rename(columns={'DMI':'DMI_fwd','Lat':'Lat_fwd','Long':'Long_fwd'})
# df_IRI_fwd=pd.concat([df_IRI_nearest,df_fwd_m], axis=1)
# df_IRI_fwd=df_IRI_fwd.rename(columns={'RefDMI_road':'DMI_id'})
# df_IRI_f=df_IRI.merge(df_IRI_fwd,how='outer', left_on='RefDMI_road', right_on='DMI_id')

"""%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
replacing the FWD grouped point coordinates into the actual coordinate columns. the FWD points are grouped while merging the nearest DMI to the IRI DMI at the end of the road

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
#%%
merged_df.loc[merged_df.duplicated(['Latitude','Longitude']), ['Longitude','Latitude','DMI','R_IRI','L_IRI','density_z4','density_z2']] = np.nan
merged_df.Longitude.fillna(merged_df.Long_fwd, inplace=True)
merged_df.Latitude.fillna(merged_df.Lat_fwd, inplace=True)
merged_df.DMI.fillna(merged_df.DMI_fwd, inplace=True)
merged_df.drop(columns=["Lat_fwd","Long_fwd"])


# """################### new"""
"""@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"""
#%%
cond_new = [
    ((merged_df['L_IRI']>1000)| (merged_df['R_IRI']>1000)),
    ((merged_df['D48']>1.80) | (merged_df['BCI']>4.0)),
    ((merged_df['L_IRI'] > 330) & (merged_df['L_IRI'] < 1000)) | ((merged_df['R_IRI'] > 330) & (merged_df['R_IRI'] <1000)) | ((merged_df['D48']>1.8) | (merged_df['SCI']>8)),
    (((merged_df['L_IRI'] > 330) & (merged_df['L_IRI'] <= 1000)) | ((merged_df['R_IRI'] > 330) & (merged_df['R_IRI'] <=1000)) | ((merged_df['D48']>1.4) & (merged_df['D48']<=1.80)) | ((merged_df['BCI']>3) & (merged_df['BCI']<=4)) | (merged_df['BDI']>8.8)),
    (((merged_df['L_IRI'] > 330) & (merged_df['L_IRI'] <= 1000)) | ((merged_df['R_IRI'] > 330) & (merged_df['R_IRI'] <=1000))|((merged_df['BDI']<=8.8) &(merged_df['BDI']>4.5))|(merged_df['SCI']>8)|(merged_df['D0']>36.4)),  
    (((merged_df['L_IRI'] > 70) & (merged_df['L_IRI'] <= 330)) | ((merged_df['R_IRI'] > 70) & (merged_df['R_IRI'] <330))|((merged_df['SCI']>6) & (merged_df['SCI']<=8))|((merged_df['D0']>24.6)&(merged_df['D0']<=36.4))),   
    ((merged_df['L_IRI'] <= 70) & (merged_df['R_IRI'] <= 70) & (merged_df['D48']<=1.4) & (merged_df['BCI']<=3) &(merged_df['BDI']<=4.5)& (merged_df['SCI']<=6)&(merged_df['D0']<=24.6)),
    ((merged_df['L_IRI'] <= 70) & (merged_df['R_IRI'] <= 70) )]
choice_new = ['high_IRI', 'Full_depth_patching_fwd','Full_depth_patching','Full_depth_patching_warning','Surface_patching','Surface_patching_warning', 'Good_condition','Good_condition']
merged_df['Patching_color_map'] = np.select(cond_new, choice_new, default='need_to_be_checked')






#%%
patching_depth={'Good_condition':1,'high_IRI':8, 'Full_depth_patching_fwd':7,'Full_depth_patching':6,'Full_depth_patching_warning':5,'Surface_patching':3,'Surface_patching_warning':2,'need_to_be_checked':4}
merged_df['Patching_depth']=merged_df['Patching_color_map'].map(patching_depth)

"""@@@@@@@@@@@@@@@@@@@@@@@@@

this is for the patching table for the app

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"""

#%%
patching_color={1:'green',8:'blue', 7:'maroon',6:'crimson',5:'salmon',3:'orange',2:'yellow',4:'grey'}
merged_df['Patching_color']=merged_df['Patching_depth'].map(patching_color)



# %%
merged_df["Lane"]=merged_df["Lane"].replace("","NA")
merged_df = merged_df.dropna(axis=0, subset=['Latitude'])
merged_df = merged_df.dropna(axis=0, subset=['Longitude'])


merged_df=merged_df.fillna(0.00)

#merged_df=merged_df.replace(0.0,"NA")
# %%
# merged_df.to_csv("/Users/jhasneha/Documents/spring2022/SPRINDOT/roadSchoolDemoData/SR327/SR327_demo_patching.csv")
merged_df.to_csv("/Users/jhasneha/Documents/spring2022/SPRINDOT/roadSchoolDemoData/I69withImages/I69_demo_patching.csv")

# %%
