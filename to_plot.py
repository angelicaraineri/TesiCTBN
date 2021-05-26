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
    json_data[item].append(["100"])
    json_data[item].append(["150"])
    json_data[item].append(["150x2"])
    json_data[item].append(["300"])

print(json_data)

with open('./output/to_plot.json', 'w',) as f:
    json.dump(json_data, f)
