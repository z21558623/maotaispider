# -*- coding: utf-8 -*-

from os import walk
import pandas as pd
import matplotlib.pyplot as plt
dataframe_list = []
old_str='\"\"'
new_str=''
#walk会返回3个参数，分别是路径，目录list，文件list，你可以按需修改下
for f, _, i in walk("comments/"):
    for j in i:        
        with open(f+j,'r', encoding="utf-8") as r:
            lines=r.readlines()
        with open(f+j,'w', encoding="utf-8") as w:
            title =True
            for l in lines:               
               if (len(l)<10 or l[0]==',') and title==False:
                  pass
               else:
                   w.write(l) 
                   title = False
                   
#        with open(f+j, "r", encoding="utf-8") as f1:
#            for line in f1:
#                if old_str in line or len(line)<10:
#                    line = line.replace(old_str, new_str)
        dataframe_list.append(pd.read_csv(f  + j,delimiter=',',parse_dates=[3]))

print (dataframe_list)
dfs = pd.DataFrame(columns=dataframe_list[0].columns)
for df in dataframe_list:
    df = df
    dfs = dfs.append(df)
    
#dfs = dataframe_list[3]
print (dfs)
dfs1=dfs.set_index(dfs['date'])
dfs1.index.drop_duplicates()
pd.to_datetime(dfs1['date'],errors='coerce')
dfs1['date'].apply(str)
#dfs1.sort_values(by=['date'])


ticks = dfs1.ix[:,['score']]
ticks1 = ticks.dropna(how='all')

pd.to_datetime(ticks1.index,errors='coerce')
bars = ticks1.score.resample('M').count()
bars.plot()
#df.sort_values(by='date')ti
#df['date'].apply(pd.to_datetime,errors='ignore')
#bars = ticks1.score.resample('M').count()
#ticks1 = ticks.dropna(how='all')
#print (df)
#ticks = df1.ix[:,['score']]
#    
    
#    list = df['date'].head(10)