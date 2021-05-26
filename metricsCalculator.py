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
import sys

json_data = {}
binary = []
ternary = []
quaternary = []

print(sys.argv[1])
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

    fp = np.sum(p_minus_t > 0)
    fn = np.sum(p_minus_t < 0)
    tp = np.sum(real == 1) - fn
    tn = np.sum(real == 0) - fp - real.shape[0]      

    ret = np.array([[tp, fp] , [fn, tn]], dtype = int)
    
    return ret, fp, fn, tp, tn


def plot_dataset(data_x_axis, data_y_axis,density, cardinality, number_trajectories):
    dataset = pd.DataFrame({'f1 score': data_y_axis, 'number of variables' : data_x_axis})
    print(dataset) 
    
    id_1 = cardinality + "_0" + str(density)

    id_2 = 0
    if (number_trajectories == "100"):
        id_2 = 1
    elif (number_trajectories == "150"):
        id_2 = 2
    elif (number_trajectories == "150x2"):
        id_2 = 3
    elif (number_trajectories == "300"):
        id_2 = 4

    for x in range(len(data_y_axis)):
        to_plot[id_1][id_2].append(data_y_axis[x])

    with open('./output/to_plot.json' , 'w') as f:
        json.dump(to_plot, f)
    """
    ax = sns.lineplot( x = 'number of variables' , y = 'f1 score', marker = 'o', data = dataset)
    ax.set_xticks(data_x_axis)
    ax.set_title(cardinality+" data with 0"+str(density)+" density and "+ \
str(number_trajectories)+" indipendent trajectories")
    name = number_trajectories+"/"+cardinality+"_0"+str(density)
    ax = ax.get_figure()
    ax.savefig("output/%s.pdf" %name)
    print("Saving graph " , name)
    ax.clf()
    """

def build_dataset(data_to_plot):
    data_x_axis.append(data_to_plot.pop(0))
    mean = statistics.mean(data_to_plot)
    data_y_axis.append(mean)
    print(statistics.mean(data_to_plot))
    return data_x_axis, data_y_axis

def calculate_f1(res):
    fp = res[1]
    fn = res[2]
    tp = res[3]
    tn = res[4]
    recall = tp / (tp + fn)
    precision = tp / (tp + fp)
    f1 = 2*((precision*recall)/(precision + recall))
    return f1

array_nodes = [[3], [4], [5], [6], [10], [15], [20]]

for i in range(4): # cardinality = 01, 02, 03, 04
    binary.append([])
    ternary.append([]) 
    quaternary.append([])
    for t in range(len(array_nodes)):
        binary[i].append(list(array_nodes[t]))
        ternary[i].append(list(array_nodes[t]))
        quaternary[i].append(list(array_nodes[t]))
    quaternary[i].pop()

number_trajectories = str(sys.argv[1])

with open("./output/%s/estimateStructure.json" %number_trajectories) as f:
    estimate_data = json.load(f)
        
with open("./output/%s/realStructure.json" %number_trajectories) as f:
    real_data = json.load(f)

with open("./output/to_plot.json") as f: 
    to_plot = json.load(f)

for item in estimate_data:
    #print(" ")
    print(item)
    struct_estimate = estimate_data.get(item)
    struct_real = real_data.get(item)[0]
    variables = real_data.get(item)[1]

    res = confusion_matrix(adj_list_to_adj_matrix_real(struct_real, variables),\
                    adj_list_to_adj_matrix_estimate(struct_estimate, variables))
    conf = res[0]
    #print("CONFUSION MATRIX : " , conf)
    f1_score = calculate_f1(res)
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
    
    json_data["File %s" %item] = {
            'F1 score' : f1_score,
            'Number of indipendent trajectories' : number_trajectories,
            'Confusion matrix' : conf.tolist()
    }
    with open('./output/metrics.json' , 'w') as f:
        json.dump(json_data, f)
    print("File metrics salvalto")
data_x_axis = []
data_y_axis = []

def fetch_data(array, cardinality):
    for i in range(len(array)):
        for x in range(len(array[i])): #all values for density = i
            data_to_plot = list(array[i][x])
            result = build_dataset(data_to_plot)
        plot_dataset(result[0], result[1], i + 1, cardinality, number_trajectories)
        del data_x_axis[:]
        del data_y_axis[:]

fetch_data(binary, "binary")

fetch_data(ternary, "ternary")

fetch_data(quaternary, "quaternary")
