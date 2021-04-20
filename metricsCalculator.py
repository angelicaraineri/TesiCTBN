import yaml
import matplotlib.pyplot as plt
import seaborn as sns
import statistics
from operator import itemgetter
import json
from sklearn.metrics import f1_score
import pandas as pd
import numpy as np
from itertools import chain


json_data = {}
list_variables = []
binary = []
ternary = []
quaternary = []
    
def adj_list_to_adj_matrix_real(adj_list, variables):
    #print("REAL MATRIX " , adj_list)
    variables = pd.DataFrame(variables)
    adj_matrix = np.zeros((variables.shape[0], variables.shape[0]))
    for edge in adj_list:
        adj_matrix[variables[variables["Name"] == edge["From"]].index[0],variables[variables["Name"] == edge["To"]].index[0]] = 1
    return adj_matrix


def adj_list_to_adj_matrix_estimate(adj_list, variables):
    #print("ESTIMATE MATRIX " , adj_list)
    variables = pd.DataFrame(variables)
    adj_matrix = np.zeros((variables.shape[0], variables.shape[0]))
    for edge in adj_list:
        adj_matrix[variables[variables["Name"] == edge[0]].index[0],variables[variables["Name"] == edge[1]].index[0]] = 1
    return adj_matrix

def confusion_matrix(real, predicted):
    p_minus_t = predicted - real
    
    global fp
    fp = np.sum(p_minus_t > 0)
    global fn
    fn = np.sum(p_minus_t < 0)
    global tp
    tp = np.sum(real == 1) - fn
    global tn
    tn = np.sum(real == 0) - fn
        
    ret = np.array([[tp, fp] , [fn, tn]], dtype = int)
    return ret

def plot_dataset(data_x_axis, data_y_axis,density, cardinality):
    dataset = pd.DataFrame({'f1 score': data_y_axis, 'number of variables' : data_x_axis})
    ax = sns.lineplot( x = 'number of variables' , y = 'f1 score', marker = 'o', data = dataset)
    ax.set_xticks(data_x_axis)
    ax.set_title(cardinality+" data with 0"+str(density)+" density and "+ \
str(number_trajectories)+" indipendent trajectories")
    name = cardinality+"_0"+str(density)
    ax = ax.get_figure()
    ax.savefig("output/Graphs/%s.pdf" %name)
    ax.clf()

def build_dataset(data_to_plot):
    data_x_axis.append(data_to_plot.pop(0))
    data_y_axis.append(statistics.mean(data_to_plot))
    return data_x_axis, data_y_axis

#array_nodes = [[3], [4], [5], [6], [10], [15], [20]]
array_nodes = [[3], [4], [5], [6], [10]]

for i in range(3): # cardinality = 01, 02, 03, 04
    binary.append([])
    ternary.append([]) 
    quaternary.append([])
    for t in range(len(array_nodes)):
        binary[i].append(list(array_nodes[t]))
        ternary[i].append(list(array_nodes[t]))
        quaternary[i].append(list(array_nodes[t]))

with open('params.yaml') as file:
    documents = yaml.full_load(file)
    number_trajectories = documents['feature']['number_trajectories']

with open("./output/estimateStructure.json") as f:
    estimate_data = json.load(f)
        
with open("./output/realStructure.json") as f:
    real_data = json.load(f)

        
for item in estimate_data:
    #print(" ")
    print(item)
    struct_estimate = estimate_data.get(item)
    struct_real = real_data.get(item)[0]
    variables = real_data.get(item)[1]

    conf = confusion_matrix(adj_list_to_adj_matrix_real(struct_real, variables),\
            adj_list_to_adj_matrix_estimate(struct_estimate, variables))
    
    #print("CONFUSION MATRIX : " , conf)

    recall = tp / (tp + fn)
    precision = tp / (tp + fp)
    f1_score = 2*((precision*recall)/(precision + recall))
    #print("F1 SCORE " , f1_score)
    
    cardinality = item.split("/")[2].split("_")[3]
    
    if (len(item.split("/")[2].split("_")) < 7):
        density = 3
        nodes = int(item.split("/")[2].split("_")[5])
    else:
        density = int((item.split("/")[2].split("_")[5])[1])
        nodes = int(item.split("/")[2].split("_")[6])

    if (nodes <= 6):
        index = nodes - 3
    elif (nodes == 10):
        index = 4
    elif (nodes == 15):
        index = 5
    else:
        index = 6

    if(cardinality == "binary"):
        binary[density - 1][index].append(f1_score)
    elif (cardinality == "ternary"):
        ternary[density - 1][index].append(f1_score)
    elif (cardinality == "quaternary"):
        quaternary[density - 1][index].append(f1_score)
                
    json_data['File %s' %item] = {
      'F1 score' : f1_score,
      'Numbero of indipendent trajectories' : number_trajectories,
      'Confusion matrix' : conf.tolist()
    }
    with open('./output/metrics.json' , 'w') as f:
        json.dump(json_data, f)

data_x_axis = []
data_y_axis = []


for i in range(len(binary)):
    for x in range(len(binary[i])): #all values for density = i
        data_to_plot = list(binary[i][x])
        result = build_dataset(data_to_plot)
    plot_dataset(result[0], result[1], i + 1, "binary")
    data_x_axis = []
    data_y_axis = []

for i in range(len(ternary)):
    for x in range(len(ternary[i])): #all values for density = i
        data_to_plot = list(ternary[i][x])
        result = build_dataset(data_to_plot)
    plot_dataset(result[0], result[1], i + 1, "ternary")
    data_x_axis = []
    data_y_axis = []

for i in range(len(quaternary)):
    for x in range(len(quaternary[i])): #all values for density = i     
        data_to_plot = list(quaternary[i][x])
        result = build_dataset(data_to_plot)
    plot_dataset(result[0], result[1], i + 1, "quaternary")
    data_x_axis = []
    data_y_axis = []

