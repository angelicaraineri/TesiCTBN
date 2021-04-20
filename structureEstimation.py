import glob
import json
import os
from PyCTBN import JsonImporter
from PyCTBN import SamplePath
from PyCTBN import StructureConstraintBasedEstimator
import yaml
from sklearn.utils import resample
import random
import itertools


class main():
    
    y = []
    list_of_path = []
    list_of_combination = []
    json_data_real = {}
    json_data_est = {}

    with open('params.yaml') as file:
        documents = yaml.full_load(file)
        number_trajectories = documents['feature']['number_trajectories']
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
        for i in range(0,10):
            print(" ")
            print(read_files[i])
            importer = JsonImporter(file_path=read_files[i], samples_label='samples',
                                structure_label='dyn.str', variables_label='variables',
                                time_key='Time', variables_key='Name')
        
            importer.import_data(0)

            if (number_trajectories != 300):
                samples = importer._raw_data[0]['samples']
                y = random.sample(samples, number_trajectories)
                newSamples = resample(y, n_samples=300, replace=True,random_state=0)
                importer._raw_data[0]['samples'] = newSamples
        
            strut = importer._raw_data[0]['dyn.str']
            var = importer._raw_data[0]['variables']
            

            json_data_real['%s' %read_files[i]] = []
            json_data_real['%s' %read_files[i]].append(strut)
            json_data_real['%s' %read_files[i]].append(var)
    
            
            #with open('./output/realStructure.json' , 'w') as f:
                #json.dump(json_data, f)
    
            s1 = SamplePath(importer=importer)
            s1.build_trajectories()
            s1.build_structure()
            se1 = StructureConstraintBasedEstimator(sample_path=s1, exp_test_alfa=0.1, chi_test_alfa=0.1,
                                                known_edges=[], thumb_threshold=25)
            #se1.estimate_structure()
            #print(se1.adjacency_matrix())
            
            json_data_est['%s' %read_files[i]] = list(se1.estimate_structure())
            #with open('./output/estimateStructure.json' , 'w') as f:
                #json.dump(json_data2, f)
            
            #completeName =  os.path.join('./output/Structure' , "estimateStructure%s.json" %cont)
            #se1.save_results(completeName)
            # se1.save_plot_estimated_structure_graph(os.path.join('./output' , "estimateStructure%s.png" %cont))
            #cont = cont+1
    with open('./output/realStructure.json' , 'w') as f:
        json.dump(json_data_real, f)

    with open('./output/estimateStructure.json' , 'w') as f:
        json.dump(json_data_est, f)
