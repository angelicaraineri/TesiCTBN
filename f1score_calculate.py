import yaml
from sklearn.metrics import confusion_matrix
import json
from sklearn.metrics import f1_score
import pandas as pd

f1_tot=0
for i in range(1,11):

    with open("./output/estimateStructure%s.json" %i) as f:
        data = json.load(f)
        
    array = data["links"]
    estimateLinks = []
    
    for x in range(len(array)):
        estimateLinks.append(array[x]["source"] + array[x]["target"])
        
    
    with open("./output/realStructure%s.json" %i) as f:
        data = json.load(f)
        
    realLinks = []
    
    for x in range(len(data)):
        realLinks.append(data[x]["From"] + data[x]["To"])
        
    estimateLinks = sorted(estimateLinks)
    
    realLinks = sorted(realLinks)
        
    cf = confusion_matrix(realLinks, estimateLinks)
    print(cf)
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
    y_pred2 = pd.Series(y_pred, name='Predicted')
    df_confusion = pd.crosstab(y_actu, y_pred2)
    #print(df_confusion)
    f1_scor = f1_score(y_actu, y_pred2)    
    print("F1 score : {}".format(f1_scor))

    f1_tot += f1_scor
    
    """
    with open('./output/f1score%s.json' %i, 'w') as f:
            json.dump(f1_scor, f)
            
f1_tot = 0
for i in range(1, 11):
   with open('./output/f1score%s.json' %i, 'r') as f:
        data = json.load(f)
        f1_tot += data
"""
f1_mean = f1_tot/10

with open('params.yaml') as file:
   documents = yaml.full_load(file)
   number_trajectories = documents['feature']['number_trajectories']
   number_variables = documents['feature']['number_variables']

json_data = {
   'F1 score medio' : f1_mean,
   'Numero variabili' : number_variables,
   'Numbero traiettorie indipendenti' : number_trajectories
}
print("F1 medio : {}".format(f1_mean))    

with open('./output/metric.json' , 'w') as f:
	json.dump(json_data, f)
