#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openpyxl
import gmaps

#%%
# df_ashhto=pd.read_csv('/Users/jhasneha/Documents/SPRINDOT/summer2021/SPRINDOT/I70/I70-EB-DL-96-104/AASHTO_Result_6ft.csv')
# df_IRI=pd.read_csv('/Users/jhasneha/Documents/SPRINDOT/summer2021/SPRINDOT/I70/I70-EB-DL-96-104/IRI-report-6ft.csv')
# df_fwd=pd.read_excel('/Users/jhasneha/Documents/SPRINDOT/summer2021/SPRINDOT/I70/SCI/I70 (PL)_East and West Bound Lane from RP 95+95 to RP 100+65.xlsx',sheet_name="I70-EB")

df_ashhto=pd.read_csv('/Users/jhasneha/Documents/SPRINDOT/summer2021/SPRINDOT/I70/I70-WB-PL-96-104 /AASHTO_Result-6ft.csv')
df_IRI=pd.read_csv('/Users/jhasneha/Documents/SPRINDOT/summer2021/SPRINDOT/I70/I70-WB-PL-96-104 /IRI-report-6ft.csv')
df_fwd=pd.read_excel('/Users/jhasneha/Documents/SPRINDOT/summer2021/SPRINDOT/I70/SCI/I70 (PL)_East and West Bound Lane from RP 95+95 to RP 100+65.xlsx',sheet_name="I70-WB")


# df_ashhto=pd.read_csv('/Users/jhasneha/Documents/SPRINDOT/summer2021/SPRINDOT/I70-EB-PL-96-104/AASHTO_Result-6ft.csv')
# df_IRI=pd.read_csv('/Users/jhasneha/Documents/SPRINDOT/summer2021/SPRINDOT/I70-EB-PL-96-104/IRI-report-6ft.csv')
# df_fwd=pd.read_excel('/Users/jhasneha/Documents/SPRINDOT/summer2021/SPRINDOT/SCI/I70 (PL)_East and West Bound Lane from RP 95+95 to RP 100+65.xlsx',sheet_name="I70-EB")


# df_ashhto=pd.read_csv('/Users/jhasneha/Documents/SPRINDOT/summer2021/SPRINDOT/I70-EB-DL-96-104/AASHTO_Result_6ft (2).csv')
# df_IRI=pd.read_csv('/Users/jhasneha/Documents/SPRINDOT/summer2021/SPRINDOT/I70-EB-DL-96-104/IRI-report-6ft.csv')
# df_fwd=pd.read_excel('/Users/jhasneha/Documents/SPRINDOT/summer2021/SPRINDOT/SCI/I70 (DL)_East and West Bound Lane from RP 95+95 to RP 100+65.xlsx',sheet_name="I70-EB")

df_ashhto.columns = df_ashhto.columns.str.replace(' ', '')
df_ashhto.columns = df_ashhto.columns.str.replace(r'\([^)]*\)', '')
df_IRI.columns = df_IRI.columns.str.replace(' ', '')
df_IRI.columns = df_IRI.columns.str.replace(r'\([^)]*\)', '')
df_fwd.columns = df_fwd.columns.str.replace(' ', '')
df_fwd.columns = df_fwd.columns.str.replace(r'\([^)]*\)', '')
df_fwd.columns = df_fwd.columns.str.replace(' ', '')
df_fwd.columns = df_fwd.columns.str.replace(r'\([^)]*\)', '')

#%%
df_fwd=df_fwd.rename(columns={"SBorWBFWDStation":"DMI","NBorEBFWDStation":"DMI"})
df_fwd=df_fwd.rename(columns={"SubgradeDeflection":"D48"})
df_fwd=df_fwd.rename(columns={"SurfaceDeflection":"D0"})
df_fwd=df_fwd.rename(columns={"SCI300":"SCI"})

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
def ashhto_dmi(df_ashhto):
    df_ashhto["DMI"]=6
    df_ashhto.loc[df_ashhto.index[0],"DMI"]=0
    df_ashhto["DMI"]=df_ashhto["DMI"].cumsum()
    return(df_ashhto)


# %%
df_ashhto_z2=ashhto_z2(df_ashhto)
df_ashhto_z4=ashhto_z4(df_ashhto)

#%%
df_ashhto_z4=ashhto_dmi(df_ashhto_z4)
df_ashhto_z2=ashhto_dmi(df_ashhto_z2)



"""------------------------------

the IRI_CD comparison codes start here

------------------------------------"""
# %%
df_plt_z4=df_ashhto_z4[["DMI","Density"]].copy()
RIRI_dict = dict(zip(df_IRI.RefDMI, df_IRI.R_IRI))
df_plt_z4['R_IRI']=df_plt_z4['DMI'].map(RIRI_dict)

#%%
df_plt_z4['Density'] = df_plt_z4['Density'].replace(0, np.nan) 
df_plt_z4 = df_plt_z4.dropna(axis=0, subset=['Density']) 


#%%
q75=df_plt_z4.R_IRI.quantile(0.75)
df_plt_z4 = df_plt_z4[df_plt_z4["R_IRI"] >=q75] 

# %%
def plot_comp_z4(df_plot):
    import matplotlib as mpl
    mpl.rcParams['figure.dpi'] = 300
    
    width=1
    fig3, ax = plt.subplots()
    max_IRI=df_plot["R_IRI"].max() + 100
    ##max_iri= round(max_iri) #commented when plotting normalised value
    max_CD=df_plot["Density"].max() + 1
    #max_cd= round(max_cd)   #commented when plotting normalised value
    ax2 = ax.twinx()
    ax2.set_ylabel('crack density(%)',fontsize=8)
    ax2.tick_params(labelsize=8)
    ax.set_ylim(0,max_IRI)
    ax2.set_ylim(0,max_CD)
    markerline, stemline,baseline, =ax.stem(df_plot['DMI'], df_plot["R_IRI"],linefmt=':',markerfmt= 'o',label= "R_IRI") 
    markerline2, stemline2, baseline2, =ax2.stem(df_plot['DMI']+ 0.1, df_plot["Density"], linefmt=':',markerfmt= 'x',  label= "CD-Right wheel path") 
    
    ax.set_box_aspect(1)
    ax.set_ylabel('IRI', fontsize=8)
    ax.set_xlabel('DMI values (ft)',fontsize=8)
    ax.tick_params(labelsize=8)
    ax.set_title('Us-41-NB-DL Comparison of crack density at zone 4 and Right IRI',fontsize=8)
    #markerline, stemline, baseline, = ax.stem(x,y,linefmt='k-',markerfmt='ko',basefmt='k.')
    plt.setp(stemline,color='white', linewidth = 0.8)
    plt.setp(markerline,color='m', markersize = 3,markeredgecolor="darkmagenta")
    plt.setp(stemline2,color='white', linewidth = 0.8)
    plt.setp(markerline2,color='b', markersize = 3,markeredgecolor="darkblue")
    ax.axhline(y=270, color='red', linewidth= 0.8,linestyle="--",label="IRI=270")
    ax.axhline(y=150, color='orange', linewidth= 0.8,linestyle="--",label="IRI=150")
    ax.axhline(y=80, color='green', linewidth= 0.8,linestyle="--",label="IRI=80")
    ax.legend(fontsize=8,loc=1)
    ax2.legend(fontsize=8,loc=2)
    #ax2.axhline(y=2, color='g', linewidth=0.8)
    return(plt.show())


#%%
plot_comp_z4(df_plt_z4)

#%%
df_plt_z2=df_ashhto_z2[["DMI","Density"]].copy()
LIRI_dict = dict(zip(df_IRI.RefDMI, df_IRI.L_IRI))
df_plt_z2['L_IRI']=df_plt_z2['DMI'].map(LIRI_dict)

#%%
df_plt_z2['Density'] = df_plt_z2['Density'].replace(0, np.nan) 
df_plt_z2 = df_plt_z2.dropna(axis=0, subset=['Density']) 


#%%
q75=df_plt_z2.L_IRI.quantile(0.75)
df_plt_z2 = df_plt_z2[df_plt_z2["L_IRI"] >=q75] 



# %%
def plot_comp_z2(df_plot):
    import matplotlib as mpl
    mpl.rcParams['figure.dpi'] = 300
    mpl.rc('font',family='Times New Roman')

    fig3, ax = plt.subplots()
    max_IRI=df_plot["L_IRI"].max()+100
    ##max_iri= round(max_iri) #commented when plotting normalised value
    max_CD=df_plot["Density"].max()+1
    #max_cd= round(max_cd)   #commented when plotting normalised value
    ax2 = ax.twinx()
    ax2.set_ylabel('crack density(%)',fontsize=14)
    ax2.tick_params(labelsize=14)
    ax.set_ylim(0,max_IRI)
    ax2.set_ylim(0,max_CD)
    markerline, stemline, baseline,=ax.stem(df_plot['DMI'], df_plot["L_IRI"],linefmt=':',label= "L_IRI") 
    markerline2, stemline2, baseline2,=ax2.stem(df_plot['DMI']+ 0.1, df_plot["Density"], linefmt=':',markerfmt= 'x',  label= "CD-Left wheel path") 
    
    ax.set_box_aspect(1)
    ax.set_ylabel('IRI', fontsize=14)
    ax.set_xlabel('DMI values (ft)',fontsize=14)
    ax.tick_params(labelsize=8)
    #ax.set_title('I70-WB-PL Comparison of crack density at zone 2, D0 and Left IRI(iri_q=0.75)',fontsize=8)
    #markerline, stemline, baseline, = ax.stem(x,y,linefmt='k-',markerfmt='ko',basefmt='k.')
    plt.setp(stemline,color='m', linewidth = 1)
    plt.setp(markerline,color='m', markersize = 3,markeredgecolor="darkmagenta")
    plt.setp(stemline2,color='b', linewidth = 1)
    plt.setp(markerline2,color='b', markersize = 3,markeredgecolor="darkblue")
    
    ax.axhline(y=270, color='m', linewidth= 0.8,linestyle="--", label="IRI=270")
    ax.legend(bbox_to_anchor=(1, 1),fontsize=14)
    ax2.legend(loc=2,fontsize=14)
    return(plt.show())

#%%
plot_comp_z2(df_plt_z2)




"""___________________________________

NOW including the FWD data to plottable data of crack density and IRI
___________________________________________"""


#%%
def nearest(df_fwd, df):
    nearest_df=pd.DataFrame()
    for index,row in df_fwd.iterrows():
        index_value=int(row["DMI"])
        ind= df["DMI"].sub(index_value).abs().idxmin()
        df_test =df.loc[ind,:]
        nearest_df=nearest_df.append(df_test,ignore_index=True)
    return(nearest_df)


#%%
df_plt_z2=df_ashhto_z2[["DMI","Density"]].copy()
LIRI_dict = dict(zip(df_IRI.RefDMI, df_IRI.L_IRI))
df_plt_z2["L_IRI"]=df_plt_z2["DMI"].map(LIRI_dict)
df_pltz2_nearest=nearest(df_fwd,df_plt_z2)
df_pltz2_nearest=df_pltz2_nearest.reset_index()

#%%
df_fwd_m=df_fwd[["DMI","D0","D48","SCI","BDI","BCI"]].copy() #some dont have AUPP calculated
df_fwd_m=df_fwd_m.rename(columns={'DMI':'DMI_fwd'})
df_concat_z2=pd.concat([df_pltz2_nearest,df_fwd_m], axis=1)



"""+++++++++++++++++++++++++++++++++++++
This plot is for zone 2 and FWD iri cd BCI SCI BDI data comment the ones you dont want
++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""

# decrease the number of points in the plot to 0.75 quantile
#%%
D0_q75=df_concat_z2.D0.quantile(0.75)
df_concat_z2 = df_concat_z2[df_concat_z2["D0"] >=D0_q75] 

#%%
D48_q75=df_concat_z2.D48.quantile(0.75)
df_concat_z2 = df_concat_z2[df_concat_z2["D48"] >=D48_q75] 




# %%
def plot_con_z2(df_plot):
    import matplotlib as mpl
    mpl.rcParams['figure.dpi'] = 300
    mpl.rc('font',family='Times New Roman')

    fig, ax = plt.subplots()
    fig.subplots_adjust(right=0.75)
    max_IRI=df_plot["L_IRI"].max() + 100
    ##max_iri= round(max_iri) #commented when plotting normalised value
    max_CD=df_plot["Density"].max() + 0.1
    max_D0=df_plot["D0"].max()+ 1
    max_D48=df_plot["D48"].max()+ 1
    #max_cd= round(max_cd)   #commented when plotting normalised value
    ax2 = ax.twinx()
    ax3 = ax.twinx()
    ax4 = ax3
    ax5 = ax3
    ax6 = ax3
    ax7 = ax3
    ax3.spines.right.set_position(("axes", 1.2))
    #ax4.spines.right.set_position(("axes", 1.4))
    ax2.set_ylabel('Crack-Density(%)',fontsize=14)
    ax2.tick_params(labelsize=14)
    ax3.set_ylabel('FWD (milli-inches)',fontsize=14)
    ax3.tick_params(labelsize=14)
    # ax4.set_ylabel('FWD(milli-inches)',fontsize=8)
    # ax4.tick_params(labelsize=8)
    if max_IRI < 270:
        iri= 300
    else:
        iri= max_IRI +50

    if max_D0 < 24.6:
        D0= 25
    else:
        D0= max_D0 +1

    
    ax.set_ylim(0,iri)
    ax2.set_ylim(0,max_CD)
    ax3.set_ylim(0,D0)
    ax4.set_ylim(0,D0)
    ax5.set_ylim(0,D0)
    ax6.set_ylim(0,D0)
    ax7.set_ylim(0,D0)

    markerline, stemline, baseline,=ax.stem(df_plot['DMI'], df_plot["L_IRI"],linefmt=':',markerfmt= 'o',basefmt=' ',label= "L_IRI") 
    markerline.set_markerfacecolor('crimson')
    markerline2, stemline2, baseline2,=ax2.stem(df_plot['DMI'], df_plot["Density"], linefmt=':',markerfmt= 'D', basefmt=' ',  label= "CD_Left wheel path") 
    markerline2.set_markerfacecolor('blue')
    markerline3, stemline3, baseline3,=ax3.stem(df_plot['DMI_fwd'], df_plot["D0"], linefmt=':',markerfmt= 'x',basefmt=' ',  label= "D0-surface") 
    markerline3.set_markerfacecolor('darkslategrey')
    markerline4, stemline4, baseline4,=ax4.stem(df_plot['DMI_fwd'], df_plot["D48"], linefmt=':',markerfmt= 's',basefmt=' ',  label= "D48-subgrade") 
    markerline4.set_markerfacecolor('orange')
    markerline5, stemline5, baseline5,=ax5.stem(df_plot['DMI_fwd'], df_plot["SCI"], linefmt=':',markerfmt= 'D', basefmt=' ', label= "SCI-surface") 
    markerline5.set_markerfacecolor('gold')
    markerline6, stemline6, baseline6,=ax6.stem(df_plot['DMI_fwd'], df_plot["BDI"], linefmt=':',markerfmt= 'o',basefmt=' ',  label= "BDI-Middle layer") 
    markerline6.set_markerfacecolor('crimson')
    markerline7, stemline7, baseline7,=ax7.stem(df_plot['DMI_fwd'], df_plot["BCI"], linefmt=':',markerfmt= 'x',basefmt=' ',  label= "BCI- Lower layer") 
    markerline7.set_markerfacecolor('navy')
    ax.set_box_aspect(1)
    ax.set_ylabel('IRI (in/mi)', fontsize=14)
    ax.tick_params(labelsize=14)
    ax.set_xlabel('DMI values(ft)',fontsize=14)
    #ax.set_title('I74-WB-DL  Comparison of crack density at zone 2(left wheel), D0 , D48, SCI, BDI, BCI and left IRI',fontsize=8)
    #markerline, stemline, baseline, = ax.stem(x,y,linefmt='k-',markerfmt='ko',basefmt='k.')
    plt.setp(stemline,color='m', linewidth = 0.8)
    plt.setp(markerline, markersize = 3,markeredgecolor="m",markeredgewidth=0.5)
    
    plt.setp(stemline2,color='darkgoldenrod', linewidth = 0.8)
    plt.setp(markerline2, markersize = 3,markeredgecolor="darkgoldenrod", markeredgewidth=0.7)
    
    plt.setp(stemline3,color='darkslategrey', linewidth = 0.8)
    plt.setp(markerline3, markersize = 6 ,markeredgecolor="darkslategrey",markeredgewidth=0.9)
    
    plt.setp(stemline4,color='green', linewidth = 0.8)
    plt.setp(markerline4, markersize =6,markeredgecolor="green",markeredgewidth=0.7)

    plt.setp(stemline5,color='black', linewidth = 0.8)
    plt.setp(markerline5, markersize = 5,markeredgecolor="black",markeredgewidth=0.7)

    plt.setp(stemline6,color='darkgreen', linewidth = 0.8)
    plt.setp(markerline6, markersize = 4,markeredgecolor="darkgreen",markeredgewidth=0.8)

    plt.setp(stemline7,color='navy', linewidth = 0.8)
    plt.setp(markerline7, markersize = 6,markeredgecolor="navy", markeredgewidth=0.5)
   
    ax.axhline(y=270, color='m', linewidth= 0.8, linestyle="--",label="IRI=270")
    ax3.axhline(y=36.4, color='darkslategrey', linewidth= 0.8, linestyle="--", label="D0=24.6")
    ax4.axhline(y=1.8, color='g', linewidth= 0.8, linestyle="--", label="D48=1.8")
    ax5.axhline(y=8, color='black', linewidth= 0.8, linestyle="--", label="SCI=8")
    ax6.axhline(y=4.5, color='red', linewidth= 0.8, linestyle="--", label="BDI=4.5")
    ax7.axhline(y=4, color='blue', linewidth= 0.8, linestyle="--", label="BCI=4")
    ax.legend(bbox_to_anchor=(-0.2,1),loc=1,fontsize=6,markerscale=1)
    ax2.legend(bbox_to_anchor=(-0.2, 0.9),loc=1,fontsize=6, markerscale=1) #using a loc1 with bbox fixes the location to right corner and helps the bbox to plot at the right position
    ax3.legend(bbox_to_anchor=(-0.2,0.9),loc=1,fontsize=6,markerscale=1)
    ax4.legend(bbox_to_anchor=(-0.2, 0.85),loc=1,fontsize=6,markerscale=1)
    ax5.legend(bbox_to_anchor=(-0.2, 0.8),loc=1,fontsize=6,markerscale=1)
    ax6.legend(bbox_to_anchor=(-0.2, 0.75),loc=1,fontsize=6,markerscale=1)
    ax7.legend(bbox_to_anchor=(-0.2, 0.7),loc=1,fontsize=6,markerscale=1)
    ax.set_facecolor('lavenderblush')
    return(plt.show())



""" larger font graph for ITSC conference paper"""
# %%
def plot_con_z2(df_plot):
    import matplotlib as mpl
    mpl.rcParams['figure.dpi'] = 300
    mpl.rc('font',family='Times New Roman')
    # plt.rcParams["figure.figsize"] = (4,50)
    # from matplotlib.pyplot import figure
    # figure(figsize = (10, 5), dpi = 80)

    fig, ax = plt.subplots()
    fig.subplots_adjust(right=0.75)
    max_IRI=df_plot["L_IRI"].max() + 100
    ##max_iri= round(max_iri) #commented when plotting normalised value
    max_CD=df_plot["Density"].max() + 0.1
    max_D0=df_plot["D0"].max()+ 1
    max_D48=df_plot["D48"].max()+ 1
    #max_cd= round(max_cd)   #commented when plotting normalised value
    ax2 = ax.twinx()
    ax3 = ax.twinx()
    ax4 = ax3
    ax5 = ax3
    ax6 = ax3
    ax7 = ax3
    ax3.spines.right.set_position(("axes", 1.2))
    #ax4.spines.right.set_position(("axes", 1.4))
    ax2.set_ylabel('Crack-Density(%)',fontsize=14)
    ax2.tick_params(labelsize=14)
    ax3.set_ylabel('FWD (milli-inches)',fontsize=14)
    ax3.tick_params(labelsize=14)
    # ax4.set_ylabel('FWD(milli-inches)',fontsize=8)
    # ax4.tick_params(labelsize=8)
    if max_IRI < 270:
        iri= 300
    else:
        iri= max_IRI +50

    if max_D0 < 36.4:
        D0= 25
    else:
        D0= max_D0 +1

    
    ax.set_ylim(0,iri)
    ax2.set_ylim(0,max_CD)
    ax3.set_ylim(0,D0)
    ax4.set_ylim(0,D0)
    ax5.set_ylim(0,D0)
    ax6.set_ylim(0,D0)
    ax7.set_ylim(0,D0)

    markerline, stemline, baseline,=ax.stem(df_plot['DMI'], df_plot["L_IRI"],linefmt=':',markerfmt= 'o',basefmt=' ',label= "L_IRI") 
    markerline.set_markerfacecolor('crimson')
    markerline2, stemline2, baseline2,=ax2.stem(df_plot['DMI'], df_plot["Density"], linefmt=':',markerfmt= 'D', basefmt=' ',  label= "CD_Left wheel path") 
    markerline2.set_markerfacecolor('blue')
    markerline3, stemline3, baseline3,=ax3.stem(df_plot['DMI_fwd'], df_plot["D0"], linefmt=':',markerfmt= 'x',basefmt=' ',  label= "D0-surface") 
    markerline3.set_markerfacecolor('darkslategrey')
    markerline4, stemline4, baseline4,=ax4.stem(df_plot['DMI_fwd'], df_plot["D48"], linefmt=':',markerfmt= 's',basefmt=' ',  label= "D48-subgrade") 
    markerline4.set_markerfacecolor('orange')
    markerline5, stemline5, baseline5,=ax5.stem(df_plot['DMI_fwd'], df_plot["SCI"], linefmt=':',markerfmt= 'D', basefmt=' ', label= "SCI-surface") 
    markerline5.set_markerfacecolor('gold')
    markerline6, stemline6, baseline6,=ax6.stem(df_plot['DMI_fwd'], df_plot["BDI"], linefmt=':',markerfmt= 'o',basefmt=' ',  label= "BDI-Middle layer") 
    markerline6.set_markerfacecolor('crimson')
    markerline7, stemline7, baseline7,=ax7.stem(df_plot['DMI_fwd'], df_plot["BCI"], linefmt=':',markerfmt= 'x',basefmt=' ',  label= "BCI- Lower layer") 
    markerline7.set_markerfacecolor('navy')
    ax.set_box_aspect(1)
    ax.set_ylabel('IRI (in/mi)', fontsize=14)
    ax.tick_params(labelsize=14)
    ax.set_xlabel('DMI values(ft)',fontsize=14)
    #ax.set_title('I74-WB-DL  Comparison of crack density at zone 2(left wheel), D0 , D48, SCI, BDI, BCI and left IRI',fontsize=8)
    #markerline, stemline, baseline, = ax.stem(x,y,linefmt='k-',markerfmt='ko',basefmt='k.')
    plt.setp(stemline,color='m', linewidth = 0.8)
    plt.setp(markerline, markersize = 3,markeredgecolor="m",markeredgewidth=0.5)
    
    plt.setp(stemline2,color='darkgoldenrod', linewidth = 0.8)
    plt.setp(markerline2, markersize = 3,markeredgecolor="darkgoldenrod", markeredgewidth=0.7)
    
    plt.setp(stemline3,color='darkslategrey', linewidth = 0.8)
    plt.setp(markerline3, markersize = 6 ,markeredgecolor="darkslategrey",markeredgewidth=0.9)
    
    plt.setp(stemline4,color='green', linewidth = 0.8)
    plt.setp(markerline4, markersize =6,markeredgecolor="green",markeredgewidth=0.7)

    plt.setp(stemline5,color='black', linewidth = 0.8)
    plt.setp(markerline5, markersize = 5,markeredgecolor="black",markeredgewidth=0.7)

    plt.setp(stemline6,color='darkgreen', linewidth = 0.8)
    plt.setp(markerline6, markersize = 4,markeredgecolor="darkgreen",markeredgewidth=0.8)

    plt.setp(stemline7,color='navy', linewidth = 0.8)
    plt.setp(markerline7, markersize = 6,markeredgecolor="navy", markeredgewidth=0.5)
    
    ax.set_ylim([0,600])
    ax2.set_ylim([0,5])
    ax3.set_ylim([0,25])
    fig.set_figwidth(15)
    fig.set_figheight(5)
    ax.axhline(y=270, color='m', linewidth= 1, linestyle="--",label="IRI=270")
    ax3.axhline(y=24.6, color='darkslategrey', linewidth= 1, linestyle="--", label="D0=24.6")
    ax4.axhline(y=1.8, color='g', linewidth= 1, linestyle="--", label="D48=1.8")
    ax5.axhline(y=8, color='black', linewidth= 1, linestyle="--", label="SCI=8")
    ax6.axhline(y=4.5, color='red', linewidth= 1, linestyle="--", label="BDI=4.5")
    ax7.axhline(y=4, color='blue', linewidth= 1, linestyle="--", label="BCI=4")
    ax.legend(bbox_to_anchor=(-0.2,0.95),loc=1,fontsize=12,markerscale=1)
    ax2.legend(bbox_to_anchor=(-0.2, 0.79),loc=1,fontsize=12, markerscale=1) #using a loc1 with bbox fixes the location to right corner and helps the bbox to plot at the right position
    ax3.legend(bbox_to_anchor=(-0.2, 0.85),loc=1,fontsize=12,markerscale=1)
    ax4.legend(bbox_to_anchor=(-0.2, 0.85),loc=1,fontsize=12,markerscale=1)
    ax5.legend(bbox_to_anchor=(-0.2, 0.8),loc=1,fontsize=12,markerscale=1)
    ax6.legend(bbox_to_anchor=(-0.2, 0.75),loc=1,fontsize=12,markerscale=1)
    ax7.legend(bbox_to_anchor=(-0.2, 0.7),loc=1,fontsize=12,markerscale=1)
    #ax.set_facecolor('lavenderblush')
    plt.savefig("graphs/scatter_I70/I70_zone2.svg", dpi=600)
    return(plt.show())

#%%
plot_con_z2(df_concat_z2)



# %%
df_plt_z4=df_ashhto_z4[["DMI","Density"]].copy()
RIRI_dict = dict(zip(df_IRI.RefDMI, df_IRI.R_IRI))
df_plt_z4['R_IRI']=df_plt_z4['DMI'].map(RIRI_dict)
df_pltz4_nearest=nearest(df_fwd,df_plt_z4)
df_pltz4_nearest=df_pltz4_nearest.reset_index()

#%%
df_fwd_m=df_fwd[["DMI","D0","D48","SCI","BDI","BCI"]].copy()
df_fwd_m=df_fwd_m.rename(columns={'DMI':'DMI_fwd'})
df_concat_z4=pd.concat([df_pltz4_nearest,df_fwd_m], axis=1)


# %%
def plot_con_z4(df_plot):
    import matplotlib as mpl
    mpl.rcParams['figure.dpi'] = 300

    fig, ax = plt.subplots()
    max_IRI=df_plot["R_IRI"].max() 
    ##max_iri= round(max_iri) #commented when plotting normalised value
    max_CD=df_plot["Density"].max() + 0.1
    max_D0=df_plot["D0"].max() + 1
    max_D48=df_plot["D48"].max() + 1
    #max_cd= round(max_cd)   #commented when plotting normalised value
    ax2 = ax.twinx()
    ax3 = ax.twinx()
    ax4 = ax.twinx()
    ax3.spines.right.set_position(("axes", 1.2))
    ax4.spines.right.set_position(("axes", 1.4))
    ax2.set_ylabel('crack density(%)',fontsize=)
    ax2.tick_params(labelsize=8)
    ax3.set_ylabel('D0 (milli-inches)',fontsize=7)
    ax3.tick_params(labelsize=8)
    ax4.set_ylabel('D48(milli-inches)',fontsize=7)
    ax4.tick_params(labelsize=8)
    if max_IRI < 270:
        iri= 300
    else:
        iri= max_IRI +50

    if max_D0 < 36.5:
        D0= 25
    else:
        D0= max_D0 +1
    ax.set_ylim(0,iri)
    ax2.set_ylim(0,max_CD)
    ax3.set_ylim(0,D0)
    ax4.set_ylim(0,D0)
    markerline, stemline, baseline,=ax.stem(df_plot['DMI'], df_plot["R_IRI"],linefmt=':',markerfmt= 'o',label= "R_IRI") 
    markerline.set_markerfacecolor('m')
    markerline2, stemline2, baseline2,=ax2.stem(df_plot['DMI']+ 0.1, df_plot["Density"], linefmt=':',markerfmt= 'D',  label= "CD_right wheel path") 
    markerline2.set_markerfacecolor('b')
    markerline3, stemline3, baseline3,=ax3.stem(df_plot['DMI_fwd'], df_plot["D0"], linefmt=':',markerfmt= 'x',  label= "D0-surface") 
    markerline3.set_markerfacecolor('k')
    markerline4, stemline4, baseline4,=ax4.stem(df_plot['DMI_fwd'], df_plot["D48"], linefmt=':',markerfmt= 's',  label= "D48-subgrade") 
    markerline4.set_markerfacecolor('g')
    ax.set_box_aspect(1)
    ax.set_ylabel('IRI', fontsize=8)
    ax.set_xlabel('DMI values (ft)',fontsize=8)
    ax.tick_params(labelsize=8)
    ax.set_title('I70-EB-PL Comparison of crack density at zone 4, D0,D48 and Right IRI',fontsize=7)
    #markerline, stemline, baseline, = ax.stem(x,y,linefmt='k-',markerfmt='ko',basefmt='k.')
    plt.setp(stemline,color='m', linewidth = 1)
    plt.setp(markerline, markersize = 2.5,markeredgecolor="darkmagenta")
    
    plt.setp(stemline2,color='blue', linewidth = 1)
    plt.setp(markerline2, markersize = 3,markeredgecolor="darkblue")
    
    plt.setp(stemline3,color='black', linewidth =1)
    plt.setp(markerline3, markersize = 5,markeredgecolor="black")
    
    plt.setp(stemline4,color='g', linewidth = 1)
    plt.setp(markerline4, markersize = 3,markeredgecolor="darkgreen")
    
    ax.axhline(y=270, color='m', linewidth= 0.8, label="IRI=270")
    ax3.axhline(y=24.6, color='k', linewidth= 0.8, linestyle="--", label="D0=24.6")
    ax4.axhline(y=1.8, color='g', linewidth= 0.8, linestyle="--", label="D48=1.8")
    ax.legend(loc=1,fontsize=6,markerscale=4)
    ax2.legend(loc=2,fontsize=6, markerscale=4)
    ax3.legend(loc=9,fontsize=6,markerscale=4)
    ax4.legend(bbox_to_anchor=(1, 0.75),loc=1,fontsize=6,markerscale=4)
    return(plt.show())



#%%
plot_con_z4(df_concat_z4)


"""______________________________
including FWD SCI300, BDI etc"

_________________________________"""

# decrease the number of points in the plot to 0.75 quantile
#%%
D0_q75=df_concat_z4.D0.quantile(0.75)
df_concat_z4 = df_concat_z4[df_concat_z4["D0"] >=D0_q75] 

#%%
D48_q75=df_concat_z4.D48.quantile(0.75)
df_concat_z4 = df_concat_z4[df_concat_z4["D48"] >=D48_q75] 



#%%
def plot_con_z4(df_plot):
    import matplotlib as mpl
    mpl.rcParams['figure.dpi'] = 300

    fig, ax = plt.subplots()
    fig.subplots_adjust(right=0.75)
    max_IRI=df_plot["R_IRI"].max() + 100
    ##max_iri= round(max_iri) #commented when plotting normalised value
    max_CD=df_plot["Density"].max() + 0.1
    max_D0=df_plot["D0"].max()+ 1
    max_D48=df_plot["D48"].max()+ 1
    #max_cd= round(max_cd)   #commented when plotting normalised value
    ax2 = ax.twinx()
    ax3 = ax.twinx()
    ax4 = ax3
    ax5 = ax3
    ax6 = ax3
    ax7 = ax3
    ax3.spines.right.set_position(("axes", 1.2))
    #ax4.spines.right.set_position(("axes", 1.4))
    ax2.set_ylabel('Crack-Density(%)',fontsize=8)
    ax2.tick_params(labelsize=8)
    ax3.set_ylabel('FWD (milli-inches)',fontsize=8)
    ax3.tick_params(labelsize=8)
    # ax4.set_ylabel('FWD(milli-inches)',fontsize=8)
    # ax4.tick_params(labelsize=8)
    if max_IRI < 270:
        iri= 300
    else:
        iri= max_IRI +50

    if max_D0 < 24.6:
        D0= 25
    else:
        D0= max_D0 +1

    
    ax.set_ylim(0,iri)
    ax2.set_ylim(0,max_CD)
    ax3.set_ylim(0,D0)
    ax4.set_ylim(0,D0)
    ax5.set_ylim(0,D0)
    ax6.set_ylim(0,D0)
    ax7.set_ylim(0,D0)

    markerline, stemline, baseline,=ax.stem(df_plot['DMI'], df_plot["R_IRI"],linefmt=':',markerfmt= 'o',basefmt=' ',label= "R_IRI") 
    markerline.set_markerfacecolor('crimson')
    markerline2, stemline2, baseline2,=ax2.stem(df_plot['DMI'], df_plot["Density"], linefmt=':',markerfmt= 'D', basefmt=' ',  label= "CD_Left wheel path") 
    markerline2.set_markerfacecolor('blue')
    markerline3, stemline3, baseline3,=ax3.stem(df_plot['DMI_fwd'], df_plot["D0"], linefmt=':',markerfmt= 'x',basefmt=' ',  label= "D0-surface") 
    markerline3.set_markerfacecolor('darkslategrey')
    markerline4, stemline4, baseline4,=ax4.stem(df_plot['DMI_fwd'], df_plot["D48"], linefmt=':',markerfmt= 's',basefmt=' ',  label= "D48-subgrade") 
    markerline4.set_markerfacecolor('orange')
    markerline5, stemline5, baseline5,=ax5.stem(df_plot['DMI_fwd'], df_plot["SCI"], linefmt=':',markerfmt= 'D', basefmt=' ', label= "SCI-surface") 
    markerline5.set_markerfacecolor('gold')
    markerline6, stemline6, baseline6,=ax6.stem(df_plot['DMI_fwd'], df_plot["BDI"], linefmt=':',markerfmt= 'o',basefmt=' ',  label= "BDI-Middle layer") 
    markerline6.set_markerfacecolor('crimson')
    markerline7, stemline7, baseline7,=ax7.stem(df_plot['DMI_fwd'], df_plot["BCI"], linefmt=':',markerfmt= 'x',basefmt=' ',  label= "BCI- Lower layer") 
    markerline7.set_markerfacecolor('navy')
    ax.set_box_aspect(1)
    ax.set_ylabel('IRI (in/mi)', fontsize=8)
    ax.tick_params(labelsize=8)
    ax.set_xlabel('DMI values(ft)',fontsize=8)
    ax.set_title('I64-WB-DL RP 78-85 Comparison of crack density at zone 4(right wheel), D0, D48, SCI, BDI, BCI and Right IRI',fontsize=8)
    #markerline, stemline, baseline, = ax.stem(x,y,linefmt='k-',markerfmt='ko',basefmt='k.')
    plt.setp(stemline,color='m', linewidth = 0.8)
    plt.setp(markerline, markersize = 3,markeredgecolor="m",markeredgewidth=0.5)
    
    plt.setp(stemline2,color='darkgoldenrod', linewidth = 0.8)
    plt.setp(markerline2, markersize = 3,markeredgecolor="darkgoldenrod", markeredgewidth=0.7)
    
    plt.setp(stemline3,color='darkslategrey', linewidth = 0.8)
    plt.setp(markerline3, markersize = 6 ,markeredgecolor="darkslategrey",markeredgewidth=0.9)
    
    plt.setp(stemline4,color='green', linewidth = 0.8)
    plt.setp(markerline4, markersize =6,markeredgecolor="green",markeredgewidth=0.7)

    plt.setp(stemline5,color='black', linewidth = 0.8)
    plt.setp(markerline5, markersize = 5,markeredgecolor="black",markeredgewidth=0.7)

    plt.setp(stemline6,color='darkgreen', linewidth = 0.8)
    plt.setp(markerline6, markersize = 4,markeredgecolor="darkgreen",markeredgewidth=0.8)

    plt.setp(stemline7,color='navy', linewidth = 0.8)
    plt.setp(markerline7, markersize = 6,markeredgecolor="navy", markeredgewidth=0.5)
   
    ax.axhline(y=270, color='m', linewidth= 0.8, linestyle="--",label="IRI=270")
    ax3.axhline(y=24.6, color='darkslategrey', linewidth= 0.8, linestyle="--", label="D0=24.6")
    ax4.axhline(y=1.8, color='g', linewidth= 0.8, linestyle="--", label="D48=1.8")
    ax5.axhline(y=8, color='black', linewidth= 0.8, linestyle="--", label="SCI=8")
    ax6.axhline(y=4.5, color='red', linewidth= 0.8, linestyle="--", label="BDI=4.5")
    ax7.axhline(y=4, color='blue', linewidth= 0.8, linestyle="--", label="BCI=4")
    ax.legend(bbox_to_anchor=(-0.2,1),loc=1,fontsize=6,markerscale=1)
    ax2.legend(bbox_to_anchor=(-0.2, 0.9),loc=1,fontsize=6, markerscale=1) #using a loc1 with bbox fixes the location to right corner and helps the bbox to plot at the right position
    ax3.legend(bbox_to_anchor=(-0.2,0.9),loc=1,fontsize=6,markerscale=1)
    ax4.legend(bbox_to_anchor=(-0.2, 0.85),loc=1,fontsize=6,markerscale=1)
    ax5.legend(bbox_to_anchor=(-0.2, 0.8),loc=1,fontsize=6,markerscale=1)
    ax6.legend(bbox_to_anchor=(-0.2, 0.75),loc=1,fontsize=6,markerscale=1)
    ax7.legend(bbox_to_anchor=(-0.2, 0.7),loc=1,fontsize=6,markerscale=1)
    ax.set_facecolor('mintcream')
    return(plt.show())


#%%
def plot_con_z4(df_plot):
    import matplotlib as mpl
    mpl.rcParams['figure.dpi'] = 300

    fig, ax = plt.subplots()
    fig.subplots_adjust(right=0.75)
    max_IRI=df_plot["R_IRI"].max() + 100
    ##max_iri= round(max_iri) #commented when plotting normalised value
    max_CD=df_plot["Density"].max() + 0.1
    max_D0=df_plot["D0"].max()+ 1
    max_D48=df_plot["D48"].max()+ 1
    #max_cd= round(max_cd)   #commented when plotting normalised value
    ax2 = ax.twinx()
    ax3 = ax.twinx()
    ax4 = ax3
    ax5 = ax3
    ax6 = ax3
    ax7 = ax3
    ax3.spines.right.set_position(("axes", 1.2))
    #ax4.spines.right.set_position(("axes", 1.4))
    ax2.set_ylabel('Crack-Density(%)',fontsize=14)
    ax2.tick_params(labelsize=14)
    ax3.set_ylabel('FWD (milli-inches)',fontsize=14)
    ax3.tick_params(labelsize=14)
    # ax4.set_ylabel('FWD(milli-inches)',fontsize=8)
    # ax4.tick_params(labelsize=8)
    if max_IRI < 270:
        iri= 300
    else:
        iri= max_IRI +50

    if max_D0 < 36.4:
        D0= 25
    else:
        D0= max_D0 +1

    
    ax.set_ylim(0,iri)
    ax2.set_ylim(0,max_CD)
    ax3.set_ylim(0,D0)
    ax4.set_ylim(0,D0)
    ax5.set_ylim(0,D0)
    ax6.set_ylim(0,D0)
    ax7.set_ylim(0,D0)

    markerline, stemline, baseline,=ax.stem(df_plot['DMI'], df_plot["R_IRI"],linefmt=':',markerfmt= 'o',basefmt=' ',label= "R_IRI") 
    markerline.set_markerfacecolor('crimson')
    markerline2, stemline2, baseline2,=ax2.stem(df_plot['DMI'], df_plot["Density"], linefmt=':',markerfmt= 'D', basefmt=' ',  label= "CD_Left wheel path") 
    markerline2.set_markerfacecolor('blue')
    markerline3, stemline3, baseline3,=ax3.stem(df_plot['DMI_fwd'], df_plot["D0"], linefmt=':',markerfmt= 'x',basefmt=' ',  label= "D0-surface") 
    markerline3.set_markerfacecolor('darkslategrey')
    markerline4, stemline4, baseline4,=ax4.stem(df_plot['DMI_fwd'], df_plot["D48"], linefmt=':',markerfmt= 's',basefmt=' ',  label= "D48-subgrade") 
    markerline4.set_markerfacecolor('orange')
    markerline5, stemline5, baseline5,=ax5.stem(df_plot['DMI_fwd'], df_plot["SCI"], linefmt=':',markerfmt= 'D', basefmt=' ', label= "SCI-surface") 
    markerline5.set_markerfacecolor('gold')
    markerline6, stemline6, baseline6,=ax6.stem(df_plot['DMI_fwd'], df_plot["BDI"], linefmt=':',markerfmt= 'o',basefmt=' ',  label= "BDI-Middle layer") 
    markerline6.set_markerfacecolor('crimson')
    markerline7, stemline7, baseline7,=ax7.stem(df_plot['DMI_fwd'], df_plot["BCI"], linefmt=':',markerfmt= 'x',basefmt=' ',  label= "BCI- Lower layer") 
    markerline7.set_markerfacecolor('navy')
    ax.set_box_aspect(1)
    ax.set_ylabel('IRI (in/mi)', fontsize=14)
    ax.tick_params(labelsize=14)
    ax.set_xlabel('DMI values(ft)',fontsize=14)
    #ax.set_title('I64-WB-DL RP 78-85 Comparison of crack density at zone 4(right wheel), D0, D48, SCI, BDI, BCI and Right IRI',fontsize=8)
    #markerline, stemline, baseline, = ax.stem(x,y,linefmt='k-',markerfmt='ko',basefmt='k.')
    plt.setp(stemline,color='m', linewidth = 0.8)
    plt.setp(markerline, markersize = 3,markeredgecolor="m",markeredgewidth=0.5)
    
    plt.setp(stemline2,color='darkgoldenrod', linewidth = 0.8)
    plt.setp(markerline2, markersize = 3,markeredgecolor="darkgoldenrod", markeredgewidth=0.7)
    
    plt.setp(stemline3,color='darkslategrey', linewidth = 0.8)
    plt.setp(markerline3, markersize = 6 ,markeredgecolor="darkslategrey",markeredgewidth=0.9)
    
    plt.setp(stemline4,color='green', linewidth = 0.8)
    plt.setp(markerline4, markersize =6,markeredgecolor="green",markeredgewidth=0.7)

    plt.setp(stemline5,color='black', linewidth = 0.8)
    plt.setp(markerline5, markersize = 5,markeredgecolor="black",markeredgewidth=0.7)

    plt.setp(stemline6,color='darkgreen', linewidth = 0.8)
    plt.setp(markerline6, markersize = 4,markeredgecolor="darkgreen",markeredgewidth=0.8)

    plt.setp(stemline7,color='navy', linewidth = 0.8)
    plt.setp(markerline7, markersize = 6,markeredgecolor="navy", markeredgewidth=0.5)
   
    ax.set_ylim([0,600])
    ax2.set_ylim([0,5])
    ax3.set_ylim([0,25])
    fig.set_figwidth(15)
    fig.set_figheight(5)
    ax.axhline(y=270, color='m', linewidth= 1, linestyle="--",label="IRI=270")
    ax3.axhline(y=36.4, color='darkslategrey', linewidth= 1, linestyle="--", label="D0=36.4")
    ax4.axhline(y=1.8, color='g', linewidth= 1, linestyle="--", label="D48=1.8")
    ax5.axhline(y=8, color='black', linewidth= 1, linestyle="--", label="SCI=8")
    ax6.axhline(y=4.5, color='red', linewidth= 1, linestyle="--", label="BDI=4.5")
    ax7.axhline(y=4, color='blue', linewidth= 1, linestyle="--", label="BCI=4")
    ax.legend(bbox_to_anchor=(-0.2,0.95),loc=1,fontsize=12,markerscale=1)
    ax2.legend(bbox_to_anchor=(-0.2, 0.79),loc=1,fontsize=12, markerscale=1) #using a loc1 with bbox fixes the location to right corner and helps the bbox to plot at the right position
    ax3.legend(bbox_to_anchor=(-0.2,0.9),loc=1,fontsize=12,markerscale=1)
    ax4.legend(bbox_to_anchor=(-0.2, 0.85),loc=1,fontsize=12,markerscale=1)
    ax5.legend(bbox_to_anchor=(-0.2, 0.8),loc=1,fontsize=12,markerscale=1)
    ax6.legend(bbox_to_anchor=(-0.2, 0.75),loc=1,fontsize=12,markerscale=1)
    ax7.legend(bbox_to_anchor=(-0.2, 0.7),loc=1,fontsize=12,markerscale=1)
    #ax.set_facecolor('mintcream')
    plt.savefig("graphs/scatter_I70/I70_zone4.svg", dpi=600)
    return(plt.show())
#%%
plot_con_z4(df_concat_z4)






















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
    ax.plot(df_plot['DMI'], df_plot["CrkArea_100z4"],alpha=1,color='blue',label= "CrkArea_100") 
    ax2.plot(df_plot['DMI']+0.9, df_plot["CrkArea"], alpha=1, color='red',  label= "CrkArea_10") 
    ax.legend(loc=2,fontsize=8)
    ax2.legend(loc=1,fontsize=8)
    ax.set_box_aspect(0.25)
    ax.set_ylabel('CrkArea_100z4', fontsize=8)
    ax.set_xlabel('DMI values',fontsize=8)
    ax.set_title(' Comparison of CrkArea at 10 DMI and 100 DMI for zone 4',fontsize=10)

    return(plt.show())
# %%
plot_comp(df_plt_z4_ca)

# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl  
mpl.rc('font',family='Times New Roman')

csfont = {'fontname':'Times New Roman'}
parameter="Surface Deflection"
df_liri=pd.read_excel('/Users/jhasneha/Documents/SPRINDOT/summer2021/SPRINDOT/boxwhisker.xlsx',sheet_name=parameter)
column=[]
fig4, ax = plt.subplots()
column=list(df_liri.columns.values)
ax=df_liri.boxplot(column=column,showmeans=True)
#dict=ax.boxplot(df_liri)
#ax.set_title(' Box whisker plot for '+ parameter+ '.',fontsize=14, **csfont)
ax.axhline(y=1.8, color='m', linewidth= 0.8, linestyle="--", label=parameter+" threshold=1.8")
#ax.axhline(y=36.4, color='m', linewidth= 0.8, linestyle="--", label=parameter+" threshold=36.4")
#ax.axhline(y=270, color='m', linewidth= 0.8, linestyle="--", label=parameter+" threshold=270")
ax.legend(loc=9,fontsize=14,markerscale=1)
plt.ylim([0,10])
plt.xticks(rotation =80,fontsize=14)
plt.yticks(rotation =0,fontsize=14)

#ax.set_ylabel('IRI (in/mi)', fontsize=14,**csfont)
ax.set_ylabel(parameter+" (milli inches)", fontsize=14,**csfont)
plt.savefig("graphs/boxwhisker_I70/threeroadsboxwhisker_"+parameter+".jpg",bbox_inches="tight", dpi=600)
df_liri.describe()




"""==========================================

Scatter plot for CD and IRI 


============================================="""

#%%
import matplotlib.pyplot as plt
import numpy as np

# Fixing random state for reproducibility
#df_plt_z4 = df_plt_z4[df_plt_z4["R_IRI"] <=1000]
plt.scatter(df_plt_z4["Density"], df_plt_z4["R_IRI"], c="g", alpha=0.1, marker=r'o',
            label="correlation")
plt.xlabel("Crack Density(%)")
plt.ylabel("R_IRI (in/mi)")
plt.legend(loc='upper right')
plt.show()





















"""+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        Creating patching algorithm

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""


