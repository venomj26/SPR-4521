# %%
import pandas as pd
import geopandas
df_IRI=pd.read_csv('/Users/jhasneha/Documents/SPRINDOT/summer2021/SPRINDOT/Roads_3d/Stateroads/SR57/GLL#41 SR-57 RP-49+55 to 50+75SR57 SB-PL-20201027.130712Result-IRI-report.csv')
df_aashto=pd.read_csv('/Users/jhasneha/Documents/SPRINDOT/summer2021/SPRINDOT/Roads_3d/Stateroads/SR57/GLL#41 SR-57 RP-49+55 to 50+75SR57 SB-PL-20201027.130712Result-AASHTO_Result.csv')
df_fwd=pd.read_excel('/Users/jhasneha/Documents/SPRINDOT/summer2021/SPRINDOT/Roads_3d/Stateroads/SR57/SR 57_fwd/SR-57 NB RP-49+55 to RP-50+75  AC.xlsx',sheet_name="Sheet1")

#df_j4=pd.read_csv('/Users/jhasneha/Documents/DOE/summer2021/Re__Ault_Harvest_Data/gott_east93_2012_harvest.csv',dtype="unicode", encoding= 'unicode_escape')
df_IRI.columns = df_IRI.columns.str.replace(' ', '')
df_IRI.columns = df_IRI.columns.str.replace(r'\([^)]*\)', '')
df_aashto.columns = df_aashto.columns.str.replace(' ', '')
df_aashto.columns = df_aashto.columns.str.replace(r'\([^)]*\)', '')
df_IRI.columns = df_IRI.columns.str.replace(' ', '')
df_IRI.columns = df_IRI.columns.str.replace(r'\([^)]*\)', '')
df_fwd.columns = df_fwd.columns.str.replace(' ', '')
df_fwd.columns = df_fwd.columns.str.replace(r'\([^)]*\)', '')
df_fwd.columns = df_fwd.columns.str.replace(' ', '')
df_fwd.columns = df_fwd.columns.str.replace(r'\([^)]*\)', '')

df_fwd=df_fwd.rename(columns={"SBorWBFWDStation":"DMI","NBorEBFWDStation":"DMI"})
df_fwd=df_fwd.rename(columns={"SubgradeDeflection":"D48"})
df_fwd=df_fwd.rename(columns={"SurfaceDeflection":"D0"})
df_fwd=df_fwd.rename(columns={"SCI300":"SCI"})

#%%
dfIRI_map=df_IRI[["L_IRI","GPSLng","GPSLat"]].copy()


high_iri=dfIRI_map.L_IRI.quantile(0.999)
dfIRI_map = dfIRI_map[dfIRI_map["L_IRI"] <=high_iri] 

#dfj4_map=dfj4_map.iloc[::50,:]
gdf_iri = geopandas.GeoDataFrame(
    dfIRI_map, geometry=geopandas.points_from_xy(dfIRI_map.GPSLng, dfIRI_map.GPSLat))
# %%
import plotly.express as px


geo_df = gdf_iri
geo_df["L_IRI"]=geo_df["L_IRI"].astype(float) 
px.set_mapbox_access_token(open("mbtoken.mapbox_token").read())
fig = px.scatter_mapbox(geo_df,
                        lat=geo_df.geometry.y,
                        lon=geo_df.geometry.x,
                        hover_name="L_IRI",
                        mapbox_style="streets",
                        color="L_IRI",
                        #color_discrete_sequence=("red","blue","green"),
                        zoom=10,
                        size_max=3,
                        height=900)

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.write_html("iri_test.html")
fig.show()

#%%
from merge_parameters import merged_cd_iri_fwd
df_merged= merged_cd_iri_fwd(df_aashto,df_IRI,df_fwd)



#%%
df_merged=df_merged.rename(columns={'Density_x_x':'density_z4','R_IRI_x':'R_IRI','Density_y_x':'density_z2','L_IRI_x':'L_IRI'})
lat_dict= dict(zip(df_IRI.RefDMI, df_IRI.GPSLat))
df_merged['Latitude']=df_merged['DMI'].map(lat_dict)
lon_dict= dict(zip(df_IRI.RefDMI, df_IRI.GPSLng))
df_merged['Longitude']=df_merged['DMI'].map(lon_dict)














#%%
cond1 = [
    ((df_merged['L_iri']>270)| (df_merged['R_iri']>270) |  )
    ((df_merged['L_IRI'] > 270) & (df_merged['L_IRI'] < 1000)) | ((df_merged['R_IRI'] > 270) & (df_merged['R_IRI'] <1000)) | ((df_merged['D0']>24.6) | (df_merged['SCI']>8) | (df_merged['BDI']>8)),
    ((df_merged['D48']>1.80) | (df_merged['BCI']>4)),
    (df_merged['L_IRI'] > 1000) | (df_merged['R_IRI'] >1000),
    (df_merged['D48']<=1.80) & (df_merged['BCI']<=4) & (df_merged['D0']<=24.6) & (df_merged['L_IRI'] <= 270) & (df_merged['R_IRI'] <= 270)  & (df_merged['BDI']<=4.5)]
choice1 = ['Surface_patching', 'Full_depth_patching','High_IRI', 'Good_condition']
df_merged['Patching_color_map'] = np.select(cond1, choice1, default='need_to_be_checked')

"""################### new"""
"""@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"""
#%%
cond_new = [
    ((df_merged['L_IRI']>1000)| (df_merged['R_IRI']>1000)),
    ((df_merged['L_IRI'] > 330) & (df_merged['L_IRI'] < 1000)) | ((df_merged['R_IRI'] > 330) & (df_merged['R_IRI'] <1000)) | ((df_merged['D48']>1.8) | (df_merged['SCI']>8)),
    ((df_merged['D48']>1.80) | (df_merged['BCI']>4)),
    (((df_merged['L_IRI'] > 330) & (df_merged['L_IRI'] < 1000)) | ((df_merged['R_IRI'] > 330) & (df_merged['R_IRI'] <1000)) | ((df_merged['D48']>1.4) & (df_merged['D48']<1.80)) | ((df_merged['BCI']>3) & (df_merged['BCI']<4)) | (df_merged['BDI']>8.8)),
    (((df_merged['L_IRI'] > 330) & (df_merged['L_IRI'] < 1000)) | ((df_merged['R_IRI'] > 330) & (df_merged['R_IRI'] <1000))|((df_merged['BDI']<8.8) &(df_merged['BDI']>4.5))|(df_merged['SCI']>8)|(df_merged['D0']>36.4)),  
    (((df_merged['L_IRI'] > 70) & (df_merged['L_IRI'] < 330)) | ((df_merged['R_IRI'] > 70) & (df_merged['R_IRI'] <330))|((df_merged['SCI']>6) & (df_merged['SCI']<8))|((df_merged['D0']>24.6)&(df_merged['D0']<36.4))),   
    ((df_merged['L_IRI'] < 70) & (df_merged['R_IRI'] < 70) & (df_merged['D48']<1.8) & (df_merged['BCI']<3) &(df_merged['BDI']<4.5)& (df_merged['SCI']<6)&(df_merged['D0']<24.6)),
    ((df_merged['L_IRI'] < 70) & (df_merged['R_IRI'] < 70) )]
choice_new = ['high_IRI', 'Full_depth_patching','Full_depth_patching_fwd','Full_depth_patching_warning','Surface_patching','Surface_patching_warning', 'Good_condition','Good_condition']
df_merged['Patching_color_map'] = np.select(cond_new, choice_new, default='need_to_be_checked')






#%%
patching_depth={'Good_condition':1,'high_IRI':8, 'Full_depth_patching':7,'Full_depth_patching_fwd':6,'Full_depth_patching_warning':5,'Surface_patching':3,'Surface_patching_warning':2,'need_to_be_checked':4}
df_merged['Patching_depth']=df_merged['Patching_color_map'].map(patching_depth)

"""@@@@@@@@@@@@@@@@@@@@@@@@@

this is for the patching table for the app

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"""

#%%
patching_color={1:'green',8:'blue', 7:'red',6:'orangered',5:'orange',3:'salmon',2:'yellow',4:'grey'}
df_merged['Patching_color']=df_merged['Patching_depth'].map(patching_color)
df_merged=df_merged.fillna(0.0)


# %%
import geopandas
#df_IRI=pd.read_csv('/Users/jhasneha/Documents/SPRINDOT/summer2021/SPRINDOT/I64/WB_DL_78-85/GLL#3 I-64 RP-78+00 to RP-85+00WB DL-20180327.122648Result_IRI-report_6ft.csv')
#df_j4=pd.read_csv('/Users/jhasneha/Documents/DOE/summer2021/Re__Ault_Harvest_Data/gott_east93_2012_harvest.csv',dtype="unicode", encoding= 'unicode_escape')

#%%
gdf_iri = geopandas.GeoDataFrame(
    df_merged, geometry=geopandas.points_from_xy(df_merged.Longitude, df_merged.Latitude))
# %%
import plotly.express as px


geo_df = gdf_iri
#geo_df[" L_IRI(in/mi)"]=geo_df[" L_IRI(in/mi)"].astype(float) 
#df_merged["text"]=
px.set_mapbox_access_token(open("mbtoken.mapbox_token").read())
fig = px.scatter_mapbox(geo_df,
                        lat=geo_df.geometry.y,
                        lon=geo_df.geometry.x,
                        hover_name="Patching_color_map",
                        mapbox_style="streets",
                        color="Patching_depth",
                        color_continuous_scale=px.colors.diverging.Temps,
                        zoom=10,
                        size_max=3,
                        height=900)

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.write_html("iri_test_SR57.html")
fig.show()
#%%
"""+++++++++++++++++++++++++++++++++++++

    creating linestring from points

+++++++++++++++++=+++++=====+=====++============"""



#%%
geom0 = gdf_iri.loc[0]['geometry']
geom1 = gdf_iri.loc[1]['geometry']

print("Geometry type:", str(type(geom0)))
print(f"geom0 coordinates: {geom0.x}, {geom0.y}")
print(f"geom1 coordinates: {geom1.x}, {geom1.y}")

#%%
# Create LineString from coordinates
from shapely.geometry import LineString
start, end = [(geom0.x, geom0.y), (geom1.x, geom1.y)]
line = LineString([start, end])
print(f"Geometry type: {str(type(line))}")
line

#%%
""" -------------------------------------------------
creating function to convert all points to linestring
------------------------------------------------------"""

def make_lines(gdf, df_out, i, geometry = 'geometry'):
    geom0 = gdf.loc[i][geometry]
    geom1 = gdf.loc[i + 1][geometry]
    
    start, end = [(geom0.x, geom0.y), (geom1.x, geom1.y)]
    line = LineString([start, end])
    
    # Create a DataFrame to hold record
    data = {'id': i,
            'geometry': [line]}
    df_line = pd.DataFrame(data, columns = ['id', 'geometry'])
    
    # Add record DataFrame of compiled records
    df_out = pd.concat([df_out, df_line])
    return df_out

#%%
#calling the linestring making function from above
# initialize an output DataFrame
df_iri_ls = pd.DataFrame(columns = ['id', 'geometry'])

# Loop through each row of the input point GeoDataFrame
x = 0
while x < len(gdf_iri) - 1:
    df_iri_ls = make_lines(gdf_iri, df_iri_ls, x)
    x = x + 1
    
df_iri_ls.head()


#%%

df_merged = df_merged.reset_index() #to be used once
ls_dict= dict(zip(df_iri_ls.id, df_iri_ls.geometry))
df_merged['geometry_ls']=df_merged['level_0'].map(ls_dict)



#%%
import plotly.express as px


geo_df_ls = gdf_iri
#geo_df[" L_IRI(in/mi)"]=geo_df[" L_IRI(in/mi)"].astype(float) 
#df_merged["text"]=
px.set_mapbox_access_token(open("mbtoken.mapbox_token").read())
fig = px.scatter_mapbox(geo_df_ls,
                        lat=geo_df.geometry.y,
                        lon=geo_df.geometry.x,
                        hover_name="Patching_color_map",
                        mapbox_style="streets",
                        color="Patching_depth",
                        color_continuous_scale=px.colors.diverging.Temps,
                        zoom=10,
                        size_max=8,
                        height=900)

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.write_html("iri_test_SR57.html")
fig.show()


#%%
import plotly.express as px
import geopandas as gpd
import shapely.geometry
import numpy as np
px.set_mapbox_access_token(open("mbtoken.mapbox_token").read())
geo_df = df_merged

lats = []
lons = []
names = []
#colors= []
for feature, name, color in zip(geo_df.geometry_ls, geo_df.Patching_color_map,geo_df.Patching_depth):
    if isinstance(feature, shapely.geometry.linestring.LineString):
        linestrings = [feature]
    else:
        continue
    for linestring in linestrings:
        x, y = linestring.xy
        lats = np.append(lats, y)
        lons = np.append(lons, x)
        names = np.append(names, [name]*len(y))
        #colors = np.append(colors, [color]*len(y))
        lats = np.append(lats, None)
        lons = np.append(lons, None)
        names = np.append(names, None)
        #colors=np.append(colors, None)

from colormap import rgb2hex
import matplotlib.colors

cmap = matplotlib.colors.LinearSegmentedColormap.from_list("gyr", [[0.0, 'green'], [0.5, 'yellow'], [1.0, 'red']], N=8)
discr_map = {}
for i in range(0, 8, 1):
    discr_map.update({"c"+str(i): rgb2hex(int(255 * cmap(i)[0]), int(255 * cmap(i)[1]), int(255 * cmap(i)[2]))})

#discr_map={"1":"green","2":"lightgreen","3":"yellow","4":"black","5":"orange","6":"salmon","7":"red","8":"blue"}

fig = px.line_mapbox(geo_df,lat=lats, lon=lons, 
                        hover_name=names,
                        line_group=names,
                        #color="Patching_depth",
                        color_discrete_map=discr_map, 
                        mapbox_style="streets", 
                        height=900)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update_traces(line=dict(width=4))
fig.write_html("iri_test_lines.html")

fig.show()

##%%
from geopandas import GeoDataFrame
crs = {'init': 'epsg:4326'}
gdf = GeoDataFrame(df_merged, crs=crs, geometry=df_merged["geometry_ls"])
ax = gdf.plot(cmap="viridis") 
gdf=gdf.drop(columns="geometry_ls")
#%%
import os
import folium

print(folium.__version__)

#%%
indiana_map = folium.Map([40.2672,-86.1349], zoom_start=12.4, tiles='cartodbpositron')
#gdf=gdf.drop(["geometry_ls"], axis=1)
folium.GeoJson(gdf).add_to(indiana_map)
# plot map
indiana_map

#%%
gdf['geometry'] = gdf['geometry'].replace("None", np.nan)
gdf= gdf.dropna(axis=0, subset=['geometry'])

#%%
import branca.colormap as cm
import math
import folium
from folium.features import GeoJsonPopup, GeoJsonTooltip


f2 = folium.Figure(height = 400)
indiana_map = folium.Map([38.195889,-87.288635],zoom_start=12,#tiles="cartodbpositron")
                    tiles='https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
                    # access_token='pk.eyJ1IjoidmVub21qIiwiYSI6ImNrY3Z0c3ZhYzA3cHYyeHFsZXk4cXQwMmIifQ.kYc2bb8QRPiZ1L9CBqgtLw',
                    attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>')

max_p = math.ceil(df_merged['Patching_depth'].max())
step = cm.StepColormap(['green','yellow'],vmin=0,vmax=max_p, caption="Good_condition:0,Surface_patching:1, Full_depth_patching:2,High_IRI:3")
#patching_depth={'Good_condition':1,'Surface_patching':2, 'Full_depth_patching':3, 'High_IRI':4,'need_to_be_checked':5}
print(step)
# popup = GeoJsonPopup(
#     fields=["DMI", "D0"],
#     aliases=["DMI_", "D0_"],
#     localize=True,
#     labels=True,
#     style="background-color: limegreen;",
# )

tooltip = GeoJsonTooltip(
    fields=["DMI", "D0", "D48","L_IRI","R_IRI","Patching_color_map"],
    aliases=["DMI:", "Surface:", "Subgrade:","L_IRI:","R_IRI:","Patching:"],
    localize=True,
    sticky=False,
    labels=True,
    style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """,
    max_width=800,
)
print("before g", tooltip)
#%%
g = folium.GeoJson(
    gdf
    #popup=popup,
).add_to(indiana_map)

step.add_to(indiana_map)
#indiana_map.save("I-64-RP-39+15-RP-48-70eb-Pl.html")
indiana_map


#%%
""" -----------------------------------------
EXAMPLE LEAFLET MAP LAYERS WHICH ARE FREE 
-----------------------------------------------"""

# var CartoDB_DarkMatter = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
# 	attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
# 	subdomains: 'abcd',
# 	maxZoom: 19
# });

# var HikeBike_HikeBike = L.tileLayer('https://tiles.wmflabs.org/hikebike/{z}/{x}/{y}.png', {
# 	maxZoom: 19,
# 	attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
# });

var USGS_USTopo = L.tileLayer('https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer/tile/{z}/{y}/{x}', {
	maxZoom: 20,
	attribution: 'Tiles courtesy of the <a href="https://usgs.gov/">U.S. Geological Survey</a>'
});

var USGS_USImageryTopo = L.tileLayer('https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryTopo/MapServer/tile/{z}/{y}/{x}', {
	maxZoom: 20,
	attribution: 'Tiles courtesy of the <a href="https://usgs.gov/">U.S. Geological Survey</a>'
});

var Jawg_Streets = L.tileLayer('https://{s}.tile.jawg.io/jawg-streets/{z}/{x}/{y}{r}.png?access-token={accessToken}', {
	attribution: '<a href="http://jawg.io" title="Tiles Courtesy of Jawg Maps" target="_blank">&copy; <b>Jawg</b>Maps</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
	minZoom: 0,
	maxZoom: 22,
	subdomains: 'abcd',
	accessToken: '<your accessToken>'
});

var OpenStreetMap_Mapnik = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
	maxZoom: 19,
	attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
});

var Esri_WorldStreetMap = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {
	attribution: 'Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012'
});
""" -----------------------------------------
EXAMPLE LEAFLET MAP LAYERS WHICH ARE FREE 
-----------------------------------------------"""






#%%
# Create LineString from coordinates

start, end = [(geom0.x, geom0.y), (geom1.x, geom1.y)]
gdf["line"] = ([start, end])











# %%
