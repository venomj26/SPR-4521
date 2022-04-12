#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gmaps


#%%
from dotenv import load_dotenv
from pathlib import Path
import os
 
load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)
google_KEY = os.getenv("googleapi")
gmaps.configure(api_key='AIzaSyD92EVDPuhc-IE7hDCnHxWbds_NbYBq-yQ')
#%%
df_ukscanner=pd.read_csv('/Users/jhasneha/Documents/Spring2021/SPR_indot/data/6ft/UKScan-report_6ft.csv')
df_ashhto=pd.read_csv('/Users/jhasneha/Documents/Spring2021/SPR_indot/data/6ft/AASHTO_Result_6ft.csv')
df_IRI=pd.read_csv('/Users/jhasneha/Documents/Spring2021/SPR_indot/data/6ft/IRI-report_6ft.csv')
df_ukscanner.columns = df_ukscanner.columns.str.replace(' ', '')
df_ukscanner.columns = df_ukscanner.columns.str.replace(r'\([^)]*\)', '')
df_ashhto.columns = df_ashhto.columns.str.replace(' ', '')
df_ashhto.columns = df_ashhto.columns.str.replace(r'\([^)]*\)', '')
df_IRI.columns = df_IRI.columns.str.replace(' ', '')
df_IRI.columns = df_IRI.columns.str.replace(r'\([^)]*\)', '')
#df_IRIF = df_IRI[df_IRI["R_IRI"] <= 500] 
#df_IRIFF = df_IRIF[df_IRIF["L_IRI"] <= 500] 
df_IRIFF=df_IRI.copy()


"""-----------------------------------------------
checking the crack density data from Yaguang
--------------------------------------------------"""


# #%%
# df_ashhto=pd.read_csv('/Users/jhasneha/Documents/Spring2021/SPR_indot/data/6ft/AASHTO_Result_6ftFrame_Yaguang_20210506.csv')
# df_ashhto.columns = df_ashhto.columns.str.replace(' ', '')
# df_ashhto.columns = df_ashhto.columns.str.replace(r'\([^)]*\)', '')

# #%%
# df_check=pd.DataFrame()
# for index,row in df_EB.iterrows():
#     index_value=int(row["DMI"])
#     ind= df_ashhto_2['DMI'].sub(index_value).abs().idxmin()
#     df_test =df_ashhto_2.loc[ind,:]
#     df_check=df_check.append(df_test,ignore_index=True)


# #%%
# df_ashhto_2=df_ashhto
# df_ashhto_2['Zone'] = df_ashhto_2['Zone'].replace([1,4,3,5], np.nan)
# df_ashhto_2= df_ashhto_2.dropna(axis=0, subset=['Zone'])
# df_ashhto_2["DMI"]=6
# df_ashhto_2.loc[df_ashhto_2.index[0],"DMI"]=0
# df_ashhto_2["DMI"]=df_ashhto_2["DMI"].cumsum()

#%%
df_ashhto_2=df_ashhto
df_ashhto_2['Zone'] = df_ashhto_2['Zone'].replace(4, np.nan)
df_ashhto_2= df_ashhto_2.dropna(axis=0, subset=['Zone'])


#%%
df_ashhto_4=df_ashhto
df_ashhto_4['Zone'] = df_ashhto_4['Zone'].replace(2, np.nan)
df_ashhto_4= df_ashhto_4.dropna(axis=0, subset=['Zone'])


# %%
df_ashhto_2["DMI"]=6
df_ashhto_2.loc[df_ashhto_2.index[0],"DMI"]=0
df_ashhto_2["DMI"]=df_ashhto_2["DMI"].cumsum()



# %%
df_ashhto_4["DMI"]=6
df_ashhto_4.loc[df_ashhto_4.index[0],"DMI"]=0
df_ashhto_4["DMI"]=df_ashhto_4["DMI"].cumsum()


# %%

#merging all the values  CD, IRI into a single dataframe using dictionary mapping
df_plot=df_ashhto_2[['DMI','Density']].copy()
UK_dict = dict(zip(df_ukscanner.EndLogMi, df_ukscanner.Percent))
df_plot['UK_Scanner']=df_plot['DMI'].map(UK_dict)
ashhto_dict_4 = dict(zip(df_ashhto_4.DMI, df_ashhto_4.Density))
df_plot['Density_ashhto4']=df_plot['DMI'].map(ashhto_dict_4)
IRI_dict = dict(zip(df_IRIFF.RefDMI, df_IRIFF.L_IRI))
df_plot['L_IRI']=df_plot['DMI'].map(IRI_dict)
IRI_dict = dict(zip(df_IRIFF.RefDMI, df_IRIFF.R_IRI))
df_plot['R_IRI']=df_plot['DMI'].map(IRI_dict)
df_plot.UK_Scanner=df_plot.UK_Scanner*100
df_plot.Density=df_plot.Density*100
df_plot.Density_ashhto4=df_plot.Density_ashhto4*100



# %%
#reading the FWD data 
import openpyxl
df_EB=pd.read_excel("/Users/jhasneha/Documents/Spring2021/SPR_indot/SPRprojectcodes/data/I70 (DL).xlsx", sheet_name="I70-EB")
df_EB.columns = df_EB.columns.str.replace(' ', '')
df_EB.columns = df_EB.columns.str.replace(r'\([^)]*\)', '')





"""------------------
 FWD comparison with IRI 
 -----------------------"""

#%%
appended_df_IRI=pd.DataFrame()
for index,row in df_EB.iterrows():
    index_value=int(row["DMI"])
    ind= df_IRIFF['RefDMI'].sub(index_value).abs().idxmin()
    df_test =df_IRIFF.loc[ind,:]
    appended_df_IRI=appended_df_IRI.append(df_test,ignore_index=True)

# %%
df_EB_map=df_EB[["Latitude","Longitude","D0"]].copy()
location=df_EB_map[["Latitude","Longitude"]]
data=df_EB_map["D0"]
location_IRI=appended_df_IRI[["GPSLat","GPSLng"]]
data_IRI=appended_df_IRI["L_IRI"]




#%%
#data = [(51.5, 1), (51.7, 2), (51.4, 2), (51.49, 1)]

fig = gmaps.Map()
fig = gmaps.figure(map_type='ROADMAP')

heatmap_layer = gmaps.WeightedHeatmap(locations=location, weights=data)
# heatmap_layer.gradient = [
#     'white',
#     'green',
#     'blue'

# ]
fig.add_layer(heatmap_layer)
heatmap_layer1 = gmaps.WeightedHeatmap(locations=location_IRI, weights=data_IRI)
heatmap_layer1.gradient = [
    'white',
    'black',
    'yellow'

]

fig.add_layer(heatmap_layer1)
fig


# %%

heatmap_layer.max_intensity = 10
heatmap_layer.point_radius = 10
heatmap_layer1.max_intensity = 30
heatmap_layer1.point_radius = 10
heatmap_layer1.opacity = 0.5
heatmap_layer.opacity = 1.0
# %%

# %%
from ipywidgets.embed import embed_minimal_html
embed_minimal_html('export_Liri_D48.html', views=[fig])

# %%



"""------------------
 IRI comparison with CD 
 -----------------------"""




#%%
df_map=df_IRIFF.copy()
ashhto_dict_2 = dict(zip(df_ashhto_2.DMI, df_ashhto_2.Density))
df_map['Density_2']=df_map['RefDMI'].map(ashhto_dict_2)
ashhto_dict_4 = dict(zip(df_ashhto_4.DMI, df_ashhto_4.Density))
df_map['Density_4']=df_map['RefDMI'].map(ashhto_dict_2)

#%%
df_map['Density_2'] = df_map['Density_2'].replace(0, np.nan)
df_map= df_map.dropna(axis=0, subset=['Density_2'])
#%%
df_map['Density_4'] = df_map['Density_4'].replace(0, np.nan)
df_map= df_map.dropna(axis=0, subset=['Density_4'])

#%%
df_map["GPSLng_mod"]=df_map["GPSLng"]+0.00001
#%%
#Comparing density and IRI we have the whole bigger length of road of interest

location_IRI=df_map[["GPSLat","GPSLng"]]
data_LIRI=df_map["L_IRI"]
data_RIRI=df_map["R_IRI"]

location_CD=df_map[["GPSLat","GPSLng_mod"]]
data_cd2=df_map["Density_2"]
data_cd4=df_map["Density_4"]

#%%
#data = [(51.5, 1), (51.7, 2), (51.4, 2), (51.49, 1)]

fig1 = gmaps.Map()
#fig.add_layer(gmaps.traffic_layer())
#gmaps.figure(map_type='TERRAIN')

heatmap_layer = gmaps.WeightedHeatmap(locations=location_CD, weights=data_cd4)

fig1.add_layer(heatmap_layer)
heatmap_layer1 = gmaps.WeightedHeatmap(locations=location_IRI, weights=data_RIRI)
heatmap_layer1.gradient = [
    'white',
    'red',
    'black',

]

fig1.add_layer(heatmap_layer1)

fig1


# %%

heatmap_layer.max_intensity = 1
heatmap_layer.point_radius = 8
heatmap_layer1.max_intensity = 1
heatmap_layer1.point_radius = 8
heatmap_layer1.opacity = 0.3 #this is causing the map layer opacoty to change
heatmap_layer.opacity = 1.0
# %%

# %%
from ipywidgets.embed import embed_minimal_html
embed_minimal_html('export_riricd4_check.html', views=[fig1])
# %%


"""------------------
 FWD comparison with CD 
 -----------------------"""

#use IRI lat lon for crack density and compare it with FWD data
#%%
appended_df_CD=pd.DataFrame()
for index,row in df_EB.iterrows():
    index_value=int(row["DMI"])
    ind= df_map['RefDMI'].sub(index_value).abs().idxmin()
    df_test =df_map.loc[ind,:]
    appended_df_CD=appended_df_CD.append(df_test,ignore_index=True)


#%%
#appended_df_CD['Density_2'] = appended_df_CD['Density_2'].replace(0.001, np.nan)

#%%
#Comparing density and FWD we have the whole bigger length of road of interest

location=df_EB[["Latitude","Longitude"]]
data=df_EB["D0"]

location_CD=appended_df_CD[["GPSLat","GPSLng"]]
data_cd2=appended_df_CD["Density_2"]
data_cd4=appended_df_CD["Density_4"]

#%%

#data = [(51.5, 1), (51.7, 2), (51.4, 2), (51.49, 1)]

fig2 = gmaps.Map()
#fig.add_layer(gmaps.traffic_layer())
gmaps.figure(map_type='TERRAIN')

heatmap_layer = gmaps.WeightedHeatmap(locations=location, weights=data)

fig2.add_layer(heatmap_layer)
heatmap_layer1 = gmaps.WeightedHeatmap(locations=location_CD, weights=data_cd4)
heatmap_layer1.gradient = [
    'white',
    'black',
    'white',

]

fig2.add_layer(heatmap_layer1)

fig2


# %%

heatmap_layer.max_intensity = 10
heatmap_layer.point_radius = 10
heatmap_layer1.max_intensity = 0.6
heatmap_layer1.point_radius = 10
heatmap_layer1.opacity = 0.5 #this is causing the map layer opacoty to change
heatmap_layer.opacity = 1.0
# %%
# %%
from ipywidgets.embed import embed_minimal_html
embed_minimal_html('export_fwdcd.html', views=[fig2])





""" FWD IRI and CD have values at"""

#%%
appended_df_CD['Density_2'] = appended_df_CD['Density_2'].replace(0, np.nan)

"""---------------------------
Kepler.gl trial
-------------------------------"""

#%%
from keplergl import KeplerGl 
map_1 = KeplerGl(height=500)
map_1
# %%
df_kepler=df_Eb.copy()
df_kepler=df_kepler.rename(columns={})


#%%
map_1.add_data(data=df_EB, name='D0')


"""________________________________________

    Leaflet using python 
___________________________________________"""



# %%
import geopy 
import pandas 
from geopy.geocoders import Nominatim, GoogleV3



#%%
def main():
	io = pandas.read_csv('/Users/jhasneha/Documents/Spring2021/SPR_indot/data/6ft/IRI-report_6ft.csv', index_col=None, header=0, sep=",")
def get_latitude(x):
  return x.latitude

def get_longitude(x):
  return x.longitude


geolocator=Nominatim() #mention Nominatim (timeout=5) when and if throwing error 


#%%
