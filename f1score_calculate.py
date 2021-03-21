import json
from sklearn.metrics import f1_score
import pandas as pd

with open("./output/estimateStructure.json") as f:
    data = json.load(f)
    
array = data["links"]
estimateLinks = []

for x in range(len(array)):
    estimateLinks.append(array[x]["source"] + array[x]["target"])
    

with open("./output/realStructure.json") as f:
    data = json.load(f)
    
realLinks = []

for x in range(len(data)):
    realLinks.append(data[x]["From"] + data[x]["To"])
    
estimateLinks = sorted(estimateLinks)

realLinks = sorted(realLinks)
    
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

f1_scor = f1_score(y_actu, y_pred2)

print("F1 score : {}".format(f1_scor))

