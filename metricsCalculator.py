import yaml
import json
from sklearn.metrics import f1_score
import pandas as pd

f1_tot=0
json_data_to_plot = {}
json_data = {}
with open('params.yaml') as file:
   documents = yaml.full_load(file)
   number_trajectories = documents['feature']['number_trajectories']
   number_variables = documents['feature']['number_variables']


for i in range(1,11):

    with open("./output/estimateStructure.json") as f:
        data = json.load(f)
        
    array = data["links"]
    estimateLinks = []
    
    for x in range(len(array)):
        estimateLinks.append(array[x]["source"] + array[x]["target"])
        
    
    with open("./output/Structure/realStructure%s.json" %i) as f:
        data = json.load(f)
        
    realLinks = []
    
    for x in range(len(data)):
        realLinks.append(data[x]["From"] + data[x]["To"])
    
    y_real = [1]*len(realLinks)
    y_pred = []
    
    
    for x in range(len(realLinks)):
        if realLinks[x] in estimateLinks:
            y_pred.append(1)
        else:
            y_pred.append(0)
            
    if len(realLinks)>len(estimateLinks):
        y_real.append(1)
        y_pred.append(0)
    
    if len(realLinks)<len(estimateLinks):
        y_real.append(0)
        y_pred.append(1)
           
    
    y_actu = pd.Series(y_real, name='Actual')
    y_pred = pd.Series(y_pred, name='Predicted')
    df_confusion = pd.crosstab(y_pred, y_actu)
    print(df_confusion)
    f1 = f1_score(y_actu, y_pred)    
    print("F1 score : {}".format(f1))

    json_data['File %s' %i] = {
      'F1 score' : f1,
      'Numero of nodes' : number_nodes,
      'Numbero of indipendent trajectories' : number_trajectories,
      'Confusion matrix' : df_confusion.to_json()
    }

    with open('./output/metrics.json' , 'a') as f:
        json.dump(json_data, f)

    f1_tot += f1
    
f1_mean = f1_tot/10

print("F1 medio : {}".format(f1_mean)) 

json_data['Metrics generali'] = {
   'F1 score mean' : f1_mean,
   'Number of nodes' : number_nodes,
   'Number of indipendent trajectories' : number_trajectories,
}   

with open('./output/metrics.json' , 'w') as f:
	json.dump(json_data, f)

json_data_to_plot = {
    'F1 score' : f1_mean,
    'Number of nodes' : number_nodes,
}

data = json.load(open('./output/metrics_to_plot.json'))
if type(data) is dict:
    data = [data]
data.append(json_data_to_plot)

with open('./output/metrics_to_plot.json','w') as f:
        json.dump(data, f)
