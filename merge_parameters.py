#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#%%
def aashto_z2(df_aashto):
        df_aashto_2=df_aashto.copy()
        df_aashto_2['Zone'] = df_aashto_2['Zone'].replace(4, np.nan)
        df_aashto_2= df_aashto_2.dropna(axis=0, subset=['Zone'])
        return(df_aashto_2)

#%%
def aashto_z4(df_aashto):
        df_aashto_4=df_aashto.copy()
        df_aashto_4['Zone'] = df_aashto_4['Zone'].replace(2, np.nan)
        df_aashto_4= df_aashto_4.dropna(axis=0, subset=['Zone'])
        return(df_aashto_4)
#%%
def aashto_dmi(df_aashto):
    df_aashto["DMI"]=6
    df_aashto.loc[df_aashto.index[0],"DMI"]=0
    df_aashto["DMI"]=df_aashto["DMI"].cumsum()
    return(df_aashto)

#%%   
def nearest(df_fwd, df):
    nearest_df=pd.DataFrame()
    for index,row in df_fwd.iterrows():
        index_value=int(row["DMI"])
        ind = df["RefDMI_road"].sub(index_value).abs().idxmin()
        df_test =  df.loc[ind,:]
        nearest_df=nearest_df.append(df_test,ignore_index=True)
    return(nearest_df)

#%%

def merged_cd_iri_fwd(df_aashto,df_IRI,df_fwd):
    df_IRI_work = df_IRI[["RefDMI_road"]].copy()
    df_aashto_z2=aashto_z2(df_aashto)
    df_aashto_z4=aashto_z4(df_aashto)

    df_aashto_z4=aashto_dmi(df_aashto_z4)
    df_aashto_z2=aashto_dmi(df_aashto_z2)

    df_plt_z4=df_aashto_z4[["DMI","Density"]].copy()
    # RIRI_dict = dict(zip(df_IRI.RefDMI_road, df_IRI.R_IRI))
    # df_plt_z4['R_IRI']=df_plt_z4['DMI'].map(RIRI_dict)
    df_plt_z2=df_aashto_z2[["DMI","Density"]].copy()
    # LIRI_dict = dict(zip(df_IRI.RefDMI_road, df_IRI.L_IRI))
    # df_plt_z2['L_IRI']=df_plt_z2['DMI'].map(LIRI_dict)

    cdz4_dict=dict(zip(df_plt_z4.DMI,df_plt_z4.Density))
    df_IRI_work['density_z4']=df_IRI_work["RefDMI_road"].map(cdz4_dict)

    cdz2_dict=dict(zip(df_plt_z2.DMI,df_plt_z2.Density))
    df_IRI_work['density_z2']=df_IRI_work["RefDMI_road"].map(cdz2_dict)

    # df_plt_z2=df_plt_z2.rename(columns={'DMI':'DMI_z2'})
    # df_cd=pd.DataFrame()
    # df_cd=df_plt_z4.merge(df_plt_z2,how='left', left_on='DMI', right_on='DMI_z2')

    if df_fwd.empty:
        df_IRI_cd=pd.concat([df_IRI,df_IRI_work], axis=1)

        return df_IRI_cd

    else:

        # df_cd_nearest=nearest(df_fwd,df_cd)
        # df_cd_nearest=df_cd_nearest.reset_index()
        df_IRI_nearest=nearest(df_fwd,df_IRI_work)
        df_IRI_nearest=df_IRI_nearest.reset_index()
        # df_pltz4_nearest=nearest(df_fwd,df_plt_z4)
        # df_pltz4_nearest=df_pltz4_nearest.reset_index()
        #print("df_cd_nearest_head",df_cd_nearest.head())
        df_fwd_m=df_fwd[["DMI","D0","D48","SCI","BDI","BCI","Lat","Long"]].copy() #some dont have AUPP calculated
        df_fwd_m=df_fwd_m.rename(columns={'DMI':'DMI_fwd','Lat':'Lat_fwd','Long':'Long_fwd'})
        # df_cd_fwd=pd.concat([df_cd_nearest,df_fwd_m], axis=1)
        # df_cd_fwd=df_cd_fwd.rename(columns={'DMI':'DMI_id'})
        df_IRI_fwd=pd.concat([df_IRI_nearest,df_fwd_m], axis=1)
        df_IRI_fwd=df_IRI_fwd.rename(columns={'RefDMI_road':'DMI_id'})
        print(df_IRI.head())

    
    #df_merged=pd.DataFrame()
        # df_cd_f=df_cd.merge(df_cd_fwd,how='left', left_on='DMI', right_on='DMI_id')
        df_IRI_f=df_IRI.merge(df_IRI_fwd, how='outer', left_on='RefDMI_road', right_on='DMI_id')

        return df_IRI_f


# %%
# df_aashto=pd.read_csv("/Users/jhasneha/Documents/spring2022/SPRINDOT/interState/I65/NB-DL/GLL#29 I-65 RP-137+19 to RP-141+50NB DL-20190712.105904Result-AASHTO_Result.csv")
# df_IRI=pd.read_csv("/Users/jhasneha/Documents/spring2022/SPRINDOT/interState/I65/NB-DL/GLL#29 I-65 RP-137+19 to RP-141+50NB DL-20190712.105904Result-IRI-report.csv")
# #df_fwd=pd.read_excel("/Users/jhasneha/Documents/spring2022/SPRINDOT/interState/I65/NB-DL/I-65 NB RP-137+20 to RP-141+00 Lane 1.xlsx")
# df_fwd=pd.DataFrame()
# df_aashto.columns = df_aashto.columns.str.replace(' ', '')
# df_aashto.columns = df_aashto.columns.str.replace(r'\([^)]*\)', '')
# df_IRI.columns = df_IRI.columns.str.replace(' ', '')
# df_IRI.columns = df_IRI.columns.str.replace(r'\([^)]*\)', '')
# df_fwd.columns = df_fwd.columns.str.replace(' ', '')
# df_fwd.columns = df_fwd.columns.str.replace(r'\([^)]*\)', '')
# df_fwd.columns = df_fwd.columns.str.replace(' ', '')
# df_fwd.columns = df_fwd.columns.str.replace(r'\([^)]*\)', '')
# df_fwd=df_fwd.rename(columns={"SBorWBFWDStation":"DMI","NBorEBFWDStation":"DMI"})
# df_fwd=df_fwd.rename(columns={"SubgradeDeflection":"D48"})
# df_fwd=df_fwd.rename(columns={"SurfaceDeflection":"D0"})
# df_fwd=df_fwd.rename(columns={"SCI300":"SCI"})
# # %%
#  test_df=merged_cd_iri_fwd(df_aashto,df_IRI,df_fwd)
# # %%
# df_aashto_z2=aashto_z2(df_aashto)
# df_aashto_z4=aashto_z4(df_aashto)
# #%%
# df_aashto_z4=aashto_dmi(df_aashto_z4)
# df_aashto_z2=aashto_dmi(df_aashto_z2)
# #%%
# df_plt_z4=df_aashto_z4[["DMI","Density"]].copy()
# RIRI_dict = dict(zip(df_IRI.RefDMI, df_IRI.R_IRI))
# df_plt_z4['R_IRI']=df_plt_z4['DMI'].map(RIRI_dict)
# df_plt_z2=df_aashto_z2[["DMI","Density"]].copy()
# LIRI_dict = dict(zip(df_IRI.RefDMI, df_IRI.L_IRI))
# df_plt_z2['L_IRI']=df_plt_z2['DMI'].map(LIRI_dict)
# #%%
# df_plt_z2=df_plt_z2.rename(columns={'DMI':'DMI_z2'})
# df_cd=pd.DataFrame()
# df_cd=df_plt_z4.merge(df_plt_z2,how='left', left_on='DMI', right_on='DMI_z2')
# #%%
# if df_fwd.empty:

#     print(df_cd.head()) 

# else:
# #%%
# df_cd_nearest=nearest(df_fwd,df_cd)
# df_cd_nearest=df_cd_nearest.reset_index()
# # df_pltz4_nearest=nearest(df_fwd,df_plt_z4)
# # df_pltz4_nearest=df_pltz4_nearest.reset_index()
# #print("df_cd_nearest_head",df_cd_nearest.head())
# #%%
# df_fwd_m=df_fwd[["DMI","D0","D48","SCI","BDI","BCI","Lat","Long"]].copy() #some dont have AUPP calculated
# df_fwd_m=df_fwd_m.rename(columns={'DMI':'DMI_fwd','Lat':'Lat_fwd','Long':'Long_fwd'})
# df_cd_fwd=pd.concat([df_cd_nearest,df_fwd_m], axis=1)
# df_cd_fwd=df_cd_fwd.rename(columns={'DMI':'DMI_id'})


# #df_merged=pd.DataFrame()
# df_cd_f=df_cd.merge(df_cd_fwd,how='left', left_on='DMI', right_on='DMI_id')

# print (df_cd_f.head())
# # %%

# %%
# df_aashto_z2=aashto_z2(df_aashto)
# df_aashto_z4=aashto_z4(df_aashto)

# df_aashto_z4=aashto_dmi(df_aashto_z4)
# df_aashto_z2=aashto_dmi(df_aashto_z2)

# df_plt_z4=df_aashto_z4[["DMI","Density"]].copy()
# # RIRI_dict = dict(zip(df_IRI.RefDMI_road, df_IRI.R_IRI))
# # df_plt_z4['R_IRI']=df_plt_z4['DMI'].map(RIRI_dict)
# df_plt_z2=df_aashto_z2[["DMI","Density"]].copy()

# # %%
# cdz4_dict=dict(zip(df_plt_z4.DMI,df_plt_z4.Density))
# df_IRI['density_z4']=df_IRI["RefDMI_road"].map(cdz4_dict)
# cdz2_dict=dict(zip(df_plt_z2.DMI,df_plt_z2.Density))
# df_IRI['density_z2']=df_IRI["RefDMI_road"].map(cdz2_dict)

# # %%
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

# %%
