import glob
import json
import os

from PyCTBN import JsonImporter
from PyCTBN import SamplePath
from PyCTBN import StructureConstraintBasedEstimator
import yaml
from sklearn.utils import resample
import random



class main():
   
    # <read the json files in ./data path>
    read_files = glob.glob(os.path.join('./data/networks_and_trajectories_ternary_data_01_3', "*.json"))
    # <initialize a JsonImporter object for the first file>
    cont = 1
    for i in range(0,10):
        importer = JsonImporter(file_path=read_files[i], samples_label='samples',
                                structure_label='dyn.str', variables_label='variables',
                                time_key='Time', variables_key='Name')
        
        importer.import_data(0)
        
        with open('params.yaml') as file:
            documents = yaml.full_load(file)
            number_trajectories = documents['feature']['number_trajectories']
            print(number_trajectories)
        
        if (number_trajectories != 300):
            samples = importer._raw_data[0]['samples']
            y = random.sample(samples, number_trajectories)
            newSamples = resample(y, n_samples=300, replace=True,random_state=0)
            importer._raw_data[0]['samples'] = newSamples
        
        strut = importer._raw_data[0]['dyn.str']
        with open('./output/realStructure%s.json' %cont, 'w') as f:
            json.dump(strut, f)
    
        # construct a SamplePath Object passing a filled AbstractImporter object
        s1 = SamplePath(importer=importer)
        # build the trajectories
        s1.build_trajectories()
        # build the information about the net
        s1.build_structure()
        # construct a StructureEstimator object passing a correctly build SamplePath object and the
        # independence tests significance, if you have prior knowledge about the net structure create a list of tuples
        # that contains them and pass it as known_edges parameter
        se1 = StructureConstraintBasedEstimator(sample_path=s1, exp_test_alfa=0.1, chi_test_alfa=0.1,
                                                known_edges=[], thumb_threshold=25)
        # call the algorithm to estimate the structure
        se1.estimate_structure()
        # obtain the adjacency matrix of the estimated structure
        print(se1.adjacency_matrix())
        # save the estimated structure  to a json file (remember to specify the path AND the .json extension)....
        completeName =  os.path.join('./output' , "estimateStructure%s.json" %cont)
        se1.save_results(completeName)
        # ...or save it also in a graphical model fashion (remember to specify the path AND the .png extension)
        # se1.save_plot_estimated_structure_graph(os.path.join('./output' , "estimateStructure%s.png" %cont))
        cont = cont+1
