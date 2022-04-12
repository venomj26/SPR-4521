#%%
import pandas as pd, json
import numpy as np
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster
import os
import openpyxl
import gmaps

# %%
df_map=pd.read_csv('/Users/jhasneha/Documents/DOE/summer2021/DOE_ag/Soil data/SEPAC/J4/j4_2007_J4_nobuffer_harvest.csv')
df_map['Latitude']=df_map['Latitude'].astype(float)
df_map['Longitude']=df_map['Longitude'].astype(float)


#%%
m = folium.Map(location=[45.5236, -122.6750], zoom_start=12)
m
#.save("/Users/jhasneha/Documents/Spring2021/SPR_indot/SPRprojectcodes/html_files/map.html")

#%%
m = folium.Map(
   location=[45.523, -122.675],
   zoom_start=12,
   tiles='https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
   attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>')

m





# %%
df_map_resampled=df_map.iloc[::20, :]

df_speed=df_map_resampled[["Latitude","Longitude","ELEVATION_","SPEED_MPH_"]].copy()
# %%
df_speed_h=df_speed.head(4)

#%%
#overlay= os.path.join('data','dataset.js')
map1 = f"/Users/jhasneha/Documents/Spring2021/SPR_indot/SPRprojectcodes/map1.geojson"
m_t = folium.Map(
    location=[ 38.9915, -85.6846],
    tiles='https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
    attr='Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
    zoom_start=12
)

folium.GeoJson(map1, name="trial").add_to(m_t)
m_t
#m_t.save("speed.html")
#print("map_saved")


# %%

#%%
import pandas as pd
import geojson

def data2geojson(df):
    features = []
    insert_features = lambda X: features.append(
            geojson.Feature(geometry=geojson.Point((X["Latitude"],
                                                    X["Longitude"],
                                                    X["ELEVATION_"])),
                            properties=dict(speed=X["SPEED_MPH_"])))
    df.apply(insert_features, axis=1)
    with open('map1.geojson', 'w', encoding='utf8') as fp:
        geojson.dump(geojson.FeatureCollection(features), fp, sort_keys=True, ensure_ascii=False)

# col = ['lat','long','elev','name','description']
# data = [[-29.9953,-70.5867,760,'A','Place ñ'],
#         [-30.1217,-70.4933,1250,'B','Place b'],
#         [-30.0953,-70.5008,1185,'C','Place c']]

#df = pd.DataFrame(data, columns=col)

data2geojson(df_speed_h)
#%%
import requests
url = (
    "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data"
)
antarctic_ice_edge = f"{url}/antarctic_ice_edge.json"
antarctic_ice_shelf_topo = f"{url}/antarctic_ice_shelf_topo.json"


# m = folium.Map(
#     location=[-59.1759, -11.6016],
#     tiles="cartodbpositron",
#     zoom_start=2,
# )

folium.GeoJson(antarctic_ice_edge, name="geojson").add_to(m_t)


folium.TopoJson(
    json.loads(requests.get(antarctic_ice_shelf_topo).text),
    "objects.antarctic_ice_shelf",
    name="topojson",
).add_to(m)

folium.LayerControl().add_to(m_t)

#%%
m_t



# %%
import simplekml
df_US31=pd.read_excel("/Users/jhasneha/Documents/fall2021/sprindot/US 31_Patch SB_1383498.xlsx", sheet_name="US 31 Patch SB PL")
df_US31=df_US31[2:]
df_US31.columns=df_US31.iloc[0]
df_US31=df_US31.drop([2])
df_US31=df_US31.reset_index()
df_US31=df_US31.drop(["index"], axis=1)
df_US31["RP_actual"]=df_US31["RP"]+df_US31["RP Offset"]
df_US31["description"]="L_IRI="+ df_US31[" L_IRI"].astype(str) + "," + "R_IRI= " + df_US31["R_IRI"].astype(str) 
# %%
kml=simplekml.Kml()
df_US31.apply(lambda X: kml.newpoint(name=X["RP_actual"], description= X["description"], coords=[( X["Longitude"],X["Latitude"])]) ,axis=1)
kml.save("US31_SBPL.kml")
# %%
