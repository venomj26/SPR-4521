#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openpyxl
import gmaps


#%%
# import os
# import pathlib

# #def create_df(rootfilepath):
# root_files=os.listdir(rootfilepath)
# df_dict={}
# for entry in root_files:
#     if not entry.startswith('.'):
#         print("File names: " ,entry)
#         destination_root= rootfilepath + '/'+entry
#         print("destination" ,destination_root)
#         pattern= "**/*AASHTO*.csv"
#         df_name= 'df_'+entry
#         df_dict[df_name]=pd.DataFrame()
#         print("the dataframe to be written into is :  ", df_name)
#         list_p=list(pathlib.Path(destination_root).glob(pattern))
#         #print(list_p)
#         for index in list_p:
#             df=pd.read_csv(index)
#             print(df.head())
#             #df=df.head()
#             df.columns=df.columns.str.replace(' ', '')
#             df.columns=df.columns.str.replace(r'\([^)]*\)', '')
#             df_density=df["Density"]
#             df_density= df_density.replace(0, np.nan)
#             df_density= df_density.dropna(axis=0)
#             #df_density_ls=df_density.to_list()
#         df_dict[df_name]=df_dict[df_name].append(df_density, ignore_index=False)
#         print(index)
#         print("dataframe was created ",df_name)
#             #return (df1)



#%%
#rootfilepath='/Users/jhasneha/Documents/SPRINDOT/summer2021/SPRINDOT/Roads_3d/Interstate'
#rootfilepath='/Users/jhasneha/Documents/SPRINDOT/summer2021/SPRINDOT/Roads_3d/Stateroads'
rootfilepath='/Users/jhasneha/Documents/SPRINDOT/summer2021/SPRINDOT/Roads_3d'



"""    ############################
____________________ better version of creating the above list of fdataframes

*************************************************** """


#%%
import os
import pathlib

#def create_df(rootfilepath):
root_files=os.listdir(rootfilepath)
df_roads_density=pd.DataFrame()
for entry in root_files:
    if not entry.startswith('.'):
        print("File names: " ,entry)
        destination_root= rootfilepath + '/'+entry
        #print("destination" ,destination_root)
        pattern= "**/*AASHTO*.csv"
        list_p=list(pathlib.Path(destination_root).glob(pattern))
        print(list_p)
        list_density=[]
        df_density=pd.DataFrame(columns=["Density"])
        for index in list_p:
            #print("in the 2nd loop: ",index)
            df=pd.read_csv(index)
            #print(df.head())
            df.columns=df.columns.str.replace(' ', '')
            df.columns=df.columns.str.replace(r'\([^)]*\)', '')
            # df["Density"]= df["Density"].replace(0, np.nan)
            # df= df.dropna(axis=0,subset=['Density'])
            list_density.append(df["Density"])
            print(df["Density"].shape[0])
            print("inside   ", len(list_density))
        print("outside   ",len(list_density))   
        final_df=pd.concat(list_density) 
        print(" shape of final df: ",final_df.shape[0])
        df_density=final_df.to_frame()
        df_density.columns=[str(entry)]
        print("colname:   ",df_density.columns)   
    df_roads_density=pd.concat([df_roads_density,df_density])
    print("dataframe was created ",df_roads_density.columns)
     
"""@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                    IRI
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"""


#%%
import os
import pathlib

#def create_df(rootfilepath):
root_files=os.listdir(rootfilepath)
df_roads_IRI=pd.DataFrame()
for entry in root_files:
    if not entry.startswith('.'):
        print("File names: " ,entry)
        destination_root= rootfilepath + '/'+entry
        #print("destination" ,destination_root)
        pattern= "**/*IRI*.csv"
        list_p=list(pathlib.Path(destination_root).glob(pattern))
        #print(list_p)
        df_density=pd.DataFrame(columns=["IRI"])
        appended_iri=[]
        for index in list_p:
            #print ("the files are: ",index)
            df=pd.read_csv(index)
            #print(df.head())
            df.columns=df.columns.str.replace(' ', '')
            df.columns=df.columns.str.replace(r'\([^)]*\)', '')
            appended_iri.append(df["R_IRI"])
            appended_iri.append(df["L_IRI"])
            print("inside   ", len(appended_iri))
        print("outside   ",len(appended_iri))   
        final_df=pd.concat(appended_iri)
        print(final_df.head())    
        df_density=final_df.to_frame()
        df_density.columns=[str(entry)]
        #print(df_density.head())
        print("colname:   ",df_density.columns)
    df_roads_IRI=pd.concat([df_roads_IRI,df_density])#, axis=1)
    print("dataframe was created ",df_roads_IRI.columns)
     
#%%
def justify(a, invalid_val=0, axis=1, side='left'):    
    """
    Justifies a 2D array

    Parameters
    ----------
    A : ndarray
        Input array to be justified
    axis : int
        Axis along which justification is to be made
    side : str
        Direction of justification. It could be 'left', 'right', 'up', 'down'
        It should be 'left' or 'right' for axis=1 and 'up' or 'down' for axis=0.

    """

    if invalid_val is np.nan:
        mask = ~np.isnan(a)
    else:
        mask = a!=invalid_val
    justified_mask = np.sort(mask,axis=axis)
    if (side=='up') | (side=='left'):
        justified_mask = np.flip(justified_mask,axis=axis)
    out = np.full(a.shape, invalid_val) 
    if axis==1:
        out[justified_mask] = a[mask]
    else:
        out.T[justified_mask.T] = a.T[mask.T]
    return out

#%%
arr = justify(df_roads_density.to_numpy(), invalid_val=np.nan,axis=0)
df_allrds_density = pd.DataFrame(arr, columns=df_roads_density.columns)
df_allrds_density=df_allrds_density.dropna(axis=0,how='all')



#%%

arr = justify(df_roads_IRI.to_numpy(), invalid_val=np.nan,axis=0)
df_allrds_iri = pd.DataFrame(arr, columns=df_roads_IRI.columns, index=df_roads_IRI.index)
df_allrds_iri=df_allrds_iri.dropna(axis=0,how='all')




#%%
# fit an empirical cdf to a bimodal dataset
from matplotlib import pyplot
from numpy.random import normal
import numpy as np
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 900
import dc_stat_think as dcst
# generate a sample
for road in df_roads_IRI.columns.tolist():
    fig4, ax = plt.subplots()
    ax2 = ax.twinx()
    ax3=ax
    ax4=ax2
    print(road)
    sample1 = np.array(df_roads_IRI[road])
    sample2 = np.array(df_roads_density[road])
    sample3 = np.array(df_allrds_iri["Stateroads"])
    sample4 = np.array(df_allrds_density["Stateroads"])

    ecdf1x,ecdf1y = dcst.ecdf(sample1)
    ecdf2x,ecdf2y = dcst.ecdf(sample2)
    ecdf3x,ecdf3y = dcst.ecdf(sample3)
    ecdf4x,ecdf4y = dcst.ecdf(sample4)
    
    ax.plot(ecdf1y, ecdf1x, color='blue', label="IRI")
    ax2.plot(ecdf2y, ecdf2x, color = 'green', label="Crack Density")
    ax3.plot(ecdf3y, ecdf3x, color = 'deepskyblue',linestyle="-.", label="IRI_ref")
    ax4.plot(ecdf4y, ecdf4x, color = 'limegreen',linestyle="-.", label="Crack Density_ref")

    ax.set_title('Comparison of ECDF for crack density and IRI for '+road+':' , fontsize=12)
    ax.set_xlabel("Probability")
    ax.set_ylabel('IRI (in/mi)',fontsize=8)
    ax2.set_ylabel('Crack Density (%)',fontsize=8)
    ax.axhline(y=80, color='crimson', linewidth= 1,linestyle="--", label="IRI=70")
    ax.axhline(y=170, color='orangered', linewidth= 1,linestyle="--", label="IRI=170")
    ax.axhline(y=330, color='green', linewidth= 1,linestyle="--", label="IRI=330")
    ax.legend(fontsize=8,loc=2)
    ax2.legend(fontsize=8,loc=1)
    ax.set_ylim(0,1200)
    
    pyplot.show()





#%%
# fit an empirical cdf to a bimodal dataset
def ecdf_IS(df,df1):
    import matplotlib as mpl
    mpl.rcParams['figure.dpi'] = 900
    from matplotlib import pyplot
    from numpy.random import normal
    import numpy as np
    import dc_stat_think as dcst
    fig4, ax = plt.subplots()
    ax2 = ax
    ax3=ax
    ax4=ax
    ax5=ax
    ax6=ax
    ax7=ax

    # # generate a sample

    sample1 = np.array(df["I64"])
    sample2 = np.array(df["I74"])
    sample3 = np.array(df["I70"])
    sample4 = np.array(df["I465"])
    sample5 = np.array(df["I69"])
    sample6 = np.array(df["I65"])
    sample_ref = np.array(df1["Interstate"])


    sample1 = sample1[~np.isnan(sample1)]
    sample2 = sample2[~np.isnan(sample2)]
    sample3 = sample3[~np.isnan(sample3)]
    sample4 = sample4[~np.isnan(sample4)]
    sample5 = sample5[~np.isnan(sample5)]
    sample6 = sample6[~np.isnan(sample6)]
    sample_ref = sample_ref[~np.isnan(sample_ref)]


    # fit a cdf
    ecdf1x,ecdf1y = dcst.ecdf(sample1)
    ecdf2x,ecdf2y = dcst.ecdf(sample2)
    ecdf3x,ecdf3y = dcst.ecdf(sample3)
    ecdf4x,ecdf4y = dcst.ecdf(sample4)
    ecdf5x,ecdf5y = dcst.ecdf(sample5)
    ecdf6x,ecdf6y = dcst.ecdf(sample6)
    ecdfref_x, ecdfref_y=dcst.ecdf(sample_ref)

    percentiles = np.array([83 , 99.25])





    pct_val1 = np.percentile(sample1, percentiles).round(1)
    pct_val2 = np.percentile(sample2, percentiles).round(1)
    pct_val3 = np.percentile(sample3, percentiles).round(1)
    pct_val4 = np.percentile(sample4, percentiles).round(1)
    pct_val5 = np.percentile(sample5, percentiles).round(1)
    pct_val6 = np.percentile(sample6, percentiles).round(1)
    pct_val_ref = np.percentile(sample_ref, percentiles).round(1)


    print("pct_val1 0.5, 0.85 are  : ", pct_val_ref)


    # plot the cdf
    ax.plot(ecdf1x, ecdf1y, color='fuchsia',linestyle="-.", label="I70")
    ax.plot(pct_val1, percentiles/100, marker='*', color='red', markeredgecolor="black", markeredgewidth="0.4",markersize = 8, linestyle='none')

    ax2.plot(ecdf2x, ecdf2y, color = 'gold', linestyle="-",label="I74")
    ax2.plot(pct_val2, percentiles/100, marker='o', color='red',markersize = 6,markeredgecolor="black",markeredgewidth="0.4", linestyle='none')

    ax3.plot(ecdf3x, ecdf3y, color = 'lime', label="I64")
    ax3.plot(pct_val3, percentiles/100, marker='o', color='red', markersize = 6,markeredgecolor="black",markeredgewidth="0.4", linestyle='none')

    ax4.plot(ecdf4x, ecdf4y, color = 'salmon',linestyle="-", label="I465")
    ax4.plot(pct_val4, percentiles/100, marker='*', color='red' ,markersize = 8,markeredgecolor="black",markeredgewidth="0.4",linestyle='none')

    ax5.plot(ecdf5x, ecdf5y, color = 'deepskyblue',linestyle="--", label="I69")
    ax5.plot(pct_val5, percentiles/100, marker='o', color='red', markersize = 6,markeredgecolor="black",markeredgewidth="0.4", linestyle='none')

    ax6.plot(ecdf6x, ecdf6y, color = 'blue', linestyle="-.",label="I65")
    ax6.plot(pct_val6, percentiles/100, marker='*', color='red' ,markersize = 8,markeredgecolor="black",markeredgewidth="0.4",linestyle='none')

    ax7.plot(ecdfref_x, ecdfref_y, color = 'white',linestyle="-", label="IS-Reference")
    ax7.plot(pct_val_ref, percentiles/100, marker='X', color='red' ,markersize = 8,markeredgecolor="black",markeredgewidth="0.4",linestyle='none')


    # ax.text(3, 0.6, 'I70=' + str(pct_val1[1]),fontsize= 8,color="ivory",weight='bold')    
    # ax2.text(3, 0.56, 'I74=' + str(pct_val2[1]),color="ivory",fontsize= 8, weight='bold')   
    # ax3.text(3, 0.52, 'I64=' + str(pct_val3[1]),color="ivory",fontsize= 8,weight='bold')
    # ax4.text(3, 0.48, 'I465=' + str(pct_val4[1]), fontsize= 8, color="ivory",weight='bold')
    # ax5.text(3, 0.44, 'I69=' + str(pct_val5[1]),fontsize= 8,color="ivory",weight='bold')
    # ax6.text(3, 0.40, 'I65=' + str(pct_val6[1]), fontsize= 8,color="ivory",weight='bold')
    # ax7.text(3, 0.64, 'CD(.97)=' + str(pct_val_ref[1]), fontsize= 8,color="ivory",weight='bold')

    ax.text(300, 0.6, 'I70=' + str(pct_val1[1]),fontsize= 8,color="ivory",weight='bold')
    ax2.text(300, 0.56, 'I74=' + str(pct_val2[1]),color="ivory",fontsize= 8, weight='bold')
    ax3.text(300, 0.52, 'I64=' + str(pct_val3[1]),color="ivory",fontsize= 8,weight='bold')
    ax4.text(300, 0.48, 'I465=' + str(pct_val4[1]), fontsize= 8, color="ivory",weight='bold')
    ax5.text(300, 0.44, 'I69=' + str(pct_val3[1]),fontsize= 8,color="ivory",weight='bold')
    ax6.text(300, 0.40, 'I65=' + str(pct_val4[1]), fontsize= 8,color="ivory",weight='bold')
    ax7.text(300, 0.64, 'IRI(0.992)=' + str(pct_val_ref[1]), fontsize= 8,color="ivory",weight='bold')


    ax.set_ylabel('Probability',fontsize=8)
    ax2.set_xlabel('IRI (in/mi)',fontsize=8)
    ax.set_title('ECDF plot for IRI values for Interstate Roads',fontsize=12)
    # ax.set_title('ECDF plot for CD values for Interstate Roads',fontsize=12)
    # ax2.set_xlabel('CD (%)',fontsize=8)
    ax.axhline(y=0.83, color='oldlace', linewidth= 1,linestyle="--", label="83 percentile")
    ax.axhline(y=0.95, color='lightgray', linewidth= 1,linestyle="--", label="95percentile")
    ax.axhline(y=0.9925, color='lightgray', linewidth= 1,linestyle="--", label="99.2 percentile")
    ax.axvline(x=70, color='aquamarine', linewidth= 1,linestyle="--", label="IRI=70")
    ax.axvline(x=170, color='orange', linewidth= 1,linestyle="--", label="IRI=170")
    ax.axvline(x=270, color='red', linewidth= 1,linestyle="--", label="IRI=270")

    ax.legend(fontsize=8,loc=1)
    ax2.legend(fontsize=8,loc=2)
    ax3.legend(fontsize=8,loc=4)
    ax4.legend(fontsize=8,loc=4)
    ax5.legend(fontsize=8,loc=4)
    ax6.legend(fontsize=8,loc=4)
    ax7.legend(fontsize=8,loc=4)
    ax.set_facecolor('dimgray')
    #plt.xlim([-1,10])
    plt.xlim([-10,600])

    pyplot.show()

    


#%%
ecdf_IS(df_roads_IRI,df_allrds_iri)
#ecdf_IS(df_roads_density,df_allrds_density)




#%%
# fit an empirical cdf to a bimodal dataset
def ecdf_SR(df):
    import matplotlib as mpl
    mpl.rcParams['figure.dpi'] = 900
    from matplotlib import pyplot
    from numpy.random import normal
    import numpy as np
    import dc_stat_think as dcst
    fig4, ax = plt.subplots()
    #ax.margins(0,1000)
    ax2 = ax
    ax3=ax
    #ax4=ax
    # ax5=ax
    # ax6=ax
    # ax7=ax
    # ax8=ax
    # ax9=ax
    # generate a sample
    

    sample1=np.array(df["Stateroads"])
    sample2=np.array(df["USroads"])
    sample3=np.array(df["Interstate"])



    # sample1 = np.array(df["SR327"])
    # sample2 = np.array(df["SR38"])
    # sample3 = np.array(df["SR15"])
    # sample4 = np.array(df["SR101"])
    # sample5 = np.array(df["SR57"])
    # sample6 = np.array(df["SR44"])
    # sample7 = np.array(df["SR3"])
    # sample8 = np.array(df["US27-SR930"])
    
    # sample_ref = np.array(df1["Stateroads"])


    #the rows added with nan in roads with unequal number of rows when appending into the dataframe 
    sample1 = sample1[~np.isnan(sample1)]
    sample2 = sample2[~np.isnan(sample2)]
    sample3 = sample3[~np.isnan(sample3)]
    # sample4 = sample4[~np.isnan(sample4)]
    # sample5 = sample5[~np.isnan(sample5)]
    # sample6 = sample6[~np.isnan(sample6)]
    # sample7 = sample7[~np.isnan(sample7)]
    # sample8 = sample8[~np.isnan(sample8)]
    
    # sample_ref = sample_ref[~np.isnan(sample_ref)]






    #sample = hstack((sample1, sample2))
    # fit a cdf
    ecdf1x,ecdf1y = dcst.ecdf(sample1)
    ecdf2x,ecdf2y = dcst.ecdf(sample2)
    ecdf3x,ecdf3y = dcst.ecdf(sample3)
    # ecdf4x,ecdf4y = dcst.ecdf(sample4)
    # ecdf5x,ecdf5y = dcst.ecdf(sample5)
    # ecdf6x,ecdf6y = dcst.ecdf(sample6)
    # ecdf7x,ecdf7y = dcst.ecdf(sample7)
    # ecdf8x,ecdf8y = dcst.ecdf(sample8)
    # ecdfref_x, ecdfref_y=dcst.ecdf(sample_ref)

    #percentiles = np.array([75 , 97.2])
    percentiles = np.array([50 , 92.5])


    pct_val1 = np.percentile(sample1, percentiles).round(1)
    pct_val2 = np.percentile(sample2, percentiles).round(1)
    pct_val3 = np.percentile(sample3, percentiles).round(1)
    # # pct_val4 = np.percentile(sample4, percentiles).round(1)
    # pct_val5 = np.percentile(sample5, percentiles).round(1)
    # pct_val6 = np.percentile(sample6, percentiles).round(1)
    # pct_val7 = np.percentile(sample7, percentiles).round(1)
    # pct_val8 = np.percentile(sample8, percentiles).round(1)
    # pct_val_ref = np.percentile(sample_ref, percentiles).round(1)

    #print("pct_val1 0.5, 0.85 are  : ", pct_val1)
    print("pct_val1 0.5, 0.925 are  : ", pct_val1)

    ax.plot(ecdf1x, ecdf1y, color='fuchsia',linestyle="-.", label="SR")
    ax.plot(pct_val1, percentiles/100, marker='*', color='red', markeredgecolor="black", markeredgewidth="0.4",markersize = 8, linestyle='none')

    ax2.plot(ecdf2x, ecdf2y, color = 'gold', linestyle="--",label="USH")
    ax2.plot(pct_val2, percentiles/100, marker='o', color='red',markersize = 6,markeredgecolor="black",markeredgewidth="0.4", linestyle='none')

    ax3.plot(ecdf3x, ecdf3y, color = 'lime', label="IS")
    ax3.plot(pct_val3, percentiles/100, marker='o', color='red', markersize = 6,markeredgecolor="black",markeredgewidth="0.4", linestyle='none')
    
    # plot the cdf
    # ax.plot(ecdf1x, ecdf1y, color='fuchsia',linestyle="-.", label="SR327")
    # ax.plot(pct_val1, percentiles/100, marker='*', color='red', markeredgecolor="black", markeredgewidth="0.4",markersize = 8, linestyle='none')

    # ax2.plot(ecdf2x, ecdf2y, color = 'gold', linestyle="--",label="SR38")
    # ax2.plot(pct_val2, percentiles/100, marker='o', color='red',markersize = 6,markeredgecolor="black",markeredgewidth="0.4", linestyle='none')

    # ax3.plot(ecdf3x, ecdf3y, color = 'lime', label="SR15")
    # ax3.plot(pct_val3, percentiles/100, marker='o', color='red', markersize = 6,markeredgecolor="black",markeredgewidth="0.4", linestyle='none')
    
    # ax4.plot(ecdf4x, ecdf4y, color = 'blue',linestyle="-", label="SR101")
    # ax4.plot(pct_val4, percentiles/100, marker='*', color='red' ,markersize = 8,markeredgecolor="black",markeredgewidth="0.4",linestyle='none')

    # ax5.plot(ecdf5x, ecdf5y, color = 'deepskyblue',linestyle="-", label="SR57")
    # ax5.plot(pct_val5, percentiles/100, marker='o', color='red', markersize = 6,markeredgecolor="black",markeredgewidth="0.4", linestyle='none')

    # ax6.plot(ecdf6x, ecdf6y, color = 'gold', linestyle="-",label="SR44")
    # ax6.plot(pct_val6, percentiles/100, marker='*', color='red' ,markersize = 8,markeredgecolor="black",markeredgewidth="0.4",linestyle='none')

    # ax7.plot(ecdf7x, ecdf7y, color = 'salmon',linestyle="-.", label="SR3")
    # ax7.plot(pct_val7, percentiles/100, marker='o', color='red', markersize = 6,markeredgecolor="black",markeredgewidth="0.4", linestyle='none')

    # ax8.plot(ecdf8x, ecdf8y, color = 'lime',linestyle="--", label="US27-SR930")
    # ax8.plot(pct_val8, percentiles/100, marker='*', color='red' ,markersize = 8,markeredgecolor="black",markeredgewidth="0.4",linestyle='none')
    

    # ax9.plot(ecdfref_x, ecdfref_y, color = 'white',linestyle="-", label="SR-Reference")
    # ax9.plot(pct_val_ref, percentiles/100, marker='X', color='red' ,markersize = 8,markeredgecolor="black",markeredgewidth="0.4",linestyle='none')
    
    

    # ax.text(20, 0.6, 'SR=' + str(pct_val1[1]),fontsize= 8,color="ivory",weight='bold')    
    # ax2.text(20, 0.56, 'USH=' + str(pct_val2[1]),color="ivory",fontsize= 8, weight='bold')   
    # ax3.text(20, 0.52, 'IS=' + str(pct_val3[1]),color="ivory",fontsize= 8,weight='bold')
    
    ax.text(900, 0.6, 'SR=' + str(pct_val1[1]),fontsize= 8,color="ivory",weight='bold')    
    ax2.text(900, 0.64, 'USH=' + str(pct_val2[1]),color="ivory",fontsize= 8, weight='bold')   
    ax3.text(900, 0.68, 'IS=' + str(pct_val3[1]),color="ivory",fontsize= 8,weight='bold')
    




    # ax.text(6, 0.6, 'SR327=' + str(pct_val1[1]),fontsize= 8,color="ivory",weight='bold')    
    # ax2.text(6, 0.56, 'SR38=' + str(pct_val2[1]),color="ivory",fontsize= 8, weight='bold')   
    # ax3.text(6, 0.52, 'SR15=' + str(pct_val3[1]),color="ivory",fontsize= 8,weight='bold')
    # ax4.text(6, 0.48, 'SR101=' + str(pct_val4[1]), fontsize= 8, color="ivory",weight='bold')
    # ax5.text(6, 0.44, 'SR57=' + str(pct_val5[1]),fontsize= 8,color="ivory",weight='bold')
    # ax6.text(6, 0.40, 'SR44=' + str(pct_val6[1]), fontsize= 8,color="ivory",weight='bold')
    # ax7.text(6, 0.36, 'SR3=' + str(pct_val7[1]),fontsize= 8,color="ivory",weight='bold')
    # ax8.text(6, 0.32, 'US27=' + str(pct_val8[1]), fontsize= 8,color="ivory",weight='bold')
    # ax9.text(6, 0.64, 'CD(.97)=' + str(pct_val_ref[1]), fontsize= 8,color="ivory",weight='bold')

    
    # ax.text(600, 0.6, 'SR327=' + str(pct_val1[1]),fontsize= 8,color="ivory",weight='bold')
    # ax2.text(600, 0.56, 'SR38=' + str(pct_val2[1]),color="ivory",fontsize= 8, weight='bold')
    # ax3.text(600, 0.52, 'SR15=' + str(pct_val3[1]),color="ivory",fontsize= 8,weight='bold')
    # ax4.text(600, 0.48, 'SR101=' + str(pct_val4[1]), fontsize= 8, color="ivory",weight='bold')
    # ax5.text(600, 0.44, 'SR57=' + str(pct_val3[1]),fontsize= 8,color="ivory",weight='bold')
    # ax6.text(600, 0.40, 'SR44=' + str(pct_val4[1]), fontsize= 8,color="ivory",weight='bold')
    # ax7.text(600, 0.36, 'SR3=' + str(pct_val3[1]),fontsize= 8,color="ivory",weight='bold')
    # ax8.text(600, 0.32, 'US27=' + str(pct_val4[1]), fontsize= 8,color="ivory",weight='bold')
    # ax9.text(600, 0.64, 'IRI(0.97)=' + str(pct_val_ref[1]), fontsize= 8,color="ivory",weight='bold')


    ax.set_ylabel('Probability',fontsize=8)
    # ax2.set_xlabel('CD (%)',fontsize=8)
    # ax.set_title('ECDF plot for CD values of State roads',fontsize=8)
    
    ax2.set_xlabel('IRI (in/mi)',fontsize=8)
    ax.set_title('ECDF plot for IRI values of State roads',fontsize=8)
    
    # ax.axhline(y=0.972, color='oldlace', linewidth= 1,linestyle="--", label="97.2 percentile")
    # ax.axhline(y=0.925, color='lightgray', linewidth= 1,linestyle="--", label="92.5 percentile")
    # ax.axhline(y=0.75, color='papayawhip', linewidth= 1,linestyle="--", label="75 percentile")
    



    ax.axvline(x=70, color='aquamarine', linewidth= 1,linestyle="--", label="IRI=70")
    ax.axvline(x=170, color='orange', linewidth= 1,linestyle="--", label="IRI=170")
    ax.axvline(x=330, color='red', linewidth= 1,linestyle="--", label="IRI-SR=330")
    ax.axvline(x=300, color='darkred', linewidth= 1,linestyle="--", label="IRI-USH=300")
    ax.axvline(x=270, color='brown', linewidth= 1,linestyle="--", label="IRI-ISR=270")
    # ax.axvline(x=5, color='aquamarine', linewidth= 1,linestyle="--", label="cd=5%")
    # ax.axvline(x=20, color='red', linewidth= 1,linestyle="--", label="cd=20%")
    ax.axhline(y=0.925, color='papayawhip', linewidth= 1,linestyle="--", label="92.5 percentile")



    ax.legend(fontsize=8,loc=1)
    ax2.legend(fontsize=8,loc=2)
    ax3.legend(fontsize=8,loc=4)
    # ax4.legend(fontsize=8,loc=4)
    # ax5.legend(fontsize=8,loc=4)
    # ax6.legend(fontsize=8,loc=4)
    # ax7.legend(fontsize=8,loc=4)
    # ax8.legend(fontsize=8,loc=4)
    # ax9.legend(fontsize=8,loc=4)
    
    ax.set_facecolor('dimgray')
    #plt.xlim([-1,12])
    plt.xlim([-10,1200])

    pyplot.show()



#%%
#ecdf_SR(df_roads_IRI,d_allrds_iri)
ecdf_SR(df_allrds_iri)
#ecdf_SR(df_allrds_density)
#ecdf_SR(df_roads_density,d_allrds_iri)

#%%
# fit an empirical cdf to a bimodal dataset
def ecdf_ush(df,df1):
    import matplotlib as mpl
    mpl.rcParams['figure.dpi'] = 900
    from matplotlib import pyplot
    from numpy.random import normal
    import numpy as np
    import dc_stat_think as dcst
    fig4, ax = plt.subplots()
    ax2 = ax
    ax3=ax
    ax4=ax
    # # generate a sample



    sample1 = np.array(df["US27"])
    sample2 = np.array(df["US41"])
    sample3 = np.array(df["US421"])
    sample4= np.array(df1["USroads"])


    #sample = hstack((sample1, sample2))
    # fit a cdf
    ecdf1x,ecdf1y = dcst.ecdf(sample1)
    ecdf2x,ecdf2y = dcst.ecdf(sample2)
    ecdf3x,ecdf3y = dcst.ecdf(sample3)
    ecdfref_x,ecdfref_y = dcst.ecdf(sample4)


    percentiles = np.array([81 , 98.7])

    sample1 = sample1[~np.isnan(sample1)]
    sample2 = sample2[~np.isnan(sample2)]
    sample3 = sample3[~np.isnan(sample3)]
    sample4 = sample4[~np.isnan(sample4)]




    pct_val1 = np.percentile(sample1, percentiles).round(1)
    pct_val2 = np.percentile(sample2, percentiles).round(1)
    pct_val3 = np.percentile(sample3, percentiles).round(1)
    pct_val_ref = np.percentile(sample4, percentiles).round(1)



    print("pct_val1 0.5, 0.85 are  : ", pct_val_ref)


    # plot the cdf
    ax.plot(ecdf1x, ecdf1y, color='fuchsia',linestyle="-.", label="US27")
    ax.plot(pct_val1, percentiles/100, marker='*', color='red', markeredgecolor="black", markeredgewidth="0.4",markersize = 8, linestyle='none')

    ax2.plot(ecdf2x, ecdf2y, color = 'gold', linestyle="--",label="US41")
    ax2.plot(pct_val2, percentiles/100, marker='o', color='red',markersize = 6,markeredgecolor="black",markeredgewidth="0.4", linestyle='none')

    ax3.plot(ecdf3x, ecdf3y, color = 'lime', label="US421")
    ax3.plot(pct_val3, percentiles/100, marker='o', color='red', markersize = 6,markeredgecolor="black",markeredgewidth="0.4", linestyle='none')

    ax4.plot(ecdfref_x, ecdfref_y, color = 'white',linestyle="-", label="USH-Reference")
    ax4.plot(pct_val_ref, percentiles/100, marker='X', color='red' ,markersize = 8,markeredgecolor="black",markeredgewidth="0.4",linestyle='none')
        

    # ax.text(3, 0.6, 'US27=' + str(pct_val1[1]),fontsize= 8,color="ivory",weight='bold')    
    # ax2.text(3, 0.56, 'US41=' + str(pct_val2[1]),color="ivory",fontsize= 8, weight='bold')   
    # ax3.text(3, 0.52, 'US421=' + str(pct_val3[1]),color="ivory",fontsize= 8,weight='bold')
    # ax4.text(3, 0.64, 'CD(.98)=' + str(pct_val_ref[1]), fontsize= 8,color="ivory",weight='bold')

        
    ax.text(300, 0.6, 'US27=' + str(pct_val1[1]),fontsize= 8,color="ivory",weight='bold')
    ax2.text(300, 0.56, 'US41=' + str(pct_val2[1]),color="ivory",fontsize= 8, weight='bold')
    ax3.text(300, 0.52, 'US421=' + str(pct_val3[1]),color="ivory",fontsize= 8,weight='bold')
    ax4.text(300, 0.64, 'IRI(0.98)=' + str(pct_val_ref[1]), fontsize= 8,color="ivory",weight='bold')


    ax.set_ylabel('Probability',fontsize=8)
    ax2.set_xlabel('IRI (in/mi)',fontsize=8)
    ax.set_title('ECDF plot for IRI values of US Highways',fontsize=10)
    # ax2.set_xlabel('CD (%)',fontsize=8)
    # ax.set_title('ECDF plot for CD values of US Highways',fontsize=10)


    ax.axhline(y=0.81, color='lightgray', linewidth= 1,linestyle="--", label="81 percentile")
    ax.axhline(y=0.96, color='oldlace', linewidth= 1,linestyle="--", label="96 percentile")
    ax.axhline(y=0.987, color='papayawhip', linewidth= 1,linestyle="--", label="98 percentile")

    ax.axvline(x=70, color='aquamarine', linewidth= 1,linestyle="--", label="IRI=70")
    ax.axvline(x=170, color='orangered', linewidth= 1,linestyle="--", label="IRI=170")
    ax.axvline(x=300, color='crimson', linewidth= 1,linestyle="--", label="IRI=300")

    ax.legend(fontsize=8,loc=1)
    ax2.legend(fontsize=8,loc=2)
    ax3.legend(fontsize=8,loc=4)
    ax4.legend(fontsize=8,loc=4)

    #plt.xlim([-1,6])
    plt.xlim([-10,600])


    ax.set_facecolor('dimgray')

    pyplot.show()


#%%
ecdf_ush(df_roads_IRI,df_allrds_iri)
#ecdf_ush(df_roads_density,df_allrds_density)



# %%
import matplotlib.pyplot as plt
import seaborn as sns
df_roads=df_roads_IRI.round(1)
df_roads = df_roads.where(df_roads <5000) #18 values greater than 5000 were lost
list_roads= df_roads.columns.to_list()
for roads in list_roads:
    #print (df_roads[roads].value_counts())
    sns.distplot(df_roads[roads], hist = True,bins=20, kde = True,
                 kde_kws = {'shade': True, 'linewidth': 1.5}, 
                  label = roads).set(xlim=(0,1000))
    #sns.histplot(df_roads[roads],)

plt.title('Kernel Density Estimation Plot of IRI on Stateroads')
plt.xlabel('IRI (in/mi)')
plt.ylabel('Probability Density f(x)')
# plt.axvline(x=70, color='green', linewidth= 1,linestyle="--", label="IRI=70")
# plt.axvline(x=170, color='orange', linewidth= 1,linestyle="--", label="IRI=170")
# plt.axvline(x=300, color='red', linewidth= 1,linestyle="--", label="IRI=300")
# plt.axvline(x=330, color='darkred', linewidth= 1,linestyle="--", label="IRI=330")
# plt.axvline(x=270, color='maroon', linewidth= 1,linestyle="--", label="IRI=270")

plt.legend(prop={'size': 10}, title = 'SR')


# %%
import matplotlib.pyplot as plt
import seaborn as sns
df_roads=df_allrds_density.round(1)

list_roads= df_roads.columns.to_list()
for roads in list_roads:
    #print (df_roads[roads].value_counts())
    sns.distplot(df_roads[roads], hist = True,bins=4000, norm_hist=True,kde = False,
                 hist_kws = {'alpha': 0.5}, 
                  label = roads).set(xlim=(-1,6))
    #sns.histplot(df_roads[roads],)
#bins=[0,100,200,300,400,500,600,700,800,900,1000,1500,2000,3000,4000,5000],
#plt.legend(prop={'size': 10}, title = 'US Highways')
plt.title('Histogram for CD on US highway Roads with 5 bins',fontsize=12)
plt.xlabel('CD (%)')
plt.ylabel('normalized count')
# plt.axvline(x=70, color='green', linewidth= 1,linestyle="--", label="IRI=70")
# plt.axvline(x=170, color='orange', linewidth= 1,linestyle="--", label="IRI=170")
# plt.axvline(x=300, color='red', linewidth= 1,linestyle="--", label="IRI=300")
plt.legend(prop={'size': 10}, title = 'roads')

# %%
import matplotlib.pyplot as plt
import seaborn as sns
df_roads=df_roads_IRI.round(1)
#df_roads = df_roads.where(df_roads <5000) #18 values greater than 5000 were lost
#%%
list_roads= df_roads.columns.to_list()
for roads in list_roads:
    #print (df_roads[roads].value_counts())
    sns.distplot(df_roads[roads], hist = True,bins=100, norm_hist=True,kde = True,
                 hist_kws = {'alpha': 0.5}, 
                  label = roads).set(xlim=(-10,1200))
    #sns.histplot(df_roads[roads],)
#bins=[0,100,200,300,400,500,600,700,800,900,1000,1500,2000,3000,4000,5000],
#plt.legend(prop={'size': 10}, title = 'US Highways')
plt.title('Histogram for IRI on  State roads with 100 bins',fontsize=12)
plt.xlabel('IRI (in/mi))')
plt.ylabel('normalized count')
plt.axvline(x=70, color='green', linewidth= 1,linestyle="--", label="IRI=70")
plt.axvline(x=170, color='orange', linewidth= 1,linestyle="--", label="IRI=170")
plt.axvline(x=330, color='red', linewidth= 1,linestyle="--", label="IRI=330")
#plt.axvline(x=300, color='red', linewidth= 1,linestyle="--", label="IRI=330")
#plt.axvline(x=270, color='red', linewidth= 1,linestyle="--", label="IRI=270")

plt.legend(prop={'size': 10}, title = 'Roads')


# %%
#%%



# Fixing random state for reproducibility
#df_plt_z4 = df_plt_z4[df_plt_z4["R_IRI"] <=1000]
df_roads_list=df_allrds_density.columns.to_list()
for roads in df_roads_list:
    rds_den=roads+"_den"
    rds_iri=roads+"_iri"
    #print(rds_den)
    plt.scatter(df_roads[rds_den], df_roads[rds_iri], c="g", alpha=0.1, marker=r'o',
                label= str(roads))
    plt.xlabel("Crack Density(%)")
    plt.ylabel("IRI (in/mi)")
    plt.legend(loc='upper right')
    plt.show()
# %%
df_iri_rds=df_allrds_iri.round(1)
df_iri_rds = df_iri_rds.where(df_iri_rds <1000) #18 values greater than 5000 were lost
df_roads=df_iri_rds.join(df_allrds_density, lsuffix='_iri', rsuffix='_den')
# %%
