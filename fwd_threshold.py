#%%
from numpy.core.numeric import indices
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%%
#rootfilepath='/Users/jhasneha/Documents/SPRINDOT/summer2021/SPRINDOT/Roads_3d/Interstate'
#rootfilepath='/Users/jhasneha/Documents/SPRINDOT/summer2021/SPRINDOT/FWD/Full Depth Asphalt Pavement'
#rootfilepath='/Users/jhasneha/Documents/SPRINDOT/summer2021/SPRINDOT/Roads_3d/USroads'
asphalt='/Users/jhasneha/Documents/SPRINDOT/summer2021/SPRINDOT/FWD/2019/SR/Asphalt Pavement'
asphalt='/Users/jhasneha/Documents/SPRINDOT/summer2021/SPRINDOT/FWD/2019/SR/Asphalt Pavement'


"""    ############################
____________________ better version of creating the above list of fdataframes

*************************************************** """


#%%
import os
import pathlib

def create_df(rootfilepath, parameter):
    root_files=os.listdir(rootfilepath)
    df_roads_SD=pd.DataFrame()
    for entry in root_files:
        if not entry.startswith('.'):
            print("File names: " ,entry)
            destination_root= rootfilepath + '/'+entry
            #print("destination" ,destination_root)
            pattern= "*.xlsx"
            list_p=list(pathlib.Path(destination_root).glob(pattern))
            #print(list_p)
            list_SD=[]
            df_SD=pd.DataFrame(columns=["SD"])
            for index in list_p:
                print("in the 2nd loop: ",index)
                df=pd.read_excel(index)
                #print(df.head())
                df.columns=df.columns.str.replace(' ', '')
                df.columns=df.columns.str.replace(r'\([^)]*\)', '')
                print(df.columns.to_list())
                list_SD.append(df[parameter])
                print("inside   ", len(list_SD))
            if len(list_SD) > 1:
                print("outside   ",len(list_SD))
                final_df=pd.concat(list_SD)
                print(" shape of final df: ",final_df.shape[0])
                df_SD=final_df.to_frame()
                df_SD.columns=[str(entry)]
                print("colname:   ",df_SD.columns) 
            else:
                print("outside   ",len(list_SD))
                final_df=pd.concat(list_SD)
                df_SD=final_df.to_frame()
                df_SD.columns=[str(entry)]
                print("colname:   ",df_SD.columns)
        #print("df_SD   ",df_SD.head())  
        df_roads_SD=pd.concat([df_roads_SD,df_SD])
        print(df_roads_SD.head())
        print("dataframe was created ",df_roads_SD.columns)
        arr = justify(df_roads_SD.to_numpy(), invalid_val=np.nan,axis=0)
        df_SD_justified = pd.DataFrame(arr, columns=df_roads_SD.columns)
        df_SD_justified=df_SD_justified.dropna(axis=0,how='all')

    #ecdf_fwd(df_SD_justified,parameter)
    return df_SD_justified



"""@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                    IRI
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"""



     
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
import copy
fwd_params=["BDI","SurfaceDeflection","SubgradeDeflection","BCI","SCI"]
dict_of_df = {}
for parameter in fwd_params:
    df=create_df(asphalt,parameter)

    key_name = str(parameter)   

    dict_of_df[key_name] = copy.deepcopy(df)  

dict_of_df.keys()

 
#%%
import copy
fwd_params=["BDI","SurfaceDeflection","SubgradeDeflection","BCI","SCI"]
list_df=[]
for parameter in fwd_params:
    df=create_df(asphalt,parameter)
    # print(df.head())
    # list_df.append(df)
 

#%%
df=create_df(asphalt,"BDI")






#%%
def ecdf_fwd(df,fwd,ref, road_name, year, pavement_type):
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
    # ax6=ax
    ax7=ax
    #n=1
    # # generate a sample
    # list_roads= df.columns.to_list()
    # for roads in list_roads:
    #     sample+str(n)=np.array(df[roads])

    sample1 = np.array(df["SR-4"])
    sample2 = np.array(df["SR-5"])
    sample3 = np.array(df["SR-10"])
    sample4 = np.array(df["SR-16"])
    sample5 = np.array(df["SR-32"])
    sample_ref=ref[fwd]

    sample1 = sample1[~np.isnan(sample1)]
    sample2 = sample2[~np.isnan(sample2)]
    sample3 = sample3[~np.isnan(sample3)]
    sample4 = sample4[~np.isnan(sample4)]
    sample5 = sample5[~np.isnan(sample5)]
    sample_ref=sample_ref[~np.isnan(sample_ref)]


    # fit a cdf
    ecdf1x,ecdf1y = dcst.ecdf(sample1)
    ecdf2x,ecdf2y = dcst.ecdf(sample2)
    ecdf3x,ecdf3y = dcst.ecdf(sample3)
    ecdf4x,ecdf4y = dcst.ecdf(sample4)
    ecdf5x,ecdf5y = dcst.ecdf(sample5)
    ecdfx,ecdfy = dcst.ecdf(sample_ref)
    
    percentiles = np.array([50 , 85])
 




    pct_val1 = np.percentile(sample1, percentiles)
    pct_val2 = np.percentile(sample2, percentiles)
    pct_val3 = np.percentile(sample3, percentiles)
    pct_val4 = np.percentile(sample4, percentiles)
    pct_val5 = np.percentile(sample5, percentiles)
    # pct_val6 = np.percentile(sample6, percentiles).round(1)
    pct_val_ref = np.percentile(sample_ref, percentiles).round(1)


    print("pct_val3 0.5, 0.85 are  : ", pct_val_ref, ecdfx, ecdfy)
    


    # plot the cdf
    ax.plot(ecdf1x, ecdf1y, color='fuchsia',linestyle="-.", label="SR-4")
    ax.plot(pct_val1, percentiles/100.0, marker='*', color='red', markeredgecolor="black", markeredgewidth="0.4",markersize = 8, linestyle='none')

    ax2.plot(ecdf2x, ecdf2y, color = 'gold', linestyle="-",label="SR-5")
    ax2.plot(pct_val2, percentiles/100.0, marker='o', color='red',markersize = 6,markeredgecolor="black",markeredgewidth="0.4", linestyle='none')

    ax3.plot(ecdf3x, ecdf3y, color = 'lime', label="SR-10")
    ax3.plot(pct_val3, percentiles/100.0, marker='*', color='red', markersize = 8,markeredgecolor="black",markeredgewidth="0.4", linestyle='none')

    ax4.plot(ecdf4x, ecdf4y, color = 'salmon',linestyle="-", label="SR-16")
    ax4.plot(pct_val4, percentiles/100.0, marker='*', color='red' ,markersize = 8,markeredgecolor="black",markeredgewidth="0.4",linestyle='none')

    ax5.plot(ecdf5x, ecdf5y, color = 'deepskyblue',linestyle="--", label="SR-32")
    ax5.plot(pct_val5, percentiles/100.0, marker='o', color='red', markersize = 6,markeredgecolor="black",markeredgewidth="0.4", linestyle='none')

    # ax6.plot(ecdf6x, ecdf6y, color = 'blue', linestyle="-.",label="SR327")
    # ax6.plot(pct_val6, percentiles/100, marker='*', color='red' ,markersize = 8,markeredgecolor="black",markeredgewidth="0.4",linestyle='none')

    ax7.plot(ecdfx, ecdfy, color = 'white',linestyle="-", label="Reference")
    ax7.plot(pct_val_ref, percentiles/100, marker='X', color='red' ,markersize = 8,markeredgecolor="black",markeredgewidth="0.4",linestyle='none')

    ax.text(20, 0.64, '85 percentile ',fontsize= 8,color="ivory",weight='bold')    

    ax.text(20, 0.6, 'SR4='  + str(pct_val1[1].round(1)),fontsize= 8,color="ivory",weight='bold')    
    ax2.text(20, 0.56, 'SR5= ' + str(pct_val2[1].round(1)),color="ivory",fontsize= 8, weight='bold')   
    ax3.text(20, 0.52, 'SR10= ' + str(pct_val3[1].round(1)),color="ivory",fontsize= 8,weight='bold')
    ax4.text(20, 0.47, 'SR16= ' + str(pct_val4[1].round(1)), fontsize= 8, color="ivory",weight='bold')
    ax5.text(20, 0.43, 'SR32= ' + str(pct_val5[1].round(1)),fontsize= 8,color="ivory",weight='bold')
    # ax6.text(3, 0.40, 'I65=' + str(pct_val6[1]), fontsize= 8,color="ivory",weight='bold')
    ax7.text(20, 0.7, "ref= " + str(pct_val_ref[1]), fontsize= 8,color="ivory",weight='bold')

    # ax.text(300, 0.6, 'I70=' + str(pct_val1[1]),fontsize= 8,color="ivory",weight='bold')
    # ax2.text(300, 0.56, 'I74=' + str(pct_val2[1]),color="ivory",fontsize= 8, weight='bold')
    # ax3.text(300, 0.52, 'I64=' + str(pct_val3[1]),color="ivory",fontsize= 8,weight='bold')
    # ax4.text(300, 0.48, 'I465=' + str(pct_val4[1]), fontsize= 8, color="ivory",weight='bold')
    # ax5.text(300, 0.44, 'I69=' + str(pct_val3[1]),fontsize= 8,color="ivory",weight='bold')
    # ax6.text(300, 0.40, 'I65=' + str(pct_val4[1]), fontsize= 8,color="ivory",weight='bold')
    # ax7.text(300, 0.64, 'IRI(0.992)=' + str(pct_val_ref[1]), fontsize= 8,color="ivory",weight='bold')


    ax.set_ylabel('Probability',fontsize=8)
    ax2.set_xlabel('Deflection (milli inches)',fontsize=8)
    ax.set_title('ECDF plot for '+ fwd +' values for '+ road_name+ ' of'+ pavement_type+ ' pavement in the year ' + year + '.',fontsize=10)
    # ax.set_title('ECDF plot for CD values for Interstate Roads',fontsize=12)
    # ax2.set_xlabel('CD (%)',fontsize=8)
    ax.axhline(y=0.50, color='oldlace', linewidth= 1,linestyle="--", label="50 percentile")
    ax.axhline(y=0.85, color='lightgray', linewidth= 1,linestyle="--", label="85 percentile")
    #ax.axhline(y=0.9925, color='lightgray', linewidth= 1,linestyle="--", label="99.2 percentile")
    ax.axvline(x=36.4, color='aquamarine', linewidth= 1,linestyle="--", label="D0")
    ax.axvline(x=8.8, color='beige', linewidth= 1,linestyle="--", label="BDI")
    ax.axvline(x=1.8, color='red', linewidth= 1,linestyle="--", label="D48")
    ax.axvline(x=4, color='tan', linewidth= 1,linestyle="--", label="BCI")
    ax.axvline(x=8, color='orange', linewidth= 1,linestyle="--", label="SCI")



    ax.legend(fontsize=8,loc=4)
    ax2.legend(fontsize=8,loc=4)
    ax3.legend(fontsize=8,loc=4)
    ax4.legend(fontsize=8,loc=4)
    ax5.legend(fontsize=8,loc=4)
    # ax6.legend(fontsize=8,loc=4)
    ax7.legend(fontsize=8,loc=4)
    ax.set_facecolor('dimgray')
    #plt.xlim([-1,10])
    #plt.xlim([-10,600])
    plt.savefig('/Users/jhasneha/Documents/Spring2021/SPR_indot/SPRprojectcodes/fwd_graphs/'+road_name+'_'+pavement_type+'_' +fwd+'_'+year +'.png')
    pyplot.show()
    plt.clf()
    




# %%
df_ref=pd.DataFrame()
for key, value in dict_of_df.items():
    #print (value)
    val_ref=np.array(value).flatten()
    df_ref[key]=val_ref
    










#%%
for key in  dict_of_df.keys():
    print (key, value.head())
    ecdf_fwd(value, key , df_ref,"SR","2019","Asphalt")
    
   





    




    

# %%

# %%
def ecdf_fwd(df):
    import matplotlib as mpl
    mpl.rcParams['figure.dpi'] = 900
    from matplotlib import pyplot
    from numpy.random import normal
    import numpy as np
    import dc_stat_think as dcst
    fig4, ax = plt.subplots()
    percentiles = np.array([50 , 85])
    # # generate a sample
    road_list=df.columns.to_list()
    for roads in road_list:
        sample=np.array(df[roads])
        sample= sample[~np.isnan(sample)]
        ecdfx,ecdfy = dcst.ecdf(sample)
        pct_val = np.percentile(sample, percentiles)
        ax.plot(ecdfx, ecdfy, color='fuchsia',linestyle="-.", label="SR5")
        ax.plot(pct_val, percentiles/100.0, marker='*', color='red', markeredgecolor="black", markeredgewidth="0.4",markersize = 8, linestyle='none')
        ax.set_ylabel('Probability',fontsize=8)
        ax.set_title('ECDF plot for '+ df +' values for full depth Asphalt Pavement',fontsize=10)

        ax.axhline(y=0.50, color='oldlace', linewidth= 1,linestyle="--", label="50 percentile")
        ax.axhline(y=0.85, color='lightgray', linewidth= 1,linestyle="--", label="85 percentile")
        ax.legend(fontsize=8,loc=4)
        ax.set_facecolor('dimgray')
        pyplot.show()
   
