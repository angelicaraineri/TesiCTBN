import json


json_data = {}
json_data["binary_01"] = []
json_data["binary_02"] = []
json_data["binary_03"] = []
json_data["binary_04"] = []
json_data["ternary_01"] = []
json_data["ternary_02"] = []
json_data["ternary_03"] = []
json_data["ternary_04"] = []
json_data["quaternary_01"] = []
json_data["quaternary_02"] = []
json_data["quaternary_03"] = []
json_data["quaternary_04"] = []


for item in json_data:
    json_data[item].append(["150"])
    json_data[item].append(["150x2"])
    json_data[item].append(["300"])
"""
for item in json_data:
    for x in range(3):
        json_data[item][x].append([3])
        json_data[item][x].append([4])
        json_data[item][x].append([5])
        json_data[item][x].append([6])
        json_data[item][x].append([10])
        json_data[item][x].append([15])
        if(item != "quaternary_04"):
            json_data[item][x].append([20])
"""
print(json_data)

with open('./output/to_plot.json', 'w',) as f:
    json.dump(json_data, f)
