#%%
import pandas as pd 
import numpy as np
import os 
#from pyxlsb import open_workbook



df_tsd=pd.read_excel("/Users/jhasneha/Library/CloudStorage/OneDrive-purdue.edu/SPR-4521 (Patching)/TSD_Data/Indiana_PFS_2021_01mi_iPAVe_data_1_28_22.xlsb", engine="pyxlsb", sheet_name="Indiana_PFS_2021_01mi_iPAVe")
df_tsd_ref=df_tsd.copy()
#%%
df_tsd_filtered=df_tsd[["ROUTE","FROM","TO","IRI_RIGHT (in/mi)","IRI_LEFT (in/mi)","SURVEY_SPEED (mph)","FROM_LATITUDE (deg)","FROM_LONGITUDE (deg)","TO_LATITUDE (deg)","TO_LONGITUDE (deg)","D0 (mils)","D8 (mils)","D12 (mils)","D18 (mils)","D24 (mils)","D36 (mils)","D48 (mils)","D60 (mils)","D72 (mils)","PERCENT_TOTAL_CRACK (%)","HAWKEYE_URL"]].copy()
df_tsd_filtered.columns = df_tsd_filtered.columns.str.replace(' ', '')
df_tsd_filtered.columns = df_tsd_filtered.columns.str.replace(r'\([^)]*\)', '')


# %%
df_tsd_filtered[["Road","Lane"]] = df_tsd_filtered['ROUTE'].str.split('-', expand=True)
df_tsd_filtered["milePost"]=df_tsd_filtered["FROM"]+"-" +df_tsd_filtered["TO"]
#just for this dataset as processing of FWD deflection data is incomplete. _1 should be multiplied to all value
df_tsd_filtered[["D0","D8","D12","D18","D24","D36","D48","D60","D72"]]=df_tsd_filtered[["D0","D8","D12","D18","D24","D36","D48","D60","D72"]].multiply(-1, axis="index")

df_tsd_filtered["SCI"]=df_tsd_filtered["D8"]-df_tsd_filtered["D24"]
df_tsd_filtered["BDI"]=df_tsd_filtered["D24"]-df_tsd_filtered["D48"]
df_tsd_filtered["BCI"]=df_tsd_filtered["D48"]-df_tsd_filtered["D60"]

#%%
df_tsd_filtered=df_tsd_filtered.rename(columns={"IRI_RIGHT":"R_IRI","IRI_LEFT":"L_IRI"})
# %%
def patchingAlgorithm (merged_df):
    cond_new = [
    ((merged_df['L_IRI']>1000)| (merged_df['R_IRI']>1000)),
    ((merged_df['D60']>1.80) | (merged_df['BCI']>4.0)),
    ((merged_df['L_IRI'] > 270) & (merged_df['L_IRI'] < 1000)) | ((merged_df['R_IRI'] > 270) & (merged_df['R_IRI'] <1000)) | ((merged_df['D60']>1.8) | (merged_df['SCI']>8)),
    (((merged_df['L_IRI'] > 270) & (merged_df['L_IRI'] <= 1000)) | ((merged_df['R_IRI'] > 270) & (merged_df['R_IRI'] <=1000)) | ((merged_df['D60']>1.4) & (merged_df['D60']<=1.80)) | ((merged_df['BCI']>3) & (merged_df['BCI']<=4)) | (merged_df['BDI']>8.8)),
    (((merged_df['L_IRI'] > 270) & (merged_df['L_IRI'] <= 1000)) | ((merged_df['R_IRI'] > 270) & (merged_df['R_IRI'] <=1000))|((merged_df['BDI']<=8.8) &(merged_df['BDI']>4.5))|(merged_df['SCI']>8)|(merged_df['D0']>36.4)| (merged_df['PERCENT_TOTAL_CRACK']>20)),  
    (((merged_df['L_IRI'] > 70) & (merged_df['L_IRI'] <= 330)) | ((merged_df['R_IRI'] > 70) & (merged_df['R_IRI'] <330))|((merged_df['SCI']>6) & (merged_df['SCI']<=8))|((merged_df['D0']>24.6)&(merged_df['D0']<=36.4))|((merged_df['PERCENT_TOTAL_CRACK']>5) &(merged_df['PERCENT_TOTAL_CRACK']<=20))),   
    ((merged_df['L_IRI'] <= 70) & (merged_df['R_IRI'] <= 70) & (merged_df['D60']<=1.4) & (merged_df['BCI']<=3) &(merged_df['BDI']<=4.5)& (merged_df['SCI']<=6)&(merged_df['D0']<=24.6) & (merged_df['PERCENT_TOTAL_CRACK']<=5)),
    ((merged_df['L_IRI'] <= 70) & (merged_df['R_IRI'] <= 70) )]
    choice_new = ['high_IRI', 'Full_depth_patching_fwd','Full_depth_patching','Full_depth_patching_warning','Surface_patching','Surface_patching_warning', 'Good_condition','Good_condition']
    merged_df['Patching_color_map'] = np.select(cond_new, choice_new, default='need_to_be_checked')
    patching_depth={'Good_condition':1,'high_IRI':8, 'Full_depth_patching_fwd':7,'Full_depth_patching':6,'Full_depth_patching_warning':5,'Surface_patching':3,'Surface_patching_warning':2,'need_to_be_checked':4}
    merged_df['Patching_depth']=merged_df['Patching_color_map'].map(patching_depth)
    #this is for patching table for the app
    patching_color={1:'green',8:'blue', 7:'maroon',6:'crimson',5:'salmon',3:'orange',2:'yellow',4:'grey'}
    merged_df['Patching_color']=merged_df['Patching_depth'].map(patching_color)


    return merged_df


# %%
patchingAlgorithm(df_tsd_filtered)
df_tsd_filtered=df_tsd_filtered.fillna(0.00)


#%%
df_ISTSD_Sampled=df_tsd_filtered.groupby("milePost").apply(lambda x: x.sample(frac=.03)).reset_index(drop=True)
# df_IS_Sampled.to_csv("Sampled_patching_IS.csv")
#df_IS_Sampled=df_IS_Sampled.reset_index()
df_ISTSD_Sampled.to_csv("TSDSACData_sampled.csv")

#DMI calculation
#%%
df_tsd_filtered[["MP","FROM"]]=df_tsd_filtered["FROM"].str.split(' ', expand=True)
df_tsd_filtered[["MP_T","TO"]]=df_tsd_filtered["TO"].str.split(' ', expand=True)

df_tsd_filtered["distance"]=df_tsd_filtered["TO"].astype(float) - df_tsd_filtered["FROM"].astype(float)
df_dist=pd.DataFrame()
df_dist=df_tsd_filtered["distance"].value_counts().rename_axis('unique_values').reset_index(name='counts')
df_dist["DMI"]=df_dist["unique_values"]/df_dist["counts"]
df_dist["DMI"]=df_dist["DMI"]*5280

# %%
df_tsd_filtered.to_csv("TSDSACData.csv")




# %%
data_check=pd.read_csv("TSDSACData.csv")
# %%
print("yay")
# %%
