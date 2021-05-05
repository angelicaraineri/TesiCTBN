import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
data_x_axis = [3, 4, 5, 6, 10, 15, 20]

with open("./output/to_plot.json") as f:
    json_data = json.load(f)


def prepare_data(item, index):
    data = json_data[item][index]
    data.pop(0)
    return data


for item in json_data:
    data_150 = prepare_data(item, 0)       
    data_150x2 = prepare_data(item, 1)
    data_300 = prepare_data(item, 2)
    print(item) 
    print(len(data_150))
    print(len(data_x_axis))
    if(item.split("_")[0] == "quaternary"):
        data_x_axis = [3, 4, 5, 6, 10, 15]

    plt.plot(data_x_axis, data_150, marker = ".", color='r', label = "150 trajectories")
    plt.plot(data_x_axis, data_150x2, marker = "." , color='g', label = "150x2 trajectories")
    plt.plot(data_x_axis, data_150x2, marker = "." , color='b', label = "300 trajectories")
    
    plt.xlabel("Number of variables")
    plt.xticks(data_x_axis)
    plt.ylabel("F1 score")
    
    title = item.split("_")[0] + " data with " + item.split("_")[1] + " density"
    plt.title(title)

    plt.legend()
    plt.savefig('output/%s.png' %item)
    plt.clf()

