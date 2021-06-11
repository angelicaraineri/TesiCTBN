import multiprocessing
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
import pandas as pd
import sys
import numpy as np
from PyCTBN import SampleImporter


class main():
    number_trajectories = str(sys.argv[1])
    json_data_real = {}
    json_data_est = {}
    json_data_fdr = {}

    y = []
    list_of_path = []
    list_of_combination = []
    

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

                variables = raw_data["variables"]
                prior_net_structure = raw_data["dyn.str"]
                trajectories_list_raw = raw_data["samples"]
                #trajectories_list = [pd.DataFrame(sample) for sample in trajectories_list_raw]
                if (number_trajectories == "150x2"):
                    traj = 150
                else:
                    traj = int(number_trajectories)

                if (number_trajectories != "300"):
                    y = random.sample(trajectories_list_raw, traj)
                else:
                    augmented_trajectories_list = [pd.DataFrame(sample) for sample \
                            in trajectories_list_raw]
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
            json_data_real['%s' %read_files[i]].append(prior_net_structure)
            json_data_real['%s' %read_files[i]].append(variables)
    
            real_traj = [] 
            for t in prior_net_structure:
                real_traj.append((t.get('From'), t.get('To')))
            
            s1 = SamplePath(importer=importer)
            s1.build_trajectories()
            s1.build_structure()
            alfa = 0.2
            se1 = StructureConstraintBasedEstimator(sample_path=s1, exp_test_alfa=alfa, chi_test_alfa=0.1,
                                                known_edges=[], thumb_threshold=25)
            
            est_struc = se1.estimate_structure(True, 2)
            json_data_est['%s' %read_files[i]] = list(est_struc[0])
            
            p_values = est_struc[1]
            estimate_traj = est_struc[0]
            nodes = se1.get_nodes()
            parents = {}
            fdr_dict = {}
            print(p_values)
            print("Struttura reale ", real_traj)
            print("struttura stimata  ", estimate_traj)
            print(" ")

            for t in range(len(nodes)):
                parents[nodes[t]]= []
                fdr_dict[nodes[t]] = []
                c = 0
                for n in estimate_traj:
                    if (n[1] == nodes[t]):
                        parents[nodes[t]].append(n[0])
                        if n not in real_traj:
                            c+=1
                
                if c!= 0:
                    fdr_dict[nodes[t]] = {'Real FDR' : c/len( parents.get(nodes[t]))}
                else:
                    fdr_dict[nodes[t]] = {'Real FDR' : 0}
            
            estimate_parents = {}            
            print("Genitori stimati:  ", parents)
            for t in range(len(nodes)): #Scelgo la variabile da analizzare   
                values = p_values.get(nodes[t])
                print(" ")
                print("VARIABILE ANALIZZATA ", nodes[t])
                estimate_parents[nodes[t]] = []

                for n in values: # values[n] = prendo il candidato genitore
                    if n in parents.get(nodes[t]): #se il genitore trovato dall'algoritmo è un genitore reale, procediamo
                        print("la variabile ", n, " è un genitore reale")
                        estimate_parents[nodes[t]].extend(values.get(n))
                    else:
                        print("la variabile ", n, " NON è un genitore reale")
            print(" ")
            print("Valori dei gentiori stimati  ", estimate_parents)
            
            for t in estimate_parents:
                c = 0
                max_p_value = 0 
                for n in range(len(estimate_parents.get(t))):
                    if (estimate_parents.get(t)[n] <= alfa/2):
                        c+=1
                        if(max_p_value < estimate_parents.get(t)[n]):
                            max_p_value = estimate_parents.get(t)[n]
                print("C per variabile ", t, ": ", c)
                print("lungh ", len(estimate_parents.get(t)))
                print("max ", max_p_value)
                if (c != 0):
                    estimate_fdr = max_p_value * (len(estimate_parents.get(t))/c)
                else:
                    if len(estimate_parents.get(t)) == 0:
                            estimate_fdr = None
                    else:
                        estimate_fdr = 0
                
                print("fdr stimato della variabile ",t, ": ", estimate_fdr)

                fdr_dict[t].update({'Estimate fdr' : estimate_fdr})            
            
            json_data_fdr['%s' %read_files[i]] = fdr_dict
            print(json_data_fdr)
            #with open('./output/estimateStructure.json' , 'w') as f:
            #json.dump(json_data_est, f)
            #print("strutture salvate")
        

            #completeName =  os.path.join('./output/Structure' , "estimateStructure%s.json" %cont)
            #se1.save_results(completeName)
            # se1.save_plot_estimated_structure_graph(os.path.join('./output' , "estimateStructure%s.png" %cont))
            #cont = cont+1
    
    with open('./output/%s/realStructure.json' %number_trajectories, 'w') as f:
        json.dump(json_data_real, f)

    with open('./output/%s/estimateStructure.json' %number_trajectories, 'w') as f:
        json.dump(json_data_est, f)

    with open('./output/%s/fdr.json' %number_trajectories, 'w') as f:
        json.dump(json_data_fdr, f)



