#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#%%
#df_IRI=pd.read_csv('/Users/jhasneha/Documents/SPRINDOT/summer2021/SPRINDOT/Roads_3d/Stateroads/SR57/GLL#41 SR-57 RP-49+55 to 50+75SR57 SB-PL-20201027.130712Result-IRI-report.csv')
df_uks=pd.read_csv('/Users/jhasneha/Documents/fall2021/sprindot/crackdensity_ukscanner/GLL#41 SR-57 RP-49+55 to 50+75SR57 NB-20201027.125900Result_UKScan-report.csv')
df_ashhto=pd.read_csv('/Users/jhasneha/Documents/SPRINDOT/summer2021/SPRINDOT/Roads_3d/Stateroads/SR57/GLL#41 SR-57 RP-49+55 to 50+75SR57 SB-PL-20201027.130712Result-AASHTO_Result.csv')
df_uks.columns = df_uks.columns.str.replace(' ', '')
df_uks.columns = df_uks.columns.str.replace(r'\([^)]*\)', '')
df_aashto.columns = df_aashto.columns.str.replace(' ', '')
df_aashto.columns = df_aashto.columns.str.replace(r'\([^)]*\)', '')
# %%
df_uk=df_uks[["Zone_2","Zone_4","DM"]].copy()
# %%
df_uk[["ratio_z2","Percent_z2"]]=df_uks["Zone_2"].str.split('(',expand= True)
df_uk[["ratio_z4","Percent_z4"]]=df_uks["Zone_4"].str.split('(',expand= True)
#%%
df_uk["Percent_z4"]=df_uk["Percent_z4"].replace(r'[% )]','',regex=True).astype(float)
df_uk["Percent_z2"]=df_uk["Percent_z2"].replace(r'[% )]','',regex=True).astype(float)



#%%
def aashto_z2(df_ashhto):
        df_ashhto_2=df_ashhto.copy()
        df_ashhto_2['Zone'] = df_ashhto_2['Zone'].replace(4, np.nan)
        df_ashhto_2= df_ashhto_2.dropna(axis=0, subset=['Zone'])
        return(df_ashhto_2)

#%%
def aashto_z4(df_ashhto):
        df_ashhto_4=df_ashhto.copy()
        df_ashhto_4['Zone'] = df_ashhto_4['Zone'].replace(2, np.nan)
        df_ashhto_4= df_ashhto_4.dropna(axis=0, subset=['Zone'])
        return(df_ashhto_4)
#%%
def aashto_dmi(df_ashhto):
    df_ashhto["DMI"]=6
    df_ashhto.loc[df_ashhto.index[0],"DMI"]=0
    df_ashhto["DMI"]=df_ashhto["DMI"].cumsum()
    return(df_ashhto)

#%%
df_aashto_z2=aashto_z2(df_aashto)
df_aashto_z4=aashto_z4(df_aashto)
df_aashto_z2=aashto_dmi(df_aashto_z2)
df_aashto_z4=aashto_dmi(df_aashto_z4)
# %%

