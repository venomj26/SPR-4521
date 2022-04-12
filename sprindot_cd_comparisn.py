#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gmaps

#%%
df_ashhto_10=pd.read_csv('/Users/jhasneha/Documents/summer2021/I70-EB-PL-96-104/ASHHTO-10ft/AASHTO_Result.csv')
df_ashhto_100=pd.read_csv('/Users/jhasneha/Documents/summer2021/I70-EB-PL-96-104/ASHHTO-100ft/AASHTO_Result-100ft-I70-EB-PL.csv')
df_ashhto_10.columns = df_ashhto_10.columns.str.replace(' ', '')
df_ashhto_10.columns = df_ashhto_10.columns.str.replace(r'\([^)]*\)', '')
df_ashhto_100.columns = df_ashhto_100.columns.str.replace(' ', '')
df_ashhto_100.columns = df_ashhto_100.columns.str.replace(r'\([^)]*\)', '')







# %%
def ashhto_z2(df_ashhto):
    df_ashhto_2=df_ashhto.copy()
    df_ashhto_2['Zone'] = df_ashhto_2['Zone'].replace(4, np.nan)
    df_ashhto_2= df_ashhto_2.dropna(axis=0, subset=['Zone'])
    return(df_ashhto_2)


#%%
def ashhto_z4(df_ashhto):
    df_ashhto_4=df_ashhto.copy()
    df_ashhto_4['Zone'] = df_ashhto_4['Zone'].replace(2, np.nan)
    df_ashhto_4= df_ashhto_4.dropna(axis=0, subset=['Zone'])
    return(df_ashhto_4)

# %%
def ashhto_dmi_10(df_ashhto):
    df_ashhto["DMI"]=10
    df_ashhto.loc[df_ashhto.index[0],"DMI"]=0
    df_ashhto["DMI"]=df_ashhto["DMI"].cumsum()
    return(df_ashhto)

#%%
def ashhto_dmi_100(df_ashhto):
    df_ashhto["DMI"]=100
    df_ashhto.loc[df_ashhto.index[0],"DMI"]=0
    df_ashhto["DMI"]=df_ashhto["DMI"].cumsum()
    return(df_ashhto)

# %%
df_ashhto_100_z2=ashhto_z2(df_ashhto_100)
df_ashhto_100_z4=ashhto_z4(df_ashhto_100)
df_ashhto_10_z2=ashhto_z2(df_ashhto_10)
df_ashhto_10_z4=ashhto_z4(df_ashhto_10)

#%%
df_ashhto_10_z4=ashhto_dmi_10(df_ashhto_10_z4)
df_ashhto_10_z2=ashhto_dmi_10(df_ashhto_10_z2)
df_ashhto_100_z4=ashhto_dmi_100(df_ashhto_100_z4)
df_ashhto_100_z2=ashhto_dmi_100(df_ashhto_100_z2)



# %%
df_plt_z4=df_ashhto_10_z4[["DMI","Density"]].copy()
z4_dict = dict(zip(df_ashhto_100_z4.DMI, df_ashhto_100_z4.Density))
df_plt_z4['Density_100z4']=df_plt_z4['DMI'].map(z4_dict)

# %%
def plot_comp(df_plot):
    import matplotlib as mpl
    mpl.rcParams['figure.dpi'] = 900
    width=0.9
    fig3, ax = plt.subplots()
    pos = len(df_plot['DMI'])
    ind = np.arange(pos, step = 1)
    max_10=df_plot["Density"].max()
    ##max_iri= round(max_iri) #commented when plotting normalised value
    max_100=df_plot["Density_100z4"].max()
    #max_cd= round(max_cd)   #commented when plotting normalised value
    ax2 = ax.twinx()
    ax2.set_ylabel('crack density_DMI_10(%)',fontsize=8)

    ax.set_ylim(0,max_100)
    ax2.set_ylim(0,max_10)
    rects1=ax.bar(ind, df_plot["Density_100z4"],width=width,color='blue',label= "CD_100") 
    rects2=ax2.bar(ind+width, df_plot["Density"],width=width, color='red',  label= "CD_10") 
    ax.legend(loc=2,fontsize=8)
    ax2.legend(loc=1,fontsize=8)
    ax.set_box_aspect(0.25)
    ax.set_ylabel('crack density_DMI_100(%)', fontsize=8)
    ax.set_xlabel('DMI values',fontsize=8)
    ax.set_title('Comparison of crack density at 10 DMI and 100 DMI for zone 4',fontsize=10)

    return(plt.show())


# %%
plot_comp(df_plt_z4)
# %%
df_plt_z4_ca=df_ashhto_10_z4[["DMI","CrkArea"]].copy()
z4_dict = dict(zip(df_ashhto_100_z4.DMI, df_ashhto_100_z4.CrkArea))
df_plt_z4_ca['CrkArea_100z4']=df_plt_z4_ca['DMI'].map(z4_dict)
# %%
def plot_comp(df_plot):
    import matplotlib as mpl
    mpl.rcParams['figure.dpi'] = 900
    width=0.9
    fig3, ax = plt.subplots()
    #pos = len(df_plot['DMI'])
    #ind = np.arange(pos, step = 1)
    max_10=df_plot["CrkArea"].max()
    ##max_iri= round(max_iri) #commented when plotting normalised value
    max_100=df_plot["CrkArea_100z4"].max()
    #max_cd= round(max_cd)   #commented when plotting normalised value
    ax2 = ax.twinx()
    ax2.set_ylabel('CrkArea_z4',fontsize=8)

    ax.set_ylim(0,max_100)
    ax2.set_ylim(0,max_10)
    rects1=ax.bar(df_plot['DMI'], df_plot["CrkArea_100z4"],alpha=1,color='blue',label= "CrkArea_100") 
    rects2=ax2.bar(df_plot['DMI']+0.9, df_plot["CrkArea"], alpha=1, color='red',  label= "CrkArea_10") 
    ax.legend(loc=2,fontsize=8)
    ax2.legend(loc=1,fontsize=8)
    ax.set_box_aspect(0.25)
    ax.set_ylabel('CrkArea_100z4', fontsize=8)
    ax.set_xlabel('DMI values',fontsize=8)
    ax.set_title('Comparison of CrkArea at 10 DMI and 100 DMI for zone 4',fontsize=10)

    return(plt.show())
# %%
plot_comp(df_plt_z4_ca)

# %%
