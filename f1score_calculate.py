import json
from sklearn.metrics import f1_score
import pandas as pd

with open("./output/estimateStructure.json") as f:
    data = json.load(f)
    
array = data["links"]
linksP = []

for x in range(len(array)):
    linksP.append(array[x]["source"] + array[x]["target"])
    

with open("./output/realStructure.json") as f:
    data = json.load(f)
    
linksR = []

for x in range(len(data)):
    linksR.append(data[x]["From"] + data[x]["To"])
    
linksP = sorted(linksP)

linksR = sorted(linksR)
    
y_pred = [1]*len(linksP)
y_real = []


for x in range(len(linksR)):
    if(linksR[x] == linksP[x]):
        y_real.append(1)
    else:
        y_real.append(0)
            

y_actu = pd.Series(y_real, name='Actual')
y_pred2 = pd.Series(y_pred, name='Predicted')
df_confusion = pd.crosstab(y_actu, y_pred2)

f1_scor = f1_score(y_actu, y_pred2)

print("F1 score : {}".format(f1_scor))

