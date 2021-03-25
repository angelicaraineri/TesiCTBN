import glob
import json
import os
from PyCTBN import JsonImporter
#import StructureEstimation as se
import yaml



class main():
     # <read the json files in ./data path>
    read_files = glob.glob(os.path.join('./data/networks_and_trajectories_ternary_data_01_3', "*.json"))
    # <initialize a JsonImporter object for the first file>
    cont = 1
    
    
    
    with open('params.yaml') as file:
        documents = yaml.full_load(file)
        value = documents['feature']['number_trajectories']
        print(value)
    
    
    
    
"""  
    for i in range(0,10):
        importer = JsonImporter(file_path=read_files[i], samples_label='samples',
                                structure_label='dyn.str', variables_label='variables',
                                time_key='Time', variables_key='Name')
        se.main(importer, cont)
 """       
