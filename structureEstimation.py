import sys
import multiprocessing
from pathlib import Path
import glob
import json
import os
from PyCTBN import SampleImporter
from PyCTBN import SamplePath
from PyCTBN import StructureConstraintBasedEstimator
import yaml
from sklearn.utils import resample
import random
import itertools
import pandas as pd
import numpy as np

class main():
    
    number_trajectories = str(sys.argv[1])

    print(number_trajectories)

    y = []
    list_of_path = []
    list_of_combination = []
    json_data_real = {}
    json_data_est = {}

    with open('params.yaml') as file:
        documents = yaml.full_load(file)
        number_variables = documents['feature']['number_variables']
        cardinality = documents['feature']['cardinality']
        density = documents['feature']['density']      
    
    y.append(cardinality)
    y.append(density)
    y.append(number_variables)

    for element in itertools.product(*y):
        list_of_combination.append(element)

    for x in range(len(list_of_combination)):
        if list_of_combination[x][1]==3:
             path ='./data/networks_and_trajectories_' + list_of_combination[x][0] + '_data_'+ str(list_of_combination[x][2])
        else :
            path ='./data/networks_and_trajectories_' + list_of_combination[x][0] + '_data_0' + str(list_of_combination[x][1]) + '_'+ str(list_of_combination[x][2])
        if (path != './data/networks_and_trajectories_quaternary_data_01_20' and path != './data/networks_and_trajectories_quaternary_data_02_20' and path != './data/networks_and_trajectories_quaternary_data_20'):
            list_of_path.append(path)
    
    for x in range(len(list_of_path)):
        read_files = glob.glob(os.path.join(list_of_path[x], "*.json"))
        for i in range(len(read_files)):
            print(" ")
            print(read_files[i])

            with open(read_files[i]) as f:
                raw_data = json.load(f)

                variables = pd.DataFrame(raw_data["variables"])
                prior_net_structure = pd.DataFrame(raw_data["dyn.str"])
                trajectories_list_raw = raw_data["samples"]
                #trajectories_list = [pd.DataFrame(sample) for sample in trajectories_list_raw]
                if (number_trajectories == "150x2"):
                    traj = 150
                else:
                    traj = int(number_trajectories)

                if (number_trajectories != "300"):
                    y = random.sample(trajectories_list_raw, traj)
                else:
                    augmented_trajectories_list = [pd.DataFrame(sample) for sample in trajectories_list_raw]
                if(number_trajectories == "150"):
                    trajectories_list = [pd.DataFrame(sample) for sample in y]
                    augmented_trajectories_list = trajectories_list
                elif(number_trajectories == "150x2"):
                    trajectories_list = [pd.DataFrame(sample) for sample in y]
                    augmented_trajectories_list = resample(trajectories_list, replace = True, n_samples = 300 )
                elif(number_trajectories == "100"):
                    trajectories_list = [pd.DataFrame(sample) for sample in y]
                    augmented_trajectories_list = resample(trajectories_list, replace = True, n_samples = 300 )
                
            importer = SampleImporter(trajectory_list = augmented_trajectories_list, variables = variables, prior_net_structure = prior_net_structure)
            importer.import_data()          

            json_data_real['%s' %read_files[i]] = []
            json_data_real['%s' %read_files[i]].append(prior_net_structure.to_json())
            json_data_real['%s' %read_files[i]].append(variables.to_json())
    
            s1 = SamplePath(importer=importer)
            s1.build_trajectories()
            s1.build_structure()
            se1 = StructureConstraintBasedEstimator(sample_path=s1, exp_test_alfa=0.1, chi_test_alfa=0.1,
                                                known_edges=[], thumb_threshold=25)
            #print(se1.adjacency_matrix())
            
            json_data_est['%s' %read_files[i]] = list(se1.estimate_structure(processes_number=32))
                        
            #completeName =  os.path.join('./output/Structure' , "estimateStructure%s.json" %cont)
            #se1.save_results(completeName)
            # se1.save_plot_estimated_structure_graph(os.path.join('./output' , "estimateStructure%s.png" %cont))
            #cont = cont+1
    out_folder="output/{}".format(number_trajectories)
    Path("{}/".format(out_folder)).mkdir(parents=True, exist_ok=True)
    
    with open("{}/realStructure.json".format(out_folder) , 'w') as f:
        json.dump(json_data_real, f)

    with open("{}/estimateStructure.json".format(out_folder) , 'w') as f:
        json.dump(json_data_est, f)
    
