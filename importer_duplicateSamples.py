import glob
import os
import random
from PyCTBN import JsonImporter
from sklearn.utils import resample

class main():
    read_files = glob.glob(os.path.join('./data/networks_and_trajectories_ternary_data_01_3', "*.json"))
    cont = 1
    for i in range(0, 10):
        importer = JsonImporter(file_path=read_files[i], samples_label='samples',
                            structure_label='dyn.str', variables_label='variables',
                            time_key='Time', variables_key='Name')
        importer.import_data(0)
        samples = importer._raw_data[0]['samples']
        y = random.sample(samples, 150)
        newSamples = resample(y, n_samples=300, replace=True,random_state=0)
        importer._raw_data[0]['samples'] = newSamples
     
     
     
        

