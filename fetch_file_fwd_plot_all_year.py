#%%
import os
import pathlib
import pandas as pd
year_list=[]
rootfilepath_m="/Users/jhasneha/Documents/SPRINDOT/summer2021/SPRINDOT/FWD/FWD_data"  

dict_pavements_df={}
road_types_list=[]
pavement_types_list=[]
pavement_list=[]
year_files=os.listdir(rootfilepath_m)
for year in year_files:
    if not year.startswith('.'):
        print(year)
        year_list.append(year)
        rootfilepath=rootfilepath_m +'/'+year
        year_files=os.listdir(rootfilepath)
        dict_pavements_df[year]={}
        for road_type in year_files:
            if not road_type.startswith('.'):
                road_types_list.append(road_type)
                print("File names: " ,road_type)
                destination_root= rootfilepath + '/'+ road_type
                road_type_files= os.listdir(destination_root)
                dict_pavements_df[year][road_type]={}
                for pavement_type in road_type_files:
                    
                    if not pavement_type.startswith('.'):
                        pavement_types_list.append(pavement_type)
                        print(pavement_type)
                        pavement_type_path= destination_root + '/'+pavement_type
                        pavement_type_files= os.listdir(pavement_type_path)
                        dict_pavements_df[year][road_type][pavement_type]={} 
                        for pavements in pavement_type_files:
                            if not pavements.startswith ('.'):
                                key= year+road_type+pavement_type
                                #print(key)
                                pattern= "*.xlsx"
                                list_pavements=list(pathlib.Path(pavement_type_path).glob(pattern))
                                #print(list_pavements)
                                for index in list_pavements:
                                    #print(index)
                                    pavement_key=os.path.basename(index)
                                    # pavement_key=pavement_key.replace(" ","_")
                                    # pavement_key=pavement_key.replace(".xlsx","")
                                    print("pavement_key",pavement_key)
                                    partitioned_key=pavement_key.partition(" ")
                                    pavement=partitioned_key[0]
                                    bound= partitioned_key[2].partition(" ")
                                    print("bound is : ", bound[0])
                                    df=pd.read_excel(index)
                                    #print(df.head())
                                    df.columns=df.columns.str.replace(' ', '')
                                    df.columns=df.columns.str.replace(r'\([^)]*\)', '')
                                    key_d= pavement + "-" + bound[0]
                                    print("pavement_ name: ", key_d)
                                    dict_pavements_df[year][road_type][pavement_type][pavement_key]=df
                            
                        

#%%

#input parameters

year=
road_type=
pavement_type=
# %%
# %%
# example input command to the function to create dictionary from folder
test_df=pd.DataFrame(dict_pavements_df["2016"]["Interstate"]["Full Depth Asphalt Pavement"])


""" Creates the referenc eline for the fwd parameters"""
#%%
import os
import pathlib
import pandas as pd
pavement_type="Concrete Pavement"
rootfilepath_m=("/Users/jhasneha/Library/CloudStorage/OneDrive-purdue.edu/SPR-4521 (Patching)/For Reference Line/SR/"+pavement_type) 
appended_list_ref=[]
files=os.listdir(rootfilepath_m)
for file in files:
    if not file.startswith('.'):
        print(file)
        df=pd.read_excel(rootfilepath_m+'/'+file)
        df.columns=df.columns.str.replace(' ', '')
        df.columns=df.columns.str.replace(r'\([^)]*\)', '')
        df=df.dropna(axis='columns', how='all')
        print(list(df.columns))
        appended_list_ref.append(df)
df_reference=pd.concat(appended_list_ref)



# %%
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import cm
from itertools import cycle
import dc_stat_think as dcst
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 600
mpl.rc('font',family='Times New Roman')


percentiles = np.array([90 , 95])
lines = ["-","--","-.",":"]
linecycler = cycle(lines)

cmap=plt.get_cmap("Paired")
years=list(dict_pavements_df.keys())
colors=cmap(np.linspace(0,1,len(years)))


fwd_params={"SubgradeDeflection":[1.8,1.4],"SurfaceDeflection":[37,25],"SCI":[8,6],"BCI":[4,3],"BDI":[8.8,4.4]}
#dict_year={"2016":"red","2017":"blue","2018":"green"}
def plot_fwd(pavement,road_type,df_reference):
    list_x=[]
    
    for params, threshold in fwd_params.items():
        fig,ax=plt.subplots()
        # ax1=ax
        # ax1=ax.twiny()
        print("pavement type is :", params)
        y=0.2
        for year, color in zip(years,colors):
            print(year)
            try:
                for k, v in dict_pavements_df[year][road_type][pavement].items():
                    
                        
                        partitioned_key=k.partition(" ")
                        pvmnt=partitioned_key[0]
                        bound= partitioned_key[2].partition(" ")
                        print("bound is : ", bound[0])
                        key_d= pvmnt + "-" + bound[0]+ "-"+year
                        # for pavements, v in v.items():
                        x=v[params].max()
                        list_x.append(x)
                        #     print(pavements)
                        pct_val = np.percentile(v[params], percentiles)
                        ecdfx,ecdfy = dcst.ecdf(v[params])
                        ecdfRef_x,ecdfRef_y=dcst.ecdf(df_reference[params])

                        print("pct_val",pct_val)
                        pavement_str= str(key_d)
                        plt.plot(ecdfx,ecdfy, next(linecycler), label=key_d, color=color)

                        plt.plot(pct_val, percentiles/100.0, marker='o', color='red', markeredgecolor="black", markeredgewidth="0.4",markersize = 4, linestyle='none')
                        plt.ylabel('Probability',fontsize=12)
                        plt.xlabel('Deflection (milli inches)',fontsize=12)
                        plt.title('ECDF plot for '+ params +' values on '+ road_type + ' and '+ pavement+'.',fontsize=14)
                            #road is Interstate ,SR etc. and pavement _type is composit, full depth etc.
                        # # NOTE: changed `range(1, 4)` to mach actual values count
                        
                        # ax1.set_xlim(0,1,2)
                        # ax1= plt.text(0.5,y, pavement_str + "=" + str(pct_val[1].round(1)),fontsize= 4,color="black", ha="center")    
                        # y=y+0.02
            except:
                print("missing values")
                continue
        
        plt.plot(ecdfRef_x,ecdfRef_y, linestyle="-",label= "reference", color="white", linewidth= 2)
   
        plt.axhline(y=0.90, color='pink', linewidth= 1,linestyle="--", label="90 percentile")
        plt.axhline(y=0.95, color='pink', linewidth= 1,linestyle="--", label="95 percentile")
        plt.axvline(x=threshold[1], color='greenyellow', linewidth=1.5,linestyle="--", label=params+"-lower")
        plt.axvline(x=threshold[0], color='red', linewidth= 1.5,linestyle="--", label=params+"-upper")

        plt.legend(loc="lower right",fontsize=4)  # To draw legend
        ax.set_facecolor('gray')

        plt.savefig('/Users/jhasneha/Documents/Spring2021/SPR_indot/SPRprojectcodes/fwd_graphs/'+road_type+'_'+pavement+'_' +params+'_withReference.png', orientation='landscape', pad_inches=1,bbox_inches='tight')
        plt.show()
        plt.clf()
        
    return ()  

#%%
plot_fwd("Concrete Pavement","SR",df_reference)

# %%
print("pavement_key",pavement_key)
partitioned_key=pavement_key.partition(" ")
pavement=partitioned_key[0]
bound= partitioned_key[2].partition(" ")
print("bound is : ", bound[0])





# %%
