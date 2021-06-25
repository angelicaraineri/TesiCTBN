import json
import yaml
import itertools
import math
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
data_x_axis = [3, 4, 5, 6, 10, 15, 20]
y_ticks = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

traj = [100, 150, '150x2', 300]
max_axis = -math.inf 
min_axis = math.inf 

with open("./output/to_plot.json") as f:
    json_data = json.load(f)
   
#with open("./output/to_plot.json") as f:  
    #json_datai_fdr = json.load(f) 
for item in json_data:
    for i in range(len(json_data[item])):
        for c in range(1, len(json_data[item][i])):
            if(max_axis < max(json_data[item][i][c])): 
                     max_axis = max(json_data[item][i][c])
            if(min_axis >  min(json_data[item][i][c])): 
                    min_axis = min(json_data[item][i][c])
print("SALVATAGGIO GRAFICI F1")
for item in json_data:
    data_100 = json_data[item][0]   
    data_150 = json_data[item][1]       
    data_150x2 = json_data[item][2]
    data_300 = json_data[item][3]
    if(item.split("_")[0] == "quaternary"):
        data_x_axis = [3, 4, 5, 6, 10, 15]  
    
    df = pd.DataFrame({'Number of variables': 0, 'F1 score': 0, 'Number of trajectories': 0}, index = [0])

    for i in range(len(json_data[item])):
        for n in range(1, len(json_data[item][i])):
            for y in  range(len(json_data[item][i][n])): 
                if n <= 3:
                    c = n + 2
                elif n == 4:
                    c = 10
                elif n == 5:
                    c = 15
                elif n == 6:
                    c = 20

                if(json_data[item][i][0]==100):
                    json_data[item][i][0] = '100x3' 

                df = df.append({'Number of variables': c, \
                        'F1 score': json_data[item][i][n][y],\
                        'Number of trajectories': json_data[item][i][0]+' trajectories'}, ignore_index= True)
        df = df.drop(0)
    
    ax = sns.lineplot(data=df, x='Number of variables', y='F1 score',\
                hue='Number of trajectories', ci = 95 , err_style = 'bars', \
                marker = 'o')
    ax.set_xticks(data_x_axis)
    ax.set(ylim=(min_axis-0.05, max_axis+0.05)) 
    
    title = item.split("_")[0] + " data with " + item.split("_")[1] + " density"
    ax.set_title(title)
    ax.legend()
    plt.savefig('output/GraficiGenerali/%s.pdf' %item)
    plt.clf()
    print(title)

y = []
list_of_combination = []
list_of_path = []

with open("./output/150/fdr.json") as f:
    json_data_fdr = json.load(f)
with open('params.yaml') as file:
        documents = yaml.full_load(file)
        number_variables = documents['feature']['number_variables']
        cardinality = ['binary']
        density = documents['feature']['density']      
    
y.append(cardinality)
y.append(density)
y.append(number_variables)

#df_real = pd.DataFrame({'Variable': 0, 'Real FDR': 0, 'Estimate FDR': 0}, index = [0])
print(" ")
print("SALVATAGGIO GRAFICI FDR")
for element in itertools.product(*y):
    list_of_combination.append(element)

for x in range(len(list_of_combination)):
    if list_of_combination[x][1]==3:
        path ="./data/networks_and_trajectories_" + list_of_combination[x][0] + \
                 "_data_"+ str(list_of_combination[x][2])
    else :
        path ="./data/networks_and_trajectories_" + list_of_combination[x][0] + \
                    "_data_0" + str(list_of_combination[x][1]) + "_"+ \
                str(list_of_combination[x][2])
    
    list_of_path.append(path)

for i in range(len(list_of_path)):
    df_real = pd.DataFrame({'Variable': 0, 'Real FDR': 0, 'Estimate FDR': 0, 'File': 0}, index = [0])
    for t in range(1, 11):
        path = list_of_path[i]+"/"+str(t)+".json"
        data = json_data_fdr.get(path)
        print(path)
        print(" ")
        
        for c in data:
            x = data.get(c)
            #print(c, " ", x)

            if not x.get('Estimate fdr') == None:

                df_real= df_real.append({'Variable': c, 'Real FDR': x.get('Real FDR'), \
                                    'Estimate FDR': x.get('Estimate fdr'), \
                                    'File': t}, ignore_index = True)
    df_real= df_real.drop(0)


    if (len(list_of_path[i].split("/")[2].split("_")) < 7):
        density = 3
        nodes = int(list_of_path[i].split("/")[2].split("_")[5])
    else:
        density = int((list_of_path[i].split("/")[2].split("_")[5])[1])
        nodes = int(list_of_path[i].split("/")[2].split("_")[6])
    title = 'Binary_0'+str(density)+'_'+str(nodes)
    """ 
    g = sns.FacetGrid(df_real, col = "File", height=5, col_wrap=2)
    g.map_dataframe(sns.scatterplot, x='Estimate FDR', y='Real FDR', \
                hue = "Variable", palette = "deep", marker = 'o')
    """
    X_plot = np.linspace(0.001, 10) 
    Y_plot = X_plot 
    
    df_prova = pd.DataFrame({'x': X_plot, 'y': Y_plot})

    g = sns.relplot(data=df_real, x="Estimate FDR", y= "Real FDR", \
            col= "File", hue="Variable", kind="scatter",  height=5, col_wrap=2)
    g.map(sns.lineplot, data = df_prova, x='x', y='y', linestyle = 'dotted', linewidth='0.4', color = 'black')
    
    g.fig.subplots_adjust(top=0.95)
    g.fig.suptitle('%s' %title)
    g.set_axis_labels("Estimate FDR", "Real FDR")
    g.set(ylim=(-0.05,1.05))
    g.set(xlim=(-0.05, 1.05))
    
    plt.savefig('output/GraficiGenerali/fdr/%s.pdf' %title, dpi=300, bbox_inches='tight')
    plt.clf()
    print(df_real)
    del df_real
    print(title)
"""
        ax = sns.scatterplot(data=df_real, x='Estimate FDR_mean', y='Real FDR_mean', hue = "Variable", marker = 'o')
    
    #ax.set_xticks(data_x_axis)
    ax.set(ylim=(-0.1,1))
    ax.set(xlim=(-0.1,1)) 
    if (len(list_of_path[i].split("/")[2].split("_")) < 7):
        density = 3
        nodes = int(list_of_path[i].split("/")[2].split("_")[5])
    else:
        density = int((list_of_path[i].split("/")[2].split("_")[5])[1])
        nodes = int(list_of_path[i].split("/")[2].split("_")[6])
    title = 'Binary_0'+str(density)+'_'+str(nodes)
    ax.set_title(title)
    ax.legend()
    plt.savefig('output/GraficiGenerali/fdr/%s.pdf' %title)
    plt.clf()
    del df_real
"""















