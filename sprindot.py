# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df_12 = pd.read_csv('/Users/jha/Documents/Spring2021/SPR_indot/I70EB_103924/IRI-report_12ft.csv')
x=np.array(df_12["RefDMI(ft)"])
y= np.array(df_12[" L_IRI(in/mi)"])
fig,ax= plt.subplots()
ax.plot(x,y)
plt.show()



# %%
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
directory="/Users/jha/Documents/Spring2021/SPR_indot/I70EB_103924"
fig,ax= plt.subplots()
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        df=pd.read_csv(os.path.join(directory,filename))
        x=np.array(df["RefDMI(ft)"])
        y= np.array(df[" L_IRI(in/mi)"])
        ax.plot(x,y)
        
        continue
    else:
        continue
plt.show()


# %%
# fit an empirical cdf to a bimodal dataset
from matplotlib import pyplot
from numpy.random import normal
from numpy import hstack
from statsmodels.distributions.empirical_distribution import ECDF
# generate a sample
sample1 = normal(loc=20, scale=5, size=300)
sample2 = normal(loc=40, scale=5, size=700)
sample = hstack((sample1, sample2))
# fit a cdf
ecdf = ECDF(sample)
# get cumulative probability for values
print('P(x<20): %.3f' % ecdf(20))
print('P(x<40): %.3f' % ecdf(40))
print('P(x<60): %.3f' % ecdf(60))
# plot the cdf
pyplot.plot(ecdf.x, ecdf.y)
pyplot.show()


# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
fig, (ax1, ax2,ax3,ax4,ax5,ax6) = plt.subplots(nrows=6, ncols=1,sharex=True)
df_12 = pd.read_csv('/Users/jha/Documents/Spring2021/SPR_indot/I70EB_103924/IRI-report_12ft.csv')
df_filtered_12 = df_12[df_12[" L_IRI(in/mi)"] <= 270] 
df_15 = pd.read_csv('/Users/jha/Documents/Spring2021/SPR_indot/I70EB_103924/IRI-report_15ft.csv')
df_filtered_15 = df_15[df_15[" L_IRI(in/mi)"] <= 270] 
df_18 = pd.read_csv('/Users/jha/Documents/Spring2021/SPR_indot/I70EB_103924/IRI-report_18ft.csv')
df_filtered_18 = df_18[df_18[" L_IRI(in/mi)"] <= 270] 
df_20 = pd.read_csv('/Users/jha/Documents/Spring2021/SPR_indot/I70EB_103924/IRI-report_20ft.csv')
df_filtered_20 = df_20[df_20[" L_IRI(in/mi)"] <= 270] 
df_60 = pd.read_csv('/Users/jha/Documents/Spring2021/SPR_indot/I70EB_103924/IRI-report_60ft.csv')
df_filtered_60 = df_60[df_60[" L_IRI(in/mi)"] <= 270] 
df_100 = pd.read_csv('/Users/jha/Documents/Spring2021/SPR_indot/I70EB_103924/IRI-report_100ft.csv')
df_filtered_100 = df_100[df_100[" L_IRI(in/mi)"] <= 270] 
#x=np.array(df_12["RefDMI(ft)"])
#y= np.array(df_12[" L_IRI(in/mi)"])
ax1= df_filtered_12.plot(x="RefDMI(ft)", y= " L_IRI(in/mi)", color='black',alpha= 1, linewidth="0.27",label="12ft", ax=ax1)
ax2= df_filtered_15.plot(x="RefDMI(ft)", y= " L_IRI(in/mi)",color='black',linewidth="0.27",label="15ft",ax=ax2)
ax3= df_filtered_18.plot(x="RefDMI(ft)", y= " L_IRI(in/mi)",  color='black',linewidth="0.27",label="18ft",ax=ax3)
ax4= df_filtered_20.plot(x="RefDMI(ft)", y= " L_IRI(in/mi)",  color='black',linewidth="0.27",label="20ft",ax=ax4)
ax5= df_filtered_60.plot(x="RefDMI(ft)", y= " L_IRI(in/mi)", color='black',label="60ft",linewidth="0.27",ax=ax5)
ax6= df_filtered_100.plot(x="RefDMI(ft)", y= " L_IRI(in/mi)", color="black",linewidth="0.27",label="100ft", ax=ax6)
#ax6.set_title("100ft")
#plt.tight_layout()
ax.legend()
plt.legend()
#print(ax1==ax2==ax3==ax4==ax5==ax6)

plt.savefig("/Users/jha/Documents/Spring2021/SPR_indot/graphs/L_IRI_all.pdf", dpi=900)
plt.show()




#%%
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
directory="/Users/jha/Documents/Spring2021/SPR_indot/I70EB_103924"
fig,ax= plt.subplots()
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        df=pd.read_csv(os.path.join(directory,filename))
        x=np.array(df["RefDMI(ft)"])
        y= np.array(df[" L_IRI(in/mi)"])
        ax.plot(x,y)
        
        continue
    else:
        continue
plt.show()





#%%
# fit an empirical cdf to a bimodal dataset
from matplotlib import pyplot
from numpy.random import normal
import numpy as np
from numpy import hstack
from statsmodels.distributions.empirical_distribution import ECDF
# generate a sample
df = pd.read_csv('/Users/jhasneha/Documents/Spring2021/SPR_indot/data/6ft/IRI-report_6ft.csv')
sample1 = np.array(df[" R_IRI(in/mi)"])
#sample2 = normal(loc=40, scale=5, size=700)
#sample = hstack((sample1, sample2))
# fit a cdf
ecdf = ECDF(sample1)

# get cumulative probability for values
print('P(x<100): %.3f' % ecdf(100))
print('P(x<400): %.3f' % ecdf(400))
print('P(x<1200): %.3f' % ecdf(1200))
# plot the cdf
pyplot.plot(ecdf.x, ecdf.y)
plt.title("6ft")
plt.xlabel("R_IRI")
#plt.savefig("/Users/jha/Documents/Spring2021/SPR_indot/graphs/Recdf12.pdf", dpi=900)
pyplot.show()
plt.title("6ft")
plt.xlabel("R_IRI")
pyplot.hist(sample1)
#plt.savefig("/Users/jha/Documents/Spring2021/SPR_indot/graphs/Rhist12.pdf", dpi=900)

pyplot.show()

#%%
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
directory="/Users/jha/Documents/Spring2021/SPR_indot/I70EB_103924"
fig,ax= plt.subplots()
#fig, axes = plt.subplots(nrows=6, ncols=1, figsize=(6,1),sharex=True, sharey=True)
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        print(filename)
        df=pd.read_csv(os.path.join(directory,filename))
        #df[df.a < np.percentile(df.a,95)]
        df_filtered = df[df[" L_IRI(in/mi)"] <= 270] 
        x=np.array(df_filtered["RefDMI(ft)"])
        y= np.array(df_filtered[" L_IRI(in/mi)"])
        #df_filtered=df_filtered.cumsum()
        #df_filtered.plot.area()
        ax.plot(x, y, alpha=0.5)
        #plt.show()
        #df_filtered.plot()
        
        continue
    else:
        continue
plt.show()


#%%
ts = pd.Series(np.random.randn(1000), index=pd.date_range("1/1/2000", periods=1000))
ts=ts.cumsum()
df_test= pd.DataFrame(np.random.randn(1000, 4), index=ts.index, columns=list("ABCD"))

df_test = df_test.cumsum()
plt.figure()
df_test.plot()

#%%
df=pd.read_csv('/Users/jha/Documents/Spring2021/SPR_indot/I70EB_103924/IRI-report_12ft.csv')
df=
directory="/Users/jha/Documents/Spring2021/SPR_indot/I70EB_103924"
fig,ax= plt.subplots()
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        df=pd.read_csv(os.path.join(directory,filename))

#%%
data = np.random.rand(3,101)
data[:,0] = np.arange(2,7,2)
df_test = pd.DataFrame(data)


#%%
ax1= df_filtered_12.plot(x="RefDMI(ft)", y= " L_IRI(in/mi)", alpha=0.2, color='cyan',label="12ft")
ax2= df_filtered_15.plot(x="RefDMI(ft)", y= " L_IRI(in/mi)", alpha=0.3,color='green',label="15ft")
ax3= df_filtered_18.plot(x="RefDMI(ft)", y= " L_IRI(in/mi)", alpha=0.5, color='purple',label="18ft")
ax4= df_filtered_20.plot(x="RefDMI(ft)", y= " L_IRI(in/mi)", alpha=0.7, color='orange',label="20ft")
ax5= df_filtered_60.plot(x="RefDMI(ft)", y= " L_IRI(in/mi)", alpha=0.8,color='blue', label="60ft")
ax6= df_filtered_100.plot(x="RefDMI(ft)", y= " L_IRI(in/mi)", alpha=0.9,color="black", label="100ft")


#%%import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
fig, (ax1, ax2,ax3,ax4,ax5,ax6) = plt.subplots(nrows=6, ncols=1,sharex=True)
df_12 = pd.read_csv('/Users/jha/Documents/Spring2021/SPR_indot/I70EB_103924/IRI-report_12ft.csv')
df_filtered_12 = df_12[df_12[" R_IRI(in/mi)"] <= 270] 
df_15 = pd.read_csv('/Users/jha/Documents/Spring2021/SPR_indot/I70EB_103924/IRI-report_15ft.csv')
df_filtered_15 = df_15[df_15[" R_IRI(in/mi)"] <= 270] 
df_18 = pd.read_csv('/Users/jha/Documents/Spring2021/SPR_indot/I70EB_103924/IRI-report_18ft.csv')
df_filtered_18 = df_18[df_18[" R_IRI(in/mi)"] <= 270] 
df_20 = pd.read_csv('/Users/jha/Documents/Spring2021/SPR_indot/I70EB_103924/IRI-report_20ft.csv')
df_filtered_20 = df_20[df_20[" R_IRI(in/mi)"] <= 270] 
df_60 = pd.read_csv('/Users/jha/Documents/Spring2021/SPR_indot/I70EB_103924/IRI-report_60ft.csv')
df_filtered_60 = df_60[df_60[" R_IRI(in/mi)"] <= 270] 
df_100 = pd.read_csv('/Users/jha/Documents/Spring2021/SPR_indot/I70EB_103924/IRI-report_100ft.csv')
df_filtered_100 = df_100[df_100[" R_IRI(in/mi)"] <= 270] 
#x=np.array(df_12["RefDMI(ft)"])
#y= np.array(df_12[" R_IRI(in/mi)"])
ax1= df_filtered_12.plot(x="RefDMI(ft)", y= " R_IRI(in/mi)", color='black',alpha= 1, linewidth="0.27",label="12ft", ax=ax1)
ax2= df_filtered_15.plot(x="RefDMI(ft)", y= " R_IRI(in/mi)",color='black',linewidth="0.27",label="15ft",ax=ax2)
ax3= df_filtered_18.plot(x="RefDMI(ft)", y= " R_IRI(in/mi)",  color='black',linewidth="0.27",label="18ft",ax=ax3)
ax4= df_filtered_20.plot(x="RefDMI(ft)", y= " R_IRI(in/mi)",  color='black',linewidth="0.27",label="20ft",ax=ax4)
ax5= df_filtered_60.plot(x="RefDMI(ft)", y= " R_IRI(in/mi)", color='black',label="60ft",linewidth="0.27",ax=ax5)
ax6= df_filtered_100.plot(x="RefDMI(ft)", y= " R_IRI(in/mi)", color="black",linewidth="0.27",label="100ft", ax=ax6)
#ax6.set_title("100ft")
#plt.tight_layout()
ax.legend()
#plt.title("R_IRI(in/mi) vs RefDMI(ft)")
#plt.title(label="R_IRI(in/mi) vs RefDMI(ft)", 
          #loc="left", 
          #fontstyle='italic') 
plt.legend()
#print(ax1==ax2==ax3==ax4==ax5==ax6)

plt.savefig("/Users/jha/Documents/Spring2021/SPR_indot/graphs/all_R_IRI.pdf", dpi=900)
plt.show()



#%%
# import libraries
import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
# import street map
street_map = gpd.read_file("/Users/jha/Documents/Spring2021/SPR_indot/shapefile/Imagery_2005")

#%%
from pyproj import CRS
CRS("EPSG:26973")


#%%
# designate coordinate system
crs = CRS("EPSG:")
# zip x and y coordinates into single feature
geometry = [Point(xy) for xy in zip(df_filtered_12["GPSLng"], df_filtered_12["GPSLat"])]
# create GeoPandas dataframe
geo_df = gpd.GeoDataFrame(df_filtered_12,
 crs = crs,
 geometry = geometry)


#%%
# create figure and axes, assign to subplot
fig, ax = plt.subplots(figsize=(15,15))
# add .shp mapfile to axes
street_map.plot(ax=ax, alpha=0.4,color="blue")
# add geodataframe to axes
# assign ‘price’ variable to represent coordinates on graph
# add legend
# make datapoints transparent using alpha
# assign size of points using markersize
#geo_df.plot(column=" L_IRI(in/mi)",ax=ax,alpha=0.5, legend=True,markersize=1)
# add title to graph
#plt.title(‘Rental Prices in NYC’, fontsize=15,fontweight=’bold’)
# set latitiude and longitude boundaries for map display
#plt.xlim(-85.915169 ,-85.763908)
#plt.ylim( 39.519,40.520)
# show map
plt.show()

#%%
ax = df.plot(figsize=(10, 10), alpha=0.5, edgecolor='k')
ctx.add_basemap(ax, zoom=12)

#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
import openpyxl
df_EB=pd.read_excel("/Users/jhasneha/Documents/Spring2021/SPR_indot/SPRprojectcodes/data/I70 (DL).xlsx", sheet_name="I70-EB")
df_EB.columns = df_EB.columns.str.replace(' ', '')
df_EB.columns = df_EB.columns.str.replace(r'\([^)]*\)', '')

#%%
df_EBR= df_EB[["DMI","D0","D48","AUPP"]].copy()
df_EBR.plot(x="DMI", y=[ "D0", "D48","AUPP"])
plt.show()
# %%
df_plot_ebr=df_plot["DMI"].append(df_EBR["DMI"], ignore_index= True)
df_plot_ebr=pd.DataFrame(df_plot_ebr)
#UK_dict = dict(zip(df_ukscanner.EndLogMi, df_ukscanner.Percent))
#df_plot_ebr['UK_Scanner']=df_plot_ebr['DMI'].map(UK_dict)
ashhto_dict_4 = dict(zip(df_ashhto_4.DMI, df_ashhto_4.Density))
df_plot_ebr['Density_ashhto4']=df_plot_ebr['DMI'].map(ashhto_dict_4)
ashhto_dict_2 = dict(zip(df_ashhto_2.DMI, df_ashhto_2.Density))
df_plot_ebr['Density_ashhto2']=df_plot_ebr['DMI'].map(ashhto_dict_2)
IRI_dict = dict(zip(df_IRIFF.RefDMI, df_IRIFF.L_IRI))
df_plot_ebr['L_IRI']=df_plot_ebr['DMI'].map(IRI_dict)
IRI_dict = dict(zip(df_IRIFF.RefDMI, df_IRIFF.R_IRI))
df_plot_ebr['R_IRI']=df_plot_ebr['DMI'].map(IRI_dict)
#df_plot_ebr.UK_Scanner=df_plot_ebr.UK_Scanner*100
df_plot_ebr.Density_ashhto2=df_plot_ebr.Density_ashhto2*100
df_plot_ebr.Density_ashhto4=df_plot_ebr.Density_ashhto4*100

D0_dict = dict(zip(df_EBR.DMI, df_EBR.D0))
df_plot_ebr['D0']=df_plot_ebr['DMI'].map(D0_dict)

D48_dict = dict(zip(df_EBR.DMI, df_EBR.D48))
df_plot_ebr['D48']=df_plot_ebr['DMI'].map(D48_dict)

AUPP_dict = dict(zip(df_EBR.DMI, df_EBR.AUPP))
df_plot_ebr['AUPP']=df_plot_ebr['DMI'].map(AUPP_dict)

# %%
df_plot_ebr=df_plot_ebr.replace(0,np.nan) #DONOT REPLACE 0 with NAN in ashto and iri
#df_plot_ebr=df_plot_ebr.set_index("DMI")
#df_plot_ebr=df_plot_ebr.dropna()
plt.figure()
df_plot_ebr.plot.line(x="DMI", y=[ "D0","Density_ashhto2"],linewidth =0.5, linestyle='-', marker='o', markersize="1")


# %%
df_plot_ebr1 = df_plot_ebr.drop(["UK_Scanner","Density_ashhto2","Density_ashhto4"],axis= 1)
df_plot_ebr_values=df_plot_ebr1.dropna()

#%%

df_plot_ebr_values.plot.line(x="DMI", y=[ "R_IRI","L_IRI","D0","D48","AUPP"],linewidth =0.5)
plt.figure()

# %%
#df_plot_ebr["D0"]=df_plot_ebr["D0"].replace(0,np.nan)
#df_plot_ebr = df_plot_ebr.dropna(axis=0, subset=["D0"]) 
#df_plot_ebr=df_plot_ebr.drop_duplicates(subset=['DMI'])
#df_plot_ebr=df_plot_ebr.sort_values(by=['DMI'])

plt.plot( 'DMI', 'D0', data=df_plot_ebr, marker='o', color='blue', markersize=1, linewidth=1,linestyle='-')
plt.plot( 'DMI', 'L_IRI', data=df_plot_ebr, marker='o', color='olive', linewidth=1,markersize=1,linestyle='-', alpha = 0.5)
plt.plot( 'DMI', 'Density_ashhto2', data=df_plot_ebr, marker='o', color='salmon', linewidth=1, linestyle='-', markersize=1, alpha=0.5)
plt.plot( 'DMI', 'AUPP', data=df_plot_ebr, marker='o', color='purple', linewidth=1, linestyle='-', markersize=1, alpha=0.5)
plt.legend()

# show graph
plt.show()


# %%

plt.plot( 'DMI', 'D0', data=df_EB, marker='o', color='blue', markersize=1, linewidth=1,linestyle='-')
plt.plot( 'RefDMI', 'L_IRI', data=df_IRIFF, marker='o', color='olive', linewidth=1,markersize=1,linestyle='-', alpha = 0.5)
plt.plot( 'DMI', 'Density', data=df_ashhto_2, marker='o', color='salmon', linewidth=1, linestyle='-', markersize=1, alpha=0.8)
plt.plot( 'DMI', 'AUPP', data=df_EB, marker='o', color='purple', linewidth=1, linestyle='-', markersize=1, alpha=0.2)
plt.legend()
plt.show()

# %%
df_ashhto_2.Density=df_ashhto_2.Density*100
#%%

plt.plot( 'DMI', 'D48', data=df_EB, marker='o', color='blue', markersize=1, linewidth=1,linestyle='-',alpha=1)
plt.plot( 'DMI', 'D0', data=df_EB, marker='o', color='red', markersize=1, linewidth=1,linestyle='-',alpha=1)
plt.plot( 'RefDMI', 'L_IRI', data=df_IRIFF, marker='o', color='olive', linewidth=1,markersize=1,linestyle='-', alpha = 0.4)
plt.plot( 'DMI', 'Density', data=df_ashhto_2, marker='o', color='salmon', linewidth=1, linestyle='-', markersize=1, alpha=0.7)
plt.plot( 'DMI', 'AUPP', data=df_EB, marker='o', color='purple', linewidth=1, linestyle='-', markersize=1, alpha=1)
plt.legend()

plt.savefig("/Users/jhasneha/Documents/Spring2021/SPR_indot/SPRprojectcodes/graphs/ashhto_LIRI_fwd_save")
plt.show()


# %%
plt.plot( 'DMI', 'D48', data=df_EB, marker='o', color='blue', markersize=1, linewidth=1,linestyle='-',alpha=1)
plt.plot( 'DMI', 'D0', data=df_EB, marker='o', color='red', markersize=1, linewidth=1,linestyle='-',alpha=1)
plt.plot( 'RefDMI', 'R_IRI', data=df_IRIFF, marker='o', color='olive', linewidth=1,markersize=1,linestyle='-', alpha = 0.4)
#plt.plot( 'DMI', 'Density', data=df_ashhto_2, marker='o', color='salmon', linewidth=1, linestyle='-', markersize=1, alpha=0.7)
plt.plot( 'DMI', 'AUPP', data=df_EB, marker='o', color='purple', linewidth=1, linestyle='-', markersize=1, alpha=1)
plt.legend()

#plt.savefig("/Users/jhasneha/Documents/Spring2021/SPR_indot/SPRprojectcodes/graphs/ashhto_LIRI_fwd_save")
plt.show()

# %%
# copy the data
df_IRIFF_scaled = df_IRIFF.copy()
  
# apply normalization techniques by Column 1
column = 'L_IRI'
df_IRIFF_scaled[column] = (df_IRIFF_scaled[column] - df_IRIFF_scaled[column].min()) / (df_IRIFF_scaled[column].max() - df_IRIFF_scaled[column].min())    

#%%
df_ashhto_2_scaled = df_ashhto_2.copy()
  
# apply normalization techniques by Column 1
column = 'Density'
df_ashhto_2_scaled[column] = (df_ashhto_2_scaled[column] - df_ashhto_2_scaled[column].min()) / (df_ashhto_2_scaled[column].max() - df_ashhto_2_scaled[column].min()) 
  
# apply normalization techniques by Column 1
column = 'Density'
df_ash


#%%
# apply normalization techniques by Column to the whole dataframe except the AUPP column because the values are related
dataset=df_EB.copy()
series_D0=pd.Series(dataset['D0'])
series_D48=pd.Series(dataset['D48'])
series_AUPP=pd.Series(dataset['AUPP'])
df_c=pd.DataFrame(pd.concat([series_D0,series_D48,series_AUPP], keys = ['D0','D48','AUPP']))
dataNorm=((df_c-df_c.min())/(df_c.max()-df_c.min()))
dataNorm= dataNorm.reset_index()
dataNorm=dataNorm.drop(["level_1"], axis=1)
dataNorm.columns=("key","value")
dfD0=dataNorm[dataNorm['key'] == 'D0']
dataset["D0_N"]=dfD0[["value"]].copy()
dfD48=dataNorm[dataNorm['key'] == 'D48']
dataset["D48_N"]=dfD48["value"].values
dfAUPP=dataNorm[dataNorm['key'] == 'AUPP']
dataset["AUPP_N"]=dfAUPP["value"].values
#dataNorm["DMI"]=dataset["DMI"]
    


#hto_2_scaled[column] = (df_ashhto_2_scaled[column] - df_ashhto_2_scaled[column].min()) / (df_ashhto_2_scaled[column].max() - df_ashhto_2_scaled[column].min()) 

#%%
df_IRIFF_scaled = df_IRIFF_scaled[df_IRIFF_scaled["RefDMI"] <= 24300] 
df_ashhto_2_scaled = df_ashhto_2_scaled[df_ashhto_2_scaled["DMI"] <= 24300] 




# %%

plt.plot( 'RefDMI', 'L_IRI', data=df_IRIFF_scaled, marker='o', color='olive', linewidth=1,markersize=1,linestyle='-', alpha = 0.4)
plt.plot( 'DMI', 'Density', data=df_ashhto_2_scaled, marker='o', color='salmon', linewidth=1, linestyle='-', markersize=1, alpha=0.5)
plt.plot( 'DMI', 'D48_N', data=dataset, marker='o', color='blue', markersize=1, linewidth=1,linestyle='-',alpha=1)
plt.plot( 'DMI', 'D0_N', data=dataset, marker='o', color='red', markersize=1, linewidth=1,linestyle='-',alpha=1)
plt.plot( 'DMI', 'AUPP_N', data=dataset, marker='o', color='purple', linewidth=1, linestyle='-', markersize=1, alpha=1)
plt.legend(loc=1)

#plt.savefig("/Users/jhasneha/Documents/Spring2021/SPR_indot/SPRprojectcodes/graphs/ashhto_LIRI_fwd_save")
plt.show()


#%%
df_corr_1=df_IRIFF_scaled['L_IRI'].rolling(20).corr(df_IRIFF_scaled['R_IRI'])
df_corr_1.plot()

# %%
df_corr_2=df_IRIFF_scaled['L_IRI'].rolling(5).corr(df_ashhto_2_scaled['Density'])
df_corr_2.plot()
# %%
df_corr_3=dataset['D0'].rolling(2).corr(dataset['D48'])
df_corr_3.plot()
# %%
df_corr_4=dataset['D0'].rolling(75).corr(dataset['AUPP'])
df_corr_4.plot()

# %%
#dataset=dataset.set_index("DMI") #do it only once

import matplotlib.gridspec as gridspec

fig = plt.figure()
ax1 = plt.subplot2grid((3,1), (0,0))
ax2 = plt.subplot2grid((3,1), (1,0), sharex=ax1)
ax3 = plt.subplot2grid((3,1), (2,0), sharex=ax1)

#HPI_data = pd.read_pickle('fiddy_states3.pickle') #reading the datat into a dataframe
#TX_AK_12corr = pd.rolling_corr(HPI_data['TX'], HPI_data['AK'], 12)
dataset_corr1=dataset['D0'].rolling(3).corr(dataset['D48'])
dataset_corr2=dataset['D0'].rolling(6).corr(dataset['D48'])

#HPI_data['TX'].plot(ax=ax1, label="TX HPI")
dataset['D0'].plot(ax=ax1,label="D0")
#plt.legend(loc='upper right')

#HPI_data['AK'].plot(ax=ax1, label="AK HPI")
dataset['D48'].plot(ax=ax1,label="D48")
#plt.legend(loc='upper right')


ax1.legend(loc=1)

#TX_AK_12corr.plot(ax=ax2)
dataset_corr1.plot(ax=ax2, label="window_3")
plt.legend(loc='best')
ax2.legend(loc=4)

dataset_corr2.plot(ax=ax3, label="window_6")
plt.legend(loc=4)


plt.show()


# %%
#dataset=dataset.set_index("DMI") #do it only once

import matplotlib.gridspec as gridspec

fig = plt.figure()
ax1 = plt.subplot2grid((5,1), (0,0))
ax2 = plt.subplot2grid((5,1), (1,0), sharex=ax1)
ax3 = plt.subplot2grid((5,1), (2,0), sharex=ax1)
ax4 = plt.subplot2grid((5,1), (3,0), sharex=ax1)
ax5 = plt.subplot2grid((5,1), (4,0), sharex=ax1)

#HPI_data = pd.read_pickle('fiddy_states3.pickle') #reading the datat into a dataframe
#TX_AK_12corr = pd.rolling_corr(HPI_data['TX'], HPI_data['AK'], 12)
dataset_corr1=dataset['D0'].rolling(2).corr(dataset['AUPP'])
dataset_corr2=dataset['D0'].rolling(3).corr(dataset['AUPP'])
dataset_corr3=dataset['D0'].rolling(4).corr(dataset['AUPP'])
dataset_corr4=dataset['D0'].rolling(10).corr(dataset['AUPP'])
#HPI_data['TX'].plot(ax=ax1, label="TX HPI")
dataset['D0'].plot(ax=ax1,label="D0")
#plt.legend(loc='upper right')

#HPI_data['AK'].plot(ax=ax1, label="AK HPI")
dataset['AUPP'].plot(ax=ax1,label="AUPP")
#plt.legend(loc='upper right')


ax1.legend(loc=1)

#TX_AK_12corr.plot(ax=ax2)
dataset_corr1.plot(ax=ax2, label="window_2")

ax2.legend(loc=4)

dataset_corr2.plot(ax=ax3, label="window_3")

ax3.legend(loc=4)
dataset_corr3.plot(ax=ax4, label="window_4")

ax4.legend(loc=4)
dataset_corr4.plot(ax=ax5, label="window_10")

ax5.legend(loc=1)




plt.show()









# %%
#df_plot=df_plot.set_index("DMI") #do it only once
#df_plot['Density'].interpolate(method='polynomial', order=2)
# copy the data
# apply normalization techniques by Column 1
df_plot1=df_plot.copy()
df_plot1["L_IRI_N"] = (df_plot1["L_IRI"] - df_plot1["L_IRI"].min()) / (df_plot1["L_IRI"].max() - df_plot1["L_IRI"].min())    
df_plot1["Density_N"] = (df_plot1["Density"] - df_plot1["Density"].min()) / (df_plot1["Density"].max() - df_plot1["Density"].min())

import matplotlib.gridspec as gridspec

fig = plt.figure()
ax1 = plt.subplot2grid((5,1), (0,0))
ax2 = plt.subplot2grid((5,1), (1,0), sharex=ax1)
ax3 = plt.subplot2grid((5,1), (2,0), sharex=ax1)
ax4 = plt.subplot2grid((5,1), (3,0), sharex=ax1)
ax5 = plt.subplot2grid((5,1), (4,0), sharex=ax1)

#HPI_data = pd.read_pickle('fiddy_states3.pickle') #reading the datat into a dataframe
#TX_AK_12corr = pd.rolling_corr(HPI_data['TX'], HPI_data['AK'], 12)



df_plot_corr1=df_plot1['L_IRI'].rolling(6).corr(df_plot1['Density'])
df_plot_corr2=df_plot1['L_IRI'].rolling(100).corr(df_plot1['Density'])
df_plot_corr3=df_plot1['L_IRI'].rolling(200).corr(df_plot1['Density'])
df_plot_corr4=df_plot1['L_IRI'].rolling(500).corr(df_plot1['Density'])
#HPI_data['TX'].plot(ax=ax1, label="TX HPI")
df_plot1['L_IRI_N'].plot(ax=ax1,label="L_IRI_N")
#HPI_data['AK'].plot(ax=ax1, label="AK HPI")
df_plot1['Density_N'].plot(ax=ax1,label="Density_N")
ax1.legend(loc=1)
#ax1.legend(loc=4)


#TX_AK_12corr.plot(ax=ax2)
df_plot_corr1.plot(ax=ax2, label="corr_window6")
ax2.legend(loc=4)
df_plot_corr2.plot(ax=ax3, label="corr_window100")
ax3.legend(loc=4)
df_plot_corr3.plot(ax=ax4, label="corr_window200")
ax4.legend(loc=4)
df_plot_corr4.plot(ax=ax5, label="corr_window500")
ax5.legend(loc=4)
plt.show()


#%%



#FWD IRI correlation


# %%
#interpolation of FWD values
df_plot_ebr1=df_plot_ebr.copy()
df_plot_ebr1=df_plot_ebr1.drop_duplicates()
df_filled_pp=df_plot_ebr1.interpolate(method='piecewise_polynomial', order=2)
#df_filled_pp=df_filled_pp.sort_values(by=['DMI'])


#%%
#no interpolation
df_filled_pp=df_plot_ebr.copy()
#df_filled_pp=df_filled_pp.drop_duplicates()






#%%
# apply normalization techniques by Column to the whole dataframe except the AUPP column because the values are related
dataset=df_filled_pp.copy()
series_D0=pd.Series(dataset['D0'])
series_D48=pd.Series(dataset['D48'])
series_AUPP=pd.Series(dataset['AUPP'])
df_c=pd.DataFrame(pd.concat([series_D0,series_D48,series_AUPP], keys = ['D0','D48','AUPP']))
dataNorm=((df_c-df_c.min())/(df_c.max()-df_c.min()))
dataNorm= dataNorm.reset_index()
dataNorm=dataNorm.drop(["level_1"], axis=1)
dataNorm.columns=("key","value")
dfD0=dataNorm[dataNorm['key'] == 'D0']
df_filled_pp["D0_N"]=dfD0[["value"]].copy()
dfD48=dataNorm[dataNorm['key'] == 'D48']
df_filled_pp["D48_N"]=dfD48["value"].values
dfAUPP=dataNorm[dataNorm['key'] == 'AUPP']
df_filled_pp["AUPP_N"]=dfAUPP["value"].values
#dataNorm["DMI"]=dataset["DMI"]

#%%
df_filled_pp["L_IRI_N"] = (df_filled_pp["L_IRI"] - df_filled_pp["L_IRI"].min()) / (df_filled_pp["L_IRI"].max() - df_filled_pp["L_IRI"].min()) 
#df_filled_pp["Density"] = (df_filled_pp["L_IRI"] - df_filled_pp["L_IRI"].min()) / (df_filled_pp["L_IRI"].max() - df_filled_pp["L_IRI"].min()) 
df_filled_pp = df_filled_pp[df_filled_pp["DMI"] <= 24281] 
df_filled_pp=df_filled_pp.drop_duplicates()






#DMI plot

# %%
fig = plt.figure()
ax1 = plt.subplot2grid((2,1), (0,0))
#ax2 = plt.subplot2grid((2,1), (1,0))
df_ts=df_IRIFF[['RefDMI']].copy()
df_ts["value"]=df_IRIFF[['RefDMI']].copy()
#df_ts=df_ts.set_index("value")
df_ts= df_ts[df_ts["RefDMI"] <= 24296] 

df_fs=df_EB[['DMI']].copy()
df_fs["value"]=df_EB[['DMI']].copy()
#df_fs=df_fs.set_index("value")
df_ts.plot.scatter(x='RefDMI',y='value',ax=ax1,label="DMI_IRI", c="red", s= 0.25)
df_fs.plot.scatter(x='DMI',y='value', ax=ax1,label="DMI_FWD",s= 0.5)
ax1.legend(loc=4)




#matching the DMI


 # %%
appended_df_IRI=pd.DataFrame()
for index,row in df_EB.iterrows():
    index_value=int(row["DMI"])
    ind= df_IRIFF['RefDMI'].sub(index_value).abs().idxmin()
    df_test =df_IRIFF.loc[ind-2:ind+2,:]
    appended_df_IRI=appended_df_IRI.append(df_test,ignore_index=True)


# %%
# appended_df_IRI1=appended_df_IRI.loc[3:,:]
# appended_IRI=appended_df_IRI1[["No","L_IRI","R_IRI","RefDMI"]].copy()


# # %%
# n = 5  #chunk row size
# list_df_app = [appended_IRI[i:i+n] for i in range(0,appended_IRI.shape[0],n)]

# # %%
# appended_df=pd.DataFrame()
# for index in list_df_app :
#     df1=pd.DataFrame()
#     df=index
#     #print(df)
#     df1.at[0,"No"]=df["No"].median()
#     df1.at[0,"R_DMI"]=df["RefDMI"].median()
#     df1.at[0,"L_IRI"]=df["L_IRI"].mean()
#     df1.at[0,"R_IRI"]=df["R_IRI"].mean()
#     appended_df=appended_df.append(df1,ignore_index=True) 

# #inserting the values for the first three rows of the dataframe
# # %%
# df=appended_df_IRI.loc[0:3,:]
# df1.at[0,"No"]=df["No"].median()
# df1.at[0,"R_DMI"]=df["RefDMI"].median()
# df1.at[0,"L_IRI"]=df["L_IRI"].mean()
# df1.at[0,"R_IRI"]=df["R_IRI"].mean()
# print(df1)
# appended_df=appended_df.append(df1,ignore_index=True) 


# #%%
# appended_df=appended_df.sort_values("R_DMI")
# appended_df=appended_df.reset_index()
# appended_df= appended_df.drop("index", axis=1)
# appended_df["L_IRI_N"] = (appended_df["L_IRI"] - appended_df["L_IRI"].min()) / (appended_df["L_IRI"].max() - appended_df["L_IRI"].min()) 
# appended_df["R_IRI_N"] = (appended_df["R_IRI"] - appended_df["R_IRI"].min()) / (appended_df["R_IRI"].max() - appended_df["R_IRI"].min()) 




# #this is correlation for the D48 and L_IRI dataframe using the compressed IRI data



# # %%
# #df_filled_pp=df_filled_pp.set_index("DMI") #do it only once
# import matplotlib.gridspec as gridspec

# fig = plt.figure()
# ax1 = plt.subplot2grid((3,1), (0,0))
# ax2 = plt.subplot2grid((3,1), (1,0), sharex=ax1)
# ax3 = plt.subplot2grid((3,1), (2,0), sharex=ax1)
# #HPI_data = pd.read_pickle('fiddy_states3.pickle') #reading the datat into a dataframe
# #TX_AK_12corr = pd.rolling_corr(HPI_data['TX'], HPI_data['AK'], 12)
# df_filled_pp_corr2=appended_df['L_IRI'].rolling(3).corr(df_EB['D0'])
# df_filled_pp_corr3=appended_df['L_IRI'].rolling(2).corr(df_EB['D0'])

# #HPI_data['TX'].plot(ax=ax1, label="TX HPI")
# appended_df['L_IRI_N'].plot(ax=ax1,label="L_IRI_N")
# ##plt.legend(loc='upper right')

# #HPI_data['AK'].plot(ax=ax1, label="AK HPI")
# dataset['D0_N'].plot(ax=ax1,label="D0")
# #plt.legend(loc='upper right')


# ax1.legend(loc=1)

# #TX_AK_12corr.plot(ax=ax2)
# df_filled_pp_corr2.plot(ax=ax2, label="corr_window3")
# ax2.legend(loc=4)
# df_filled_pp_corr3.plot(ax=ax3, label="corr_window2")
# ax3.legend(loc=4)
# ax1.set_title("Correlation between L_IRI and D0")
# plt.show()


# # this doesnot work yet but I have tried to make the plot as a function
# # %%
# # def Plot_corr(x,x_n,y,y_n):
#     import matplotlib.gridspec as gridspec
#     #print("this:"appended_df.x)
#     print("thees:",appended_df[[x]])

#     fig = plt.figure()
#     ax1 = plt.subplot2grid((3,1), (0,0))
#     ax2 = plt.subplot2grid((3,1), (1,0), sharex=ax1)
#     ax3 = plt.subplot2grid((3,1), (2,0), sharex=ax1)
#     #HPI_data = pd.read_pickle('fiddy_states3.pickle') #reading the datat into a dataframe
#     #TX_AK_12corr = pd.rolling_corr(HPI_data['TX'], HPI_data['AK'], 12)
#     df_filled_pp_corr2=appended_df.x.rolling(3).corr(df_EB.y)
#     df_filled_pp_corr3=appended_df.x.rolling(2).corr(df_EB.y)

#     #HPI_data['TX'].plot(ax=ax1, label="TX HPI")
#     appended_df.x_n.plot(ax=ax1,label=x_n)
#     ##plt.legend(loc='upper right')

#     #HPI_data['AK'].plot(ax=ax1, label="AK HPI")
#     dataset.y_n.plot(ax=ax1,label=y_n)
#     #plt.legend(loc='upper right')


#     ax1.legend(loc=1)

#     #TX_AK_12corr.plot(ax=ax2)
#     df_filled_pp_corr2.plot(ax=ax2, label="corr_window3")
#     ax2.legend(loc=4)
#     df_filled_pp_corr3.plot(ax=ax3, label="corr_window2")
#     ax3.legend(loc=4)
#     ax1.set_title("Correlation between "+ x +"  and " + y +" :")
#     return plt.show()











# #standard deviation of the compressed IRI df

# # %%
# appended_df_stat=pd.DataFrame()
# for index in list_df_app :
#     df1=pd.DataFrame()
#     df=index
#     #print(df)
#     df1.at[0,"No"]=df["No"].median()
#     df1.at[0,"R_DMI"]=df["RefDMI"].median()
#     df1.at[0,"L_IRI_mean"]=df["L_IRI"].mean()
#     df1.at[0,"R_IRI_mean"]=df["R_IRI"].mean()
#     df1.at[0,"L_IRI_sd"]=df["L_IRI"].std()
#     df1.at[0,"R_IRI_sd"]=df["R_IRI"].std()
#     appended_df_stat=appended_df_stat.append(df1,ignore_index=True) 


# # %%

# #plot for mean and standard deviation values for L_IRI and R_IRI (LINE PLOT)


# # %%

# import matplotlib.gridspec as gridspec

# fig = plt.figure()
# ax1 = plt.subplot2grid((2,1), (0,0))
# ax2 = plt.subplot2grid((2,1), (1,0), sharex=ax1)
# #ax3 = plt.subplot2grid((3,1), (2,0), sharex=ax1)
# appended_df_stat['L_IRI_mean'].plot(ax=ax1,label="L_IRI_mean")
# appended_df_stat['L_IRI_sd'].plot(ax=ax2,label="L_IRI_sd")
# #iridf_std["L_IRI_sd"]=appended_df['L_IRI'].rolling(3).corr(df_EB['D0'])
# ax1.legend(loc=1)
# ax2.legend(loc=4)
# ax1.set_title("Mean and standard deviation of 5 nearby DMI")
# plt.show()



# # %%
# IRI_series=appended_df_IRI1[["L_IRI"]].copy()
# n = 5  #chunk row size
# list_series_app = [IRI_series[i:i+n] for i in range(0,IRI_series.shape[0],n)]
# df_boxp=pd.concat(list_series_app, axis=1)
# colnames=appended_df_stat["R_DMI"].to_list()
# df_boxp.columns=colnames
# df_boxp.boxplot(fontsize=4,rot=90)

# chart elements



# %%



# #comparing the 0.75 quantile FWD values to nearby IRI values

# #%%
# q75=dataset.D0.quantile(0.75)
# dataset_q3 = dataset[dataset["D0"] >=q75] 
# df_EB_q3= df_EB_q3[df_EB_q3["D0"]>=q75]

# #is selecting the 5 IRI values near the FWD values and saving them as a new dataframes
# # %%
# appended_df_IRI=pd.DataFrame()
# for index,row in df_EB_q3.iterrows():
#     index_value=int(row["DMI"])
#     ind= df_IRIFF['RefDMI'].sub(index_value).abs().idxmin()
#     df_test =df_IRIFF.loc[ind-2:ind+2,:]
#     appended_df_IRI=appended_df_IRI.append(df_test,ignore_index=True)

# # %%
# #appended_df_IRI1=appended_df_IRI.loc[3:,:]
# appended_IRI=appended_df_IRI[["No","L_IRI","R_IRI","RefDMI"]].copy()

# #%%
# n = 5  #chunk row size
# list_df_app = [appended_IRI[i:i+n] for i in range(0,appended_IRI.shape[0],n)]

# # %%
# appended_df=pd.DataFrame()
# for index in list_df_app :
#     df1=pd.DataFrame()
#     df=index
#     #print(df)
#     df1.at[0,"No"]=df["No"].median()
#     df1.at[0,"R_DMI"]=df["RefDMI"].median()
#     df1.at[0,"L_IRI"]=df["L_IRI"].mean()
#     df1.at[0,"R_IRI"]=df["R_IRI"].mean()
#     appended_df=appended_df.append(df1,ignore_index=True) 

#inserting the values for the first three rows of the dataframe
# %%
# df=appended_df_IRI.loc[0:3,:]
# df1.at[0,"No"]=df["No"].median()
# df1.at[0,"R_DMI"]=df["RefDMI"].median()
# df1.at[0,"L_IRI"]=df["L_IRI"].mean()
# df1.at[0,"R_IRI"]=df["R_IRI"].mean()
# print(df1)
# appended_df=appended_df.append(df1,ignore_index=True) 


#%%
# appended_df=appended_df.sort_values("R_DMI")
# appended_df=appended_df.reset_index()
# appended_df= appended_df.drop("index", axis=1)
# appended_df["L_IRI_N"] = (appended_df["L_IRI"] - appended_df["L_IRI"].min()) / (appended_df["L_IRI"].max() - appended_df["L_IRI"].min()) 
# appended_df["R_IRI_N"] = (appended_df["R_IRI"] - appended_df["R_IRI"].min()) / (appended_df["R_IRI"].max() - appended_df["R_IRI"].min()) 


# # %%
# #df_filled_pp=df_filled_pp.set_index("DMI") #do it only once
# import matplotlib.gridspec as gridspec

# fig = plt.figure()
# ax1 = plt.subplot2grid((3,1), (0,0))
# ax2 = plt.subplot2grid((3,1), (1,0), sharex=ax1)
# ax3 = plt.subplot2grid((3,1), (2,0), sharex=ax1)
# #HPI_data = pd.read_pickle('fiddy_states3.pickle') #reading the datat into a dataframe
# #TX_AK_12corr = pd.rolling_corr(HPI_data['TX'], HPI_data['AK'], 12)
# df_filled_pp_corr2=appended_df['L_IRI'].rolling(3).corr(df_EB['D0'])
# df_filled_pp_corr3=appended_df['L_IRI'].rolling(2).corr(df_EB['D0'])

# #HPI_data['TX'].plot(ax=ax1, label="TX HPI")
# appended_df['L_IRI_N'].plot(ax=ax1,label="L_IRI_N")
# ##plt.legend(loc='upper right')

# #HPI_data['AK'].plot(ax=ax1, label="AK HPI")
# dataset['D0_N'].plot(ax=ax1,label="D0")
# #plt.legend(loc='upper right')


# ax1.legend(loc=1)

# #TX_AK_12corr.plot(ax=ax2)
# df_filled_pp_corr2.plot(ax=ax2, label="corr_window3")
# ax2.legend(loc=4)
# df_filled_pp_corr3.plot(ax=ax3, label="corr_window2")
# ax3.legend(loc=4)
# ax1.set_title("Correlation between L_IRI and D0")
# plt.show()


# #%%
# appended_df=appended_df.reset_index()
# dataset_q3=dataset_q3.reset_index()

# # %%
# import matplotlib.pyplot as plt
# fig, ax = plt.subplots()
# pos = len(dataset_q3['index'])
# ind = np.arange(pos, step = 1)

# width =0.20
# #ax1=appended_df["L_IRI_N"].plot(pos, kind='bar', width= width ,color=color)
# rects1=ax.bar(ind, appended_df["R_IRI_N"], width,color='Red',alpha=0.5,label= "R_IRI_N") 


# #ax2= dataset["D0"].plot(pos,kind= 'bar',width= width ,color=color)
# rects2=ax.bar(ind+0.2, dataset_q3["D0_N"], width, alpha=0.5,color='blue',  label= "D0_N") 
# ax.legend((rects1[0], rects2[0]), ('R_IRI_N', 'D0_N'), loc =5)

# ax.set_ylabel('Values')
# ax.set_xlabel('DMI Number')
# ax.set_title('Comaprison of 0.75 quantile FWD data')
# ax.set_xticks(ind)
# ax.set_xticklabels(ind)

# ax2 = ax.twiny()
# dmi = list(dataset_q3['DMI'])
# new_tick_locations = np.array(ind+1)
# ax2.set_xticks(new_tick_locations)
# ax2.set_xticklabels(dmi,rotation = 90, ha="right",color='blue')
# #ax2.set_xlabel('FWD_DMI',color='blue')
# ax3 = ax.twiny()
# dmi1 = list(appended_df['R_DMI'].astype(int))
# new_tick_locations = np.array(ind+1)
# ax3.set_xticks(new_tick_locations)
# ax3.set_xticklabels(dmi1,rotation = 90, ha="right",va= "top",color='Red')
# #ax3.set_xlabel('IRI_DMI',color='red')

# plt.tight_layout()  # otherwise the right y-label is slightly clipped

# plt.show()







# # %%
# fig3, ax = plt.subplots()
# pos = len(dataset_q3['index'])
# ind = np.arange(pos, step = 1)

# ax2 = ax.twinx()
# ax2.set_ylabel('D48 values')

# ax.set_ylim(0,100)
# ax2.set_ylim(0,15)
# rects1=ax.bar(ind, appended_df["L_IRI"], width,color='Red',alpha=0.7,label= "L_IRI") 
# rects2=ax2.bar(ind+0.2, dataset_q3["D48"], width, alpha=0.7,color='blue',  label= "D48") 
# ax.legend(loc=2)
# ax2.legend(loc=1)
# ax.set_box_aspect(1)
# ax.set_ylabel('IRI values')
# ax.set_xlabel('DMI Number')
# ax.set_title('Comaprison of L_IRI and FWD (D48) ).75 quantile data')

# plt.show()

""""........................................


#taking only one nearest value
#taking only one nearest value
#taking only one nearest value
#taking only one nearest value
......................................."""

# %%

#%%
q75=dataset.D0.quantile(0.75)
dataset_q3 = dataset[dataset["D0"] >=q75] 
df_EB_q3= df_EB[df_EB["D0"]>=q75]

 # %%
appended_df_IRI=pd.DataFrame()
for index,row in df_EB_q3.iterrows():
    index_value=int(row["DMI"])
    ind= df_IRIFF['RefDMI'].sub(index_value).abs().idxmin()
    df_test =df_IRIFF.loc[ind,:]
    appended_df_IRI=appended_df_IRI.append(df_test,ignore_index=True)


# %%

appended_IRI_q3=appended_df_IRI[["No","L_IRI","R_IRI","RefDMI"]].copy()


#%%
appended_IRI_q3["L_IRI_N"] = (appended_IRI_q3["L_IRI"] - appended_IRI_q3["L_IRI"].min()) / (appended_IRI_q3["L_IRI"].max() - appended_IRI_q3["L_IRI"].min()) 
appended_IRI_q3["R_IRI_N"] = (appended_IRI_q3["R_IRI"] - appended_IRI_q3["R_IRI"].min()) / (appended_IRI_q3["R_IRI"].max() - appended_IRI["R_IRI"].min()) 


# %%
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
pos = len(dataset_q3['index'])
ind = np.arange(pos, step = 1)

width =0.20
#ax1=appended_df["L_IRI_N"].plot(pos, kind='bar', width= width ,color=color)
rects1=ax.bar(ind, appended_IRI_q3["R_IRI_N"], width,color='Red',alpha=0.5,label= "R_IRI_N") 


#ax2= dataset["D0"].plot(pos,kind= 'bar',width= width ,color=color)
rects2=ax.bar(ind+0.2, dataset_q3["D0_N"], width, alpha=0.5,color='blue',  label= "D0_N") 
ax.legend((rects1[0], rects2[0]), ('R_IRI_N', 'D0_N'), loc =5)

ax.set_ylabel('Normalised Values')
ax.set_xlabel('DMI Index')
ax.set_title('Comaprison of exact IRI value nearest to 0.75 quantile FWD data')
ax.set_xticks(ind)
ax.set_xticklabels(ind)

ax2 = ax.twiny()
dmi = list(dataset_q3['DMI'])
new_tick_locations = np.array(ind+1)
ax2.set_xticks(new_tick_locations)
ax2.set_xticklabels(dmi,rotation = 90, ha="right",color='blue')
#ax2.set_xlabel('FWD_DMI',color='blue')
ax3 = ax.twiny()
dmi1 = list(appended_df['R_DMI'].astype(int))
new_tick_locations = np.array(ind+1)
ax3.set_xticks(new_tick_locations)
ax3.set_xticklabels(dmi1,rotation = 90, ha="right",va= "top",color='Red')
#ax3.set_xlabel('IRI_DMI',color='red')

plt.tight_layout()  # otherwise the right y-label is slightly clipped

plt.show()




###
"""the next section of code is written to create
comparison of crack density and IRI"""


###
#%%
def round( n ):
 
    # Smaller multiple
    a = (n // 10) * 10
    # Larger multiple
    b = a + 10
    return (int(b))
 


#%%
#Merging the L_IRI data with the zone 2 crack density data for plotting only those DMI values which have non zero crack density values
df_ashhto_2com= df_ashhto_2.copy()
df_ashhto_2com['Density'] = df_ashhto_2com['Density'].replace(0, np.nan) 
df_ashhto_2com = df_ashhto_2com.dropna(axis=0, subset=['Density']) 
IRI_dict = dict(zip(df_IRIFF.RefDMI, df_IRIFF.L_IRI))
df_ashhto_2com['L_IRI']=df_ashhto_2com['DMI'].map(IRI_dict)

#%%
q75=df_ashhto_2com.Density.quantile(0.75)
df_ashhto_2com = df_ashhto_2com[df_ashhto_2com["Density"] >=q75] 
df_ashhto_2com["L_IRI_N"] = (df_ashhto_2com["L_IRI"] - df_ashhto_2com["L_IRI"].min()) / (df_ashhto_2com["L_IRI"].max() - df_ashhto_2com["L_IRI"].min()) 
df_ashhto_2com["Density_N"] = (df_ashhto_2com["Density"] - df_ashhto_2com["Density"].min()) / (df_ashhto_2com["Density"].max() - df_ashhto_2com["Density"].min()) 


# %%
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 900
fig3, ax = plt.subplots()
pos = len(df_ashhto_2com['DMI'])
ind = np.arange(pos, step = 1)
max_iri=df_ashhto_2com["L_IRI_N"].max()
##max_iri= round(max_iri) #commented when plotting normalised value
max_cd=df_ashhto_2com["Density_N"].max()
#max_cd= round(max_cd)   #commented when plotting normalised value
ax2 = ax.twinx()
ax2.set_ylabel('crack density left wheel (%)',fontsize=8)

ax.set_ylim(0,max_iri)
ax2.set_ylim(0,max_cd)
rects1=ax.bar(ind, df_ashhto_2com["L_IRI_N"], width,color='Red',alpha=1,label= "L_IRI_N") 
rects2=ax2.bar(ind+0.2, df_ashhto_2com["Density_N"], width, alpha=1,color='blue',  label= "C.Density_N") 
ax.legend(loc=2,fontsize=8)
ax2.legend(loc=1,fontsize=8)
ax.set_box_aspect(0.25)
ax.set_ylabel('IRI values', fontsize=8)
ax.set_xlabel('DMI Index',fontsize=8)
ax.set_title('Comparison of L_IRI and crack Density zone 2 data quantile (0.75)',fontsize=10)

plt.show()

# %%
#Merging the R_IRI data with the zone 4 crack density data for plotting only those DMI values which have non zero crack density values
df_ashhto_4com= df_ashhto_4.copy()
df_ashhto_4com['Density'] = df_ashhto_4com['Density'].replace(0, np.nan) 
df_ashhto_4com = df_ashhto_4com.dropna(axis=0, subset=['Density']) 
IRI_dict = dict(zip(df_IRIFF.RefDMI, df_IRIFF.R_IRI))
df_ashhto_4com['R_IRI']=df_ashhto_4com['DMI'].map(IRI_dict)

#%%
q75=df_ashhto_4com.Density.quantile(0.75)
df_ashhto_4com = df_ashhto_4com[df_ashhto_4com["Density"] >=q75] 
df_ashhto_4com["R_IRI_N"] = (df_ashhto_4com["R_IRI"] - df_ashhto_4com["R_IRI"].min()) / (df_ashhto_4com["R_IRI"].max() - df_ashhto_4com["R_IRI"].min()) 
df_ashhto_4com["Density_N"] = (df_ashhto_4com["Density"] - df_ashhto_4com["Density"].min()) / (df_ashhto_4com["Density"].max() - df_ashhto_4com["Density"].min()) 


# %%
import matplotlib as mpl
width =0.20
mpl.rcParams['figure.dpi'] = 900
fig3, ax = plt.subplots()
pos = len(df_ashhto_4com['DMI'])
ind = np.arange(pos, step = 1)
#ind=df_ashhto_4com['DMI']
max_iri=df_ashhto_4com["R_IRI_N"].max()
#max_iri= round(max_iri) #commented when plotting normalised value
max_cd=df_ashhto_4com["Density_N"].max()
#max_cd= round(max_cd)   #commented when plotting normalised value
ax2 = ax.twinx()
ax2.set_xticks(ind)
ax.set_xticklabels(list(df_ashhto_4com['DMI']), rotation=65, fontsize=2)
ax2.set_ylabel('crack density Right wheel (%)',fontsize=8)

ax.set_ylim(0,max_iri)
ax2.set_ylim(0,max_cd)
rects1=ax.bar(ind, df_ashhto_4com["R_IRI_N"], width,color='Red',alpha=1,label= "R_IRI_N") 
rects2=ax2.bar(ind+0.2, df_ashhto_4com["Density_N"], width, alpha=1,color='blue',  label= "C.Density_N") 
ax.legend(loc=2,fontsize=8)
ax2.legend(loc=1,fontsize=8)
ax.set_box_aspect(0.25)
ax.set_ylabel('IRI values',fontsize=8)
ax.set_xlabel('DMI',fontsize=8)
ax.set_title('Comparison of R_IRI and crack Density zone 4 data quantile (0.75)',fontsize=10)
plt.tight_layout()
plt.show()


"""---------------------------------------------- 
example from stack overflow for linear regressssion
-------------------------------------------------"""



# %%
import matplotlib.pyplot as plt
plt.plot(df_ashhto_4com["R_IRI"], df_ashhto_4com["Density"])
plt.xlabel("R_IRI")
plt.ylabel("Density_4")
plt.show()
# %%
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

X = df_ashhto_4com["R_IRI"].values
y = df_ashhto_4com["Density"].values
X = X.reshape(-1, 1)
poly = PolynomialFeatures(degree=7)
poly_data = poly.fit_transform(X)
model = LinearRegression()
model.fit(poly_data,y)
coef = model.coef_
intercept = model.intercept_

# %%
plt.scatter(X,y,color='red')
plt.plot(X,model.predict(poly.fit_transform(X)),color='blue')
plt.legend(['Prediction','Original'])
plt.show()




#box whisker plot for the CD2,CD4, L_IRI,R_IRI values


# %%
df_boxp_cd=pd.DataFrame()
df_boxp_cd=df_ashhto_4com[["R_IRI","Density"]].copy()
df_boxp_cd=df_boxp_cd.rename(columns={"Density":"Density_Z2"})

df_boxp_cd.boxplot(fontsize=4,rot=90)





"""--------------------------------------------------- 

Comparison of fwd and crack density 

------------------------------------------------------"""






# %%
#Starting to select crack density zone 2 DMI nearest to FWD DMI 
appended_df_cd=pd.DataFrame()
for index,row in df_EB.iterrows():
    index_value=int(row["DMI"])
    ind= df_ashhto_2['DMI'].sub(index_value).abs().idxmin()
    df_test =df_ashhto_2.loc[ind,:]
    appended_df_cd=appended_df_cd.append(df_test,ignore_index=True)


#%%
# appended_IRI_q3["L_IRI_N"] = (appended_IRI_q3["L_IRI"] - appended_IRI_q3["L_IRI"].min()) / (appended_IRI_q3["L_IRI"].max() - appended_IRI_q3["L_IRI"].min()) 
# appended_IRI_q3["R_IRI_N"] = (appended_IRI_q3["R_IRI"] - appended_IRI_q3["R_IRI"].min()) / (appended_IRI_q3["R_IRI"].max() - appended_IRI["R_IRI"].min()) 


# %%
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
pos = len(df_EB['DMI'])
ind = np.arange(pos, step = 1)

width =0.20
#ax1=appended_df["L_IRI_N"].plot(pos, kind='bar', width= width ,color=color)
rects1=ax.bar(ind, appended_df_cd["Density"], width,color='Red',alpha=0.5,label= "Density") 


#ax2= dataset["D0"].plot(pos,kind= 'bar',width= width ,color=color)
rects2=ax.bar(ind+0.2, df_EB["D0"], width, alpha=0.5,color='blue',  label= "D0") 
ax.legend((rects1[0], rects2[0]), ('Density_2', 'D0'), loc =5)

ax.set_ylabel('crack density %')
ax.set_xlabel('DMI Index')
ax.set_title('Comaprison of exact Density zone2 value nearest to FWD data')
ax.set_xticks(ind)
ax.set_xticklabels(ind)

ax2 = ax.twiny()
ax2.set_ylabel('FWD ')
dmi = list(df_EB['DMI'])
new_tick_locations = np.array(ind+1)
ax2.set_xticks(new_tick_locations)
ax2.set_xticklabels(dmi,rotation = 90, ha="right",color='blue')
#ax2.set_xlabel('FWD_DMI',color='blue')
ax3 = ax.twiny()
dmi1 = list(appended_df_cd['DMI'].astype(int))
new_tick_locations = np.array(ind+1)
ax3.set_xticks(new_tick_locations)
ax3.set_xticklabels(dmi1,rotation = 90, ha="right",va= "top",color='Red')
#ax3.set_xlabel('IRI_DMI',color='red')

plt.tight_layout()  # otherwise the right y-label is slightly clipped

plt.show()


# %%
